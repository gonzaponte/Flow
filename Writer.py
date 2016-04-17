from Algorithm import Algorithm

class Writer( Algorithm ):
    '''
        Algorithm to write to files.
    '''

    def __init__( self, ID = 'Writer', input = None, fileout = '', **kwargs ):
        '''
            Initialize with an ID, the input data, the file where to store it and,
            optionally, keyword arguments to be used by other methods.
        '''
        Algorithm.__init__( self, ID, input )
        self.kwargs = kwargs
        self.Nevts = 0
        self.fileout = fileout

    def Begin(self):
        if self.fileout:
            self.Open( self.fileout )
        else:
            self.msg('Crucial','WARNING: File is not open in writer ' + str(self.ID) )

    def End(self):
        self.Close()

    def Execute( self, data ):
        self.Nevts += 1
        if data is None: return False, None
        self.Write(data)
        return True, None

    def Open( self, filename ):
        '''
            Open file and prepare for writing. To be coded in each particular case.
        '''
        raise NotImplementedError('Writer.Open method not implemented')

    def Close( self ):
        '''
            To be coded in each particular case.
        '''
        raise NotImplementedError('Writer.Close method not implemented')

    def Write( self, data ):
        '''
            Write data to file. To be coded in each particular case.
        '''
        raise NotImplementedError('Writer.Write method not implemented')
