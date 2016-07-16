import numpy as np

class TDC2ensemble(object):
    """
    In TDC2, we expect time delays to be inferred by the Good Teams and
    submitted as ensembles of posterior samples, in plain text tables,
    one time delay per column (AB, AC, AD) for quads, and just (AB) for
    doubles. The headers of these files will contain the same Fermat potential
    information that was provided in the data file, ie an 'observed' FP
    difference and its uncertainty for each image pair, plus an overall 'Q'
    factor that enables the conversion between time delay, FP, and time
    delay distance.

    This class is a data structure, for storing all the information provided
    in a TDC2 inferred time delay sample file.

    Use cases:

    1. Get samples and header information from a file

    2. Enable SLCosmo factory method to create mock TDC2 ensembles from scratch

    3. Write mock samples and header information to a file

    """
    def __init__(self):
        self.source = None
        self.Nsamples = None
        self.samples = []
        return

    def read_in_from(self,tdc2samplefile):
        """
        Read in both the posterior sample time delays and the Fermat potential
        header information, and store it for re-use.
        """
        self.source = tdc2samplefile
        self.samples = np.loadtxt(self.source,skiprows=18)
        # BUG: THIS SHOULD BE A DATAFRAME, REALLY, WITH COLUMN HEADERS
        self.Nsamples = len(self.samples)
        # BUG: HEADER INFORMATION NEEDS TO BE READ IN AS WELL
        # BUG: NEED TO STORE NO OF DELAYS AS WELL AS NO OF SAMPLES
        return

    def write_out_to(self,tdc2samplefile):
        """
        Write out both the posterior sample time delays and the Fermat potential
        header information in a plain text file.
        """
        if self.Nsamples is None:
            print("No samples to write out, skipping.")
        else:
            np.savetxt(tdc2samplefile,self.samples)
            # BUG: HEADER INFORMATION NEEDS TO BE WRITTEN OUT AS WELL
        return
