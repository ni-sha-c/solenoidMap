ARCH=70
CUDA=-Wno-deprecated-gpu-targets -m64 -x cu -arch=sm_${ARCH}  -lineinfo -Xptxas --warn-on-local-memory-usage -Xptxas --warn-on-spills --use_fast_math

default:	solenoid.exe

%.exe:	%.o
	CXX=g++-6 CC=gcc-6 ${CUDA_HOME}/bin/nvcc -arch=sm_${ARCH} $< -o $@

%.o:	%.cpp
	CXX=g++-6 CC=gcc-6 ${CUDA_HOME}/bin/nvcc -D_FORCE_INLINES -std=c++11 ${CUDA} ${INC} -Xcompiler -fPIC -I. -O3 -dc $< -o $@
