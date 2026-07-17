import sdf_helper as sh
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.constants import mu_0, epsilon_0, k, m_p
from decimal import Decimal
import matplotlib.patches as patches
from matplotlib.ticker import FormatStrFormatter


def remove_exponent(d):
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()

B0 = 0.001
L0 = 100e6
rho0 = 1.e-6

v0 = B0 / np.sqrt(mu_0 * rho0)
T0 = v0**2 * 1.2 * m_p / k
t0 = L0 / v0

fig1, (ax11, ax12, ax13) = plt.subplots(1,3, sharey = True)
fig1.set_size_inches(8,5)
fig2, ax2 = plt.subplots(1,1)
fig2.set_size_inches(4,5)
fig3, (ax31,ax32, ax33) = plt.subplots(1,3, sharey = True)
fig4, ax4 = plt.subplots(1,1)
fig3.set_size_inches(8,5)
fig5, ax5 = plt.subplots(1,1)
fig5.set_size_inches(4,5)
fig6, ax6 = plt.subplots(1,1)


starts = ["sh", "fl/0.01", "fl/0.06", "fl/0.2", "fl/1.0", "snb"]
fields = np.array(["1.5","2.0","2.5","3.0","3.5"])
mark = ["x", "^", "^", "^", "^", "s"]
col = ["k", "blue", "red", "orange", "green", "red"]
lin = ['solid', 'dotted','dotted', 'dotted', 'dotted', 'dashed']

for start in starts:
    ind = starts.index(start)
    maxTs = np.array([])
    maxvs = np.array([])
    minvs = np.array([])
    for field in fields:
       
        ftemp = np.array([])
        fden = np.array([])
        temperature = np.array([])
        density = np.array([])
        time = np.array([])
        waveT = np.array([])
        corona = np.array([])
        velocity = np.array([])


        maxT = 0.0
        maxv = 0.0
        minv = 0.0
        for i in range(100):
            #i*= 10
            i += 100
            si = (4-len(str(i))) * "0" + str(i)
            try: data = sh.getdata("/storage/physics/phubjv/DiracData/DiracData/smooth/" + start + "/" + field + "/" + si + ".sdf")
            except: 
                break
            
            T = data.Fluid_Temperature.data * T0
            rho = data.Fluid_Rho.data * rho0
            vy = data.Velocity_Vy.data * v0


            x = np.linspace(-20,20,len(T))
            y = np.linspace(0,60, len(T[1]))
            
            apexT = np.mean(T[360:440,490:610])
            apexR = np.mean(rho[360:440,490:610])
            
            footT = np.mean(T[420:448, 180:290])
            footR = np.mean(rho[420:448, 180:290])
            footvy = np.amax(vy[420:448, 180:290])
            
            peakT = np.amax(T[380:420,500:600])
            coronalT = np.mean(T[330:470,200:600])
            wave = T[360][400]
            

            if (i > 40): peakvy = np.amax(vy[420:448, 185:335])
            maxT = max(maxT, peakT)
            maxv = max(maxv, peakvy)
            peakvy = np.amin(vy[420:448, 180:335])
            minv = min(minv, peakvy)

            temperature = np.append(temperature, apexT)
            density = np.append(density, apexR)
            ftemp = np.append(ftemp, footT)
            fden = np.append(fden, footR)
            time = np.append(time, t*t0)
            velocity = np.append(velocity, footvy)
            
            corona = np.append(corona, coronalT)
            waveT = np.append(waveT, wave)
            
            print(t)
            """
            if (i == 170 and start == 'snb' and field == "3"):
                out = ax5.imshow(np.swapaxes(T[100:300,0:300],0,1), origin = "lower", norm = 'log', vmin = 5.e5, vmax = 1.e7, extent = (-20,20,0,40), cmap = 'magma')   
                rect1 = patches.Rectangle((x[190],y[130]),x[210]-x[190],y[160]-y[130], fill = False, color = 'blue')
                rect2 = patches.Rectangle((-7,5),14,20, fill = False, color = 'darkgreen')
                ax5.add_patch(rect1) 
                ax5.add_patch(rect2) 
                ax5.set_ylabel("Y (Mm)")
                ax5.set_xlabel("X (Mm)")
                cbar = fig5.colorbar(out)
                cbar.set_ticks([5.e5,1.e6,1.e7])
                cbar.set_label("Temperature (K)")
            """
        if (field == "3.0"):
            ax4.plot(time-time[0], velocity / 1000, label = start.upper(), color = col[ind], linestyle = lin[ind])
            #ax5.plot(time-time[0], waveT / 1.e6, label = start)
            ax6.plot(fden, ftemp, label = start.upper())

        if (start == "snb"):  
            ax13.plot(time-time[0], temperature / 1e6, label = str(int(10*float(field)))+"G")
            ax33.plot(time-time[0], fden * 1.e12, label = str(int(10*float(field)))+"G") 
        
        if (start == "sh"):
            ax11.plot(time-time[0], temperature / 1.e6, label = str(int(10*float(field)))+"G")
            ax31.plot(time-time[0], fden * 1.e12, label = str(int(10*float(field)))+"G")
    
        if (start == "fl/0.2"):
            ax12.plot(time-time[0], temperature / 1.e6, label = str(int(10*float(field)))+"G")
            ax32.plot(time-time[0], fden * 1.e12, label = str(int(10*float(field)))+"G")

        maxTs = np.append(maxTs, maxT)
        maxvs = np.append(maxvs,maxv)
        minvs = np.append(minvs,minv)
    #print(maxTs) 
    if (start != "fl/0.2" or start != "fl/0.06"): 
        ax2.scatter(np.asfarray(fields)*10, maxTs / 1.e6, marker = mark[ind], color = col[ind], label = start.upper())
        #ax5.scatter(np.asfarray(fields)*10, maxvs/1000, marker = mark[ind], color = col[ind], label = start.upper())
        ax5.scatter(np.asfarray(fields)*10, minvs/1000, marker = mark[ind], color = col[ind], label = start.upper())
    if (start == "fl/0.01"): 
        prevTs = maxTs
        prevVs = maxvs
        prevmin = minvs
    if (start == "fl/1.0"): 
        ax2.vlines(np.asfarray(fields)*10, maxTs/1.e6, prevTs/1.e6, color = 'grey', linestyle = "dotted")
        #ax5.vlines(np.asfarray(fields)*10, maxvs/1000, prevVs/1000, color = 'grey', linestyle = "dotted")
        ax5.vlines(np.asfarray(fields)*10, minvs/1000, prevmin/1000, color = 'grey', linestyle = "dotted")
