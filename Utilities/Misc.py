'''
    Useful algorithms that are not catalogued.
'''

from Algorithm import Algorithm

class Concatenator(Algorithm):
    '''
        Contatenate several inputs. Those must be set as the input parameter
        (in iterable or in a space-split string)
        Examples:
        Concatenator('someid','input1 input2 input3')
        Concatenator('someid',['input1', 'input2', 'input3'])
    '''
    def Begin(self):
        self.inputs = self.input.split() if isinstance(self.input,str) else list(self.input)
        self.input  = None

    def Execute(self,data):
        data = map( self.data.get, self.inputs )
        return (True,) + tuple(data)

