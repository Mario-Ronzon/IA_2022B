import numpy as np 
import matplotlib.pyplot as plt 

from Adaline import AdalineGD
import pdr

x = np.linspace(0, 2 * np.pi, num=10000)
n = np.random.normal(scale=0.24, size=x.size)
s = 1 * np.sin(x)
y = 1 * np.sin(x) + n

n_input = 10
output = y[:n_input]

model1 = AdalineGD(n_iter = 50, eta = 0.005)#50,0.005

for i in range(0,x.size - n_input):
    inputs = np.column_stack([x[i:i+n_input],y[i:i+n_input]])
    desired = y[i:i+n_input]
    model1.fit(inputs, desired)
    aux = model1.predict(inputs[-1])
    output = np.append(output, aux)

print(y.size, output.size)
print(np.column_stack([y,output]))

plt.plot(x, y, label='Total', color='#ff8780')
plt.plot(x, output, label='Adaline', color='#eb4034')
plt.plot(x, s, label='Sine', color='#ffad1f')

plt.show()