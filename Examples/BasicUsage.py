'''
    General example of the Flow framework. It reads a couple of numbers
    from a file, adds them and then the result is printed and saved again
    in a new file.
'''
from Flow import Flow
from Algorithm import Algorithm
from Utilities import Dumper, TxtReader, TxtWriter

# Define adder algorithm. Gets the data and sums them up to return it.
class Adder (Algorithm):
    def Execute( self, data ):
        x = reduce( lambda x,y: x+y, data )
        return True, x

# Create instances of the algorithms to be used
a0 = TxtReader( 'ExampleReader', 't.txt' )
a1 = Adder('adder','ExampleReader')
a2 = Dumper('dumper','adder')
a3 = TxtWriter( 'ExampleWriter', 'adder', 'x.txt' )

# Create an instance of the Flow framework, set verbosity level and
# add the algorithms
flw = Flow()
flw.msg.VL = 2
flw.AddAlgorithm(a0)
flw.AddAlgorithm(a1)
flw.AddAlgorithm(a2)
flw.AddAlgorithm(a3)

# Run 10 thousand events
flw.Run(10000)
