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

temp_norm = 96.4
rho_norm = 10**-6

avt = np.array([])
avr = np.array([])
chrom = np.array([])
time = np.array([])
xfield = np.array([])
yfield = np.array([])
velocity = np.array([])
apext = np.array([])
apexr = np.array([])
foott = np.array([])
footr = np.array([])
mgi = np.array([])
intensity = np.array([])
times = []

t500 = 3 * 10**6
nt = 50 

tstart = 0.2
#starts = ["Q1fs1", "Q1fs2", "Q1fs3", "Q2fs1", "Q2fs2", "Q2fs3", "Q3fs1", "Q3fs2", "Q3fs3"]
starts = ["newsh", "new"]
for start in starts:
    first = True
    for i in range(nt):
        #i += 200
        si = (4 - len(str(i)))*"0" + str(i)
        if ("data" in start):
            data = sh.getdata("../../Lare2d-dev/Data/" + si + ".sdf")
        elif ("large" in start):
            data = sh.getdata("../../Lare2d-dev/Data/21-big/" + si + ".sdf")
        elif ("Dirac" in start):
            data = sh.getdata("../DiracData/waves/FL2/" + si + ".sdf")
        else:  
            #data = sh.getdata("../../Lare2d-dev/Data/" + start + "/" + si + ".sdf")
            data = sh.getdata("../DiracData/reconnection/" + start + "/" + si + ".sdf")

        time = np.append(time, t)  
        
        temp = data.Fluid_Temperature.data[100] * temp_norm
        rho = data.Fluid_Rho.data[460] * rho_norm  
        by = data.Magnetic_Field_By.data[100][199]
        bx = data.Magnetic_Field_Bx.data[100][199]

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
        
        #for j in range(len(temp)):
        #    if (temp[j] > 1e5):
        #        yc = j
        #        break
        
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
        apext = np.append(apext, max(data.Fluid_Temperature.data[int(len(temp)/2)]))
        apexr = np.append(apexr, rho[int(len(rho)/2)])
        
        foott = np.append(foott, temp[150])
        footr = np.append(footr, rho[150])

        if (temp[int(len(temp)/2)] < 5.0e6 and first):
            times.append((t - time[0]) * 78609.82097)
            first = False

        velocity = np.append(velocity, vy)
        xfield = np.append(xfield, bx)
        yfield = np.append(yfield, by)
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
starts = ['SH', 'FL']
t_end = 10000 
#time = np.linspace(0,t_end,nt)
time = (time - time[0]) * 122799
xfield = (xfield - xfield[0]) * 0.002
yfield = (yfield - yfield[0]) * 0.002

for i in range(len(starts)):
    plt.plot(time[i*nt:(i+1)*nt], xfield[i*nt:(i+1)*nt], label = "x")
    plt.plot(time[i*nt:(i+1)*nt], yfield[i*nt:(i+1)*nt], label = "y")
plt.legend()

plt.show()


for i in range(len(starts)):
    if i > 1: linestyle = '--'
    else: linestyle = '-'
    if (i%3 == 0): colour = 'r'
    elif (i%3 ==1): colour = 'g'
    else: colour = 'k'
    plt.plot(time[i*nt:(i+1)*nt], apext[i*nt:(i+1)*nt] / 10**6, label = starts[i], linestyle = linestyle, color = colour)
    
plt.title("Footpoint temperature")
#for i in range(nt):
#    if (abs(apext[i] - apext[2*nt + i]) > apext[i] / 100):
#        t1 = time[i]
#        break
#for i in range(nt):
#    if (abs(apext[i+nt] - apext[3*nt + i]) > apext[i+nt] / 100):
#        t2 = time[i]
#        break
#print(t1,t2)
#plt.axvline(t1, color = 'k', linestyle = '-.')
#plt.axvline(t2, color = 'r', linestyle = '-.')
plt.ylabel("Temperature [MK]", fontsize = 16)
plt.xlabel("Time [s]", fontsize = 16)
plt.yticks(fontsize = 13)
plt.xticks(fontsize = 13)
#plt.yscale("log")
plt.legend(fontsize = 13)
plt.tight_layout()
fig = plt.gcf()
fig.set_size_inches(7, 5)
#plt.savefig("apext.pdf", format = 'pdf')
plt.show()

for i in range(len(starts)):
    if i > 1: linestyle = '--'
    else: linestyle = '-'
    if (i%3 == 0): colour = 'r'
    elif (i%3 ==1): colour = 'g'
    else: colour = 'k'
    plt.plot(time[i*nt:(i+1)*nt], footr[i*nt:(i+1)*nt]*10**12, label = starts[i], color = colour, linestyle = linestyle)

plt.title("Footpoint density")
plt.ylabel("Density / $10^{-12}$kg/$m^3$", fontsize = 16)
plt.xlabel("Time / s", fontsize = 16)
plt.yticks(fontsize = 13)
plt.xticks(fontsize = 13)
#plt.yscale("log")
plt.legend(fontsize = 13)
plt.tight_layout()
fig = plt.gcf()
fig.set_size_inches(7, 5)
plt.savefig("footdensity.png")
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








