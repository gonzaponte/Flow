from sys import argv, path
from Flow import Flow

_parameters_struc = {None: lambda v:v,'V': lambda v,c: map(c,v),'M':lambda v,c:map(lambda row:map(c,row),m))}
_parameters_types = {'I':int,'D':float,'B':bool,'S':str}
jobfile = argv[1]

parameters = {}
parameters['FlowJob'] = {
'JobName' : 'FlowJob',
'Verbosity' : 'Info',
'Paths':[],
'Algos':[]
}
for line in open(jobfile,'r'):
    if not len(line) or line[0] == '#': continue
    line = line.rstrip()

    data = line.split(' ')
    if parameters.get(data[0]) is None:
        parameters[data[0]] = {}

    index = len(data[0]) + len(data[1]) + 2

    if data[-1] == '+':
        exec('_______ = ' + ' '.join( data[2:-1]))
        if not isinstance(parameters[data[0]][data[1]],list):
            parameters[data[0]][data[1]] = [parameters[data[0]][data[1]]]
        parameters[data[0]][data[1]].append( _______ )
    else:
        exec('_______ = ' + ' '.join( data[2:]))
        parameters[data[0]][data[1]] = _______

flow = Flow(parameters['FlowJob']['JobName'])
flow.msg.SetVerbosity(parameters['FlowJob']['Verbosity'])

for algopath in parameters['FlowJob']['Paths']:
    path.append(algopath)

for algo, pars in parameters.items():
    if algo == 'FlowJob': continue
    exec('from %s import *' % algo)
    flow.AddAlgorithm( algo, **pars )
