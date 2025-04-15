
import os
import pandas as pd
import sdf_helper as sh
#import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import LogLocator, NullLocator
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
import numpy as np
from os import listdir
from os.path import isfile, join
#from sunpy.visualization.colormaps import cm
from scipy.constants import Boltzmann as kb, epsilon_0 as ep0, electron_mass as me
from scipy.constants import proton_mass as mp, mu_0,  elementary_charge as qe
from scipy.interpolate import interp1d
import warnings
warnings.filterwarnings('ignore')
import math
import scipy.constants as sc
from pynput.keyboard import Listener, Key
import matplotlib.animation as animation


def next_image(key):
    if (key == Key.space):
        plt.close()

listener = Listener(on_press = next_image)
listener.start()

for i in range(1):
    f = open("/home/physics/phubjv/Lare2d-dev/flux.dat", "r")
    lines = f.readlines()
    sh_flux = []
    snb_flux = []
    if (i == 0): diff = np.array([])
    for line in lines:
        split = line.split()
        snb_flux.append(float(split[1]))
        sh_flux.append(float(split[0]))
        
    snb_flux.pop()
    sh_flux.pop()
    
    y = np.linspace(0,170,num  = len(snb_flux))
    
    #plt.plot(y,snb_flux, label = "snb")
    #if (i == 0): plt.plot(y, sh_flux, label = "sh")
    #plt.legend()
    #if (i == 0): 
    #    diff = np.array(snb_flux)
    #else:
    #    diff = (np.array(snb_flux) - diff) /  max(diff) * 100
#plt.savefig("Lare2d")
#plt.show()

#plt.plot(y, diff)
#plt.show()

L0 = 70.e6
rho_0 = 1.003e-6
t0 = 78609.8
m = 1.2 * 1.673e-27
E0 = 792944
v0 = math.sqrt(E0)

# Thomas algorithm
def thomas(a, b, c, d):
    ac = np.copy(a)
    bc = np.copy(b)
    cc = np.copy(c)
    dc = np.copy(d)
    x = np.zeros(a.size)
    for i in np.arange(1, a.size):
        tmp = ac[i] / bc[i-1]
        bc[i] -= tmp * cc[i-1]
        dc[i] -= tmp * dc[i-1]

    x[-1] = dc[-1] / bc[-1]
    for i in np.arange(a.size-2, -1, -1):
        x[i] = (dc[i] - cc[i] * x[i+1]) / bc[i]
    return x


def gammaz(zbar):
    """Approximate form of zbar dependance of local SH flux"""
    return 13.6 * (zbar + 0.44) / (zbar + 4.24)


def snb(T0, n0, x, zbar=1.0, coulomb_log=20.0):
    # Plasma parameters
    n_e = np.concatenate(([n0[0]], 0.5 * (n0[1:] + n0[:-1]),[n0[-1]]))

    # Set up grid
    Nx = len(T0)
    xmax = 70e6
    xmin = 0

    dx = (xmax - xmin) / Nx
    x_grid_b = np.linspace(xmin, xmax, Nx+1)
    x_grid_c = x

    # Initial temperature profile
    Te_b = np.concatenate(([T0[0]],0.5 * (T0[1:] + T0[:-1]),[T0[-1]]))
    Te_c = T0

    # Set up energy groups for SNB
    ng = 100
    emin = 0.0
    # Max energy group
    emax = 20 * Te_c.max()  # Kelvin

    e_grid_b = np.linspace(emin, emax, ng+1)
    e_grid_c = 0.5 * (e_grid_b[1:] + e_grid_b[:-1])

    # Calculate thermal speed and Spitzer Harm conductivity
    vt_b = np.sqrt(2 * kb * Te_b / me)

    # Calculate local flux
    kappa0 = 12.0 * np.pi**1.5 * ep0**2 * kb**3.5 / (qe**4 * np.sqrt(2.0 * me))
    kappa_SH_b = Te_b**2.5 * kappa0 * gammaz(zbar) / coulomb_log / zbar


    # Zero flux at boundaries
    grad_T_b = np.concatenate(
        [np.zeros(1), (Te_c[1:] - Te_c[:-1]) / dx, np.zeros(1)])

    # Spitzer Harm heat flux
    Q_SH_B = -grad_T_b * kappa_SH_b

    # Source term for SNB energy groups
    source_term = np.zeros([Nx, ng])

    # Weights for SNB groups
    weight = np.zeros([Nx+1, ng])

    def weight_fn(x):
        return - np.exp(-x) * (x**4 + 4.0 * x**3 + 12 * x**2 + 24 * x + 24)

    for i in range(ng):
        xm = e_grid_b[i] / Te_b[:]
        x = e_grid_b[i+1] / Te_b[:]
        weight[:, i] = (weight_fn(x) - weight_fn(xm)) / 24

    # Now set up source term
    for i in range(ng):
        div_Ug = (Q_SH_B[1:] * weight[1:, i] -
                  Q_SH_B[:-1] * weight[:-1, i]) / dx
        source_term[:, i] = -div_Ug * dx**2

    # Now need so solve for corrected flux
    H_g = np.zeros([Nx, ng])
    grad_H_g = np.zeros([Nx+1, ng])

    a = np.zeros(Nx)
    b = np.zeros(Nx)
    c = np.zeros(Nx)


    lambda_e_b = 12.0 * np.pi**1.5 * ep0**2 * kb**2 * Te_b**2 / (
        n_e * np.sqrt(2.0) * qe**4 * zbar * coulomb_log)

    lambda_g_b = np.zeros([Nx+1, ng])
    lambda_g_c = np.zeros([Nx, ng])

    for i in range(ng):
        lambda_g_b[:, i] = lambda_e_b * (e_grid_c[i] / Te_b)**2

    lambda_g_c = 0.5 * (lambda_g_b[1:] + lambda_g_b[:-1])

    # Solve linear systems
    for i in range(ng):
        a = - lambda_g_b[0:-1, i] / 3.0
        c = - lambda_g_b[1:, i] / 3.0
        b = dx**2 / lambda_g_c[:, i]
        b = b - a - c

        H_g = thomas(a, b, c, source_term[:, i])
        grad_H_g[1:-1, i] = (H_g[1:] - H_g[:-1]) / dx

    grad_H = np.sum(grad_H_g * lambda_g_b, axis=1) / 3

    # Resulting SHB heat flux
    Q_SNB = Q_SH_B - grad_H

    # FL heat flux
    alpha = 0.06  # Flux limiter value
    q_fs = n_e * vt_b * kb * Te_b
    q_fs_l = alpha * q_fs
    Q_lim_l = q_fs_l * Q_SH_B / np.sqrt(abs(Q_SH_B)**2 + q_fs_l**2)

    return (x_grid_b, Q_SH_B, Q_SNB, Q_lim_l, Te_b, q_fs)

