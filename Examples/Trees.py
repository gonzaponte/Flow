from Flow import Flow
from Algorithm import Algorithm
from Services.ROOTsvc import TreeReader, TreeWriter
from Utilities.IO import Dumper
from ROOT import TRandom3

class RNG(Algorithm):
    '''
        Generate a random number.
    '''
    def Begin(self):
        self.rng = TRandom3(0)

    def Execute(self,input = None):
        return True, self.rng.Gaus(0,1)

class Adapt(Algorithm):
    '''
        Adapt data to tree format.
    '''
    def Execute(self,input):
        return True, {'x':input, 'y':input**2, 'z':input**3}

output = 'outputtree.root'
flw = Flow()
flw.msg.VL = 2
N = 100000

def WriteTree():
    rng   = RNG('rng')
    adapt = Adapt('adapt','rng')
    write = TreeWriter( 'treewriter', 'adapt', output, treename = 'tree', branches = ('x','y','z') )

    flw.AddAlgorithm(rng)
    flw.AddAlgorithm(adapt)
    flw.AddAlgorithm(write)
    flw.Run(N)

def ReadTree():
    read  = TreeReader( 'treereader', output, treename = 'tree', branches = ('x','y','z') )
    dump  = Dumper('dumper','treereader')

    flw.AddAlgorithm(read)
    flw.AddAlgorithm(dump)
    flw.Run(20)

#WriteTree()
ReadTree()
