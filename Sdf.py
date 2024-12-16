
#Plots the standard SDF output files using
#sdf_helper's plot_auto function



import sdf_helper as sh
import numpy as np
import matplotlib.pyplot as plt
import math

array = np.array([])

for i in range(100):
    i += 60
    i = (3 -  len(str(i)))*"0" + str(i)
    data = sh.getdata("../../Lare2d-dev/Data/0" + i + ".sdf")
 
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
   
    sh.plot_auto(e)
    plt.show()
    
    #sh.plot_auto(rho)
    #plt.show()
 
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    temp = t.data[2]
    density = rho.data[2]
    
    y = np.linspace(-10,80,len(temp))
    ax1.set_xlabel("Height")

    ax1.plot(y,np.log10(temp), color = "r")
    ax1.set_ylabel("Temperature")

    ax2.plot(y,np.log10(density), color = "g")
    ax2.set_ylabel("Density")

    plt.show()
   
    
#shh.plot_auto(vy)
#t = np.linspace(0,250,num =250)
#plt.plot(t, array)
#plt.show()
