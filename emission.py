import sdf_helper as sh
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.constants as sc

temp_norm = 115.276
rho_norm = 10**-6
time_norm = 78609.8


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

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, figsize = (10,6))

nt = 200
files = ["aia131", "aia171", "aia304", "aia335"]

for file in files:
    file1 = open("../chiantitables/goft_table_" + file + "_abco.dat")
    lines = file1.readlines()
    
    time = np.array([])
    bins = np.array([])
    apex_intensity = np.array([])
    foot_intensity = np.array([])
    coronal_intensity = np.array([])
    apext = np.array([])
    foott = np.array([])
    apexr = np.array([])
    footr = np.array([])
    density = np.array([])
    
    for i in range(40):
        for x in lines[i+7].split():
            bins = np.append(bins, float(x))
    
    for i in range(200):
        density = np.append(density, lines[i*41+49])
    
    
    starts = ["SH","SNB"]
    
    for start in starts:
        for i in range(nt):
            i += 100
            si = (4 - len(str(i)))*"0" + str(i)
            data = sh.getdata("./Flares/10^20/" + start + "/" + si + ".sdf")
            
            
            time = np.append(time, t * time_norm)
            temp = data.Fluid_Temperature.data[2] * temp_norm
            rho = data.Fluid_Rho.data[2] * rho_norm
            ne = rho / 1.67e-27 / 1e6
            
            if (i==100):
                for j in range(len(temp)):
                    if temp[j] > 1 * 10**6:
                        a1 = j
                        break
                for j in range(len(temp)):
                    if temp[j] > 1 * 10**6:
                        a2 = j
                        break
             
            t_apex = temp[int(len(temp)/2)]
            ne_apex = rho[int(len(temp)/2)] / 1.67e-27 / 1e6
            

             
            t_foot = temp[a1]
            ne_foot = rho[a1] / 1.67e-27 / 1e6
                
            for l in range(2):
                if (l==0):
                    response = index(t_apex, ne_apex)
                    log_t = np.log10(t_apex)
                    log_n = np.log10(ne_apex)
                else:
                    response = index(t_foot, ne_foot)
                    log_t = np.log10(t_foot)
                    log_n = np.log10(ne_foot)
            
                if (l==0):
                    apex_intensity = np.append(apex_intensity, response * ne_apex**2)
                    apext = np.append(apext, t_apex)
                    apexr = np.append(apexr, ne_apex)
                else:
                    foot_intensity = np.append(foot_intensity, response * ne_foot**2)
                    foott = np.append(foott, t_foot)
                    footr = np.append(footr, ne_foot)
            
            cintensity = np.array([])
            for l in range(300, 1100):
                T = temp[l]
                n = rho[l] / 1.67e-27 / 1.e6
                response = index(T,n)
                cintensity = np.append(cintensity, response * n**2)
            coronal_intensity = np.append(coronal_intensity, np.average(cintensity))
                
            intensity = np.array([])
            
            for l in range(len(temp) - 100):
                response = index(temp[l+ 50], ne[l+50])
                intensity = np.append(intensity, response * ne[l+50]**2)
            
            y = np.linspace(0,70, len(temp)-100)
   #         plt.plot(y , intensity)
    #        plt.show()

        length = len(apex_intensity)
    #apex_intensity /= max(apex_intensity)
    #foot_intensity /= max(foot_intensity)
    apex_intensity *= 2.e8 / 1.e10
    foot_intensity *= 2.e8 / 1.e10
    coronal_intensity *= 2.e8 * 2.8e-9
    time = time - time[0]
    starts = ["SH", "SNB"]
    colours = ['black', 'red']
    linestyles = ['-', '--']
    for i in range(len(starts)):
        if (file == "aia131"):
            ax1.plot(time[i*nt: (i+1)*nt], coronal_intensity[i*nt: (i+1)*nt], label = starts[i], color = colours[i], linestyle = linestyles[i])
        if (file == "aia171"):
            ax2.plot(time[i*nt: (i+1)*nt], coronal_intensity[i*nt: (i+1)*nt], label = starts[i], color = colours[i], linestyle = linestyles[i])
        if (file == "aia304"):
            ax3.plot(time[i*nt: (i+1)*nt], coronal_intensity[i*nt: (i+1)*nt], label = starts[i], color = colours[i], linestyle = linestyles[i])
        if (file == "aia335"):
            ax4.plot(time[i*nt: (i+1)*nt], coronal_intensity[i*nt: (i+1)*nt], label = starts[i], color = colours[i], linestyle = linestyles[i])
        


#fig.text(0.01, 0.5, "Intensity [DN s$^{-1}$ $sr^{-1}$]", va = 'center', rotation = 'vertical', fontsize = 14)
#ax2.set_ylabel("Emissivity [erg s$^{-1}$ cm$^{-3}$ $sr^{-1}$]")

ax1.set_title(r"$131 \, \mathrm{\AA}$", fontsize = 15)
ax2.set_title(r"$171 \, \mathrm{\AA}$", fontsize = 15)
ax3.set_title(r"$304 \, \mathrm{\AA}$", fontsize = 15)
ax4.set_title(r"$335 \,\mathrm{\AA}$", fontsize = 15)

ax1.set_xlabel("Time [s]", fontsize = 13)
ax2.set_xlabel("Time [s]", fontsize = 13)
ax3.set_xlabel("Time [s]", fontsize = 13)
ax4.set_xlabel("Time [s]", fontsize = 13)


ax1.set_ylabel("Intensity [DN/s]", fontsize = 13)
ax2.set_ylabel("Intensity [DN/s]", fontsize = 13)
ax3.set_ylabel("Intensity [DN/s]", fontsize = 13)
ax4.set_ylabel("Intensity [DN/s]", fontsize = 13)

#plt.xlabel("Time [s]", fontsize = 14)
#ax1.set_title("Apex", fontsize = 16)
#ax2.set_title("Footpoint", fontsize = 16)

ax1.legend(loc = 1)
ax2.legend(loc = 1)
ax3.legend(loc = 1)
ax4.legend(loc = 1)

#ax1.legend(loc = 'upper right')
#ax1.legend(loc = 'lower right')    

#plt.xlim(0, 600)
#plt.ylim(0, 1.6)   
fig.tight_layout(rect = (0.025,0, 1,1))
plt.savefig("quad_emission.pdf", format = 'pdf')
plt.show()
"""
    
    for i in range(len(starts)):
        plt.plot(time[i*nt: (i+1)*nt], foot_intensity[i*nt: (i+1)*nt], label = starts[i] + file)
    plt.legend()
    plt.show()
    
"""

