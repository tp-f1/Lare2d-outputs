
#Plots the standard SDF output files using
#sdf_helper's plot_auto function



import sdf_helper as sh
import numpy as np
import matplotlib.pyplot as plt
import math
from pynput.keyboard import Listener, Key

def next_image(key):
    if (key == Key.space):
        plt.close()

listener = Listener(on_press = next_image) 
listener.start()

array = np.array([])

starts = ["implicit", "superstepping"]

for start in starts:
    
    for i in range(1000):
        i+=100 
        si = (4 -  len(str(i)))*"0" + str(i)
        if (start == "implicit"):
            data = sh.getdata("../../Lare2d-dev/Data/" + si + ".sdf")
        if (start == "superstepping"):
            data = sh.getdata("../../Lare2d-dev/Data/sh500/tri60/3Mm/" + si + ".sdf")

        rho = data.Fluid_Rho
        vx = data.Velocity_Vx
        vy = data.Velocity_Vy
        bx = data.Magnetic_Field_Bx
        by = data.Magnetic_Field_By
        e = data.Fluid_Energy
        #n = data.PIP_neutral_fraction
        p = data.Fluid_Pressure
        t = data.Fluid_Temperature   
    
        #sh.list_variables(data)
   
        #sh.plot_auto(e)
        #plt.show()
    
    
        #sh.plot_auto(rho)
        #plt.show()

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        temp = t.data[2] * 115.3
        density = rho.data[2] * 1.003 * 10**(-6)
        
        y = np.linspace(0, 170, len(temp))
        ax1.set_xlabel("Distance along loop / Mm")

        ax1.plot(y,temp, color = "r")
        ax1.set_ylabel("Temperature / K")
        ax1.set_yscale("log")
        
        ax2.plot(y,density, color = "g")
        ax2.set_ylabel("Density / kgm$^-3$")
        ax2.set_yscale("log")

        plt.show()

        print(temp[0], temp[1], temp[2], temp[3])
         #plt.savefig("SH" + si + ".png")
        #plt.show()
        
        #if (i / 10 == int(i/10)):
        #plt.savefig("conduct_only" + str(i/10) + ".png") 
plt.show()     
#shh.plot_auto(vy)
#t = np.linspace(0,250,num =250)
#plt.plot(t, array)
#plt.show()
