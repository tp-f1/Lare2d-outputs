



import sdf_helper as sh
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.constants import mu_0, epsilon_0, k, m_p
from pynput.keyboard import Listener, Key
import matplotlib.animation as animation
import matplotlib.patches as patches


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


fig1, ax1 = plt.subplots(3,3, sharey = True, sharex=True)
fig1.set_size_inches(15,15)

fig2, ax2 = plt.subplots(3,3, sharey = True,sharex=True)
fig2.set_size_inches(15,15)

fig3, ax3 = plt.subplots(3,3, sharey = True,sharex=True)
fig3.set_size_inches(15,15)
for i in range(3):
    indx = i
    i *= 50
    i += 30
    si = (4-len(str(i))) * "0" + str(i)
    #data1 = sh.getdata("../../Lare2d-dev/Data/simple/SNB/5e-3/" + si + ".sdf")
    #data2 = sh.getdata("../../Lare2d-dev/Data/simple/SNB/1e-3/" + si + ".sdf")
    data1 = sh.getdata("../DiracData/fixed/2.5/sh/" + si + ".sdf")
    data2 = sh.getdata("../DiracData/fixed/2.5/fl/" + si + ".sdf")
    data3 = sh.getdata("../DiracData/fixed/2.5/snb/" + si + ".sdf")

    T1 = data1.Fluid_Temperature.data * T0
    T1 = T1[100:300,:300]
    T1 = np.swapaxes(T1,0,1)
    rho1 = data1.Fluid_Rho.data * rho0
    rho1 = rho1[100:300,:300]
    rho1 = np.swapaxes(rho1,0,1)
    vy1 = data1.Velocity_Vy.data * v0
    vy1 = vy1[100:300, :300]
    vy1 = np.swapaxes(vy1,0,1)


    T2 = data2.Fluid_Temperature.data * T0
    T2 = T2[100:300,:300]
    T2 = np.swapaxes(T2,0,1)
    rho2 = data2.Fluid_Rho.data * rho0
    rho2 = rho2[100:300,:300]
    rho2 = np.swapaxes(rho2,0,1)
    vy2 = data2.Velocity_Vy.data * v0
    vy2 = vy2[100:300, :300]
    vy2 = np.swapaxes(vy2,0,1)
    
    T3 = data3.Fluid_Temperature.data * T0
    T3 = T3[100:300,:300]
    T3 = np.swapaxes(T3,0,1)
    rho3 = data3.Fluid_Rho.data * rho0
    rho3= rho3[100:300,:300]
    rho3 = np.swapaxes(rho3,0,1)
    vy3 = data3.Velocity_Vy.data * v0
    vy3 = vy3[100:300, :300]
    vy3 = np.swapaxes(vy3,0,1)
    
    x = np.linspace(-20, 20, len(T1[0]))
    y = np.linspace(0, 40, len(T1[1]))
    ext = (-20, 20, 0, 40)

    out1 = ax1[0, indx].imshow(T1, extent = ext, origin = 'lower', norm = 'log', vmin = 5.e5, vmax = 1.e7, cmap = 'magma')
    out1 = ax1[1, indx].imshow(T2, extent = ext, origin = 'lower', norm = 'log', vmin = 5.e5, vmax = 1.e7, cmap = 'magma') 
    out1 = ax1[2, indx].imshow(T3, extent = ext, origin = 'lower', norm = 'log', vmin = 5.e5, vmax = 1.e7, cmap = 'magma') 
    ax1[2, indx].set_xlabel('X (Mm)', fontsize = 16)
    ax1[2, indx].set_xticks([-20,-10,0,10,20])
    ax1[2, indx].xaxis.set_tick_params(labelsize = 16) 
    ax1[0, indx].set_title("{:.0f}".format(t*t0) + " s", fontsize = 18)
    ax1[indx,0].set_ylabel("Y (Mm)", fontsize = 16)
    ax1[indx,0].set_yticks([0,10,20,30,40])
    ax1[indx,0].yaxis.set_tick_params(labelsize=16)
    
    if (indx == 2):
        rect1 = patches.Rectangle((-3,16.5),6,6, fill = False, color = 'blue')
        rect2 = patches.Rectangle((-7,5),14,20, fill = False, color = 'red', linestyle = "--")
        ax1[2,indx].add_patch(rect1)
        ax1[2,indx].add_patch(rect2)


    out2 = ax2[0,indx].imshow(rho1, extent = ext, origin = 'lower', norm = 'log', vmin = 1.e-12, vmax = 1.e-11, cmap = 'viridis')
    out2 = ax2[1,indx].imshow(rho2, extent = ext, origin = 'lower', norm = 'log', vmin = 1.e-12, vmax = 1.e-11, cmap = 'viridis')
    out2 = ax2[2,indx].imshow(rho3, extent = ext, origin = 'lower', norm = 'log', vmin = 1.e-12, vmax = 1.e-11, cmap = 'viridis')
    ax2[2,indx].set_xlabel('X (Mm)', fontsize = 16)
    ax2[2, indx].set_xticks([-20,-10,0,10,20])
    ax2[2, indx].xaxis.set_tick_params(labelsize = 16) 
    ax2[0, indx].set_title("{:.0f}".format(t*t0) + " s", fontsize = 18)
    ax2[indx,0].set_ylabel("Y (Mm)", fontsize = 16)
    ax2[indx,0].set_yticks([0,10,20,30,40])
    ax2[indx,0].yaxis.set_tick_params(labelsize=16)

    out3 = ax3[0,indx].imshow(vy1/1.e3, extent = ext, origin = 'lower', vmin = -1.e2, vmax = 1.e2, cmap = 'bwr')
    out3 = ax3[1,indx].imshow(vy2/1.e3, extent = ext, origin = 'lower', vmin = -1.e2, vmax = 1.e2, cmap = 'bwr')
    out3 = ax3[2,indx].imshow(vy3/1.e3, extent = ext, origin = 'lower', vmin = -1.e2, vmax = 1.e2, cmap = 'bwr')
    ax3[2,indx].set_xlabel('X (Mm)', fontsize = 16)
    ax3[2, indx].set_xticks([-20,-10,0,10,20])
    ax3[2, indx].xaxis.set_tick_params(labelsize = 16) 
    ax3[0, indx].set_title("{:.0f}".format(t*t0) + " s", fontsize = 16)
    ax3[indx,0].set_ylabel("Y / Mm", fontsize = 16)
    ax3[indx,0].set_yticks([0,10,20,30,40])
    ax3[indx,0].yaxis.set_tick_params(labelsize=16)

