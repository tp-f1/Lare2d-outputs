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
    
    min_diff = 10
    for j in range(200):
        diff = abs(bins[j] - log_t)
        if diff < min_diff:
            min_diff = diff
            ind = j
    
    d = int(ind/5)
    r = ind - 5 * d
            
    k = 48 + int((log_n - 8) * 100 / 3) * 41 
    k = min(8207, k)

    response = float(lines[d+k].split()[r])
    return response


fig, axes = plt.subplots(1, 3, figsize = (16,6), sharey=False)

nt = 25
files = ["aia094", "aia171", "aia211"]

for file in files:
    
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
    
    starts = ["sh","fl","snb"]
     
    for start in starts:
         
        ind = files.index(file)
        time = np.array([])
        coronal_intensity = np.array([])
        footpoint_intensity = np.array([])
        apex_intensity = np.array([])
        
        for i in range(nt):
            i *= 2  
            #i += 150
            si = (4 - len(str(i)))*"0" + str(i)
            #data = sh.getdata("./Flares/10^20/" + start + "/" + si + ".sdf")
            data = sh.getdata("../DiracData/fixed/3.5/" + start + "/" + si + ".sdf")
            #data = sh.getdata("../DiracData/new/" + si + ".sdf")
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
            len1 = temp.shape[1]
            len2 = temp.shape[0]
            
            y = np.linspace(0,0.8, len1)
            x = np.linspace(-0.4,0.4, len2)

            const = (y[-1]-y[0])*(x[-1]-x[0])*1.e20 / (len1*len2) / 1.e7 / (1.48e13)**2 

            emission = np.zeros((len1,len2))
            coronal = 0 
            footpoint = 0
            apex = 0
            n1 = 0
            n2 = 0
            n3 = 0
            
            
            for i in range(len1):
                for j in range(len2):
                    T = temp[j][i]
                    n = ne[j][i]
                    

                    response = index(T, n)
                    log_t = np.log10(T)
                    log_n = np.log10(n)
                    
                    emission[i][j] = response * n**2
                    #emission[i][j] *= const


                    if ((abs(x[j]) < 0.08) and (abs(y[i] - 0.17) > 0.09)):
                        coronal += emission[i][j]
                        n1 += 1
                    if ((abs(x[j] - 0.1) < 0.05) and (abs(y[i] - 0.15) < 0.05)):
                        footpoint += emission[i][j]
                        n2 += 1
                    if ((abs(x[j]) < 0.05) and (abs(y[i] - 0.35) < 0.05)):
                        apex += emission[i][j]
                        n3 += 1

            coronal_intensity = np.append(coronal_intensity, coronal/n1)
            footpoint_intensity = np.append(footpoint_intensity, footpoint/n2)
            apex_intensity = np.append(apex_intensity, apex/n3)
            
            
            #plt.imshow(emission, origin = 'lower', vmax = 1.e3, cmap = "viridis")
            #plt.colorbar()
            #plt.show()
            #plt.imshow(ne**2 * temp, vmax = 1.e25, cmap = 'inferno')
            #plt.imshow(rho, origin = 'lower',  cmap = "viridis")   
            #plt.show()   


        axes[ind].plot(time-time[0], coronal_intensity / coronal_intensity[0], label = "coronal-"+start)
        #axes[ind].plot(time-time[0], footpoint_intensity / footpoint_intensity[0], label = "footpoint-"+start)
        #axes[ind].plot(time-time[0], apex_intensity / apex_intensity[0], label = "apex-"+start)
        axes[ind].set_title(file)
        axes[ind].set_xlabel("Time (s)")
        axes[ind].set_ylabel("Mean Intensity (normalised units)")
        axes[ind].legend()
        #axes[files.index(file)].imshow(emission, origin = 'lower', vmin = 100, vmax = 1.e2, cmap = "viridis")


plt.savefig("coronal_emission.png")
plt.show()

