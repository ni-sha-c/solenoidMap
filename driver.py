from subprocess import Popen, PIPE
from pylab import *
from numpy import *

procs = []
for iDevice in range(2):
    p = Popen(['./solenoid.exe', str(iDevice), str(20), str(20), str(3), str(1.4), str(0)],
              stdout=PIPE)
    procs.append(p)

obj = []
for p in procs:
    output = array([line.split() for line in p.stdout.read().splitlines()], float)
    obj.append(output[:,2])

obj = array(obj).mean(0).reshape([20,20]).T


procs = []
for iDevice in range(2):
    p = Popen(['./solenoid.exe', str(iDevice), str(20), str(20), str(3), 
          str(1.45), str(0)],
              stdout=PIPE)
    procs.append(p)

p1obj = []

for p in procs:
    output = array([line.split() for line in p.stdout.read().splitlines()], float)
    p1obj.append(output[:,2])

p1obj = array(p1obj).mean(0).reshape([20,20]).T

procs = []
for iDevice in range(2):
    p = Popen(['./solenoid.exe', str(iDevice), str(20), str(20), str(3), str(1.4), str(0.05)],
              stdout=PIPE)
    procs.append(p)

p2obj = []
for p in procs:
    output = array([line.split() for line in p.stdout.read().splitlines()], float)
    p2obj.append(output[:,2])

p2obj = array(p2obj).mean(0).reshape([20,20]).T

r = arange(20) / 20. * 3
t = arange(20) * 2*pi/20.
r, t = meshgrid(r, t, indexing='ij')
x = r * cos(t)
y = r * sin(t)
x = hstack([x, x[:,:1]])
y = hstack([y, y[:,:1]])
ds = 0.05
dobjds1 = (p1obj - obj)/ds
dobjds2 = (p2obj - obj)/ds
savetxt("dPhids_r_fd.txt",dobjds1[:])
savetxt("dPhids_t_fd.txt",dobjds2[:])

dobjds1 = hstack([dobjds1, dobjds1[:,:1]])
dobjds2 = hstack([dobjds2, dobjds2[:,:1]])
#f = figure(1)
#contour(x, y, dobjds1)
#colorbar()
#f.show()
#g = figure(2)
#contour(x, y, dobjds2)
#colorbar()
#g.show()
