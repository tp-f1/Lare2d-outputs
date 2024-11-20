import struct
import numpy as np
from dataclasses import dataclass

def read_probe(fname):
    @dataclass
    class probe:
        x: float
        y: float
        t: np.ndarray
        vx: np.ndarray
        vy: np.ndarray
        vz: np.ndarray
        bx: np.ndarray
        by: np.ndarray
        bz: np.ndarray
    with open(fname, mode='rb') as f:
        data = f.read()
    fpos = 0
    nbytes = 8
    n = struct.unpack('q',data[fpos:fpos+nbytes])[0]
    fpos += nbytes
    nbytes = 16
    x,y = struct.unpack('dd',data[fpos:fpos+nbytes])
    fpos += nbytes
    t = []
    pdata = []
    for i in range(n):
        nbytes = 8
        t.append(struct.unpack('d',data[fpos:fpos+nbytes])[0])
        fpos +=nbytes
        nbytes = 48
        pdata.append(struct.unpack('dddddd',data[fpos:fpos+nbytes]))
        fpos +=nbytes
    t = np.array(t)
    pdata = np.array(pdata)
    vx = np.array(pdata[:,0])
    vy = np.array(pdata[:,1])
    vz = np.array(pdata[:,2])
    bx = np.array(pdata[:,3])
    by = np.array(pdata[:,4])
    bz = np.array(pdata[:,5])
    return probe(x, y, t, vx, vy, vz, bx, by, bz)
