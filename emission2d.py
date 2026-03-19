import sdf_helper as sh
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.constants import mu_0, epsilon_0, k, m_p
import sunpy.visualization.colormaps as cm


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


fig, ax = plt.subplots(3, 3, figsize = (15,15), sharey=True, sharex = True)
fig2, axes = plt.subplots(1,1)

nt = 3

files = ["aia211"]

for file in files:

    if (file != "x-ray"):
        #colour = plt.colormaps['sdo'+file]
        file1 = open("../chiantitables/goft_table_" + file + "_abco.dat")
        lines = file1.readlines()
    
        bins = np.array([])
        density = np.array([])
    
    
        for i in range(40):
            for x in lines[i+7].split():
                bins = np.append(bins, float(x))
    
        for i in range(200):
            density = np.append(density, lines[i*41+49])
   

    starts = ["sh","fl","fl2"]
     
    for start in starts:
         
        ind = starts.index(start)
        if (start == "fl2"): start = "fl"
        #ind = files.index(file)
        time = np.array([])
        coronal_intensity = np.array([])
        footpoint_intensity = np.array([])
        apex_intensity = np.array([])
        total_intensity = np.array([])
        coronal_x_intensity = np.array([])
        footpoint_x_intensity = np.array([])
        apex_x_intensity = np.array([])
        total_x_intensity = np.array([])
        
        for i in range(nt):
            indx = i
            i *= 40  
            i += 120
            si = (4 - len(str(i)))*"0" + str(i)
            #data = sh.getdata("./Flares/10^20/" + start + "/" + si + ".sdf")
            #data = sh.getdata("../DiracData/fixed/2.5/" + start + "/" + si + ".sdf")
            data = sh.getdata("../DiracData/final/" + start + "/3/" + si + ".sdf")
            #data = sh.getdata("../../Lare2d-dev/Data/simple/strong" + start + "/5e-3/"  + si + ".sdf")
            #if (start=="SH"): data = sh.getdata("../../Lare2d-dev/Data/" + si + ".sdf")


            time = np.append(time, t * t0)
            temp = data.Fluid_Temperature.data * T0
            rho = data.Fluid_Rho.data * rho0
            ne = rho / 1.67e-27 / 1e6
            
            #if (i==0):
            #    for j in range(len(temp)):
            #        if temp[j] > 1 * 10**6:
            #            a1 = j
            #            break
            #    for j in range(len(temp)):
            #        if temp[j] > 1 * 10**6:
            #            a2 = j
            #            break
            
            temp = temp[250:550,50:400]
            ne = ne[250:550,50:400]

            len1 = temp.shape[1]
            len2 = temp.shape[0]

            y = np.linspace(0.05,0.4, len1)
            x = np.linspace(-0.15,0.15, len2)

            const = (y[-1]-y[0])*(x[-1]-x[0])*1.e20 / (len1*len2) / 1.e7 / (1.48e13)**2 

            emission = np.zeros((len1,len2))
            x_rays = np.zeros((len1,len2))
            
            coronal = 0 
            footpoint = 0
            apex = 0
            total = 0
            coronal_x = 0
            footpoint_x = 0
            apex_x = 0
            total_x= 0
            n1 = 0
            n2 = 0
            n3 = 0
            n4 = 0 
            
            for i in range(len1):
                for j in range(len2):
                    T = temp[j][i]
                    n = ne[j][i]
                    
                    log_t = np.log10(T)
                    log_n = np.log10(n)
                    
                    
                    if (file != "x-ray"):
                        response = index(T, n)
                        emission[i][j] = response * n**2
                    else: 
                        emission[i][j] = x_ray_emission(T, n, 1, 8)
                    
                    emission[i][j] *= const

                    if ((abs(x[j]) < 0.04) and (abs(y[i] - 0.2) > 0.1)):
                        coronal += emission[i][j]
                        n1 +=1
                    if ((abs(x[j] - 0.02) < 0.01) and (abs(y[i] - 0.12) < 0.015)):
                        footpoint += emission[i][j]
                        n2 += 1
                    if ((abs(x[j]) < 0.05) and (abs(y[i] - 0.3) < 0.05)):
                        apex += emission[i][j]
                        n3 += 1
                    total += emission[i][j]
                    n4+=1
                     
            n1 = 1
            n2 = 1
            n3 = 1
            n4 = 1
    

            coronal_intensity = np.append(coronal_intensity, coronal/n1)
            footpoint_intensity = np.append(footpoint_intensity, footpoint/n2)
            apex_intensity = np.append(apex_intensity, apex/n3)
            total_intensity = np.append(total_intensity, total/n4)  
            
            #emission = emission[50:400,200:600]
            
            ext = (-15,15,5,40)
            out = ax[ind,indx].imshow(emission * 1.e16, extent = ext, origin = "lower", vmin  = 0.1, vmax = 10)
            ax[2,indx].set_xlabel('X (Mm)', fontsize = 16)
            ax[2,indx].set_xticks([-10,0,10])
            ax[2,indx].xaxis.set_tick_params(labelsize = 16)
            ax[0,indx].set_title("{:.0f}".format((t-0.25)*t0) + "s", fontsize = 18)
            ax[indx,0].set_ylabel("Y (Mm)", fontsize = 16)
            ax[indx,0].set_yticks([10,20,30,40])
            ax[indx,0].yaxis.set_tick_params(labelsize = 16)
            #plt.imshow(emission, origin = 'lower', vmin = 1.e-17, vmax = 5.e-16, cmap = "viridis")
            #plt.colorbar()
            #plt.show()
            #plt.imshow(ne**2 * temp, vmax = 1.e25, cmap = 'inferno')
            #plt.imshow(rho, origin = 'lower',  cmap = "viridis")   
            #plt.show()   

        
        #axes[ind].plot(time-time[0], coronal_intensity, label = start)
        axes.plot(time-time[0], footpoint_intensity / max(footpoint_intensity), label = start)
        #axes[ind].plot(time-time[0], apex_intensity, label = "apex-"+start)
        #axes[ind].plot(time-time[0], total_intensity/max(total_intensity), label = "total-"+start)
        axes.set_title("aia_211")
        axes.set_xlabel("Time (s)")
        axes.set_ylabel("Normalised intensity")
        #axes[ind].legend()
        #axes[files.index(file)].imshow(emission, origin = 'lower', vmin = 100, vmax = 1.e2, cmap = "viridis")

ax[0,2].set_ylabel("SH", rotation =-45, labelpad = 25, fontsize = 18)
ax[1,2].set_ylabel("FL", rotation =-45, labelpad = 25, fontsize = 18)
ax[2,2].set_ylabel("SNB", rotation =-45, labelpad = 25, fontsize = 18)
ax[0,2].yaxis.set_label_position("right")
ax[1,2].yaxis.set_label_position("right")
ax[2,2].yaxis.set_label_position("right")
fig.tight_layout()
fig.subplots_adjust(right = 0.8)
cbar_ax = fig.add_axes([0.85,0.1,0.05,0.8])
cbar = fig.colorbar(out, cax = cbar_ax)
cbar.ax.tick_params(labelsize = 16)
cbar.set_label("AIA 211$\AA$ Intensity (a.u.)", fontsize = 20)
fig.savefig("aia_211_emission.pdf", format = 'pdf')
fig2.savefig("211_emission_time.pdf", format = 'pdf')
plt.show()

