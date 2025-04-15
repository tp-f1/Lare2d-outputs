import ChiantiPy
import ChiantiPy.core as ch
import ChiantiPy.tools.filters as chfilters
import ChiantiPy.tools.io as chio
import sdf_helper as sh
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.constants as sc
from pynput.keyboard import Listener, Key

def next_image(key):
    if (key == Key.space):
        plt.close()

listener = Listener(on_press = next_image)
listener.start()

temp_norm = 115.27582493
rho_norm = 10**-6

avt = np.array([])
avr = np.array([])
chrom = np.array([])
time = np.array([])
apext = np.array([])
apexr = np.array([])
foott = np.array([])
footr = np.array([])
mgi = np.array([])
intensity = np.array([])
times = []

t500 = 3 * 10**6
nt = 100 

tstart = 0.2
#starts = ["Q1fs1", "Q1fs2", "Q1fs3", "Q2fs1", "Q2fs2", "Q2fs3", "Q3fs1", "Q3fs2", "Q3fs3"]
starts = ["sh", "snb", "sh-rad", "snb-rad"]
for start in starts:
    first = True
    for i in range(nt):
        i += 112
        si = (4 - len(str(i)))*"0" + str(i)
        if ("new" in start):
            data = sh.getdata("../../Lare2d-dev/Data/"  + si + ".sdf")
        elif ("large" in start):
            data = sh.getdata("../../Lare2d-dev/Data/21-big/" + si + ".sdf")
        elif ("2" in start):
            data = sh.getdata("../../Lare2d-dev/Data/initialtsh/" + start[:-1] + "/" + si + ".sdf")
        else:  
            data = sh.getdata("../../Lare2d-dev/Data/initialt/" + start + "/" + si + ".sdf")

        time = np.append(time, t)  
        
        temp = data.Fluid_Temperature.data[2] * temp_norm
        rho = data.Fluid_Rho.data[2] * rho_norm  
        
        if (start == "lim1000"):
            lbl = "flux-limited"
        elif (start == "sh1000"):
            lbl = "Spitzer-Harm"
        else: 
            lbl = "trac"
        
        lbl = start

        #if (i == 800):        
            #y = np.linspace(0,170, len(t))
        
        #plt.plot(y, rho, label = lbl)     
        
        for j in range(len(temp)):
            if (temp[j] > 1e5):
                yc = j
                break
        foott = np.append(foott, temp[116])
        footr = np.append(footr, rho[116])
        
        intensity = np.append(intensity, np.sum(rho**2 * temp**4))


        #mg = ch.ion('he_1', temp, rho / 9.11e-25)
        #mg.gofnt()
        #mg.intensity() 
        #s = np.linspace(0,170, len(temp))
        #dist = np.abs(np.asarray(mg.Intensity['wvl']) - 656)
        #idx = np.argmin(dist)
        #plt.loglog(temp, mg.Intensity['intensity'][:,idx])
        #plt.show()

        #mgi = np.append(mgi, np.sum(mg.Intensity['intensity'][:, idx] * (rho / 9.11e-25)**2)) 
        #print(mgi[i-100])
        #print(mg.Intensity['intensity'][yc, idx]) 

        #plt.plot(s, mg.Intensity['intensity'][:,idx])   
        #plt.show() 

        yc = int(len(temp) / 4)
        temp = np.delete(temp, np.arange(len(temp) - yc, len(temp)))
        temp = np.delete(temp, np.arange(0,yc))
        rho = np.delete(rho, np.arange(0,yc))
        rho = np.delete(rho, np.arange(len(rho) - yc, len(rho)))

        avt = np.append(avt, np.average(temp))
        avr = np.append(avr, np.average(rho))
        #chrom = np.append(chrom, t[yc])
        apext = np.append(apext, temp[int(len(temp)/2)])
        apexr = np.append(apexr, rho[int(len(rho)/2)])

        if (temp[int(len(temp)/2)] < 5.0e6 and first):
            times.append((t - time[0]) * 78609.82097)
            first = False


#for i in range(len(starts)):
#        apext[i*nt: (i+1)*nt] /= apext[(i+1)*nt-1]
#        apexr[i*nt: (i+1)*nt] /= apexr[(i+1)*nt-1]
#        foott[i*nt: (i+1)*nt] /= foott[(i+1)*nt-1]
#        footr[i*nt: (i+1)*nt] /= footr[(i+1)*nt-1]

print(times)
#plt.ylabel("Temperature / K")
#plt.xlabel("Distance along loop / Mm")
#plt.yscale("log")
#plt.legend()
#plt.show()
starts = ['SH', 'SNB', 'SH - no rad. losses', 'SNB - no rad. losses']
t_end = 10000 
#time = np.linspace(0,t_end,nt)
time = (time - time[0]) * 78609.82097
for i in range(len(starts)):
    if i > 1: linestyle = '--'
    else: linestyle = '-'
    if (i%2 == 0): colour = 'k'
    else: colour = 'r'
    plt.plot(time[i*nt:(i+1)*nt], apext[i*nt:(i+1)*nt] / 10**6, label = starts[i], linestyle = linestyle, color = colour)
    
#plt.title("Apex temperature")
for i in range(nt):
    if (abs(apext[i] - apext[2*nt + i]) > apext[i] / 100):
        t1 = time[i]
        break
for i in range(nt):
    if (abs(apext[i+nt] - apext[3*nt + i]) > apext[i+nt] / 100):
        t2 = time[i]
        break
print(t1,t2)
#plt.axvline(t1, color = 'k', linestyle = '-.')
#plt.axvline(t2, color = 'r', linestyle = '-.')
plt.ylabel("Temperature [MK]", fontsize = 18)
plt.xlabel("Time [s]", fontsize = 18)
plt.yticks(fontsize = 13)
plt.xticks(fontsize = 13)
#plt.yscale("log")
plt.legend(fontsize = 13)
plt.tight_layout()
fig = plt.gcf()
fig.set_size_inches(8, 5)
plt.savefig("apext.svg", format = 'svg')
plt.show()

for i in range(len(starts)):
    plt.plot(time[i*nt:(i+1)*nt], apexr[i*nt:(i+1)*nt], label = starts[i])

#plt.title("Apex density")
plt.ylabel("Density / kg/$m^3$")
plt.xlabel("time / s")
#plt.yscale("log")
plt.legend()
plt.tight_layout()
#plt.savefig("apexr.png")
plt.show()



for i in range(len(starts)):
    line = plt.plot(apext[i*nt:(i+1)*nt] / 10**6, apexr[i*nt:(i+1)*nt]*10**12, label = starts[i])[0]
    colour = line.get_color()
    xdata = line.get_xdata()
    ydata = line.get_ydata()
    position = xdata.mean()
    for j in range(3):
        start_ind = (j+1) * 10
        end_ind = start_ind + 1
        line.axes.annotate('', xytext = (xdata[start_ind], ydata[start_ind]),
            xy=(xdata[end_ind], ydata[end_ind]),
            arrowprops=dict(arrowstyle="-|>", color=colour),
            size=25)

#plt.title("T-Rho evolution")
plt.xlabel("Temperature / MK")
plt.ylabel("Density / $10^{-12}$kgm$^{-3}$")
#plt.xscale("log")
#plt.yscale("log")
fig = plt.gcf()
fig.set_size_inches(8,5)
plt.legend()
#plt.savefig("T-rho.svg", format = 'svg')


plt.show()


"""

a = []
for i in range(len(starts)):
    for j in range(nt):
        if (chrom[j + i*nt] > 10**5):
            a.append(j * 1909 / nt)
            break

"""








