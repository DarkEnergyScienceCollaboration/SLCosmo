import numpy as np

class TDC2ensemble(object):

    def __init__(self):
        self.source = None
        self.Nsamples = None
        self.samples = []
        return

    def read_in_from(self,tdc2samplefile):
        self.source = tdc2samplefile
        self.samples = np.loadtxt(self.source,skiprows=18)
        self.Nsamples = len(self.samples)
        return

    def write_out_to(self,tdc2samplefile):
        if self.Nsamples is None:
            print("No samples to write out, skipping.")
        else:
            np.savetxt(tdc2samplefile,self.samples)
        return
