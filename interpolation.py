import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as fg

import tkinter as tk

class MainApplication(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("645x560")

        container = tk.Frame(self, borderwidth=1, relief="sunken")
        container.pack(fill="both")

        self.title("Interpolasi Application")

        menu = tk.Menu(self)
        itemMenu = tk.Menu(menu)
        itemMenu.add_command(label="Newton", command=lambda : self.showFrame(FrameInterpolasiNewton))# add command do something
        itemMenu.add_command(label="Lagrage", command=lambda : self.showFrame(FrameInterpolasiLagrage))# add command do something
        menu.add_cascade(label="Pilihan", menu=itemMenu)
        self.config(menu=menu)

        # add frame
        self.frames = {}
        for F in (FrameInterpolasiNewton, FrameInterpolasiLagrage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(FrameInterpolasiNewton)

    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class FrameInterpolasiNewton(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        tittle = tk.Label(self, text="Interpolasi Newton", font=("Verdana", 12))
        tittle.grid(row=0, column=0, columnspan=3)

        labelPoint = tk.Label(self, text="Input x y ")
        entryPoint = tk.Entry(self)

        labelGrad = tk.Label(self, text="Input Xmin Xmax Ymin Ymax")
        entryGrad = tk.Entry(self)

        btnDrawInterpolasi = tk.Button(self, text="Draw Interpolasi", command= lambda: self.getInput(entryPoint, entryGrad))

        labelPoint.grid(row=1, column=0, sticky="w")
        entryPoint.grid(row=1, column=1, sticky="nsew")
        labelGrad.grid(row=2, column=0, sticky="w")
        entryGrad.grid(row=2, column=1, sticky="nsew")
        btnDrawInterpolasi.grid(row=1, column=2, rowspan=2, sticky="nsew")

    def getInput(self, entryPoint, entryGrad):
        # dapatkan Input user
        ttk = entryPoint.get().split()
        x = []
        y = []
        for i in range(len(ttk)):
            if i == 0 or i%2 == 0:
                x.append(float(ttk[i]))
            else:
                y.append(float(ttk[i]))
        points = (x, y)

        ttk = entryGrad.get().split()
        axisX = [float(ttk[0]), float(ttk[1])]
        axisY = [float(ttk[2]), float(ttk[3])]

        # Panggil kelas Interpolasi dan methode Polynomial Newton
        fungsi = Interpolasi().getRestultPolynomialNewton(points)
        self.showCanvas(fungsi, axisX, axisY)

    def showCanvas(self, fungsi, axisX, axisY):
        # titik plot fungsi
        x = np.linspace(axisX[0], axisX[1], num=5000) # ganti dengan x min dan x max
        y = np.polyval(fungsi, x)

        figure = plt.figure()
        ploting = figure.add_subplot()
        ploting.plot(x, y)
        ploting.set_title(np.poly1d(fungsi))
        ploting.set_ylabel("Y")
        ploting.set_xlabel("X")
        ploting.set_ylim(axisY)

        canvas = fg.FigureCanvasTkAgg(figure, self)
        canvas.get_tk_widget().grid(row=3, column=0, columnspan=3, sticky="nsew")

class FrameInterpolasiLagrage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        tittle = tk.Label(self, text="Interpolasi Lagrange", font=("Verdana", 12))
        tittle.grid(row=0, column=0, columnspan=3)

        labelPoint = tk.Label(self, text="Input x y ")
        entryPoint = tk.Entry(self)

        labelGrad = tk.Label(self, text="Input Xmin Xmax Ymin Ymax")
        entryGrad = tk.Entry(self)

        btnDrawInterpolasi = tk.Button(self, text="Draw Interpolasi", command= lambda: self.getInput(entryPoint, entryGrad))

        labelPoint.grid(row=1, column=0, sticky="w")
        entryPoint.grid(row=1, column=1, sticky="nsew")
        labelGrad.grid(row=2, column=0, sticky="w")
        entryGrad.grid(row=2, column=1, sticky="nsew")
        btnDrawInterpolasi.grid(row=1, column=2, rowspan=2, sticky="nsew")

    def getInput(self, entryPoint, entryGrad):
        # dapatkan Input dari user
        ttk = entryPoint.get().split()
        x = []
        y = []
        for i in range(len(ttk)):
            if i == 0 or i%2 == 0:
                x.append(float(ttk[i]))
            else:
                y.append(float(ttk[i]))
        points = (x, y)

        ttk = entryGrad.get().split()
        axisX = [float(ttk[0]), float(ttk[1])]
        axisY = [float(ttk[2]), float(ttk[3])]
        
        # panggil kelas interpolasi dan methode lagrange
        fungsi = Interpolasi().getRestultPolynomialLagrage(points)
        self.showCanvas(fungsi, axisX, axisY)

    def showCanvas(self, fungsi, axisX, axisY):
        # titik plot fungsi
        x = np.linspace(axisX[0], axisX[1], num=5000) # ganti dengan x min dan x max
        y = np.polyval(fungsi, x)

        figure = plt.figure()
        ploting = figure.add_subplot()
        ploting.plot(x, y)
        ploting.set_title(np.poly1d(fungsi))
        ploting.set_ylabel("Y")
        ploting.set_xlabel("X")
        ploting.set_ylim(axisY)

        canvas = fg.FigureCanvasTkAgg(figure, self)
        canvas.get_tk_widget().grid(row=3, column=0, columnspan=3, sticky="nsew")

class Interpolasi():

    def getRestultPolynomialNewton(self, points):
        """ Keluaran berupa hasil polynomial Newton """
        x, y = points
        coeff_vector = self.getNDDCoeffs(points)
        # create as many polynomials as size of coeff_vector
        final_pol = np.polynomial.Polynomial([0.]) # hasil dari polynomial
        n = coeff_vector.shape[0]
        for i in range(n):
            p = np.polynomial.Polynomial([1.]) # lambang x
            for j in range(i):
                p_temp = np.polynomial.Polynomial([-x[j], 1.]) # operasi x - x[j]
                p = np.polymul(p, p_temp)
            p *= coeff_vector[i]
            final_pol = np.polyadd(final_pol, p)
        p = np.flip(final_pol[0].coef, axis=0)
        return p

    def getNDDCoeffs(self, points):
        """ Creates NDD pyramid and extracts coeffs """
        x, y = points
        n = np.shape(y)[0]
        pyramid = np.zeros([n, n])
        pyramid[::, 0] = y
        for j in range(1, n):
            for i in range(n-j):
                pyramid[i][j] = (pyramid[i+1][j-1] - pyramid[i][j-1]) / (x[i+j] - x[i])
        print(pyramid)
        return pyramid[0]

    def getRestultPolynomialLagrage(self, points):
        """ Keluaran berupa hasil perkalian polynomial Lagrange """
        x, y = points
        final_pol = np.polynomial.Polynomial([0.])
        n = len(x) # banyak point
        for i in range(n):
            p = np.polynomial.Polynomial([1.]) # pembilang
            q = 1 # penyebut
            for j in range(n):
                if i == j:
                    continue
                p_temp = np.polynomial.Polynomial([-x[j], 1.]) # x - x[j]
                p = np.polymul(p, p_temp)
                q_temp = x[i] - x[j] # x[i] - x[j]
                q *= q_temp
            p *= y[i]/q
            final_pol = np.polyadd(final_pol, p)
        p = np.flip(final_pol[0].coef, axis=0)
        return p


app = MainApplication()
app.mainloop()