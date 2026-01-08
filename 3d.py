import sdf_helper as sh
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.constants import mu_0, epsilon_0, k, m_p
from pynput.keyboard import Listener, Key

def next_image(key):
    if (key == Key.space):
        plt.close()

listener = Listener(on_press= next_image)
listener.start()

B0 = 0.001
L0 = 1.e6
rho0 = 1.e-6

v0 = B0 / np.sqrt(mu_0 * rho0)
T0 = v0**2 / 1.2 * m_p / k
t0 = L0 / v0

print(v0)

for i in range(210):
    #i *= 10
    #i += 29
    si = (4-len(str(i))) * "0" + str(i)
    data = sh.getdata("../DiracData/3d/" + si + ".sdf")
    #data = sh.getdata("../../Lare3d-dev/Data/" + si + ".sdf")
    
    vz = data.Velocity_Vz
    rho = data.Fluid_Rho
    temp = data.Fluid_Temperature
    Bx = data.Magnetic_Field_Bx
    By = data.Magnetic_Field_By
    Bz = data.Magnetic_Field_Bz
    sh.plot_auto(temp, iy = 50)
    plt.show()


