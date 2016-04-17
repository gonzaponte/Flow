'''
    Flow is a python framework devoted to task sequenciation for moderately
    large amounts of data.
'''

from Messenger import Messenger, stdout
from time import localtime

class Flow:
    '''
        Main sequencer. It controls everything that is linked to it and executes a list of algorithms.
    '''
    def __init__( self, ID = 'Flow', msg = None ):
        '''
            Initialize with some identification @ID and some messenger @msg.
        '''
        self.ID   = ID
        self.msg  = Messenger( ID + '_msg', 3, stdout ) if msg is None else msg
        self.algs = list()
        self.data = dict()

        self.msg( 'Debug', 'Flow instance created with ID ' + str(ID) )

    def AddAlgorithm( self, algorithm ):
        '''
            Add algorithm to the list of algorithms to be executed. It also adds
            the algorithm ID to the  data dictionary to store its output.
        '''
        self.msg( 'Debug', 'Algorithm {0} has been added'.format(algorithm.ID) )
        self.algs.append( algorithm )
        self.data[ algorithm.ID ] = None

    def _Prepare( self ):
        '''
            Setup environment. Add messenger and data storage to the algorithms
            so they can be easily accessed. Also calls the Begin method of every
            algorithm.
        '''
        self.data[None] = None
        for alg in self.algs:
            alg.msg  = self.msg
            alg.data = self.data
            alg.Begin()

    def _Loop( self, Nevts ):
        '''
            Loop over Nevents calling the algorithms sequentially.
        '''
        for i in xrange(Nevts):
            [ alg() for alg in self.algs ]

    def _End( self ):
        [ alg.End() for alg in self.algs ]

    def Run( self, Nevts ):
        def GetTime():
            t = localtime()
            return t[3:6] + t[:3][::-1]
        self.msg('Info','Run start! Local time: {0}:{1}:{2} on {3}/{4}/{5}'.format(*GetTime()) )
        self._Prepare()
        self._Loop(int(Nevts))
        self._End()
        self.msg('Info','Run end! Local time: {0}:{1}:{2} on {3}/{4}/{5}'.format(*GetTime()) )