ax1[0,0].set_ylabel("Y (Mm)", fontsize = 16)
ax1[0,0].set_yticks([0,10,20,30,40])
ax1[1,0].set_ylabel("Y (Mm)", fontsize = 16)
ax1[1,0].set_yticks([0,10,20,30,40])
ax1[2,0].set_ylabel("Y (Mm)", fontsize = 16)
ax1[2,0].set_yticks([0,10,20,30,40])
ax1[0,2].set_ylabel("SH", rotation=-45, labelpad = 25, fontsize=18)
ax1[1,2].set_ylabel("FL", rotation=-45, labelpad = 25, fontsize=18)
ax1[2,2].set_ylabel("SNB", rotation=-45, labelpad = 25, fontsize=18)
ax1[0,2].yaxis.set_label_position("right")
ax1[1,2].yaxis.set_label_position("right")
ax1[2,2].yaxis.set_label_position("right")
#fig1.suptitle("Temperature", fontsize = 16)
fig1.tight_layout()
fig1.subplots_adjust(right = 0.8)
cbar_ax = fig1.add_axes([0.85, 0.1, 0.05, 0.8])
cbar1 = fig1.colorbar(out1, cax=cbar_ax)
#cbar1.set_ticks([5.e5, 1.e6, 1.e7])
cbar1.ax.tick_params(labelsize=16)
cbar1.set_label("Temperature (K)", fontsize = 20)
fig1.savefig("2d-temperature.pdf", format = 'pdf')

ax2[0,2].set_ylabel("SH", rotation = -45, labelpad = 25, fontsize=18)
ax2[1,2].set_ylabel("FL", rotation = -45, labelpad = 25, fontsize=18)
ax2[2,2].set_ylabel("SNB", rotation = -45, labelpad = 25, fontsize=18)
ax2[0,2].yaxis.set_label_position("right")
ax2[1,2].yaxis.set_label_position("right")
ax2[2,2].yaxis.set_label_position("right")
#fig2.suptitle("Density", fontsize = 16)
fig2.tight_layout()
fig2.subplots_adjust(right = 0.8)
cbar_ax = fig2.add_axes([0.85, 0.1, 0.05, 0.8])
cbar2 = fig2.colorbar(out2, cax=cbar_ax)
cbar2.ax.tick_params(labelsize=16)
cbar2.set_ticks([1.e-12, 2.e-12, 3.e-12, 4.e-12, 6.e-12, 1.e-11])
cbar2.set_label("Density (kgm$^{-3}$)", fontsize = 20)
fig2.savefig("2d-density.pdf", format = 'pdf')


ax3[0,0].set_ylabel("Y (Mm)", fontsize = 16)
ax3[0,0].set_yticks([0,10,20,30,40])
ax3[1,0].set_ylabel("Y (Mm)", fontsize = 16)
ax3[1,0].set_yticks([0,10,20,30,40])
ax3[2,0].set_ylabel("Y (Mm)", fontsize = 16)
ax3[2,0].set_yticks([0,10,20,30,40])
ax3[0,2].set_ylabel("SH", rotation=-45, labelpad = 25, fontsize=18)
ax3[1,2].set_ylabel("FL", rotation=-45, labelpad = 25, fontsize=18)
ax3[2,2].set_ylabel("SNB", rotation=-45, labelpad = 25, fontsize=18)
ax3[0,2].yaxis.set_label_position("right")
ax3[1,2].yaxis.set_label_position("right")
ax3[2,2].yaxis.set_label_position("right")
#fig1.suptitle("Temperature", fontsize = 16)
fig3.tight_layout()
fig3.subplots_adjust(right = 0.8)
cbar_ax = fig3.add_axes([0.85, 0.1, 0.05, 0.8])
cbar3 = fig3.colorbar(out3, cax=cbar_ax)
#cbar3.set_ticks([1.e5, 1.e6, 1.e7])
cbar3.ax.tick_params(labelsize=16)
cbar3.set_label("Velocity (km/s)", fontsize = 20)
fig3.savefig("2d-velocity.pdf", format = 'pdf')
plt.show()

