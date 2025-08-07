import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.ticker
from scipy.optimize import curve_fit
from scipy.constants import m_p, k

mechanism = ["SH", "FL", "SNB"]

L = [50,100,200]
# H = 4
T_sh = [1.398, 2.173, 3.359]
T_lim = [1.405, 2.173, 3.389]
T_snb = [1.469, 2.314, 3.579]


# H = 11
#T_sh = [1.929, 3.007, 4.494]
#T_lim = [1.955, 3.031, 4.526]
#T_snb = [2.043, 3.194, 4.714]

ne_sh = np.array([2.431, 2.723, 3.034])
ne_lim = np.array([2.423, 2.751, 3.068])
ne_snb = np.array([2.292, 2.398, 2.740])

# H = 42
T_sh = [3.066, 4.487, 6.483]
T_lim = [3.104, 4.515, 6.512]
T_snb = [3.214, 4.678, 6.698]


#list of loop lengths
Ls = np.array([50.,100.,50.,100.,200.,50.,100.,200.,50.,50.,75.,75.,75.,140.,140.,140.,140.,100.]) * 1.e6


# list of knudsen numbers
Kn = np.array([3.8,3.89,3.55,4.7,4,3.08,3.79,4.65,2.97,3.14,3.84,3.77,3.45,3.94,3.96,4.15,5.16,3.59])/1000

# list of all temps and nes
Tfull_sh = np.array([3.066, 4.487, 1.929, 3.007, 4.494, 1.398, 2.173, 3.359, 0.941, 0.669, 3.842, 2.523, 1.8, 5.368, 3.667, 2.7, 1.761, 1.428])
Tfull_lim = [3.104, 4.515, 1.955, 3.031, 4.526, 1.405, 2.191, 3.389]
Tfull_snb = np.array([3.214, 4.678, 2.043, 3.194, 4.714, 1.469, 2.314, 3.661, 0.982, 0.7, 4.009, 2.661, 1.908, 5.603, 3.847, 2.875, 1.942, 1.518]) 

rho_sh = np.array([6.007, 6.880, 2.431, 2.723, 3.034, 1.352, 1.335, 1.424, 0.606, 0.297, 6.587, 2.559, 1.392, 7.222, 2.891, 1.374, 0.523, 0.55])  * 1.e-12 
rho_lim = np.array([5.972, 6.947, 7.545, 2.423, 2.751, 3.068, 1.357, 1.341, 1.444])  * 1.e-12 
rho_snb = np.array([5.519, 6.297, 2.292, 2.398, 2.723, 1.282, 1.245, 1.214, 0.576, 0.279, 6.02, 2.393, 1.251, 6.555, 2.633, 2.148, 0.471, 0.513])  * 1.e-12 

P_sh =  rho_sh * k * Tfull_sh * 1.e6 / (0.6*m_p)
P_snb =  rho_snb * k * Tfull_snb * 1.e6 / (0.6*m_p)

# Figures for NAM poster

plt.scatter(Tfull_sh, Tfull_snb, c=Ls/1.e6, marker = '*')
plt.colorbar(label = "Loop Length / Mm")
plt.plot([0.5,6], [0.5,6], color = 'grey', linestyle = '--', label = "y = x")
plt.legend(fontsize = 14, loc = 'lower right')
plt.ylabel("Non-local SNB model / MK", fontsize = 14)
plt.xlabel("Local conduction model / MK", fontsize = 14)
plt.title("Loop Apex Temperature", fontsize = 16)
plt.savefig("Tempcomp.pdf", format = 'pdf')
plt.show()


def scalingkn(x, a, b, c, d):
    T = x[0]
    L = x[1]
    P = a * T**b * L**c * Kn**d 
    return P

constants1 = curve_fit(scalingkn, [Tfull_snb*1.e6, Ls], P_snb)

def scaling(x, a, b, c):
    T = x[0]
    L = x[1]
    P = a * T**b * L**c
    return P

constants2 = curve_fit(scaling, [Tfull_snb*1.e6, Ls], P_snb)
constants_sh = curve_fit(scaling, [Tfull_sh*1.e6, Ls], P_sh)

print(constants1[0])
print(constants2[0])
print(constants_sh[0])


T_fit = []
P_fit = []
Kn_fit = []
for i in range(len(Ls)):
    if (Ls[i] == 100.e6):
        T_fit.append(Tfull_snb[i]*1.e6)
        P_fit.append(P_snb[i])
        Kn_fit.append(Kn[i])


coefficients = np.polyfit(np.log10(T_fit), np.log10(P_fit), 1)
polynomial = np.poly1d(coefficients)
sh_fit = polynomial(np.log10(T_fit))
l1 = plt.scatter(T_fit, P_fit)
#l2 = plt.plot(T_fit, 10**sh_fit, linestyle = '--', label = ("$P = {{{}}}T^{{{}}}$").format(round(10**coefficients[1], 2), round(coefficients[0], 2)))[0]
#plt.legend(fontsize = 14)
plt.scatter(T_fit,P_fit, c=Kn_fit)
cbar = plt.colorbar(label = "Knudsen number")
for t in cbar.ax.get_yticklabels():
     t.set_fontsize(14)
