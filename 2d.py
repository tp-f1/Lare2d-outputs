



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
L0 = 100e6
rho0 = 1.00e-6

v0 = B0 / np.sqrt(mu_0 * rho0)
T0 = v0**2 * 1.2 * m_p / k
t0 = L0 / v0


fig1, ax1 = plt.subplots(2,3, sharey = True, sharex = True)
fig1.set_size_inches(15,8)

fig2, ax2 = plt.subplots(1,3, sharey = True)
fig2.set_size_inches(15,5)
for i in range(3):
    indx = i
    i*=20
    i += 30
    si = (4-len(str(i))) * "0" + str(i)
    data1 = sh.getdata("../DiracData/" + si + ".sdf")
    #data1 = sh.getdata("../DiracData/reconnection/SH/1e-3/" + si + ".sdf")
    data2 = sh.getdata("../DiracData/reconnection/FL/1e-3/" + si + ".sdf")
    
    T1 = data1.Fluid_Temperature.data * T0
    T1 = T1[:,:750]
    T1 = np.swapaxes(T1,0,1)
    rho1 = data1.Fluid_Rho.data * rho0
    rho1 = np.swapaxes(rho1,0,1)

    T2 = data2.Fluid_Temperature.data * T0
    T2 = T2[:,:750]
    T2 = np.swapaxes(T2,0,1)
    rho2 = data2.Fluid_Rho.data * rho0
    rho2 = np.swapaxes(rho2,0,1)
    
    x = np.linspace(-40, 40, len(T1[0]))
    y = np.linspace(0, 80, len(T1[1]))
    ext = (-40, 40, 0, 60)

    out1 = ax1[0, indx].imshow(T1, extent = ext, origin = 'lower', norm = 'log', vmin = 1.e5, vmax = 1.e7, cmap = 'magma')
    out1 = ax1[1, indx].imshow(T2, extent = ext, origin = 'lower', norm = 'log', vmin = 1.e5, vmax = 1.e7, cmap = 'magma') 
    ax1[1, indx].set_xlabel('X / Mm')
    ax1[1, indx].set_xticks([-40,-20,0,20,40])
    ax1[0, indx].set_title("{:.0f}".format(t*t0) + " s")
    



    out2 = ax2[indx].imshow(rho1, extent = ext, origin = 'lower', norm = 'log', vmin = 1.e-13, vmax = 1.e-11, cmap = 'Greens')
    ax2[indx].set_xlabel('X / Mm')
    ax2[indx].set_title("{:.0f}".format(t*t0) + " s")
    

ax1[0,0].set_ylabel("Y / Mm")
ax1[0,0].set_yticks([0, 20, 40, 60])
ax1[1,0].set_ylabel("Y / Mm")
ax1[1,0].set_yticks([0, 20, 40, 60])
fig1.tight_layout()
fig1.subplots_adjust(right = 0.8)
cbar_ax = fig1.add_axes([0.8, 0.1, 0.05, 0.8])
cbar1 = fig1.colorbar(out1, cax=cbar_ax)
cbar1.set_ticks([1.e5, 1.e6, 1.e7])
cbar1.set_label("Temperature / K", fontsize = 14)
fig1.savefig("2d-temperature.pdf", format = 'pdf')

ax2[0].set_ylabel("Y / Mm")
ax2[0].set_yticks([0,20,40,60,80])
fig2.subplots_adjust(right = 0.8)
cbar_ax = fig2.add_axes([0.82, 0.2, 0.05, 0.59])
cbar2 = fig2.colorbar(out2, cax=cbar_ax)
#cbar2.set_ticks([1.e-15, 1.e5, 1.e6, 1.e7])
cbar2.set_label("Density / kg$m^{-3}$")
plt.show()



