'''
    The Histo service provides tools for histogram creation, filling and saving.
'''

from Reader import Reader
from Writer import Writer
from Messenger import Messenger

from ROOT import *
from array import array

_methods = {
'pfx'  : lambda h: TH2.ProfileX(h),
'pfy'  : lambda h: TH2.ProfileY(h),
'pfxy' : lambda h: TH3.Project3DProfile(h,'xy'),
'pfyx' : lambda h: TH3.Project3DProfile(h,'yx'),
'pfxz' : lambda h: TH3.Project3DProfile(h,'xz'),
'pfzx' : lambda h: TH3.Project3DProfile(h,'zx'),
'pfyz' : lambda h: TH3.Project3DProfile(h,'yz'),
'pfzy' : lambda h: TH3.Project3DProfile(h,'zy'),
'pjx'  : lambda h: TH3.Project3D(h,'x') if isinstance(h,TH3) else TH2.ProjectionX(h),
'pjy'  : lambda h: TH3.Project3D(h,'y') if isinstance(h,TH3) else TH2.ProjectionX(y),
'pjz'  : lambda h: TH3.Project3D(h,'z') ,
'pjxy' : lambda h: TH3.Project3D(h,'xy'),
'pjyx' : lambda h: TH3.Project3D(h,'yx'),
'pjxz' : lambda h: TH3.Project3D(h,'xz'),
'pjzx' : lambda h: TH3.Project3D(h,'zx'),
'pjyz' : lambda h: TH3.Project3D(h,'yz'),
'pjzy' : lambda h: TH3.Project3D(h,'zy'),

'title': lambda g,t: TGraph.SetTitle(g,t),
'name' : lambda g,n: TGraph.SetName(g,n)}

class _TFileSvc:
    def __init__( self ):
        self._files   = {}
        self._counter = {}
        self._msg     = Messenger( '_TFileSvc_msg', 2 )

    def OpenFile( self, filename, option = '' ):
        if not filename in self._files:
            self._files[filename] = TFile(filename, option)
            self._counter[filename] = 0
            self._msg( 'Info', 'File {0} opened successfully.'.format(filename))

        self._counter[filename] += 1
        return self._files[filename]

    def CloseFile( self, filename ):
        n = self._counter.get(filename,0)
        assert n>0,'File {0} does not exist or has been already closed.'.format(filename)
        n -= 1
        if not n:
            self._files[filename].Close()
            self._msg( 'Info', 'File {0} closed successfully.'.format(filename))
        self._counter[filename] = n

_TFile = _TFileSvc()

class HistoSvc:
    '''
        A class designed to create, manage and save root objects.
    '''
    def Initialize( self, filename, option = 'recreate' ):
        self.filename = filename
        self._root_objects       = {}
        self._delayed_operations = {}

        self.file = _TFile.OpenFile( self.filename, option )

    def _MakeDerivedPlots(self):
        for name,options in self._delayed_operations.items():
            h = self._root_objects[name]
            for option in options:
                if isinstance(option,tuple):
                    derived = _methods[option[0]](h,*option[1:])
                else:
                    derived = _methods[option(h)]
                if not derived is None:
                    self._root_objects[name + '_' + option] = derived

    def Finalize(self):
        self._MakeDerivedPlots()
        for name,obj in sorted(self._root_objects.items()):
            self.file.WriteTObject(obj)
        _TFile.CloseFile(self.filename)

    def _BookH1( self, name, title, nbinsx, x0, x1 ):
        if title is None: title = name
        self._root_objects[name] = TH1F( name, title, nbinsx, x0, x1 )

    def _BookH2( self, name, title, nbinsx, x0, x1, nbinsy, y0, y1, *derived_plots ):
        if title is None: title = name
        self._root_objects[name] = TH2F( name, title, nbinsx, x0, x1, nbinsy, y0, y1 )
        self._delayed_operations[name] = list(derived_plots)

    def _BookH3( self, name, title, nbinsx, x0, x1, nbinsy, y0, y1, nbinsz, z0, z1, *derived_plots ):
        if title is None: title = name
        self._root_objects[name] = TH3F( name, title, nbinsx, x0, x1, nbinsy, y0, y1, nbinsz, z0, z1 )
        self._delayed_operations[name] = list(derived_plots)

    def _BookG1( self, name, title ):
        self._root_objects[name] = TGraph()
        self._delayed_operations[name] = [ ('name',name), ('title',title if title else '') ]

    def _BookG2( self, name, title ):
        self._root_objects[name] = TGraph2D()
        self._delayed_operations[name] = [ ('name',name), ('title',title if title else '') ]

    def Fill1D( self, xvalue, name, nbinsx, x0, x1, title = None ):
        if not name in self._root_objects:
            self._BookH1(name,title,nbinsx,x0,x1)
        self._root_objects[name].Fill(xvalue)

    def Fill2D( self, xvalue, yvalue, name, nbinsx, x0, x1, nbinsy, y0, y1, title = None, *derived_plots ):
        if not name in self._root_objects:
            self._BookH2(name,title,nbinsx,x0,x1,nbinsy,y0,y1,*derived_plots)
        self._root_objects[name].Fill(xvalue,yvalue)

    def Fill3D( self, xvalue, yvalue, zvalue, name, nbinsx, x0, x1, nbinsy, y0, y1, nbinsz, z0, z1, title = None, *derived_plots ):
        if not name in self._root_objects:
            self._BookH3(name,title,nbinsx,x0,x1,nbinsy,y0,y1,nbinsz,z0,z1,*derived_plots)
        self._root_objects[name].Fill(xvalue,yvalue,zvalue)

    def FillG1( self, xvalue, yvalue, name, title = None ):
        if not name in self._root_objects:
            self._BookG1( name, title )
        g = self._root_objects[name]
        g.SetPoint( g.GetN(), xvalue, yvalue )

    def FillG2( self, xvalue, yvalue, zvalue, name, title = None ):
        if not name in self._root_objects:
            self._BookG2( name, title )
        g = self._root_objects[name]
        g.SetPoint( g.GetN(), xvalue, yvalue, zvalue )

