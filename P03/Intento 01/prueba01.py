import numpy as np 
import matplotlib.pyplot as plt 

from Adaline import AdalineGD
import pdr

x = np.linspace(0, 2 * np.pi, num=100)
n = np.random.normal(scale=0.05, size=x.size)
s = 1 * np.sin(x)
y = 1 * np.sin(x) + n

n_input = 3
output = y[:n_input]

for i in range(0,x.size - n_input):
    inputs = np.column_stack([x[i:i+n_input],y[i:i+n_input]])
    desired = y[i:i+n_input]

plt.plot(x, y, label='Total')
plt.plot(x, s, label='Sine')
plt.plot(x, n, label='Noise')

plt.show()