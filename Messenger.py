'''
    Messenger services.
'''

from sys import stdout

VerbosityDictionary    = {}
VerbosityDictionary[0] = 'None'
VerbosityDictionary[1] = 'Crucial'
VerbosityDictionary[2] = 'Info'
VerbosityDictionary[3] = 'Debug'

for n,t in VerbosityDictionary.items():
    VerbosityDictionary[t] = n

class Messenger:
    '''
        Messenger class. It manages the information related with the verbosity.
    '''
    def __init__( self, ID = 'Msg', Verbosity = 3, SendTo = stdout ):
        self.ID = ID
        self.VL = Verbosity if isinstance(Verbosity,int) else VerbosityDictionary(Verbosity)
        self.output = open(SendTo,'w') if isinstance(SendTo,str) else SendTo

    def __call__( self, type, *messages ):
        '''
            Prints messages.
        '''
        if type == 'error':
            self.raise_error(*messages)
        if VerbosityDictionary[type] > self.VL:
            return
        self.output.write( '###=> ' + '\n'.join(messages) + '\n' )

    def raise_error( self, *messages ):
        '''
            Raises an error and leaves the program.
        '''
        self.output.write( '!!!!!!!!!=> ' + '\n'.join(messages) + '\n' )
        exit()
