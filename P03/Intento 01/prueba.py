import numpy as np 
import matplotlib.pyplot as plt 

from Adaline import AdalineGD
import pdr

# Standardize the data
X = np.array([[0,0],[1,1],[2,2],[3,1],[4,1],[5,1]])
Y = np.array([0,1,2,1,1,1])

# Create the AdalineGD model
model1 = AdalineGD(eta = 0.01)

# Train the model
model1.fit(X, Y)

# Plot the training error
plt.plot(range(1, len(model1.cost_) + 1), model1.cost_, marker = 'o', color = 'red')
plt.xlabel('Epochs')
plt.ylabel('Sum-squared-error')
plt.show()

# Plot the decision boundary
plt.plot(Y)
plt.title('Adaline - Gradient Descent')
plt.legend(loc = 'upper left')
print(X[0], model1.predict(X[0]))
print(X[1], model1.predict(X[1]))
print(X[2], model1.predict(X[2]))
print(X[3], model1.predict(X[3]))
plt.show()