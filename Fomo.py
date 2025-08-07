import numpy as np
import matplotlib.pyplot as plt



Thomas = open("../chiantitables/goft_table_aia131_abco.dat")
lines1 = Thomas.readlines()

T1 = np.array([])
G = np.array([])

for i in range(15, 47):
    for x in lines1[i].split():
        T1 = np.append(T1, 10**float(x))

for i in range(56, 88):
    for x in lines1[i].split():
        G = np.append(G, float(x))


Sergey = open("../tresp_2019.txt")
lines2 = Sergey.readlines()

T2 = np.array([])
R = np.array([])

for i in range(20,83):
    x = lines2[i].split()[0]
    y = lines2[i].split()[2]
    T2 = np.append(T2, 10**float(x))
    R = np.append(R, float(y))

G *= 8.46e-12

plt.plot(T2, R, label = "IDL")
plt.plot(T1, G, label = "FoMo")

plt.xscale('log')

plt.ylabel("Responses function")
plt.xlabel("Temperature [K]")

plt.legend()
plt.savefig("Response.png")
plt.show()
