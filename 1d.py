import sdf_helper as sh
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.constants import mu_0, epsilon_0, k, m_p
from pynput.keyboard import Listener, Key

def next_image(key):
    if (key == Key.space):
        plt.close()

listener = Listener(on_press = next_image)
listener.start()

array = np.array([])


B0 = 0.001
L0 = 100e6
rho0 = 1.e-6


v0 = B0 / np.sqrt(mu_0 * rho0)
T0 = v0**2 * 1.2 * m_p / k
t0 = L0 / v0

T02 = 115.28 
print(t0)

k = 2 * math.pi / 100 
y0 = 50

for i in range(100):
    i += 144
    si = (4-len(str(i))) * "0" + str(i)

    data2 = sh.getdata("../../Lare2d-dev/Data/simple/strongSH/5e-3/" + si + ".sdf")
    
    data = sh.getdata("../../Lare2d-dev/Data/" + si + ".sdf")


    T = data.Fluid_Temperature.data * T0
    rho = data.Fluid_Rho.data * rho0
    
    x = np.linspace(-50, 50, len(T[1]))
    y = np.linspace(0, 80, len(T[0]))
    
    field_line = np.zeros(len(T[1]))
    temp = np.array([])
    dist = np.array([])
    temp2 = np.array([])
    
    first_call = True

    for i in range(len(T[1])):
        if (x[i] > -25 and x[i] < 25):
            field_line[i] = 1 / k * math.log(math.cos(k * x[i])) + y0
            index = 0
            min_dist = 1.e10
            for j in range(len(T[0])):
                if (abs(y[j] - field_line[i]) < min_dist):
                    index = j
                    min_dist = abs(y[j] - field_line[i])


            if (first_call): 
                prev = [x[i],y[index]]
                cumulative = 0
            
            difference = np.sqrt((x[i] - prev[0])**2 + (y[index]-prev[1])**2)

            dist = np.append(dist, cumulative + difference) 
            temp = np.append(temp, T[i][index])

            prev = [x[i],y[index]]
            cumulative += difference 

            first_call = False
        
    temp / 1.e6
    
    T2 = data2.Fluid_Temperature.data[2] * T02


    s = np.linspace(0,120,len(T2))
    #plt.plot(s,T2)

    plt.plot(dist,temp)
    plt.xlabel("Distance along loop / Mm")
    plt.ylabel("Temperature / MK")

    plt.show()    
            
            


