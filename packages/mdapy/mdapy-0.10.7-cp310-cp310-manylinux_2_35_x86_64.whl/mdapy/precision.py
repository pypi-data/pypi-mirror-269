# Copyright (c) 2022, mushroomfire in Beijing Institute of Technology
# This file is from the mdapy project, released under the BSD 3-Clause License.

import numpy as np
import taichi as ti

class Precision:
    precision = "double"
    ti_fp = ti.f64 
    np_fp = np.float64
    flag = 0