def get_1d_data(data_path, file_ind, x_ind, variable='Rho'):
    data=sh.getdata(file_ind, data_path, verbose=False)
    
    if variable in ['Rho', 'Temperature', 'Energy']:
        x = data.Grid_Grid_yface.data[1][1:-1] * L0 / 1e6
        if variable == 'Rho':
            y = data.Fluid_Rho.data[x_ind,:] * rho_0
            y_label = r"Density, $kg/m^3$"
        if variable == 'Temperature':
            y = data.Fluid_Temperature.data[x_ind,:] * m * E0 / kb
            y_label = r"Temperature, K"
        if variable == 'Energy':
            y = data.Fluid_Energy.data[x_ind,:] * E0 * m
            y_label = r"Energy, J"
    else:
        x = data.Grid_Grid_yface_mid.data[1]* L0 / 1e6
        if variable == 'Vx':
            y = data.Velocity_Vx.data[x_ind,:] * v0
            y_label = r"$V_x$, m/s"
        if variable == 'Vy':
            y = data.Velocity_Vy.data[x_ind,:] * v0
            y_label = r"$V_y$, m/s"
        if variable == 'Vz':
            y = data.Velocity_Vz.data[x_ind,:] * v0
            y_label = r"$V_z$, m/s"

    time = data.__dict__['Header']['time'] * t0
    
    return np.array(x), np.array(y), y_label, time

fig, (ax1, ax2) = plt.subplots(1, 2, sharey = True)
artists = []
first = True
for i in range(120):
    #i *= 10
    i += 100
    x, rho, _, t = get_1d_data("/home/physics/phubjv/Lare2d-dev/Data/sergey/snb/", i, 3, variable='Rho')
    x, temp, _, t = get_1d_data("/home/physics/phubjv/Lare2d-dev/Data/sergey/snb/", i, 3, variable='Temperature')
    
    x = x * 1e6

    if (first): 
        initial = t
        first = False

    xb, Q_SH_B, Q_SNB, Q_lim_l, Te, _ = snb(temp, rho/m, x)
    
    ttl = plt.text(0.9, 1.05, "time = " + "{:.2f}".format(t - initial), transform = ax1.transAxes) 
    ax1.set_title("SNB")
    ax2.set_title("SH")
    ax1.set_ylim(-5.e5, 5.e5)
    plot1, = ax1.plot(xb, Q_SNB, label = "snb", color = 'g')
    plot2, = ax2.plot(xb, Q_SH_B, label = "sh", color = 'b')
    #if (i == 100): 
     #   legend = ax.legend()
    artists.append([plot1, plot2, ttl])
    #ax.set_ylim(min(Q_SH_B), max(Q_SH_B))
    
    #plt.savefig("python-script.png")
    #plt.show()
ani = animation.ArtistAnimation(fig = fig, artists = artists, interval = 100)
#ax.add_artist(legend)
ani.save(filename = "SNB_flare.gif", writer = "pillow")
plt.show()






