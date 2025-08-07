import sdf_helper as sh
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FormatStrFormatter, ScalarFormatter, LogLocator, NullLocator
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, zoomed_inset_axes, TransformedBbox, BboxPatch, BboxConnector
from scipy.constants import Boltzmann as kb, epsilon_0 as ep0, electron_mass as me
from scipy.constants import proton_mass as mp, mu_0,  elementary_charge as qe
from scipy.interpolate import interp1d

B0 = 0.001 # magnetic field normalisation, T
# L0 = 1.56E8 # spatial normalisation, m
L0 = 0.7E8 # spatial normalisation, m
m = 1.2 * mp # mean particle mass, kg
n = 1e18 # plasma number density, 1/m^3
rho_0 = 0.5 * m * 1e18 # density normalisation kg/m^3
rho_0 = 0.5 * m * 1e18 *1000 # density normalisation kg/m^3
v0 = B0 / np.sqrt(mu_0 * rho_0) # velocity normalisation, m/s
t0 = L0 / v0 # time normalisation, s
E0 = v0**2; # energy per unit mass normalisation, m^2/s^2

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

def mean_coronal_values(data_path, variable, center, window, start, end):
    times = []
    values = []
    for i in range(start, end+1):
        _, value, _, t = get_1d_data(data_path, i, 3, variable=variable)
        size = len(value)
        left = int(center - window / 2)
        right = int(center + window / 2)
        values.append(value[left:right].mean())
        times.append(t)
    return np.array(times), np.array(values)

def mark_inset(parent_axes, inset_axes, loc1a=1, loc1b=1, loc2a=2, loc2b=2, **kwargs):
    rect = TransformedBbox(inset_axes.viewLim, parent_axes.transData)

    pp = BboxPatch(rect, fill=False, **kwargs)
    parent_axes.add_patch(pp)

    p1 = BboxConnector(inset_axes.bbox, rect, loc1=loc1a, loc2=loc1b, **kwargs)
    inset_axes.add_patch(p1)
    p1.set_clip_on(False)
    p2 = BboxConnector(inset_axes.bbox, rect, loc1=loc2a, loc2=loc2b, **kwargs)
    inset_axes.add_patch(p2)
    p2.set_clip_on(False)

    return pp, p1, p2

fig, ax = plt.subplots(1, 1, figsize=(8,8))
window = 200
center = 700
start = 100
end = 450

axs = [ax]

energies = ["10^20"]
headings = [
    "Total energy released: $10^{20}$J"
]
regimes = ["SH", "FL", "SNB"]
styles = [
    ["solid", "black", "black"],
    ["dotted", "grey", "grey"], 
    ["dashed", "red", "orange"]
]

plot_ind = {}

xlims = [(1.5, 5)]
ylims = [(2.5, 10)]
offsets = [[(0.004,-0.03), (-0.02,0.02), (-0,-0.05), (0,-0.04), (0.018,-0.02), (0,-0.04), (-0.02,-0.001)], 
           [(-0.02,0.03), (-0.02,-0.01), (-0.002,0.04), (-0.01,-0.04), (0.02,0.03), (0, -0.04), (-0.02,0)],
           [(0.02,-0.03), (-0.02,0), (0.001,0.03), (0,-0.04), (0.02,0), (-0.02, -0.003), (-0.02, 0)]]

start_time = 15000

