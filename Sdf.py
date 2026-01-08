import time
import sdf_helper as sh
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.constants import mu_0, epsilon_0, k, m_p
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

B0 = 0.001
L0 = 1.e6
rho0 = 1.e-6

v0 = B0 / np.sqrt(mu_0 * rho0)
T0 = v0**2 * 1.2 * m_p / k
t0 = L0 / v0
print(v0)

starts = ["snb"]
tstart = 0.0 

for start in starts:
    artists = []
    #fig, (ax1, ax2) = plt.subplots(1,2, sharey = False)
    
    #fig2, ax3 = plt.subplots()
    artists2 = []
    for i in range(100):
        
        i*=5
        #i+=158
        si = (4 -  len(str(i)))*"0" + str(i)
        #data1 = sh.getdata("../../Lare2d-dev/Data/simple/strongSH/" + si + ".sdf")
        #data1 = sh.getdata("../../Lare2d-dev/Data/snbsolar/" + si + ".sdf")
        data1 = sh.getdata("../DiracData/fixed/3.5/fl/" + si + ".sdf")
        data2 = sh.getdata("../DiracData/fixed/3.5/sh/" + si + ".sdf")
        #data2 = sh.getdata("../../Lare2d-dev/Data/shsolar/" + si + ".sdf")
        #data3 = sh.getdata("../../Lare2d-dev/Data/shlaser/" + si + ".sdf")
        #data3 = sh.getdata("../../Lare2d-dev/Data/x-point/sh/" + si + ".sdf")

        rho = data1.Fluid_Rho
        vx = data1.Velocity_Vx
        vy = data1.Velocity_Vy
        vz = data1.Velocity_Vz
        bx = data1.Magnetic_Field_Bx
        by = data1.Magnetic_Field_By
        by2 = data2.Magnetic_Field_By
        #eta1 = data1.PIP_eta
        eta2 = data2.PIP_eta
        #bz = data2.Magnetic_Field_Bz
        #e = data3.Fluid_Energy
        #n = data.PIP_neutral_fraction
        p = data1.Fluid_Pressure
        t1 = data1.Fluid_Temperature
        t2 = data2.Fluid_Temperature
        #t3 = data3.Fluid_Temperature
        #t4 = data4.Fluid_Temperature
        t = t * t0
        #jx = data1.Current_Jx
        #jy = data1.Current_Jy
        #jz = data1.Current_Jz
        #sh.list_variables(data1)
        

        sh.plot_auto(t1)
        plt.show()
         
        sh.plot_auto(t2)
        plt.show()
        #sh.plot_auto(e)
        #plt.savefig("SH-" + si + ".png")
        #plt.clf()
        #plt.show()
        #plt.pause(4)
        #plt.close()
        
        #plt.savefig("temperature" + si + ".png") 
        #sh.plot_auto(rho)
        #plt.show()

        B = by.data * B0
        B = np.swapaxes(B,0,1)
        B = B[250]
        B2 = by2.data * B0
        B2 = np.swapaxes(B2,0,1)
        B2 = B2[100]
        x = np.linspace(-0.4,0.4, len(B))
        x2 = np.linspace(-0.4,0.4, len(B2))

        #plt.plot(x,B,label = "thin")
        #plt.plot(x2,B2,label = "wide")
        #plt.legend()
        #plt.show()
"""
        temp1 = t1.data * T0
        #temp2 = t2.data * T0
        temp3 = t3.data * T0
        #temp4 = t4.data * T0
        #temp1 = np.swapaxes(temp1, 0, 1)
        #temp2 = np.swapaxes(temp2, 0, 1)
        #temp3 = np.swapaxes(temp3, 0, 1)
        #temp4 = np.swapaxes(temp4, 0, 1)
        temp1 = temp1[50]
        #temp2 = temp2[0]
        temp3 = temp3[0]
        #temp4 = temp4[1]
        x = np.linspace(0,1,len(temp1)) * L0
        #x2 = np.linspace(0,1,len(temp2)) * L0
        x3 = np.linspace(0,1,len(temp3)) * L0
        #x4 = np.linspace(0,1,len(temp4)) * L0
        plt.plot(x,temp1, label = "snb")
        #plt.plot(x2,temp2, label = "0")
        #plt.plot(x3,temp3, label = "1d")
        #plt.plot(x4,temp4, label = "0.5")
        plt.title(f"{t:.2g} seconds")
        #plt.xlim(0,1)
        plt.ylabel("Temperature / K")
        plt.xlabel("Distance / m")
        plt.legend()
        #plt.savefig("finallaser.png") 
        plt.show()

"""
        #ax2 = ax1.twinx()
"""
        temp1 = t1.data[50] * 115.3
        density = rho.data[2] * 1.0067 * 10**(-6)
        print(temp1[int(len(temp1)/2)])
        print(density[int(len(density)/2)]) 
        #temp2 = t2.data[100] * 115.3
        #tdiff = (temp1 - temp2) / temp2 * 100
        #print(bx.data[8][50], bx.data[9][50], t1.data[10][50])
        #print(bx.data[191][50], bx.data[190][50], t1.data[189][50])
        #density = rho.data[100] * 1.0067 * 10**(-6)
        velocity = vy.data[2] * 892 
        time_norm = 70 * 10**6 / 892 
        time = 10**(-4) * (i - 100) * time_norm
        
        velocity = np.delete(velocity, -1)

        dT = temp1[1:] - temp1[0:-1]
        dx = 120 * 10**6 / len(temp1)
        temp_b = 0.5 * (temp1[1:] + temp1[0:-1])
        l_t = np.abs(temp_b * dx / dT)
        
        mfp = 5.5 * 1e7 * temp1**2 / (density / (1.2 * 1.67e-27))
        mfp = 0.5 * (mfp[1:] + mfp[0:-1])
        Kn = mfp / l_t

        Kn = np.append(Kn,0.0)
        print(Kn[int(len(Kn)/4)])
        
        y = np.linspace(0, 18, len(temp1))
        ax1.set_xlabel("Distance / Mm")
        
        #fig.suptitle("Radiation and heating (TRAC + flux limiting)")
        ax1.set_title("Temperature")
        ax1.set_ylabel("Temperature / K")
        ax1.set_yscale("log")
        plot1, = ax1.plot(y, temp1, color  = "b")
        #plt.show()
        #plot2, = ax2.plot(y, temp2, color = "g")
        #plot2, = ax2.plot(y, temp2, color = "b")
        
        ax2.set_ylabel("Temperature / K")
        ax2.set_yscale("log")
        ax2.set_xlabel("Distance / Mm")
        #ax2.set_title("Knudsen number")
        
        artists.append([plot1])
        #temps = np.append(temps, [temp1], axis = 0)
        #rhos = np.append(rhos, [density], axis = 0)

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
    
    #plt.show()
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
ax2.set_ylabel("Temperature [K]", fontsize = 13)
ax1.set_ylabel("Electron number density [cm$^{-3}$]", fontsize = 13)
ax2.set_xlabel("Distance along the loop [Mm]", fontsize = 13)
ax1.set_xlabel("Distance along the loop [Mm]", fontsize = 13)
ax1.legend(fontsize = 12)
ax2.legend(fontsize = 12)
ax1.set_xticks(np.arange(0,80, 10))
ax2.set_xticks(np.arange(0,80, 10))
ax1.tick_params(axis='both', labelsize=13)
ax2.tick_params(axis='both', labelsize=13)
#plt.yscale()
plt.tight_layout()
fig.set_size_inches(11,4)
#plt.savefig("initialboth.pdf", format = 'pdf')
plt.show()
"""
