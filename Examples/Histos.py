from Flow import Flow
from Algorithm import Algorithm
from Services.ROOTsvc import HistoSvc
from ROOT import TRandom3

class RNG(Algorithm):
    '''
        Generate a random number.
    '''
    def Begin(self):
        self.rng = TRandom3(0)

    def Execute(self,input = None):
        return True, self.rng.Gaus(0,1)

class Histos(Algorithm,HistoSvc):
    def Begin(self):
        self.Initialize('output.root')

    def Execute(self,data):
        self.Fill1D( data, 'hgaus', 500, -10, 10 )
        return True, None

    def End(self):
        self.Finalize()


rng = RNG('rng')
his = Histos('hist','rng')

flw = Flow()
flw.msg.VL = 2
flw.AddAlgorithm(rng)
flw.AddAlgorithm(his)



flw.Run(10000)
