from subprocess import Popen, PIPE
from pylab import *
from numpy import *


def computeObj(nt, nr, rmax, s1, s2):
    args = [str(nt), str(nr), str(rmax), str(s1), str(s2)]
    print(args)
    numDevices = 8
    procs = []
    for iDevice in range(numDevices):
        p = Popen(['./solenoid.exe', str(iDevice)] + args, stdout=PIPE)
        procs.append(p)
    obj = []
    for p in procs:
        lines = p.stdout.read().splitlines()
        output = array([line.split() for line in lines], float)
        obj.append(output[:,2])
    return array(obj).mean(0).reshape([nt,nr]).T

def computeObjRep(nt, nr, rmax, s1, s2, nrep):
    obj = [computeObj(nt, nr, rmax, s1, s2) for i in range(nrep)]
    return mean(obj, 0)

s1, s2 = 1.4, 0
n = 50
ds = 0.05
dobjds1 = (computeObjRep(n, n, 3, s1 + ds, s2, 10) -
           computeObjRep(n, n, 3, s1 - ds, s2, 10)) / (2 * ds)
dobjds2 = (computeObjRep(n, n, 3, s1, s2 + ds, 10) -
           computeObjRep(n, n, 3, s1, s2 - ds, 10)) / (2 * ds)

savetxt("dPhids_r_fd.txt",dobjds1)
savetxt("dPhids_t_fd.txt",dobjds2)

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
