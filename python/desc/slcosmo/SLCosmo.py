class SLCosmo(object):
    '''
    Master class for handling cosmological parameter inference. 
    
    In the TDC2 scheme (and perhaps others), we will need to read in two files for each system:
      1. The light curve data file, whose header contains measurements of the Fermat potential differences
      2. The time delay posterior samples
      
    A joint likelihood function will then compute the log likelihood of H0 given the input time delays and 
    Fermat potential differences, for each sample for each lens, and combine them into a single log likelihood value.
    
    The H0 values will be drawn from a suitable prior, and each assigned a log likelihood value, which is 
    finally converted to a posterior weight.
    '''
    def __init__(self, message):
        self.message = message
        return

    def read_in_time_delays(self, raise_error=False):
        if raise_error:
            raise RuntimeError()
        return self.message
        
    '''
    And so on...
    '''
