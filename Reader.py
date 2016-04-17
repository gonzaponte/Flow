from Algorithm import Algorithm

class Reader( Algorithm ):
    '''
        Algorithm to read from files.
    '''

    def __init__( self, ID = 'Reader', filelist = list(), **kwargs ):
        '''
            Initialize with an ID, a list of the files to be read and,
            optionally, other keyword arguments that will be used by
            other methods.
        '''
        Algorithm.__init__( self, ID )
        self.Files  = list(filelist) if hasattr( filelist, '__iter__' ) else [filelist]
        self.Nfiles = len(self.Files)
        self.Ifile  = 0
        self.Ievt   = 0
        self.Nread  = 0
        self.File   = None
        self.EOF    = '__EOF__'
        self.kwargs = kwargs

    def Begin(self):
        self.Next()

    def End(self):
        self.Close()

    def Next( self ):
        if self.File: self.Close()
        if self.Ifile == self.Nfiles: return

        self.Open( self.Files[ self.Ifile ] )
        self.Ifile += 1
        self.Ievt   = 0

    def Execute( self, data ):
        self.Nread += 1
        data = self.Read( self.Ievt)
        self.Ievt += 1
        if data == self.EOF:
            self.Next()
            data = self.Read()
        return True, data

    def Open( self, filename ):
        '''
            To be coded in each particular case.
        '''
        raise NotImplementedError('Reader.Open method not implemented')

    def Close( self ):
        '''
            To be coded in each particular case.
        '''
        raise NotImplementedError('Reader.Close method not implemented')

    def Read( self, evt ):
        '''
            Return one "event" from file. If end of file is reached, return self.EOF.
            To be coded in each particular case.
        '''
        raise NotImplementedError('Reader.Read method not implemented')


if __name__ == '__main__':
    '''
        Example about how to use the reader. First create a file with numbers. Then read them with Flow.
    '''
    from Flow import Flow
    from Utilities import TxtReader

    f = open ('t.txt','w')
    for i in range(100):
        f.write( str(i) + ' ' + str(99 - i) + '\n' )
    f.close()

    reader = TxtReader( 'ExampleReader', 't.txt' )
    flow = Flow()
    flow.AddAlgorithm(reader)
    flow.Run(100)