x = np.linspace(0.5e6, 3.e6, 100)
y = constants[0][0] * T_fit**constants[0][1] * 100.e6**constants[0][2] * Kn_fit**constants[0][3]
plt.plot(T_fit,y, label = "Using power law", color = "g", linestyle = '--')
plt.legend(fontsize = 16)
plt.title("Loop Length = 100Mm", fontsize = 18)
plt.xlabel("T / K", fontsize = 16)
plt.ylabel("P / Pa", fontsize = 16)
plt.xscale('log')
plt.yscale('log')
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.gcf().set_size_inches(8,5)
plt.savefig("new_scaling.pdf", format = 'pdf')
plt.show()


print(constants[0])

H = [40, 110, 420]

# L = 50
Th_sh = [1.398, 1.929, 3.066]
Th_lim = [1.405, 1.955, 3.104]
Th_snb = [1.469, 2.043, 3.214]


# L = 100
#Th_sh = [2.172, 3.007, 4.487]
#Th_lim = [2.191, 3.031, 4.515]
#Th_snb = [2.314, 3.194, 4.678]

# L = 200
Th_sh = [3.359, 4.494, 6.483]
Th_lim = [3.389, 4.526, 6.512]
Th_snb = [3.579, 4.714, 6.7]

temps = [T_sh, T_lim, T_snb]
tempsh = [Th_sh, Th_lim, Th_snb]

tempfull = [Tfull_sh, Tfull_lim, Tfull_snb]

nes = np.array([ne_sh, ne_lim, ne_snb])  * 1.e-27 / (1.2 * 1.673e-27)

nefull = np.array([nefull_sh, nefull_lim, nefull_snb])

fig, [ax1, ax2] = plt.subplots(1, 2, sharey = True)

ax1.set_ylabel("Apex Temperature / MK", fontsize = 14)
ax1.set_xlabel("Loop length / Mm", fontsize = 14)
ax1.set_title("Constant heating rate of 110 $\mu$W/m$^3$", fontsize = 16)
ax1.set_yscale('log')
ax1.set_xscale('log')

ax1.minorticks_off()
ax1.set_ylim([1,8])
ax1.set_yticks(np.arange(1, 7, 1))
ax1.set_xticks(np.arange(0, 220, 50))
ax1.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax1.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

ax2.set_xlabel(r"Heating rate / $\mu$W/$m^3$", fontsize = 14)
ax2.set_title("Constant loop length of 100Mm", fontsize = 16)
ax2.set_yscale('log')
ax2.set_xscale('log')

ax2.minorticks_off()
ax2.set_yticks(np.arange(1, 7, 1))
ax2.set_xticks([50, 100, 250, 500])
ax2.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax2.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

values = []
plots = []
for T in temps:
    coefficients = np.polyfit(np.log10(L), np.log10(T), 1)
    polynomial = np.poly1d(coefficients)
    sh_fit = polynomial(np.log10(L))
    l1 = ax1.scatter(L, T)
    l2 = ax1.plot(L, 10**sh_fit, linestyle = '--')[0]
    values.append([10**coefficients[1], coefficients[0], 3])
    plots.append([l1, l2]) 
    print("L", coefficients[0])

scaling = []
for value in values:
    scaling.append(("$T = {{{}}}L^{{{}}}$").format(round(value[0], 2), round(value[1], 2)))  

legend1 = ax1.legend(handles = [l[0] for l in plots], labels = mechanism, loc = 3, fontsize = 12)
ax1.legend(handles = [l[1] for l in plots], labels = scaling,loc = 4, fontsize = 12)
ax1.add_artist(legend1)

values = []
plots = []
for T in tempsh:
    coefficients = np.polyfit(np.log10(H), np.log10(T), 1)
    polynomial = np.poly1d(coefficients)
    sh_fit = polynomial(np.log10(H))
    l1 = ax2.scatter(H, T)
    l2 = ax2.plot(H, 10**sh_fit, linestyle = '--')[0]
    values.append([10**coefficients[1], coefficients[0]])
    plots.append([l1, l2]) 
    print("H", coefficients[0])

scaling = []
for value in values:
    scaling.append(("$T = {{{}}}H^{{{}}}$").format(round(value[0], 2), round(value[1], 2)))  

legend1 = ax2.legend(handles = [l[0] for l in plots], labels = mechanism, loc = 3, fontsize = 12)
ax2.legend(handles = [l[1] for l in plots], labels = scaling,loc = 4, fontsize = 12)
ax2.add_artist(legend1)

fig.set_size_inches(12,6.5)
plt.savefig("scaling.svg", format = 'svg')
plt.show()