class TreeWriter( Writer ):
    '''
        Write data to a ROOT tree. The algorithm must be provided with the
        following keyword arguments:
        - treename:  the name of the tree to be read (default: 'tree').
        - branches:  the name of the branches to be filled. One variable per branch.
        - datatypes: types of data stored (default: 'd' for all).
    '''
    def Open( self, filename ):
        self.filename   = filename
        self.treename   = self.kwargs.get('treename' , 'tree')
        self.branches   = self.kwargs.get('branches' , None)
        self.datatypes  = self.kwargs.get('datatypes', { b: 'd' for b in self.branches} )
        self.fileoption = self.kwargs.get('fileoption', 'recreate' )

        self.File = _TFile.OpenFile( filename, self.fileoption )
        self.Tree = TTree( self.treename, self.treename )

        self.arrays = { b : array( dt, [0] ) for b, dt in self.datatypes.items() }
        for b in self.branches:
            self.Tree.Branch( b, self.arrays[b], '/'.join([b,self.datatypes[b]]) )

    def Close( self ):
        self.File.WriteTObject(self.Tree)
        _TFile.CloseFile(self.filename)

    def Write( self, data ):
        '''
            data must be a dictionary linking each branch with its value.
        '''
        for b,d in data.items():
            self.arrays[b][0] = d
        self.Tree.Fill()

class TreeReader( Reader ):
    '''
        Read data from a ROOT tree. The algorithm must be provided with the
        following keyword arguments:
        - treename: the name of the tree to be read.
        - branchname: the name of the branch to be linked, if only one is used (see Nvars).
        - vars: a tuple with the name of the variables
        - Nvars: number of variables in case of only one branch
        - datatype: type of data stored (default: 'f')
    '''
    def Open( self, filename ):
        self.filename  = filename
        self.treename  = self.kwargs.get('treename' , 'tree' )
        self.branches  = self.kwargs.get('branches' , None )
        self.datatypes = self.kwargs.get('datatypes', { b: 'd' for b in self.branches} )
        self.fileoption = self.kwargs.get('fileoption', '' )

        self.File = _TFile.OpenFile( filename, self.fileoption )
        self.Tree = self.File.Get(self.treename)

        self.arrays = { b : array( dt, [0] ) for b, dt in self.datatypes.items() }
        [ self.Tree.SetBranchAddress(b,a) for b,a in self.arrays.items() ]

    def Close( self ):
        _TFile.CloseFile(self.filename)

    def Read( self, evt ):
        self.Tree.GetEntry(evt)
        return { b: self.arrays[b][0] for b in self.branches }
