'''
    Algorithm abstract implementation.

    Algorithms are the most basic pieces of code inserted into Flow code.
    It is a class that consists of 3 methods: Begin, End and Execute. The
    latter is the one manipulating actual data, while the other two may be
    used for pre- and post-processing. Algorithms will count with a messenger
    and data storage attributes.

    An Algorithm will be initialize with its ID and its input, the latter
    being either None (no input) or other algorithm(s)' ID(s). Flow will
    take the data from the output of the algorithm(s) given in input and
    pass it to the Execute method.

    The Execute method must return a boolean telling whether the calculation
    has been succesful and the output data in the desired format.
'''

_RESULTS = { True : 'Passed', False : 'Failed' }

class Algorithm:
    '''
        Performs some operations producing some result.
    '''
    def __init__( self, ID = 'Alg', input = None ):
        self.ID    = ID
        self.input = input

    def Begin( self ):
        '''
            Do something before running:
            - Define variables
            - ...
        '''
        return None

    def __call__( self ):
        '''
            Execute!
        '''
        self.msg( 'Debug', 'Calling algorithm {0} with input {1}'.format( self.ID, self.input ) )
        argument = map(self.data.get,self.input) if hasattr(self.input,'__iter__') else self.data[self.input]
        result = self.Execute( argument )
        ok = result[0]
        data = result[1:] if len(result) > 2 else result[1]
        self.data[self.ID] = data
        self.msg( 'Debug', 'Algorithm {0}: {1}'.format(self.ID,_RESULTS[ok]) )
        return ok

    def Execute( self, data ):
        '''
            Execute the code! This method takes the input from the data service.
            It must also return a tuple where the first element is a boolean
            indicating whether the calculation was succesful or not.
        '''
        raise NotImplementedError( '{0}.Execute not implemented'.format(self.ID) )

    def End( self ):
        '''
            Do something at the end of the run.
        '''
        return None
