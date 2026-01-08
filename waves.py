import sdf_helper as sh
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
from scipy.constants import mu_0, epsilon_0, k, m_p

B0 = 0.001
L0 = 100e6 
rho0 = 1.00e-6

v0 = B0 / np.sqrt(mu_0 * rho0)
T0 = v0**2 * 1.2 * m_p / k
t0 = L0 / v0


starts = [""]

for start in starts:
    reference, energy, kinetic, alfven, time = [np.array([]) for i in range(5)]
    for i in range(10):
        i*=5
        #i+=10 
        si = (4 - len(str(i)))*"0" + str(i)
        data1 = sh.getdata("../DiracData/sh/cont" + start + "/0000" + ".sdf")
        data2 = sh.getdata("../DiracData/sh/cont" + start + "/" + si + ".sdf")
        #data1 = sh.getdata("../../Lare2d-dev/Data/0100.sdf")
        #data2 = sh.getdata("../../Lare2d-dev/Data/" + si + ".sdf")
        #data2 = sh.getdata("../../Lare2d-dev/Data/simple/SNB/5e-3/" + si + ".sdf")
        time = np.append(time, t * t0)
    
    
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

        x = np.linspace(-40,40,nx)
        y = np.linspace(0,80,ny)
        
        
        vx, vy, bx, by = [np.zeros((len(rho1[0]), len(rho1))) for i in range(4)]
        
        for j in range(nx):
            for k in range(ny):
                vx[k][j] = 0.25 * (vx2[j][k] + vx2[j+1][k] + vx2[j][k+1] + vx2[j+1][k+1])
                vy[k][j] = 0.25 * (vy2[j][k] + vy2[j+1][k] + vy2[j][k+1] + vy2[j+1][k+1]) 
                bx[k][j] = 0.5 * (bx2[j][k] + bx2[j+1][k])
                by[k][j] = 0.5 * (by2[j][k] + by2[j][k+1])
                
         
        v = np.sqrt(vx**2 + vy**2)
        b = np.sqrt(bx**2 + by**2)
        
        rho1 = np.swapaxes(rho1, 0, 1)
        rho2 = np.swapaxes(rho2, 0, 1)
        energy1 = np.swapaxes(energy1, 0, 1)
        energy2 = np.swapaxes(energy2, 0, 1)
    
        e_density = b**2 / mu_0 
        
        total_energy = 0
        for es in e_density:
            for e in es: 
                total_energy += e * (0.8 * L0**2 / (nx*ny))  
    
        energy = np.append(energy, total_energy)
        
        k_density = rho2 * (vx * by - vy * bx)**2 / b**2 
        print(k_density[50][0])
        #print(vx[0][0], vy[0][0], bx[0][0], by[0][0])
        total_kinetic = 0
        for ks in k_density:
            for k in ks:
                total_kinetic += k * (0.8 * L0**2 / (nx*ny)) 
                
        kinetic = np.append(kinetic, total_kinetic)  
       
        for j in range(nx):
            for k in range(ny):
                bx[k][j] = 0.5 * ((bx2[j][k] + bx2[j+1][k]) - (bx1[j][k] + bx1[j+1][k]))
                by[k][j] = 0.5 * ((by2[j][k] + by2[j][k+1]) - (by1[j][k] + by1[j][k+1]))
        
        alfven_density = 0.5 * (rho2 * (v**2) + (bx**2+by**2) / mu_0)
    
        total_alfven = 0
        for afs in alfven_density:
            for a in afs:
                total_alfven += a * (0.8 * L0**2 / (nx*ny))
    
        alfven = np.append(alfven, total_alfven)
    
        total_ref = 0
        ref_density = rho2 * energy2 - rho1 * energy1
        for refs in ref_density:
            for ref in refs:
                total_ref += ref * (0.8 * L0**2 / (nx*ny))
    
        reference = np.append(reference, total_ref)
        
    #    bxft = np.fft.fft2(bx/np.sqrt(mu_0))
    #    byft = np.fft.fft2(by/np.sqrt(mu_0))
    #    vxft = np.fft.fft2(np.sqrt(rho)*vx)
    #    vyft = np.fft.fft2(np.sqrt(rho)*vy)
    #    
    #    print(bxft, vxft)
    #
    #    Axft = np.minimum(np.abs(vxft),np.abs(bxft))
    #    Ayft = np.minimum(np.abs(vyft),np.abs(byft))
    #
    #    Ax = np.abs(np.fft.ifft2(Axft))
    #    Ay = np.abs(np.fft.ifft2(Ayft))
    #    A = Ax**2 + Ay**2
        
        #print(total_energy, total_kinetic, total_ref)
            
        #plt.streamplot(x,y, vx, vy)
        #plt.show()
        
        #plt.imshow(ref_density, origin = "lower")
        #plt.show()
    
        #plt.imshow(e_density, origin = "lower")
        #plt.colorbar()
        #plt.show()
        #plt.contour(x,y,e_density)
        #plt.colorbar()
        #plt.show()
        
    
    #print(kinetic[-1]/reference[-1])
    #plt.plot(time, reference, label = start)
    #plt.savefig("energy.png")
    
    #plt.plot(time, energy-energy[0], label = start)
    #plt.savefig("energy.png")
    #plt.legend()
    #plt.show()
    plt.plot(time,  (energy[0]-energy), label = "wave"+start)

plt.legend()
plt.show()
