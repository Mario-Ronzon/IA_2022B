from tkinter import ttk, messagebox, IntVar
import matplotlib, numpy as np, sys
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import MouseButton
from matplotlib.figure import Figure

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

RED_DOT = '.r'
BLUE_DOT = '.b'
DASHED_LINE = '--y'
BLACK_LINE = '-k'

pointsX = []
pointsY = []
desired = []
done = False
iteration = 0
lastPred = []

class Perceptron:
    def __init__(self, n_input, learning_rate):
        self.w = -1 + 2 * np.random.rand(n_input)
        self.b = -1 + 2 * np.random.rand()
        self.eta = learning_rate
    
    def draw2d(self, last):
        global ax, f
        w1, w2, b = self.w[0], self.w[1], self.b
        li, ls = -2, 2

        linestyle = DASHED_LINE
        if last == True:
            linestyle = BLACK_LINE
        ax.plot([li,ls],
        [(1/w2)*(-w1*(li)-b),(1/w2)*(-w1*(ls)-b)],
        linestyle)
        f.canvas.draw()
        f.canvas.flush_events()
    
    def predict(self, X):
        p = X.shape[1]
        y_est = np.zeros(p)
        for i in range(p):
            y_est[i] = np.dot(self.w, X[:,i]) + self.b
            if y_est[i] >= 0:
                y_est[i] = 1
            else:
                y_est[i] = 0
        return y_est
    
    def fit(self, X, Y, epochs=50):
        global done, iteration, lastPred

        p = X.shape[1]
        prediction = np.zeros(p)
        done = False

        for current in range(epochs):
            for i in range(p):
                y_est = self.predict(X[:,i].reshape(-1,1))
                self.w += self.eta * (Y[i]-y_est) * X[:,i]
                self.b += self.eta * (Y[i]-y_est)
                prediction[i] = y_est
            
            iteration = current
            lastPred = prediction.tolist()
            if (np.array_equal(Y, prediction)) == True:
                self.draw2d(True)
                done = True
                break
            else:
                self.draw2d(False)

#EVENTS
def Canvas_Event(event):
    x,y = event.xdata, event.ydata
    global ax, f, drawMode

    if event.button is MouseButton.LEFT:
        drawMode = RED_DOT
    else:
        drawMode = BLUE_DOT

    if x is not None or y is not None:
        ax.plot(x,y, drawMode)
        pointsX.append(x)
        pointsY.append(y)
        if drawMode == RED_DOT:
            desired.append(1)
        else:
            desired.append(0)
        f.canvas.draw()
    print(x, y)

def ButtonInit_Event():
    global ax, f, neuron, scaleLearningRate
    neuron = Perceptron(2, scaleLearningRate.get())
    ax.cla()
    ax.grid('on')
    ax.set_xlim([-1,1])
    ax.set_ylim([-1,1])
    X = np.array ([
        pointsX,
        pointsY]) # INPUTS
    Y = np.array(desired)
    _, p = X.shape
    for i in range(p):
        if Y[i] == 0:
            ax.plot(X[0,i],X[1,i], BLUE_DOT)
        else:
            ax.plot(X[0,i],X[1,i], RED_DOT)
    neuron.draw2d(False)
    f.canvas.draw()
    print('init event')
    messagebox.showinfo(message='init done')

def ButtonTrain_Event():
    global scaleMaxEpoch, scaleLearningRate, neuron, done, iteration
    learning, epochs = scaleLearningRate.get(), int(scaleMaxEpoch.get())

    if epochs == 0:
        messagebox.showwarning(message='Verifique el numero de epocas')
        return
    if len(pointsX) == 0:
        messagebox.showwarning(message='No existen entradas')
        return

    neuron.eta = learning
    X = np.array ([
        pointsX,
        pointsY]) # INPUTS
    Y = np.array(desired)
    print(X.shape, Y.shape)
    neuron.fit(X,Y, epochs)
    print('train event', done, iteration)
    messagebox.showinfo(message='train status:' + str(done) + ' at epoch: ' + str(iteration + 1))

def ButtonVerify_Event():
    global lastPred, desired, pointsX, pointsY, ax, f, neuron

    X = np.array ([
        pointsX,
        pointsY]) # INPUTS
    Y = np.array(desired)
    p = X.shape[1]
    prediction = np.zeros(p)

    for i in range(p):
        y_est = neuron.predict(X[:,i].reshape(-1,1))
        prediction[i] = y_est
    lastPred = prediction.tolist()
    

    for i in range(len(lastPred)):
        if lastPred[i] == desired[i]:
            if desired[i] == 1:
                ax.plot(pointsX[i], pointsY[i], 'or')
            else:
                ax.plot(pointsX[i], pointsY[i], 'ob')
        else:
            if desired[i] == 1:
                ax.plot(pointsX[i], pointsY[i], 'xr')
            else:
                ax.plot(pointsX[i], pointsY[i], 'xb')
    f.canvas.draw()
    print('verify event')
    messagebox.showerror(message='verify done')

def ScaleLearningRate_Event(event):
    global labelLearningRate
    labelLearningRate.config(text='Learning Rate: ' + str('%.4f' % scaleLearningRate.get()))
    print('Learning Rate: ', scaleLearningRate.get())

def ScaleMaxEpoch_Event(event):
    global labelMaxEpoch
    labelMaxEpoch.config(text='MaxEpoch: ' + str(int(scaleMaxEpoch.get())))
    print('MaxEpoch: ', int(scaleMaxEpoch.get()))

#WINDOW
root = Tk.Tk()
root.geometry('500x500')
root.minsize(500, 500)
root.title('Practica 02')

#PLOT
f = Figure(figsize=(0,0), dpi=100)
ax = f.add_subplot(111)
f.canvas.callbacks.connect('button_press_event', Canvas_Event)
ax.grid('on')
ax.set_xlim([-1,1])
ax.set_ylim([-1,1])
canvas = FigureCanvasTkAgg(f, master=root)
canvas.get_tk_widget().place(relx=0.1, rely=0.05, relheight=0.65, relwidth=0.8)

#CONTROLS
labelLearningRate = ttk.Label(text='Learning Rate')
labelLearningRate.place(relx=0.1, rely=0.7, height=20, relwidth=0.4)
scaleLearningRate = ttk.Scale(from_=0.1, to=1, command=ScaleLearningRate_Event)
scaleLearningRate.place(relx=0.5, rely=0.7, height=20, relwidth=0.4)
labelMaxEpoch = ttk.Label(text='Epoch')
labelMaxEpoch.place(relx=0.1, rely=0.75, height=20, relwidth=0.4)
scaleMaxEpoch = ttk.Scale(from_=1, to=200, command=ScaleMaxEpoch_Event)
scaleMaxEpoch.place(relx=0.5, rely=0.75, height=20, relwidth=0.4)

buttonInit = ttk.Button(text='init', command=ButtonInit_Event)
buttonInit.place(relx=0.1, rely=0.80, relheight=0.1, relwidth=0.2)
buttonTrain = ttk.Button(text='train', command=ButtonTrain_Event)
buttonTrain.place(relx=0.31, rely=0.80, relheight=0.1, relwidth=0.2)
buttonVerify = ttk.Button(text='verify', command=ButtonVerify_Event)
buttonVerify.place(relx=0.52, rely=0.80, relheight=0.1, relwidth=0.2)

option = IntVar()
drawMode = RED_DOT

#PERCEPTRON
neuron = Perceptron(2, 0.1)

Tk.mainloop()