print(nefull[0:2])
points = []
markers = ['x', '^', 's']
colour = ['k', 'grey', 'r']
linestyle = ['-', ':', '--']
for i in range(3):
    points.append(plt.scatter(nefull[i], tempfull[i], marker = markers[i], color = colour[i]))  
    if (i != 3):
        coefficients = np.polyfit(nefull[i][0:3], tempfull[i][0:3], 2)
        polynomial = np.poly1d(coefficients)
        sh_fit = polynomial(nefull[i][0:3])
        plt.plot(nefull[i][0:3], sh_fit, linestyle = linestyle[i], color = colour[i])
        
        coefficients = np.polyfit(nefull[i][3:6], tempfull[i][3:6], 2)
        polynomial = np.poly1d(coefficients)
        sh_fit = polynomial(nefull[i][3:6])
        plt.plot(nefull[i][3:6], sh_fit, linestyle = linestyle[i], color = colour[i])
        
        coefficients = np.polyfit(nefull[i][6:9], tempfull[i][6:9], 2)
        polynomial = np.poly1d(coefficients)
        sh_fit = polynomial(nefull[i][6:9])
        plt.plot(nefull[i][6:9], sh_fit, linestyle = linestyle[i], color = colour[i])
    

colours = iter(plt.cm.Dark2(np.linspace(0, 1, len(Tfull_sh))))
circles = []
for j in range(len(Tfull_sh)):
        circle = plt.Circle(((nefull_sh[j] + nefull_snb[j]) / 2, (Tfull_sh[j] + Tfull_snb[j]) / 2),
            0.25, color = 'k', fill = False)
        circles.append(circle)
        #plt.gca().add_patch(circles[j])


labels = [[50,42], [100,42], [200, 42], [50,11], [100,11], [200,11], [50,4], [100,4], [200,4]]
c_label = []
for label in labels:
    c_label.append(("$L = {{{}}}, H = {{{}}}$").format(label[0], label[1]))

legend1 = plt.legend(handles = [p for p in points], labels = mechanism, loc = 4, fontsize = 14)
#plt.legend(handles = [c for c in circles], labels = c_label, loc = 4)
plt.gca().add_artist(legend1)

positions = [[2.65,2.73], [3.57, 4.5], [3.45, 6.8], [1.35,1.82], [1.45,2.95], [1.6,4.5], [0.45,1.1], [0.11,2.2], [0.41,3.75]]
for label in labels:
    i = labels.index(label)
    plt.text(positions[i][0], positions[i][1], ("${{{}}}$Mm").format(label[0]), fontsize = 13)
    #if (i < 7):
        #plt.text(positions[i][0], positions[i][1], ("$L = {{{}}}$Mm, \n$H = {{{}}}\mu$Wm$^{{-3}}$").format(label[0], label[1] * 10), fontsize = 12)
    #else:
        #plt.text(positions[i][0], positions[i][1], ("$L = {{{}}}$Mm, $H = {{{}}}\mu$Wm$^{{-3}}$").format(label[0], label[1] * 10), fontsize = 12)
plt.text(0.55, 4.3, "A", fontsize = 18)
plt.text(1.55, 5, "B", fontsize = 18)
plt.text(3, 6.8, "C", fontsize = 18)


#plt.title("Loop apex temperature and number density")
plt.ylabel("Temperature [MK]", fontsize = 15)
plt.xlabel("Electron number density [$10^{9}$$cm^{-3}$]", fontsize = 15)
plt.xticks(fontsize = 13)
plt.yticks(fontsize = 13)
plt.ylim((0.8, 7.4))
plt.xlim(0.01, 4.1)
ax = plt.gca()
ax.set_yticklabels(np.round(ax.get_yticks(),1))
fig = plt.gcf()
fig.set_size_inches(8, 6)
plt.savefig("ScalingTn.pdf", format = 'pdf')
plt.show()



TSH = []
TFL = []
TSNB = []
for i in range(8):
    TSH.append([nefull_sh[i], Tfull_sh[i]])
    TFL.append([nefull_lim[i], Tfull_lim[i]])
    TSNB.append([nefull_snb[i], Tfull_snb[i]])



"""
d = {'SH': TSH, 'FL': TFL, 'SNB': TSNB, 'text': positions} 
df = pd.DataFrame(d)
df.to_csv('locations.csv')

T_rtv = []
for label in labels:
    T_rtv.append(2013 * (label[0] * 10**6)**(4/7) * (label[1]*10**-5)**(2/7))
for i in range(3):
    for j in range(10):
        tempfull[i][j] *= 10**6

for T in tempfull:
    plt.scatter(T_rtv, T, label = mechanism[tempfull.index(T)])

plt.plot([5*10**5,8*10**6],[5*10**5,8*10**6], color = 'k')
plt.plot([5*10**5, 8*10**6], [5*10**5 / (3.5**(2/7)), 8 * 10**6 / (3.5**(2/7))], color = 'k', linestyle = '--')
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.show()"""
