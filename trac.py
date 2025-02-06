
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

t500 = 3 * 10**6
nt = 500
#starts = ["Q1fs1", "Q1fs2", "Q1fs3", "Q2fs1", "Q2fs2", "Q2fs3", "Q3fs1", "Q3fs2", "Q3fs3"]
starts = ["0.12"]
for start in starts:
    for i in range(nt):
        i += 100
    
        si = (4 - len(str(i)))*"0" + str(i)
        if (start == "0.12"):
            data = sh.getdata("../../Lare2d-dev/Data/" + si + ".sdf")
        else:
            data = sh.getdata("../../Lare2d-dev/Data/lim1000/tri60/3Mm/" + si + ".sdf")
            
        
        t = data.Fluid_Temperature.data[2] * temp_norm
        rho = data.Fluid_Rho.data[2] * rho_norm  
        
        if (start == "lim1000"):
            lbl = "flux-limited"
        elif (start == "sh1000"):
            lbl = "Spitzer-Harm"
        else: 
            lbl = "trac"
        
        lbl = start

        if (i == 800):        
            y = np.linspace(0,170, len(t))
        
            plt.plot(y, rho, label = lbl)     
        
        for j in range(len(t)):
            if (t[j] > 1e6):
                yc = j
                print(yc)
                break

        t = np.delete(t, np.arange(len(t) - yc, len(t)))
        t = np.delete(t, np.arange(0,yc))
        rho = np.delete(rho, np.arange(0,yc))
        rho = np.delete(rho, np.arange(len(rho) - yc, len(rho)))
        
        
        avt = np.append(avt, np.average(t))
        avr = np.append(avr, np.average(rho))
        chrom = np.append(chrom, t[yc])

plt.ylabel("Temperature / K")
plt.xlabel("Distance along loop / Mm")
plt.yscale("log")
plt.legend()
plt.show()
 

time = np.linspace(0,3818,nt)

for i in range(len(starts)):
    plt.plot(time, avt[i*nt:(i+1)*nt], label = starts[i])

plt.title("Average coronal temperature")
plt.ylabel("Temperature / K")
plt.xlabel("time / s")
plt.yscale("log")
plt.legend()
plt.show()

for i in range(len(starts)):
    plt.plot(time, avr[i*nt:(i+1)*nt], label = starts[i])

plt.title("Average coronal density")
plt.ylabel("Density / kg/$m^3$")
plt.xlabel("time / s")
plt.yscale("log")
plt.legend()
plt.show()

"""
for i in range(len(starts)):
    plt.plot(time, chrom[i*nt:(i+1)*nt], label = starts[i])

plt.title("Chromospheric temperature")
plt.xlabel("time, seconds")
plt.ylabel("temperature, kelvin")
plt.yscale("log")
plt.legend()
plt.show()

"""


a = []
for i in range(len(starts)):
    for j in range(nt):
        if (chrom[j + i*nt] > 10**5):
            a.append(j * 1909 / nt)
            break
print(a)










