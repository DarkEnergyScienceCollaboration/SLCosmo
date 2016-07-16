from __future__ import print_function
import numpy as np
import desc.slcosmo

c = 3.00e5

class SLCosmo(object):
    '''
    Master class for handling cosmological parameter inference given strong
    lens time delay and Fermat potential data.

    In the TDC2 scheme (and perhaps others), we will need to read in one file
    for each system, that contains the time delay posterior samples for that
    lens. The header of that file should be the same as the TDC2 data file,
    and contain the measuremd values of the Fermat potential differences,
    along with their uncertainties.

    A joint likelihood function will then compute the log likelihood of H0
    given the Fermat potential differences, for each sample time delay in each
    lens, and combine them into a single log likelihood value.

    The H0 values will be drawn from a suitable prior, and each assigned a
    log likelihood value, which is finally converted to a posterior weight.

    Use cases:

    1. Make a set of mock TDC2 sample ensembles, and analyze them as if they were
       real, aiming to recover the "true" cosmological parameters.

    2. Analyze a set of TDC2 sample files, reading them in and inferring
       the cosmological parameters. 
    '''
    def __init__(self):
        self.cosmopars = {'H0':None}
        self.cosmotruth = {'H0':None}
        self.H0_prior_mean = 70.0
        self.H0_prior_width = 7.0
        self.Npriorsamples = None
        self.Nlenses = 0
        self.lcdatafiles = []
        self.tdc2samplefiles = []
        return

    def make_some_mock_data(self,Nlenses):
        '''
        Make a mock dataset of Nlenses lens systems, and write it out as
        in a set of correctly formatted files. True time delays and Fermat
        potentials are drawn randomly from plausible distributions.
        '''
        self.Nlenses = Nlenses
        self.lenses = []
        self.cosmotruth['H0'] = 72.3
        for k in range(self.Nlenses):

            # How many images does this lens have?
            Nim = 2 # BUG: THIS SHOULD BE 4 WITH PROBABILITY 1/6, 2 WITH PROBABILITY 5/6
            Ndt = Nim - 1

            # What are its true time delays?
            dt_true = 15.0 + 2.0 * np.random.randn(Ndt)
            # What is its Q value, relating H0 to time delay distance?
            Q = 4e5 + 0.5e5 * np.random.randn()
            # What are its true Fermat potential differences?
            DeltaFP_true = (self.cosmotruth['H0'] / c) * (dt_true / Q)

            # What are its observed Fermat potential differences?
            DeltaFP_err = 50.0 * np.ones(Ndt) # BUG: USE 4% ERRORS INSTEAD, dfperr=4.0 SHOULD BE A KWARG
            DeltaFP_obs = DeltaFP_true + DeltaFP_err * np.random.randn(Ndt)

            # What are its posterior sample time delays?
            dt_err = 2.0 * np.ones(Ndt) # BUG: dtsigma=2.0 DAYS SHOULD BE A KWARG
            Nsamples = 1000  # BUG: Nsamples=1000 SHOULD BE A KWARG
            dt_obs = dt_true + dt_err * np.random.randn(Nsamples,Ndt)

            # Create a TDC2 ensemble object and have it write itself out:
            filename = 'mock_time_delays_'+str(k)+'.txt'
            self.lenses.append(desc.slcosmo.TDC2ensemble())
            self.lenses[k].Nsamples = Nsamples
            self.lenses[k].samples = dt_obs
            self.lenses[k].DeltaFP_obs = DeltaFP_obs
            self.lenses[k].DeltaFP_err = DeltaFP_err
            self.lenses[k].Q = Q
            self.lenses[k].write_out_to(filename)

        return

    def read_in_time_delays(self, tdc2samplefiles):
        '''
        Each tdc2samplefile is a multi-column plain text file, with a header
        marked by '#' marks at the start of each line and then a set of Fermat
        potential information that we need. The samples are stored in a 2D
        numpy array with one row for each lens, and one column for each time
        delay. Doubles will only have one time delay
        ('AB'), while quads will have at least three ('AB', 'AC', 'AD').
        This method overwrites any existing array of lenses.
        '''
        self.Nlenses = len(tdc2samplefiles)
        self.lenses = [] # trashing any existing data we may have had.
        for k,tdc2samplefile in enumerate(tdc2samplefiles):
            self.lenses.append(desc.slcosmo.TDC2ensemble())
            self.lenses[k].read_in_from(tdc2samplefile)
        return

    def draw_some_prior_samples(self,Nsamples):
        '''
        In simple Monte Carlo, we generate a large number of samples from the
        prior for the cosmological parameters, so that we can then evaluate
        their likelihood weights. The cosmological parameter samples are stored
        in a numpy array, which this method initializes.
        '''
        self.Npriorsamples = Nsamples
        self.cosmopars['H0'] = self.H0_prior_mean + self.H0_prior_width * np.random.randn(self.Npriorsamples)
        return

    def compute_the_joint_log_likelihood(self):
        '''
        Compute the joint log likelihood of the cosmological parameters given
        a set of time delays and the measured Fermat potential differences.
        This is a sum of log likelihoods over the ensemble of lenses, each of
        which has to first be computed. We also compute the importance weights,
        rescaling and exponentiating.
        '''
        # Compute likelihoods, looping over lenses and summing over samples:
        self.log_likelihoods = np.zeros(self.Npriorsamples)
        # BUG: THIS FUNCTION NEEDS TO DO SOMETHING USEFUL, LIKE:
        # # Loop over sampled values of H0
        # for k in range(Npriorsamples):
        #     H0 = self.cosmopars['H0'][k]
        #     jointlogL = np.array([])
        #     for lens in self.lenses:
        #         logL = np.array([])
        #         Ns = lens.Nsamples * lens.Ndelays
        #         for j in range(lens.Nsamples):
        #             for i in len(lens.Ndelays):
        #                 np.append(logL, gaussian_function(XXXXX))
        #         np.append(jointlogL, (np.logaddexp(logL) - np.log(Ns)))
        #     self.log_likelihoods[k] = np.sum(jointlogL)

        # Compute normalized importance weights:
        logLmax = np.max(self.log_likelihoods)
        self.weights = np.exp(self.log_likelihoods - logLmax)
        # BUG: THESE SHOULD SUM TO ONE...
        return

    def report_the_inferred_cosmological_parameters(self):
        '''
        For this we need the posterior weight for each prior sample, so that we
        can compute the posterior mean and standard deviation for each
        cosmological parameter.
        '''
        H0mean = np.sum(self.weights * self.cosmopars['H0'])/np.sum(self.weights)
        # BUG: NO STANDARD DEVIATION YET
        print("Posterior mean H0 = ",H0mean)
        return

# =============================================================================

if __name__ == '__main__':

    Lets = desc.slcosmo.SLCosmo()
    Lets.make_some_mock_data(10)
    Lets.draw_some_prior_samples(100000)
    Lets.compute_the_joint_log_likelihood()
    Lets.report_the_inferred_cosmological_parameters()
