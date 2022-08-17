import sympy
from sympy import solve, acos, Symbol

x = Symbol('x')
result = solve(acos(0.4654469)-x)
print(result)
print(float(sympy.pi))


import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import os
import qt5_applications
dirname = os.path.dirname(qt5_applications.__file__)
plugin_path = os.path.join(dirname, 'Qt', 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

data = np.loadtxt('Spec_results\spec_Sun_Jun_12_17_11_03_2022.txt')

print(data.shape)

lx = data[0, :]
ly = data[1, :]

print(lx.shape)

lth = np.argsort(lx)
x_smooth = np.empty_like(lx)
y_smooth = np.empty_like(ly)

for i in range(y_smooth.size):
    x_smooth[i] = lx[lth[i]]
    y_smooth[i] = ly[lth[i]]

from scipy.signal import savgol_filter

lx = x_smooth
ly = y_smooth

y_smooth = savgol_filter(y_smooth, 11, 5)

plt.subplot(121)
plt.plot(lx, ly)

plt.subplot(122)
plt.plot(x_smooth, y_smooth)

plt.show()