ax11.set_title("SH", y = 1.1, fontsize = 16)
ax11.set_xlabel("Time (s)", fontsize = 14)
ax11.set_ylabel("Apex Temperature (MK)", fontsize = 14)
ax11.legend(bbox_to_anchor=(0., 1.02, 3.4, 0.102), loc = 3, ncol = 5, mode = "expand", borderaxespad=0)
ax12.set_title("FL", y = 1.1, fontsize = 16)
ax12.set_xlabel("Time (s)", fontsize = 14)
ax13.set_title("SNB", y = 1.1, fontsize = 16)
ax13.set_xlabel("Time (s)", fontsize = 14)
ax11.set_yticks([2,4,6,8,10])
#fig1.tight_layout()
#fig1.savefig("Apex_temperature.pdf", bbox_inches='tight', format = 'pdf')

ax2.set_xlabel("Magnetic Field Strength (G)", fontsize = 12)
ax2.set_ylabel("Peak Temperature (MK)", fontsize = 12)
ax2.set_xticks([15,20,25,30,35])
ax2.tick_params(axis='x', labelsize = 10)
ax2.tick_params(axis='y', labelsize = 10)
ax2.set_yticks([0,5,10,15,20,25,30,35])
ax2.xaxis.set_major_formatter(FormatStrFormatter('%g'))
ax2.yaxis.set_major_formatter(FormatStrFormatter('%g'))
ax2.legend()
#fig2.savefig("Peak_temperature.pdf", format = 'pdf')


ax31.set_title("SH", y = 1.1, fontsize = 16)
ax31.set_xlabel("Time (s)", fontsize = 14)
ax31.set_ylabel("Footpoint Density 10$^{-12}$kg m$^{-3}$", fontsize = 14)
ax31.legend(bbox_to_anchor=(0., 1.02, 3.4, 0.102), loc = 3, ncol = 5, mode = "expand", borderaxespad=0)
ax32.set_title("FL", y = 1.1, fontsize = 16)
ax32.set_xlabel("Time (s)", fontsize = 14)
ax33.set_xlabel("Time (s)", fontsize = 14)
ax33.set_title("SNB", y = 1.1, fontsize = 16)
#fig3.savefig("Footpoint_density.pdf", bbox_inches = 'tight', format = 'pdf')

ax4.set_xlabel("Time (s)", fontsize = 14)
ax4.set_ylabel("Velocity (km s$^{-1}$)", fontsize = 14)
ax4.legend(loc = 'upper right')
ax4.xaxis.set_tick_params(labelsize = 14)
ax4.yaxis.set_tick_params(labelsize = 14)
#fig4.savefig("velocity.pdf", format = 'pdf')


ax5.set_xlabel("Magnetic Field Strength (G)", fontsize = 12)
ax5.set_ylabel("Maximum Vertical Velocity (km s$^{-1}$)", fontsize = 12)
ax5.set_xticks([15,20,25,30,35])
ax5.tick_params(axis='x', labelsize = 10)
ax5.tick_params(axis='y', labelsize = 10)
ax5.xaxis.set_major_formatter(FormatStrFormatter('%g'))
ax5.yaxis.set_major_formatter(FormatStrFormatter('%g'))
ax5.axhline(linestyle = 'dashed', color = 'grey', linewidth = 0.5)
ax5.legend(loc=7)
ax5.set_yticks([-150,-100,-50,0])
fig5.tight_layout()
fig5.savefig("Maxvspowerpoint.pdf", format = 'pdf')

ax6.set_xlabel("Density (kg/m$^3$)")
ax6.set_ylabel("Temperature (MK)")
ax6.legend()

plt.show()

