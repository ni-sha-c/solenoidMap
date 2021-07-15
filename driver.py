from subprocess import Popen, PIPE
from pylab import *
from numpy import *


def computeObj(s1, s2):
    numDevices = 1
    procs = []

    for iDevice in range(numDevices):
        p = Popen(['./solenoid.exe', str(iDevice), str(s1), str(s2)], stdout=PIPE)
        procs.append(p)
    obj = []
    for p in procs:
        lines = p.stdout.read().splitlines()
        output = array([line.split() for line in lines], float)
        print(output[0,0])
    return output[0,0]

def computeObjRep(s1, s2, nrep):
    obj = [computeObj(s1, s2) for i in range(nrep)]
    return mean(obj, 0)

s1, s2 = 1, 0.2
ds = 0.05
dobjds2 = (computeObjRep(s1, s2 + ds, 1) -
           computeObjRep(s1, s2 - ds, 1)) / (2 * ds)

savetxt("dJds2_fd.txt",32*256*2048*nrep,dobjds2)

'''
n = 50
dobjds1 = loadtxt("dPhids_r_fd.txt").T
dobjds2 = loadtxt("dPhids_t_fd.txt").T
r = arange(n) * 3. / n
t = arange(n) * 2.*pi/n
r, t = meshgrid(r, t, indexing='ij')
x = r * cos(t)
y = r * sin(t)
x = hstack([x, x[:,:1]])
y = hstack([y, y[:,:1]])

dobjds1 = hstack([dobjds1, dobjds1[:,:1]])
dobjds2 = hstack([dobjds2, dobjds2[:,:1]])
f = figure(1)
contourf(x, y, dobjds1, 100)
axis('scaled')
colorbar()
g = figure(2)
contourf(x, y, dobjds2, 100)
axis('scaled')
colorbar()
'''
