
#Plots the standard SDF output files using
#sdf_helper's plot_auto function



import sdf_helper as sh
import numpy as np
import matplotlib.pyplot as plt
import math
from pynput.keyboard import Listener, Key
import matplotlib.animation as animation

def next_image(key):
    if (key == Key.space):
        plt.close()

listener = Listener(on_press = next_image) 
listener.start()

array = np.array([])
temps = np.empty((0,1400), float)
rhos = np.empty((0,1400), float)


starts = ["sh", "lim", "snb"]
tstart = 0.0 
for start in starts:
    artists = []
    fig, (ax1, ax2) = plt.subplots(1,2, sharey = False)
    #fig2, ax3 = plt.subplots()
    artists2 = []
    for i in range(1):
        i+=100 
        si = (4 -  len(str(i)))*"0" + str(i)
        data1 = sh.getdata("../../Lare2d-dev/Data/finalresults/" + start + "/" + si + ".sdf")
        
        #data1 = sh.getdata("../../Lare2d-dev/Data/" + si + ".sdf")
        #data2 = sh.getdata("../../Lare2d-dev/Data/initialt/sh/0450"+ ".sdf")

        rho = data1.Fluid_Rho
        #vx = data.Velocity_Vx
        vy = data1.Velocity_Vy
        #bx = data.Magnetic_Field_Bx
        #by = data.Magnetic_Field_By
        #e = data.Fluid_Energy
        #n = data.PIP_neutral_fraction
        #p = data.Fluid_Pressure
        t1 = data1.Fluid_Temperature   
        #t2 = data2.Fluid_Temperature

        #sh.list_variables(data)
   
        #sh.plot_auto(vy)
        #plt.show()
    
    
        #sh.plot_auto(rho)
        #plt.show()

        #ax2 = ax1.twinx()

        temp1 = t1.data[2] * 115.3
        #temp2 = t2.data[2] * 115.3
        #tdiff = (temp1 - temp2) / temp2 * 100

        density = rho.data[2] * 1.0067 * 10**(-6)
        velocity = vy.data[2] * 892 
        time_norm = 170 * 10**6 / 892 
        time = 10**(-4) * (i - 100) * time_norm
        
        print(max(temp1), min(density))

        dT = temp1[1:] - temp1[0:-1]
        dx = 70 * 10**6 / len(temp1)
        temp_b = 0.5 * (temp1[1:] + temp1[0:-1])
        l_t = np.abs(temp_b * dx / dT)
        
        mfp = 5.5 * 1e7 * temp1**2 / (density / (1.2 * 1.67e-27))
        mfp = 0.5 * (mfp[1:] + mfp[0:-1])
        Kn = mfp / l_t

        Kn = np.append(Kn,0.0)

        y = np.linspace(0, 70, len(temp1))
        ax1.set_xlabel("Distance along loop / Mm")
        
        #fig.suptitle("Radiation and heating (TRAC + flux limiting)")
        ax1.set_title("Temperature")
        ax1.set_ylabel("Temperature / K")
        ax1.set_yscale("log")
        plot1, = ax1.plot(y, temp1, color = "b")
        plot2, = ax2.plot(y, temp1, color = "g")
        
        #plot2, = ax2.plot(y, temp2, color = "b")
        
        #ax2.set_ylabel("Temperature / K")
        ax2.set_yscale("log")
        ax2.set_xlabel("Distance along loop / Mm")
        ax2.set_title("Knudsen number")
        
        artists.append([plot1, plot2])
        temps = np.append(temps, [temp1], axis = 0)
        rhos = np.append(rhos, [density], axis = 0)

        #y = np.linspace(0, 170, len(temp1))
        #ax3.set_title("Percentage difference in temperature (TRAC + FL)")
        #ax3.set_ylabel("$T_{imp}$ - $T_{super}$ / %")
        #ax3.set_title("Velocity (Townsend method)")
        #ax3.set_ylabel("Velocity / m/s ")
        #ax3.set_xlabel("Distance along loop / Mm")
        #ax3.set_ylim(-5000,5000)
        #plot3 = ax3.plot(y, tdiff, color = "r")
        #fig2.tight_layout() 
        #artists2.append(plot3)
        #ax2.plot(y,density, label = start)
        #ax2.set_ylabel("Density / kgm$^-3$")
        #ax2.set_yscale("log")
    
    #ani = animation.ArtistAnimation(fig = fig, artists = artists,interval = 400)
    
    #ani.save(filename="limiter.gif", writer = "pillow")
    
    #ani2 = animation.ArtistAnimation(fig = fig2, artists = artists2, interval = 400)
    
    plt.show()
    #ani2.save(filename="exact-velocity.gif", writer = "pillow")    

            #print(temp[0], temp[1], temp[2], temp[3])
         #plt.savefig("SH" + si + ".png")
        #plt.show()
        
        #if (i / 10 == int(i/10)):
        #plt.savefig("conduct_only" + str(i/10) + ".png") 
#shh.plot_auto(vy)
#t = np.linspace(0,250,num =250)
#plt.plot(t, array)
#plt.show()

fig, (ax1, ax2) = plt.subplots(1, 2)
ax2.plot(y, temps[0], color = 'k', label = "SH")
ax2.plot(y, temps[1], color = 'grey', label = "FL", linestyle = ':')
ax2.plot(y, temps[2], color = 'r', label = "SNB", linestyle = '--')

ax1.plot(y, rhos[0] / (1.2 * 1.67e-21), color = 'k', label = "SH")
ax1.plot(y, rhos[1] / (1.2 * 1.67e-21), color = 'grey', label = "FL", linestyle = ':')
ax1.plot(y, rhos[2] / (1.2 * 1.67e-21), color = 'r', label = "SNB", linestyle =  '--')
ax1.set_yscale('log')
ax2.set_yscale('log')
ax2.set_ylabel("Temperature [K]", fontsize = 12)
ax1.set_ylabel("Electron number density [cm$^{-3}$]", fontsize = 12)
ax2.set_xlabel("Distance along the loop [Mm]", fontsize = 12)
ax1.set_xlabel("Distance along the loop [Mm]", fontsize = 12)
ax1.legend(fontsize = 12)
ax2.legend(fontsize = 12)
#plt.yscale()
plt.tight_layout()
fig.set_size_inches(11,4)
plt.savefig("initialboth.svg", format = 'svg')
plt.show()


