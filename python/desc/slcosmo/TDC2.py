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

    It could be nice if we moved to using pandas dataframes, so that we
    can refer to the time delays as eg dt['AB'], and the corresponding
    FP differences as DeltaFP['AB'] +/- DeltaFP_err['AB'].

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

    @staticmethod
    def read_in_from(tdc2samplefile):
        """
        Read in both the posterior sample time delays and the Fermat potential header information, and store it for re-use.

        Parameters:
        -----------
        tdc2samplefile : string
                       Name of the file to read from.

        Returns:
        --------
        TDC2ensemble object
            A TDC2ensemble object filled with the read in data.

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
        my_object = TDC2ensemble()
        my_object.source = tdc2samplefile
        my_object._read_header()
        my_object.dt_obs = np.loadtxt(my_object.source)
        if len(my_object.dt_obs.shape) == 1:
            my_object.Nim = 2
        else:
            my_object.Nim = 4
        my_object.Nsamples = len(my_object.dt_obs)
        return my_object

    def _read_header(self):
        self.DeltaFP_obs = []
        self.DeltaFP_err = []
        with open(self.source) as input_:
            for line in input_:
                if line.startswith('# Q'):
                    self.Q = float(line.strip().split(':')[1])
                if line.startswith('# Delta'):
                    key, value = line.strip()[1:].split(':')
                    if key.find('err') != -1:
                        self.DeltaFP_err.append(float(value))
                    else:
                        self.DeltaFP_obs.append(float(value))

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
        Possible failure modes:
        1. Samples array has no samples in it, even if Nsamples is not None
        2. File is not actually written
        """
        if self.Nsamples is None:
            print("No samples to write out, skipping.")
        else:
            # First write out the header, over-writing the file:
            self.form_header()
            np.savetxt(tdc2samplefile, self.dt_obs,
                       header=self.header, comments='# ')
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

    def form_header(self):
        self.header = \
"Time Delay Challenge 2 Posterior Sample Time Delays\n\
\n\
Notes:\n\
* Time delays should be given in days. Positive dt_AB means that light\n\
  curve A leads (not lags) light curve B.\n\
* Q is the H0-free time delay distance, a function of zd, zs and\n\
  cosmology. Q has units of km / s: D_dt = Q / H0\n\
* Fermat potential differences DeltaFP are given in units of\n\
  day km / s / Mpc, such that the predicted time delay is\n\
  dt = (Q / (c * H0)) * DeltaFP,  in days. c = 3.00e5 km/s\n\
\n\
Q: "+str(self.Q)+"\n"
        names = ['AB', 'AC', 'AD']
        for k in range(self.Nim - 1):
            self.header = self.header + \
"DeltaFP_"+names[k]+": "+str(self.DeltaFP_obs[k])+"\n" + \
"DeltaFP_"+names[k]+"_err: "+str(self.DeltaFP_err[k])+"\n"
        self.header = self.header + "\n"
        for k in range(self.Nim - 1):
            self.header = self.header + \
                          "                 dt_"+names[k]
        return
