import sdf_helper as sh
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
from scipy.constants import mu_0, epsilon_0, k, m_p

B0 = 0.002
L0 = 100e6 
rho0 = 1.00e-6

v0 = B0 / np.sqrt(mu_0 * rho0)
T0 = v0**2 * 1.2 * m_p / k
t0 = L0 / v0

reference, energy, kinetic, time = [np.array([]) for i in range(4)]


for i in range(10):
    i*=10
    #i+= 200 
    si = (4 - len(str(i)))*"0" + str(i)
    data1 = sh.getdata("../DiracData/reconnection/FL/" + si + ".sdf")
    #data1 = sh.getdata("../../Lare2d/Data//" + si + ".sdf")
    time = np.append(time, t * t0)
    data2 = sh.getdata("../DiracData/reconnection/FL/" + "0000" + ".sdf")
    #data2 = sh.getdata("../../Lare2d/Data/nothing/" + si + ".sdf")


    # With dynamic field
    rho1 = data1.Fluid_Rho.data * rho0
    vx1 = data1.Velocity_Vx.data * v0
    vy1 = data1.Velocity_Vy.data * v0
    bx1 = data1.Magnetic_Field_Bx.data * B0 
    by1 = data1.Magnetic_Field_By.data * B0
    temp1 = data1.Fluid_Temperature.data * T0
    energy1 = data1.Fluid_Energy.data * v0**2

    # With static field
    rho2 = data2.Fluid_Rho.data * rho0
    vx2 = data2.Velocity_Vx.data * v0 
    vy2 = data2.Velocity_Vy.data * v0
    bx2 = data2.Magnetic_Field_Bx.data * B0
    by2 = data2.Magnetic_Field_By.data * B0
    temp2 = data2.Fluid_Temperature.data * T0
    energy2 = data2.Fluid_Energy.data * v0**2

    nx = len(rho1) 
    ny = len(rho1[0]) 
    
    x = np.linspace(-100,100,nx)
    y = np.linspace(0,100,ny)
    
    
    vx, vy, bx, by = [np.zeros((len(rho1), len(rho1))) for i_ in range(4)]
    
    for j in range(nx):
        for k in range(ny):
            vx[k][j] = 0.25 * ((vx1[j][k] + vx1[j+1][k] + vx1[j][k+1] + vx1[j+1][k+1]) \
                      -(vx2[j][k] + vx2[j+1][k] + vx2[j][k+1] + vx2[j+1][k+1]))
            vy[k][j] = 0.25 * ((vy1[j][k] + vy1[j+1][k] + vy1[j][k+1] + vy1[j+1][k+1]) \
                      -(vy2[j][k] + vy2[j+1][k] + vy2[j][k+1] + vy2[j+1][k+1]))
            bx[k][j] = 0.5 * ((bx1[j][k] + bx1[j+1][k]) - (bx2[j][k] + bx2[j+1][k]))
            by[k][j] = 0.5 * ((by1[j][k] + by1[j][k+1]) - (by2[j][k] + by2[j][k+1])) 
        
    v = np.sqrt(vx**2 + vy**2)
    b = np.sqrt(bx**2 + by**2)
    
    rho = np.swapaxes(rho1, 0, 1)
    
    e_density = b**2 / mu_0 
    
    total_energy = 0
    for es in e_density:
        for e in es: 
            total_energy += e  

    energy = np.append(energy, total_energy)
    
    for j in range(nx):
        for k in range(ny):
            bx[k][j] = 0.5 * (bx1[j][k] + bx1[j+1][k])
            by[k][j] = 0.5 * (by1[j][k] + by1[j][k+1])

    k_density = rho1 * (vx * by - vy * bx)**2 / (bx**2 + by**2) 
    
    total_kinetic = 0
    for ks in k_density:
        for k in ks:
            total_kinetic += k 

    kinetic = np.append(kinetic, total_kinetic)  
    
    total_ref = 0
    ref_density = rho1 * (energy1 - energy2)
    for refs in ref_density:
        for ref in refs:
            total_ref += ref * 6.4e9

    reference = np.append(reference, total_ref)

#    print(total_energy, total_kinetic, total_ref)

    #plt.streamplot(x,y, vx, vy)
    #plt.show()
    #plt.contour(x,y,k_density)
    #plt.colorbar()
    #plt.show()
    #plt.contour(x,y,e_density)
    #plt.colorbar()
    #plt.show()
    

plt.plot(time, reference)
#plt.savefig("energy.png")
plt.show()

plt.plot(time, energy)
#plt.savefig("energy.png")
plt.show()
