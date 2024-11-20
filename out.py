import matplotlib.pyplot as plt
import numpy as np
from probe import read_probe

p = read_probe("../../Lare2d/Data/probe001.dat")

plt.plot(p.t, p.vy)
plt.show()
