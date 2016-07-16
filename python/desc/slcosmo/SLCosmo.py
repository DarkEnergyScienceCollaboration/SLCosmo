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
    '''
    def __init__(self):
        self.cosmopars = {'H0':None}
        self.cosmotruth = {'H0':None}
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
            Nim = 4 # BUG: THIS SHOULD BE 4 WITH PROBABILITY 1/6, 2 WITH PROBABILITY 5/6
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
        potential information that we need. The samples are stored in
        dataframes once read in, one for each lens, and each one containing
        one column for each time delay. Doubles will only have one time delay
        ('AB'), while quads will have at least three ('AB', 'AC', 'AD').
        This method overwrites any existing array of lenses.
        '''
        self.Nlenses = len(tdc2samplefiles)
        self.lenses = [] # trashing any existing data we may have had.
        for k,tdc2samplefile in enumerate(tdc2samplefiles):
            self.lenses.append(desc.slcosmo.TDC2ensemble())
            self.lenses[k].read_in_from(tdc2samplefile)
        return

    def log_likelihood(self):
        '''
        Compute the joint log likelihood of the cosmological parameters given
        a set of time delays and the measured Fermat potential differences.
        This is a sum of log likelihoods over the ensemble of lenses, each of
        which has to first be computed.
        '''
        return

    def draw_samples_from_prior(self,Nsamples):
        '''
        In simple Monte Carlo, we generate a large number of samples from the
        prior for the cosmological parameters, so that we can then evaluate
        their likelihood weights. The cosmological parameter samples are stored
        in a dataframe, which this method initializes.
        '''
        return
