import sdf_helper as sh
import numpy as np
import matplotlib.pyplot as plt

array = np.array([])

for i in range(10):
    i = (3 -  len(str(i)))*"0" + str(i)
    data = sh.getdata("../../Lare2d/Data/0" + i + ".sdf")
 
    rho = data.Fluid_Rho
    vx = data.Velocity_Vx
    vy = data.Velocity_Vy
    bx = data.Magnetic_Field_Bx

    #array = np.append(array, vy.data.T[150][245])
    
    #sh.plot_auto(rho)
    sh.plot_auto(vy)
    #sh.plot_auto(bx)

    plt.show()
    
#sh.plot_auto(vy)
#t = np.linspace(0,250,num =250)
#plt.plot(t, array)
#plt.show()
