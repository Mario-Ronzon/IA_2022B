import numpy as np

def umbral(entradas, pesos, theta):
    umbral = np.multiply(entradas, pesos)
    umbral = np.sum(umbral)
    umbral = umbral - theta
    return umbral

def step(umbral):
    if(umbral >= 0): return 1
    else: return 0