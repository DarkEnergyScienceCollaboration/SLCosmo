'''
Module docstring goes here.
'''

from __future__ import print_function
import numpy as np
import desc.slcosmo

c = 3.00e5

class SLCosmo(object):
    '''
    Master class for handling cosmological parameter inference given
    strong lens time delay and Fermat potential data.

    In the TDC2 scheme (and perhaps others), we will need to read in one
    file for each system, that contains the time delay posterior samples
    for that lens. The header of that file should be the same as the
    TDC2 data file, and contain the measuremd values of the Fermat
    potential differences, along with their uncertainties.

    A joint likelihood function will then compute the log likelihood of
    H0 given the Fermat potential differences, for each sample time
    delay in each lens, and combine them into a single log likelihood
    value.

    The H0 values will be drawn from a suitable prior, and each assigned
    a log likelihood value, which is finally converted to a posterior
    weight.

    Use cases:

    1. Make a set of mock TDC2 sample ensembles, and analyze them as if
    they were real, aiming to recover the "true" cosmological
    parameters.

    2. Analyze a set of TDC2 sample files, reading them in and inferring
    the cosmological parameters.
    '''
    def __init__(self):
        self.cosmopars = {'H0':[]}
        self.cosmotruth = {'H0':None}
        self.H0_prior_mean = 70.0
        self.H0_prior_width = 7.0
        self.Npriorsamples = None
        self.Nlenses = 0
        self.lenses = None
        self.lcdatafiles = []
        self.tdc2samplefiles = []
        self.log_likelihoods = None
        self.weights = None
        self.mock_files = []
        return

    def make_some_mock_data(self, Nlenses=100, Nsamples=1000,
                            percentage_dfp_err=4.0, dt_sigma=2.0,
                            quad_fraction=0.17, stem='mock'):
        '''
        Make a mock dataset of any number of lens systems, and write it
        out in a set of correctly formatted files.

        Parameters:
        -----------
        Nlenses : integer
                The number of lenses worth of time delay data to
                simulate.
        Nsamples : integer
                The number of posterior sample time delays to generate.
        percentage_dfp_err : float
                The percentage uncertainty in each and every Fermat
                potential difference, which are assumed to be independent. A very simple approximation.
        dt_sigma : float
                The absolute uncertainty in each and every time delay,
                in days. Another simple approximation.
        quad_fraction : float
                The fraction of lenses that have 4 images.

        Notes:
        ------
        True time delays and Fermat potentials are drawn randomly from
        plausible Gaussian distributions.

        Possible failure modes: 1. Simulated posterior time delays have
        incorrect width
        '''
        assert Nlenses > 0
        assert Nsamples > 1
        assert percentage_dfp_err > 0.0
        assert dt_sigma > 0.0
        self.Nlenses = Nlenses
        self.lenses = []
        self.mock_files = []
        self.cosmotruth['H0'] = 72.3
        for k in range(self.Nlenses):

            # How many images does this lens have?
            if np.random.rand() < quad_fraction:
                Nim = 4
            else:
                Nim = 2
            Ndt = Nim - 1

            # What are its true time delays?
            dt_true = 20.0 + 2.0 * np.random.randn(Ndt)
            # What is its Q value, relating H0 to time delay distance?
            Q = 4e5 + 0.5e5 * np.random.randn()
            # What are its true Fermat potential differences?
            DeltaFP_true = (c * dt_true * self.cosmotruth['H0'] / Q)

            # What are its observed Fermat potential differences?
            DeltaFP_err = DeltaFP_true * percentage_dfp_err / 100.0
            DeltaFP_obs = DeltaFP_true + \
                          DeltaFP_err * np.random.rand(Ndt)

            # What are its posterior sample time delays?
            dt_sigma_array = dt_sigma * np.ones(Ndt)
            dt_obs = dt_true + \
                     dt_sigma_array * np.random.randn(Nsamples, Ndt)

            # Create a TDC2 ensemble object and have it write
            # itself out:
            filename = stem+'_time_delays_'+str(k)+'.txt'
            self.lenses.append(desc.slcosmo.TDC2ensemble())
            self.lenses[k].Nsamples = Nsamples
            self.lenses[k].Nim = Nim
            self.lenses[k].dt_obs = dt_obs
            self.lenses[k].DeltaFP_obs = DeltaFP_obs
            self.lenses[k].DeltaFP_err = DeltaFP_err
            self.lenses[k].Q = Q
            self.lenses[k].write_out_to(filename)
            self.mock_files.append(filename)
        return

    def read_in_time_delay_samples_from(self, paths):
        '''
        Ingest time delay data from a number of TDC2 submission files,
        storing it in a list of `TDC2ensemble` objects, one for each
        lens (and overwriting any existing list).

        Parameters:
        -----------
        paths : [list of] string[s[]
            A list of the files to be read from, or a string containing wildcards.

        Notes:
        ------
        Each tdc2samplefile is a multi-column plain text file, with a
        header marked by '#' marks at the start of each line and
        containing a set of Fermat potential information that we need.
        '''
        if type(paths) is str:
            import glob
            tdc2samplefiles = glob.glob(paths)
        else:
            tdc2samplefiles = paths
        self.Nlenses = len(tdc2samplefiles)
        self.lenses = [] # trashing any existing data we may have had.
        quad_count = 0
        for tdc2samplefile in tdc2samplefiles:
            self.lenses.append(desc.slcosmo.TDC2ensemble.read_in_from(tdc2samplefile))
            if self.lenses[-1].Nim == 4:
                quad_count += 1
        print("Read in", self.Nlenses, "lenses, quad fraction =",
              np.round(float(quad_count)/float(self.Nlenses), 2))
        return

    def draw_some_prior_samples(self, Npriorsamples=1000):
        '''
        In simple Monte Carlo, we generate a large number of samples
        from the prior for the cosmological parameters, so that we can
        then evaluate their likelihood weights.

        Parameters:
        -----------
        Npriorsamples : integer
                      The number of prior samples to draw.

        Notes:
        ------
        The cosmological parameter samples are stored in a numpy array,
        which this method initializes.
        '''
        assert Npriorsamples > 20
        self.Npriorsamples = Npriorsamples
        self.cosmopars['H0'] = self.H0_prior_mean + \
            self.H0_prior_width * np.random.randn(self.Npriorsamples)
        return

    def compute_the_joint_log_likelihood(self):
        '''
        Compute the joint log likelihood of the cosmological parameters
        given a set of time delays and the measured Fermat potential
        differences.

        Notes:
        ------
        The calculation is a sum of log likelihoods over the ensemble
        of lenses, each of which has to first be computed. We also
        compute the importance weights, rescaling and exponentiating.
        '''
        import time as wallclock
        start = wallclock.time()
        # Compute likelihoods, looping over lenses and summing
        # over samples:
        self.log_likelihoods = np.zeros(self.Npriorsamples)
        # Loop over sampled values of H0
        for k in range(self.Npriorsamples):
            H0 = self.cosmopars['H0'][k]
            jointlogL = np.array([])
            for lens in self.lenses:
                jointlogL = np.append(jointlogL,
                                      lens.log_likelihood(H0))
            self.log_likelihoods[k] = np.sum(jointlogL)

        # Compute normalized importance weights:
        logLmax = np.max(self.log_likelihoods)
        self.weights = np.exp(self.log_likelihoods - logLmax)

        # How long did that take?
        end = wallclock.time()
        print("Wallclock time spent characterizing posterior = ",
                   round(end-start), "seconds")

        return

    def estimate_H0(self):
        '''
        For this we need the posterior weight for each prior sample, so
        that we can compute the posterior mean and standard deviation
        for each cosmological parameter.

        Notes:
        ------
        Should probably be a static function.
        '''
        H0_sum = np.sum(self.weights * self.cosmopars['H0'])
        H0_sumsq = np.sum(self.weights * self.cosmopars['H0']**2)
        H0_N = np.sum(self.weights)
        H0_mean = H0_sum / H0_N
        H0_stdv = np.sqrt((H0_sumsq - H0_N*H0_mean**2)/H0_N)
        return H0_mean, H0_stdv

    def report_the_inferred_cosmological_parameters(self):
        '''
        For this we need the posterior weight for each prior sample, so
        that we can compute the posterior mean and standard deviation
        for each cosmological parameter.

        Returns:
        --------
        (H0, sigma) : Tuple of floats
                    An estimate of H0, and its uncertainty.

        Notes:
        ------
        Convenience function.
        '''
        estimate, uncertainty = self.estimate_H0()
        kmsMpc = "km/s/Mpc"
        print("H0 =", round(estimate,1), "+/-",
                      round(uncertainty,1), kmsMpc)
        if self.cosmotruth['H0'] is not None:
            print("True H0 =", self.cosmotruth['H0'], kmsMpc)
        return

    def plot_the_inferred_cosmological_parameters(self):
        '''
        Make a nice plot of the histogram of posterior H0 samples,
        overlaying the assumed prior PDF and the underlying true value,
        if known.
        '''
        import pylab as plt
        # Start figure:
        fig = plt.figure(figsize=(8,5))
        # Set font sizes:
        params = {'axes.labelsize': 20,
                  'font.size': 20,
                  'legend.fontsize': 20,
                  'xtick.labelsize': 14,
                  'ytick.labelsize': 14}
        plt.rcParams.update(params)
        # Linear xes for histogram:
        hax = fig.add_axes([0.15,0.15,0.85,0.80])
        H0min, H0max = 60.0, 80.0
        hax.set_xlim(H0min, H0max)
        for label in hax.get_yticklabels():
            label.set_visible(False)
        for tick in hax.yaxis.get_ticklines():
            tick.set_visible(False)

        # Plot the posterior histogram:
        Nbins = 0.1*self.Npriorsamples
        bins = np.linspace(H0min, H0max, Nbins, endpoint=True)
        plt.hist(self.cosmopars['H0'], weights=self.weights,
                 bins=bins, histtype='stepfilled', normed=True,
                 color='red', edgecolor='red', alpha=0.5,
                 label='Posterior PDF')

        # Overlay Gaussian approximation to the posterior:
        mu, sigma = self.estimate_H0()
        value = str(round(mu,1))+' +/- '+str(round(sigma,1))
        x = np.linspace(H0min, H0max, 1000, endpoint=True)
        y = np.exp(-0.5*((x-mu)**2)/sigma**2) / \
              np.sqrt(2*np.pi*sigma**2)
        plt.plot(x, y, linewidth=2, color='red',
                 label='Posterior estimate: '+value)

        # Overlay Gaussian prior:
        mu, sigma = self.H0_prior_mean, self.H0_prior_width
        assumption = str(round(mu,1))+' +/- '+str(round(sigma,1))
        x = np.linspace(H0min, H0max, 1000, endpoint=True)
        y = np.exp(-0.5*((x-mu)**2)/sigma**2) / \
              np.sqrt(2*np.pi*sigma**2)
        plt.plot(x, y, linestyle='dotted', linewidth=2, color='gray',
                 label='Prior PDF: '+assumption)

        # Overlay true value:
        value = self.cosmotruth['H0']
        plt.axvline(x=value,
                    color='black', linestyle='dashed', linewidth=2,
                    label='Truth: '+str(value))

        # Label axes of course:
        plt.xlabel("$H_0 / {\\rm km s}^{-1}{\\rm Mpc}^{-1}$")
        plt.ylabel("${\\rm Pr}(H_0 \\vert \Delta t_{\\rm obs} )$")
        plt.legend(prop={'size':10}, framealpha=1.0, loc=0)

        # Write out to file and report:
        filename = "H0posterior.pdf"
        plt.savefig(filename, dpi=300)
        print("Plot saved to",filename)
        return

# ======================================================================

if __name__ == '__main__':

    Lets = desc.slcosmo.SLCosmo()
    Lets.make_some_mock_data()
    Lets.draw_some_prior_samples()
    Lets.compute_the_joint_log_likelihood()
    Lets.report_the_inferred_cosmological_parameters()
    Lets.plot_the_inferred_cosmological_parameters()
