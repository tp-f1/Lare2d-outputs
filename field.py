import numpy as np
import sdf_helper as sh
import matplotlib.pyplot as plt
import math
import matplotlib.animation as animation
from pynput.keyboard import Listener, Key

def next_image(key):
    if (key == Key.space):
        plt.close()

listener = Listener(on_press = next_image)
listener.start()
artists = []
fig, ax = plt.subplots()
for i in range(100):
    #i*=5
    #i += 50
    i = (4 - len(str(i))) * "0" + str(i)
    #data = sh.getdata("../../Lare2d-dev/Data/" + i + ".sdf")
    data = sh.getdata("../DiracData/" + i + ".sdf")
    #data = sh.getdata("../../Lare2d/Data/waves/" + i + ".sdf")

    bx = np.asarray(data.Magnetic_Field_Bx.data * 20)
    by = np.asarray(data.Magnetic_Field_By.data * 20)
    bz = np.asarray(data.Magnetic_Field_Bz.data * 20)
    B = np.zeros([bx.shape[0]-1,bx.shape[1]])
    

    bx = np.delete(bx, 20,0)
    by = np.delete(by, 20,1)
    
    J = ((by-bz)**2 + (bz-bx)**2 + (bx-by)**2)**0.5
    
    bx = np.swapaxes(bx, 0, 1)
    by = np.swapaxes(by, 0, 1)
    
    B = np.linalg.norm(np.array([bx,by]), axis = 0)

    x = np.linspace(-30, 30, bx.shape[1])
    y = np.linspace(-10, 90, bx.shape[0])
    
    graph = plt.streamplot(x,y, bx, by, color = J)
    fig.colorbar(graph.lines, label = "Magnetic Field Strength / G")
    plt.title("{:.1f}".format(t* 56327) + "s") 
    plt.xlabel("x / Mm")
    plt.ylabel("y / Mm")

    #plt.savefig("field-lines" + i + ".png") 

    plt.show()
    #sh.plot_auto(data.Magnetic_Field_Bx)
    #plt.show()
    #sh.plot_auto(data.Magnetic_Field_By)
    #plt.show()
    
    #while j < len(bx.data[1])
    #    while k < len(bx.data[2])
    #B[ = math.sqrt(bx.data[2]**2 + by.data[2]**2)


