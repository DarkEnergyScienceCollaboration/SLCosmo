import numpy as np
import scipy.misc
c = 3e5 #km/s

class TDC2ensemble(object):
    """
    In TDC2, we expect time delays to be inferred by the Good Teams and
    submitted as ensembles of posterior samples, in plain text tables,
    one time delay per column (AB, AC, AD) for quads, and just (AB) for
    doubles. The headers of these files will contain the same Fermat
    potential information that was provided in the data file, ie an
    'observed' FP difference and its uncertainty for each image pair,
    plus an overall 'Q' factor that enables the conversion between time
    delay, FP, and time delay distance.

    This class is a data structure, for storing all the information
    provided in a TDC2 inferred time delay sample file.

    Use cases:

    1. Get samples and header information from a file

    2. Enable SLCosmo factory method to create mock TDC2 ensembles from scratch

    3. Write mock samples and header information to a file

    """
    def __init__(self):
        self.source = None
        self.Nsamples = None
        self.dt_obs = []
        return

    def read_in_from(self, tdc2samplefile):
        """
        Read in both the posterior sample time delays and the Fermat potential header information, and store it for re-use.

        Parameters:
        -----------
        tdc2samplefile : string
                       Name of the file to read from.

        Notes:
        ------
        The samples are stored in a 2D numpy array with one row for each
        lens, and one column for each time delay. Doubles will only have
        one time delay ('AB'), while quads will have at least three
        ('AB', 'AC', 'AD').

        Possible failure modes:
        1. File does not exist
        2. File has no samples in it
        3. File has no header in it
        4. Samples are not 2D numpy array
        5. Array has wrong number of columns (time delays - should be 1 or 3, and equal to Ndt)
        """
        self.source = tdc2samplefile
        self.dt_obs = np.loadtxt(self.source) #, skiprows=18)
        # BUG: THIS SHOULD BE A DATAFRAME, REALLY, WITH COLUMN HEADERS
        self.Nsamples = len(self.dt_obs)
        # BUG: HEADER INFORMATION NEEDS TO BE READ IN AS WELL
        # BUG: NEED TO STORE NO OF DELAYS AS WELL AS NO OF SAMPLES
        return

    def write_out_to(self, tdc2samplefile):
        """
        Write out both the posterior sample time delays and the Fermat
        potential header information in a plain text file.

        Parameters:
        -----------
        tdc2samplefile : string
                       The name of the file to be written to.

        Notes:
        ------
        Currently the data is written out with no header - this is a
        problem, issue #10.

        Possible failure modes:
        1. Samples array has no samples in it, even if Nsamples is not None
        2. File is not actually written
        """
        if self.Nsamples is None:
            print("No samples to write out, skipping.")
        else:
            np.savetxt(tdc2samplefile, self.dt_obs)
            # BUG: HEADER INFORMATION NEEDS TO BE WRITTEN OUT AS WELL
        return

    def log_likelihood(self, H0, fast=True):
        """
        Compute the likelihood of the proposed Hubble constant H0 given
        the Fermat potential difference data, marginalizing over the
        time delay PDF provided (approximately) in the samples.

        Parameters:
        -----------
        H0 : float
             The Hubble constant under evaluation.
        fast : Boolean, optional
             Just in case you want to do the calculation
             without vectorisation.

        Returns:
        --------
        logL : float
              The value of the log likelihood.

        See Also:
        ---------
        SLCosmo.compute_the_joint_log_likelihood

        Notes:
        ------
        Don't choose `fast=False`.
        """
        if fast:
            x = self.DeltaFP_obs - (c * self.dt_obs * H0 / self.Q)
            chisq = (x/self.DeltaFP_err)**2.0
            logL = -0.5 * chisq \
                   - np.log(np.sqrt(2*np.pi) * self.DeltaFP_err)

        else:
            logL = np.array([])
            Ns = 0
            for i in range(self.Nsamples):
                for j in range(self.Nim - 1):
                    Ns += 1
                    x = self.DeltaFP_obs[j] - \
                        (c * self.dt_obs[i,j] * H0 / self.Q)
                    chisq = (x/self.DeltaFP_err[j])**2.0
                    logL_el = -0.5 * chisq \
                        - np.log(np.sqrt(2*np.pi) * self.DeltaFP_err[j])
                    logL = np.append(logL,logL_el)

        return scipy.misc.logsumexp(logL) - np.log(len(np.ravel(logL)))





'''
Here's what a typical header should look like:

# Time Delay Challenge 2 Posterior Sample Time Delays
#
# Notes:
# * Time delays should be given in days. Positive dt_AB means that light curve
#     A leads (not lags) light curve B.
# * Q is the H0-free time delay distance, a function of zd, zs and cosmology
# * Q has units of km / s: D_dt = Q / H0
# * Fermat potential differences DeltaFP are given in units of day km / s / Mpc,
#     such that the predicted time delay is dt = (Q / (c * H0)) * DeltaFP
#     in days. c = 3.00e5 km/s
#
# Q: 419170.8224
# DeltaFP_AB: 2686.7945
# DeltaFP_AB_err: 79.6675
# DeltaFP_AC: 970.4846
# DeltaFP_AC_err: 32.1524
# DeltaFP_AD: 3657.5896
# DeltaFP_AD_err: 101.5637
#
#    dt_AB    dt_AC    dt_AD

A double would look the same, but would have no AC or AD lines, so the header
would be 4 lines shorter.

Nice if we moved to using pandas dataframes, so that we can refer to the
time delays as eg dt['AB'], and the corresponding FP differences as
DeltaFP['AB'] +/- DeltaFP_err['AB'].
'''