for i in range(1):
    ax = axs[i]
    energy = energies[i]

    if i == 0:
        # Create zoomed-in inset axis
        ax_inset = inset_axes(ax, width = "27%", height = "38%", loc = "lower left", bbox_to_anchor= (0.1,0.08,0.95,1), bbox_transform=ax.figure.transFigure)  # Zoom factor

    for k in range(3):
        regime = regimes[k]
        data_path = f'../Flares_ch_50/{energy}/{regime}'
        t, y = mean_coronal_values(data_path, 'Temperature', center, window, start, end)
        t, x = mean_coronal_values(data_path, 'Rho', center, window, start, end)
        x = x / m / 1e6 / 1e9
        y = y / 1e6
        ax.plot(x, y, label=regime, linestyle=styles[k][0], color=styles[k][1])
        # Add markers
        t_sh = t - start_time
        ind1 = np.where((t_sh >= 0) & (t_sh <= 600))[0][0]
        ind4 = np.where((t_sh >= 0) & (t_sh <= 600))[0][-1]
        ind3 = np.argmax(y)
        ind2 = np.argmin(x[:ind3])
        ind5 = np.argmax(x)
        ind6 = np.argmin(y)
        ind7 = np.argmin(x[ind6:]) + ind6
        idxs = [ind1, ind2, ind3, ind4, ind5, ind6, ind7]
        markers1 = ['$1$', '$2$', '$3$', '$4$', '$5$', '$6$', '$7$']
        markers2 = ['*'] + 6 * ['.']

        plot_ind[regime + "_" + energy] = idxs
        
        for j in range(len(markers1)):
            idx = idxs[j]
            marker = markers1[j]
            if (j > 0 and j < 6):
                if (j!=5 or k!=2):
                    ax.scatter(
                        (1+offsets[k][j][0]) * x[idx], (1+offsets[k][j][1]) * y[idx],
                        color=styles[k][2], s=100, zorder=3, marker=marker
                        )  # Highlight the point
            
            marker = markers2[j]
            ax.scatter(x[idx], y[idx],
                    color = styles[k][2], s = 100, zorder = 3, marker = marker)

        if i==0:
            window_size = 9
            x_smooth = np.convolve(x, np.ones(window_size)/window_size, mode='valid')
            y_smooth = np.convolve(y, np.ones(window_size)/window_size, mode='valid')
            ax_inset.plot(x_smooth, y_smooth, label=regime, linestyle=styles[k][0], color=styles[k][1])
            for j in range(len(markers1)):
                idx = idxs[j]
                marker = markers1[j]
                ax_inset.scatter(
                    (1+offsets[k][j][0]) * x_smooth[idx], (1+offsets[k][j][1]) * y_smooth[idx],
                    color=styles[k][2], s=100, zorder=3, marker=marker
                )  # Highlight the point
                marker = markers2[j]
                ax_inset.scatter(
                    x_smooth[idx],y_smooth[idx],
                    color=styles[k][2], s=100, zorder=3, marker=marker
                )  # Highlight the point
            ax_inset.scatter(
                    x[ind1], y[ind1],
                    color=styles[k][2], s=100, zorder=3, marker=markers2[0]
                )  # Highlight the point
        
            ax_inset.scatter(
                    x[ind1] + offsets[k][0][0], y[ind1] + offsets[k][0][1],
                    color=styles[k][2], s=100, zorder=3, marker=markers1[0]
                )  # Highlight the point
        

    ax.set_ylabel("Temperature [MK]",  fontsize=14)
    ax.set_xlabel(r"Electron number density $[10^9$cm$^{-3}$]", fontsize=14)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(xlims[i][0], xlims[i][1])
    ax.set_ylim(ylims[i][0], ylims[i][1])
    #ax.set_title(headings[i], fontsize=18)
    ax.minorticks_off()
    ax.set_xticks([2.0, 3.0, 4.0])
    ax.get_xaxis().set_major_formatter(FormatStrFormatter('%.1f'))
    ax.set_yticks([3.0, 4.5, 6.0, 7.5, 9.0])
    ax.get_yaxis().set_major_formatter(FormatStrFormatter('%.1f'))
    # ax.set_aspect(0.5)
    ax.tick_params(axis = 'both', labelsize = 12)
    ax.legend(fontsize = 13)

    if i==0:
        # ax_inset.set_ylabel("Temperature, K",  fontsize=14)
        # ax_inset.set_xlabel(r"Electron number density, $cm^{-3}$", fontsize=14)
        ax_inset.set_xscale("log")
        ax_inset.set_yscale("log")
        # Set limits for zoomed-in region
        x1, x2 = 2.5, 3.2  # X-range to zoom
        y1, y2 = 2.85, 3.2  # Y-range to zoom
        ax_inset.set_xlim(x1, x2)
        ax_inset.set_ylim(y1, y2)
        ax_inset.set_xticks([])  # Custom x-axis ticks
        ax_inset.xaxis.set_minor_locator(NullLocator())
        ax_inset.set_yticks([])  # Custom x-axis ticks
        ax_inset.yaxis.set_minor_locator(NullLocator())
        ax_inset.set_aspect(3)
        
        mark_inset(ax, ax_inset, loc1a=1, loc1b =2, loc2a=4, loc2b = 3, fc="black", ec="grey", linestyle="dashed")

fig.tight_layout()
plt.savefig("cycle.pdf", format = 'pdf')
plt.show()
