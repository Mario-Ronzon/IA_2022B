import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, num=600)
n = np.random.normal(scale=8, size=x.size)
s = 100 * np.sin(x)
y = 100 * np.sin(x) + n

plt.plot(x, y, label='Total')
plt.plot(x, s, label='Sine')
plt.plot(x, n, label='Noise')

plt.show()