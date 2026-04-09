import sdf_helper as sh
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.constants import mu_0, epsilon_0, k, m_p
from scipy.integrate import quad
import sunpy.visualization.colormaps as cm
from matplotlib.ticker import ScalarFormatter

B0 = 0.001
L0 = 100e6
rho0 = 1.e-6

v0 = B0 / np.sqrt(mu_0 * rho0)
T0 = v0**2 * 1.2 * m_p / k
t0 = L0 / v0


def index(T, ne):

    log_t = np.log10(T)
    log_n = np.log10(ne)
    
    log_n = max(8,log_n)

    min_diff = 10
    for j in range(200):
        diff = abs(bins[j] - log_t)
        if diff < min_diff:
            min_diff = diff
            ind1 = j

    d = int(ind1/5)
    r = ind1 - 5 * d
            
    k = 48 + int((log_n - 8) * 100 / 3) * 41 
    k = min(8207, k)
    
    response = float(lines[d+k].split()[r])
    return response



# l0 and l1 in Angstroms
def x_ray_emission(T, ne, l0, l1):
    kb_keV_per_K = 8.617333262e-8
    ang_to_keV = 12.398
    A = 8.1e-39
    to_Watt = 1.60218e-12
    depth = 1.e8

    e0 = ang_to_keV / l0
    e1 = ang_to_keV / l1    

    flux = A * ne*ne * kb_keV_per_K * np.sqrt(T) * (np.exp(-e0/(kb_keV_per_K * T)) \
            * np.exp(-e1/(kb_keV_per_K * T))) * depth * to_Watt
    
    return flux

def integral(t, a, b):
    return math.sqrt(a**2 * math.sin(t)**2 + b**2 * math.cos(t)**2)

len1 = 120
len2 = 300

x = np.linspace(-0.06,0.06, len1)
y = np.linspace(0.05,0.35, len2)
x_space = x[1]-x[0]
y_space = y[1]-y[0]

s = np.linspace(-math.pi, 0, 1000)
a = 0.019
b = 0.21
x_new = a*np.cos(s)
y_new = -b*np.sin(s) + 0.09
x_diff, y_diff, index1, index2 = ([] for i in range(4))
dist = np.array([])
cumulative = 0
for i in range(len(s)):
    ind1 = np.argmin(np.abs(x-x_new[i]))
    ind2 = np.argmin(np.abs(y-y_new[i]))
    if (x[ind1]-x_new[i] > 0): ind1 -= 1 
    if (y[ind2]-y_new[i] > 0): ind2 -= 1 
     
    x_diff.append((x_new[i] - x[ind1]) / x_space)
    y_diff.append((y_new[i] - y[ind2]) / y_space)
    
    index1.append(ind1)
    index2.append(ind2)
    
    if (i == 0):
        difference = 0
    else:
        difference, _ = quad(integral, s[i-1], s[i], args = (a,b))

    cumulative += difference
    dist = np.append(dist, cumulative)

nt = 148

files = ["aia211"]

starts = ["sh", "fl", "snb"]
lin = ['solid', 'dotted', 'dashed']
col = ['k', 'grey', 'red']
mark = ['x', '^', 's']


fields = ["2.5"]

fig, ax = plt.subplots(3,1, sharex = True)
ax1 = ax[0].twinx()
ax2 = ax[1].twinx()
ax3 = ax[2].twinx()
fig.set_size_inches(15,15)

for file in files:

    if (file != "x-ray"):
        #colour = plt.colormaps['sdo'+file]
        file1 = open("../chiantitables/goft_table_" + file + "_abco.dat")
        lines = file1.readlines()
    
        bins = np.array([])
        density = np.array([])
    
    
        for i in range(40):
            for part in lines[i+7].split():
                bins = np.append(bins, float(part))
    
        for i in range(200):
            density = np.append(density, lines[i*41+49])
   


    for start in starts:
        
        emission_time = []
        ind = starts.index(start)
        for field in fields:

            time = np.array([])
            intensity = np.array([])
            
            for i in range(nt):
                indx = i
                i += 101
                si = (4 - len(str(i)))*"0" + str(i)
                data = sh.getdata("../DiracData/final/" + start + "/" + field + "/" + si + ".sdf")                
                time = np.append(time, t * t0)
                temp = data.Fluid_Temperature.data * T0
                rho = data.Fluid_Rho.data * rho0
                ne = rho / 1.67e-27 / 1e6
                
                temp = temp[340:460,50:350]
                ne = ne[340:460,50:350]
                
                
                Ts = np.array([])
                nes = np.array([])

                for i in range(len(s)):
                    i1 = index1[i]
                    i2 = index2[i]
                    x0 = x_diff[i]
                    y0 = y_diff[i]
                    T_av = temp[i1][i2] * (1 - x0) * (1 - y0) \
                         + temp[i1+1][i2] * x0 * (1 - y0) \
                         + temp[i1][i2+1] * (1 - x0) * y0 \
                         + temp[i1+1][i2+1] * x0 * y0
                    
                    n_av = ne[i1][i2] * (1 - x0) * (1 - y0) \
                         + ne[i1+1][i2] * x0 * (1 - y0) \
                         + ne[i1][i2+1] * (1 - x0) * y0 \
                         + ne[i1+1][i2+1] * x0 * y0
                    
                    Ts = np.append(Ts, T_av)
                    nes = np.append(nes, n_av)


                const = (y[-1]-y[0])*(x[-1]-x[0])*1.e20 / (len1*len2) / 1.e7 / (1.48e13)**2 

                emission = np.zeros(len(s))

                for i in range(len(s)):
                    T = Ts[i]
                    n = nes[i]
                    if (file != "x-ray"):
                        response = index(T, n)
                        emission[i] = response * n**2
                    else: 
                        emission[i] = x_ray_emission(T, n, 1, 8)

                    emission[i] *= const 

                emission_time.append(emission)
                
        emission_time = np.swapaxes(emission_time, 0,1)
        maxval = np.max(emission_time)
        emission_time /= maxval / 10
        plot = ax[ind].pcolormesh(time-time[0], dist*100, emission_time, vmin = 0.01, vmax = 1.0, norm = 'log', cmap = 'hot')
        ax[ind].set_ylabel("Distance (Mm)", fontsize = 16)
        ax[ind].set_yticks([0,10,20,30,40])
        ax[ind].yaxis.set_tick_params(labelsize =16)

ax1.set_ylabel("SH", rotation = -45, labelpad = 32, fontsize = 18)
ax2.set_ylabel("FL", rotation = -45, labelpad = 32, fontsize = 18)
ax3.set_ylabel("SNB", rotation = -45, labelpad = 32, fontsize = 18)
ax1.set_yticks([])
ax2.set_yticks([])
ax3.set_yticks([])
ax[2].set_xlabel("Time (s)", fontsize = 16)
ax[2].xaxis.set_tick_params(labelsize = 16)
fig.tight_layout()
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.1, 0.05, 0.8])
cbar = fig.colorbar(plot, cax = cbar_ax, format = '%.2f')
cbar.ax.tick_params(labelsize=16)
cbar.set_label("AIA 211$\mathrm{\AA}$ Intensity (a.u.)", fontsize = 20)
fig.savefig("1d-emission.png")
plt.show()


