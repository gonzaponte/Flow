'''
    Some useful algorithms already defined.
'''

from Algorithm import Algorithm
from Reader    import Reader
from Writer    import Writer


class Dumper(Algorithm):
    '''
        Print out the input.
    '''
    def Execute( self, data ):
        print data
        return True, None

class TxtReader( Reader ):
    '''
        Read data from a plain text file.
    '''
    def Open( self, filename ):
        self.File = open( filename, 'r' )

    def Close( self ):
        self.File.close()

    def Read( self, evt ):
        return map( float, self.File.readline().split() )

class TxtWriter( Writer ):
    '''
        Write data to a plain text file.
    '''
    def Open( self, filename ):
        option = self.kwargs.get('option','w')
        self.File = open( filename, option )

    def Close( self ):
        self.File.close()

    def Write( self, data ):
        if not hasattr(data,'__iter__'):
            data = [data]
        self.File.write(' '.join(map(str,data)) + '\n')
