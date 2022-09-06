from tkinter import ttk, messagebox, IntVar
import matplotlib, numpy as np, sys
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as Tk

from activations import *

pointsX = []
pointsY = []

#FUNCTIONS
def draw2d(pesos, theta):
    global ax, f
    w1, w2 = pesos[0], pesos[1]
    li, ls = -2, 2
    b = theta * -1

    ax.plot([li,ls], [(1/w2)*(-w1*(li)-b), (1/w2)*(-w1*(ls)-b)], '--k')
    f.canvas.draw()

#EVENTS
def Canvas_Event(event):
    x,y = event.xdata, event.ydata
    global ax, f
    if x is not None or y is not None:
        ax.plot(x,y, '.k')
        pointsX.append(x)
        pointsY.append(y)
        f.canvas.draw()
    print(x, y)

def ButtonDraw_Event():
    global entryW1, entryW2, entryTheta

    w1 = 0
    w2 = 0
    theta = 0

    try:
        w1 = float(entryW1.get())
        w2 = float(entryW2.get())
        theta = float(entryTheta.get())
    except:
        print('some values are incorrect')

    entradas = np.arange(1,3)
    pesos = np.array([w1,w2])
    _umbral = umbral(entradas, pesos, theta)
    escalon = step(_umbral)
    
    print(entradas, pesos)
    print('draw with the following walues:')
    print('w1:', w1, ' w2:', w2, ' theta:', theta)
    print('umbral', _umbral)
    print('escalon', escalon)
    draw2d(pesos, theta)


def ButtonClas_Event():
    global ax, f, entryTheta
    
    w1 = 0
    w2 = 0
    theta = 0

    try:
        w1 = float(entryW1.get())
        w2 = float(entryW2.get())
        theta = float(entryTheta.get())
    except:
        print('some values are incorrect')
    
    pesos = np.array([w1,w2])

    for i in range(len(pointsX)):
        entradas = np.array([pointsX[i],pointsY[i]])
        _umbral = umbral(entradas, pesos, theta)
        result = step(_umbral)

        if(result == 1): ax.plot(pointsX[i],pointsY[i], '.b')
        else: ax.plot(pointsX[i],pointsY[i], '.r')
    
    f.canvas.draw()

#WINDOW
root = Tk.Tk()
root.geometry('500x500')
root.minsize(500, 500)
root.title('Practica 01')

#PLOT
f = Figure(figsize=(0,0), dpi=100)
ax = f.add_subplot(111)
f.canvas.callbacks.connect('button_press_event', Canvas_Event)
ax.grid('on')
ax.set_xlim([-2,2])
ax.set_ylim([-2,2])
canvas = FigureCanvasTkAgg(f, master=root)
canvas.get_tk_widget().place(relx=0.1, rely=0.05, relheight=0.65, relwidth=0.8)

#CONTROLS
labelW1 = ttk.Label(text='W1:', anchor='e')
labelW1.place(relx=0.1, rely=0.7, height=20, relwidth=0.1)
entryW1 = ttk.Entry()
entryW1.place(relx=0.2, rely=0.7, height=20, relwidth=0.1)

labelW2 = ttk.Label(text='W2:', anchor='e')
labelW2.place(relx=0.3, rely=0.7, height=20, relwidth=0.1)
entryW2 = ttk.Entry()
entryW2.place(relx=0.4, rely=0.7, height=20, relwidth=0.1)

labelTheta = ttk.Label(text='Theta:', anchor='e')
labelTheta.place(relx=0.5, rely=0.7, height=20, relwidth=0.1)
entryTheta = ttk.Entry()
entryTheta.place(relx=0.6, rely=0.7, height=20, relwidth=0.1)

buttonDraw = ttk.Button(text='Draw', command=ButtonDraw_Event)
buttonDraw.place(relx=0.7, rely=0.7, height=20, relwidth=0.1)

buttonClas = ttk.Button(text='Clas', command=ButtonClas_Event)
buttonClas.place(relx=0.8, rely=0.7, height=20, relwidth=0.1)

#PERCEPTRON

Tk.mainloop()