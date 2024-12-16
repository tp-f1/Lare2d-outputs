import numpy as np
import sdf_helper as sh
import matplotlib.pyplot as plt
import math

for i in range(100):
    i = (3 - len(str(i))) * "0" + str(i)
    data = sh.getdata("../../Lare2d/Data/0" + i + ".sdf")
    

    bx = np.asarray(data.Magnetic_Field_Bx.data)
    by = np.asarray(data.Magnetic_Field_By.data)
    B = np.zeros([bx.shape[0]-1,bx.shape[1]])
    
    bx = np.delete(bx, 100,0)
    by = np.delete(by, 100,1)
    
    bx = np.swapaxes(bx, 0, 1)
    by = np.swapaxes(by, 0, 1)

    print(np.shape(bx))
    print(np.shape(by))
    for j in range(bx.shape[0]-1):
        for k in range(bx.shape[1]):
             
            B[k][j] = math.sqrt(bx[j][k]**2 + by[j][k]**2)
    
    x = np.linspace(-20, 20, bx.shape[0])
    y = np.linspace(-10, 80, bx.shape[1])
    
    graph = plt.streamplot(x,y, bx, by)
    
    plt.xlabel("x / normalised units")
    plt.ylabel("y / normalised units")


    plt.show()
    #while j < len(bx.data[1])
    #    while k < len(bx.data[2])
    #B[ = math.sqrt(bx.data[2]**2 + by.data[2]**2)




