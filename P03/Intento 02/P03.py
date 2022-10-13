from tkinter import ttk, messagebox, IntVar
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt 
import tkinter as Tk
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import MouseButton
from matplotlib.figure import Figure
from Adaline import AdalineGD
import pdr

x = None
n = None
s = None
y = None

def draw_noise(scale):
    global x, n, s, y
    global ax, f
    x = np.linspace(0, scale * np.pi, num=10000)
    n = np.random.normal(scale=0.24, size=x.size)
    s = 1 * np.sin(x)
    y = 1 * np.sin(x) + n

    ax.plot(x, y, label='Total', color='#ff8780')
    #ax.plot(x, output, label='Adaline', color='#eb4034')
    ax.plot(x, s, label='Sine', color='#ffad1f')
    f.canvas.draw()


def adaline_train_anim():
    global ax, f
    global y, x

    n_input = 10
    output = y[:n_input]

    model1 = AdalineGD(n_iter = 50, eta = 0.005)#50,0.005

    for i in range(0,x.size - n_input):
        inputs = np.column_stack([x[i:i+n_input],y[i:i+n_input]])
        desired = y[i:i+n_input]
        model1.fit(inputs, desired)
        aux = model1.predict(inputs[-1])
        output = np.append(output, aux)
        ax.plot(x[:i+n_input+1], output, label='Adaline', color='#eb4034')
        f.canvas.draw()
        f.canvas.flush_events()
        print('.')

def adaline_train(lr):
    global ax, f
    global y, x, s

    n_input = 10
    output = y[:n_input]

    model1 = AdalineGD(n_iter = 50, eta = lr)#50,0.005

    for i in range(0,x.size - n_input):
        inputs = np.column_stack([x[i:i+n_input],y[i:i+n_input]])
        desired = y[i:i+n_input]
        model1.fit(inputs, desired)
        aux = model1.predict(inputs[-1])
        output = np.append(output, aux)
    
    ax.plot(x[:i+n_input+1], output, label='Adaline', color='#eb4034')
    ax.plot(x, s, label='Sine', color='#ffad1f')
    f.canvas.draw()


#EVENTS
def ButtonTrain_Event():
    adaline_train(scaleLearningRate.get())

def ButtonDrawCurve_Event():
    global scaleScale, ax, f
    ax.clear()
    ax.grid('on')
    draw_noise(scaleScale.get())

    pass

def ScaleLearningRate_Event(event):
    print('Learning Rate: ', scaleLearningRate.get())

def ScaleScale_Event(event):
    print('Scale: ', scaleScale.get())

#WINDOW
root = Tk.Tk()
root.geometry('1000x500')
root.minsize(500, 500)
root.title('Practica 03')

#PLOT
f = Figure(figsize=(0,0), dpi=100)
ax = f.add_subplot(111)
ax.grid('on')
canvas = FigureCanvasTkAgg(f, master=root)
canvas.get_tk_widget().place(relx=0.05, rely=0.05, relheight=0.90, relwidth=0.8)

#CONTROLS

scaleLearningRate = ttk.Scale(from_=0.001, to=0.01, command=ScaleLearningRate_Event)
scaleLearningRate.place(relx=0.875, rely=0.7, height=20, relwidth=0.1)
scaleScale = ttk.Scale(from_=0.5, to=2, command=ScaleScale_Event)
scaleScale.place(relx=0.875, rely=0.75, height=20, relwidth=0.1)

buttonDraw = ttk.Button(text='draw', command=ButtonDrawCurve_Event)
buttonDraw.place(relx=0.875, rely=0.85, relheight=0.05, relwidth=0.1)
buttonTrain = ttk.Button(text='train', command=ButtonTrain_Event)
buttonTrain.place(relx=0.875, rely=0.90, relheight=0.05, relwidth=0.1)

draw_noise(2)
Tk.mainloop()