#include<cmath>
#include<cstdio>
#include<cassert>
#include<cstdlib>
#include<algorithm>

using namespace std;

template<typename ftype>
__device__ __forceinline__ void step(ftype u[3], ftype s[2], int n)
{
    const ftype c1 = 4.0, c2 = 2.0;
    for (int i = 0; i < n; ++i) {
        ftype x = u[0];
        ftype y = u[1];
        ftype z = u[2];
    
        ftype r2 = x * x + y * y;
        ftype r = sqrt(r2);
        ftype rtilde = s[0] + (r - s[0]) / c1 + x / c2 / r;
        ftype c2t = 2 * x * x / r2 - 1;
        ftype s2t = 2 * x * y / r2;
    
        ftype p = s[1]  * s2t / 4;
        ftype cp = cos(p);
        ftype sp = sin(p);
        ftype s2tp = s2t * cp + c2t * sp;
        ftype c2tp = c2t * cp - s2t * sp;
    
        u[0] = rtilde * c2tp;
        u[1] = rtilde * s2tp;
        u[2] = z / c1 + y / c2 / r;
    }
}

template<typename ftype>
__device__ __forceinline__ ftype gaussian(ftype x)
{
    return exp(-x*x/2);
}

template<typename ftype>
__device__ __forceinline__ ftype objective(ftype u[3], ftype s[2], int it, ftype dt, int ir, ftype dr)
{
    const double PI = 3.1415926;//atan2(1.0, 0.0) * 2;
    ftype x = u[0];
    ftype y = u[1];

    ftype r2 = x * x + y * y;
    ftype r = sqrt(r2);
    ftype t = atan2(y, x);

    t += PI;
    if (it == 0) t = fmod(t + dt, (ftype)(2*PI)) - dt;

    ftype rFrac = r / dr - ir;
    ftype tFrac = t / dt - it;
    return max((ftype)0, min(1 - rFrac, 1 + rFrac)) *
           max((ftype)0, min(1 - tFrac, 1 + tFrac));
}

template<typename ftype, typename objType>
__global__ void accumulate(ftype (*u)[3], ftype s[2], objType *obj,
                           int nt, int nr, ftype rmax, int steps)
{
    //const double PI = atan2(1.0, 0.0) * 2;
    const double PI = 3.1415926;//atan2(1.0, 0.0) * 2;
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    step(u[i], s, steps);
    ftype dr = rmax / nr;
    ftype dt = (2*PI) / nt;
    for (int ir = 0; ir < nr; ++ir) {
        for (int it = 0; it < nt; ++it) {
            int ibin = ir * nt + it;
            ftype obji = objective(u[i], s, it, dt, ir, dr);
            if (obji) atomicAdd(obj + ibin, obji);
        }
    }
}

typedef float ftype;

void init(ftype (**u)[3], ftype ** s, ftype s1, ftype s2, int nBlocks, int threadsPerBlock)
{
    const int nSamples = nBlocks * threadsPerBlock;
    ftype (*uCPU)[3] = new ftype[nSamples][3];
    for (int i = 0; i < nSamples; ++i) {
        uCPU[i][0] = rand() / (ftype)RAND_MAX;
        uCPU[i][1] = rand() / (ftype)RAND_MAX;
        uCPU[i][2] = rand() / (ftype)RAND_MAX;
    }
    cudaMalloc(u, sizeof(ftype) * nSamples * 3);
    cudaMemcpy(*u, uCPU, sizeof(ftype) * nSamples * 3, cudaMemcpyHostToDevice);
    delete[] uCPU;

    ftype sCPU[2] = {s1, s2};
    cudaMalloc(s, sizeof(ftype) * 2);
    cudaMemcpy(*s, sCPU, sizeof(ftype) * 2, cudaMemcpyHostToDevice);

    accumulate<<<nBlocks, threadsPerBlock>>>(*u, *s, (ftype*)0, 0, 0, (ftype)0, 1000);
}

int main(int argc, char * argv[])
{
    const int nBlocks = 10000;
    const int threadsPerBlock = 256;

    assert (argc == 7);
    int iDevice = atoi(argv[1]);
    if (cudaSetDevice(iDevice)) {
        fprintf(stderr, "error selecting %d\n", iDevice);
        exit(-1);
    }
    int nt0 = atoi(argv[2]);
    int nr0 = atoi(argv[3]);
    ftype rmax = atof(argv[4]);
	ftype s1 = atof(argv[5]);
	ftype s2 = atof(argv[6]); 

    ftype (*u)[3], *s;
    init(&u, &s, s1, s2,nBlocks, threadsPerBlock);

    ftype * objCPU = new ftype[nt0 * nr0];
    double * objFinal = new double[nt0 * nr0];
    memset(objFinal, 0, sizeof(double) * nt0 * nr0);

    ftype * objective;
    cudaMalloc(&objective, sizeof(ftype) * nr0 * nt0);

    const int nRepeat = 10000;
    for (int iRepeat = 0; iRepeat < nRepeat; ++iRepeat) {
        cudaMemset(objective, 0, sizeof(ftype) * nr0 * nt0);
        const int nAccums = 10;
        for (int i = 0; i < nAccums; ++i) {
            accumulate<<<nBlocks, threadsPerBlock>>>(u, s, objective, nt0, nr0, rmax, 10);
        }
        cudaMemcpy(objCPU, objective, sizeof(ftype) * nr0 * nt0, cudaMemcpyDeviceToHost);
    
        for (int i = 0; i < nt0 * nr0; ++i) {
            objFinal[i] += objCPU[i] / nRepeat / nAccums / nBlocks / threadsPerBlock;
        }
    }

    for (int it0 = 0; it0 < nt0; ++it0) {
        for (int ir0 = 0; ir0 < nr0; ++ir0) {
            int i = it0 * nr0 + ir0;
            printf("%d %d %40.30f\n", it0, ir0, objFinal[i]);
        }
    }
}
