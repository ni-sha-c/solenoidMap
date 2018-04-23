from subprocess import Popen, PIPE
from pylab import *
from numpy import *

procs = []
for iDevice in range(8):
    p = Popen(['./solenoid.exe', str(iDevice), str(20), str(20), str(3)],
              stdout=PIPE)
    procs.append(p)

obj = []
for p in procs:
    output = array([line.split() for line in p.stdout.read().splitlines()], float)
    obj.append(output[:,2])

obj = array(obj).mean(0)

r = arange(20) / 20. * 3
t = arange(20) * 2*pi/20.
r, t = meshgrid(r, t, indexing='ij')
x = r * cos(t)
y = r * sin(t)
x = hstack([x, x[:,:1]])
y = hstack([y, y[:,:1]])
obj = obj.T
obj = hstack([obj, obj[:,:1]])

contour(x, y, obj)
show()
