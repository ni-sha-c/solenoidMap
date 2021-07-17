using PyPlot
using DelimitedFiles
using JLD
X01 = readdlm("data/dJds2_0.01.txt")
X05 = readdlm("data/dJds2_0.05.txt")
nS01 = X01[:,1]
nS05 = X05[:,1]
dJds01 = X01[:,2]
dJds05 = X05[:,2]
truth = dJds05[1]

#s3 parameter in S3 is actually s2 in the Fd code.
X = load("data/dJds3_K12_N.jld")
nSS3 = X["n_samples"]
dJdsS3 = X["dJds"]



fig, ax = subplots()
ax.loglog(nS01, abs.((dJds01.-truth)./truth), ".-", ms=20)
ax.loglog(nS05, abs.((dJds05.-truth)./truth), "P-", ms=20)

ax.grid(true)
ax.xaxis.set_tick_params(labelsize=28)
ax.yaxis.set_tick_params(labelsize=28)




