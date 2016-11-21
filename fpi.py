import traceback
import matplotlib.pyplot as plt
from numpy import linspace
from math import *
from tkinter import *


def fixedpoint(g, x0, n, eps=1e-4):
    xs = [0] * (n + 1)
    xs[0] = x0
    kk = n
    COL_FMT = "%2s    %16.9s   %-16.9s   %-16.9s"
    ROW_FMT = "%2d    %16.9g   %-16.9g   %-16.9g"
    print(COL_FMT % ('#', 'g(x[k])', 'x[k+1]', 'error'))
    print('-' * 60)

    # start of iteration
    for k in range(1, n + 1):
        try:
            xs[k] = g(xs[k - 1])
        except Exception as e:
            print(e)
            kk = k-1
            break
        error = abs(xs[k]-xs[k-1])
        print(ROW_FMT % (k, xs[k-1], xs[k], error))
        # stop early if converged or diverged
        if isnan(xs[k]) or isinf(xs[k]):
            kk = k-1
            break
        if error < eps:
            kk = k
            break
    return xs[:kk+1]

def plot_fixedpoint(g, x0, n, show_arrow=True):
    xs = fixedpoint(g, x0, n)
    n = len(xs)-1

    if n < 1:
        return

    xmin, xmax = min(xs), max(xs)
    dist = xmax - xmin
    xmax += dist * 0.1
    xmin -= dist * 0.1
    y0 = max(xmin, min(0, xmax))

    # plot points
    plt.scatter(xs[0:n], xs[1:], s=5)
    plt.scatter(xs[1:], xs[1:], s=5)

    # plot cobweb
    for k in range(1, n):
        plt.annotate('$x_{%d}$'%(k), (xs[k], xs[k+1]), color='b')
    if show_arrow:
        arrow_config = {
            "color": "b",
            "lw": 0.4, 
            "length_includes_head": True,
        }
        plt.arrow(xs[0], y0, 0, xs[1]-y0, **arrow_config)
        for k in range(1, n):
            plt.arrow(xs[k-1], xs[k], xs[k]-xs[k-1], 0, **arrow_config)
            plt.arrow(xs[k], xs[k], 0, xs[k+1]-xs[k], **arrow_config)
    else:
        plt.plot((xs[0], xs[0]), (y0, xs[1]), 'b--')
        for k in range(1, n):
            plt.plot((xs[k-1], xs[k]), (xs[k], xs[k]), 'b--')
            plt.plot((xs[k], xs[k]), (xs[k], xs[k+1]), 'b--')

    plt.annotate('$x_0$', (xs[0], y0), color='b')

    # plot function
    X = list(linspace(xmin, xmax, 100))
    # X = list(linspace(0, -10, 10))
    G = [None for x in X]
    for i in range(len(X)):
        try:
            G[i] = g(X[i])
        except:
            pass
    plt.plot(X, X, 'k', linewidth=1)
    plt.plot(X, G, 'g', linewidth=2)

    plt.xlabel("$x$")
    plt.ylabel("$y$")

def grid(widget, padx=3, pady=3, sticky=W+E+N+S, **kwargs):
    widget.grid(
        padx=padx, pady=pady, 
        sticky=sticky,
        **kwargs)
    return widget


class App(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        Grid.columnconfigure(self, 0, weight=0, minsize=50)
        Grid.columnconfigure(self, 1, weight=1, minsize=100)
        grid(self)
        self.create_widgets()
        self.figure_count = 0

    def create_widgets(self):
        self.txt_func = StringVar()
        grid(
            Label(self, text="g(x)"),
            row=0, column=0)
        grid(
            Entry(self, textvariable=self.txt_func),
            row=0, column=1)

        self.txt_x0 = StringVar()
        grid(
            Label(self, text="x0"),
            row=1, column=0)
        grid(
            Entry(self, textvariable=self.txt_x0),
            row=1, column=1)

        self.txt_n = StringVar()
        grid(
            Label(self, text="n"),
            row=2, column=0)
        grid(
            Entry(self, textvariable=self.txt_n),
            row=2, column=1)

        self.int_arrow = IntVar()
        grid(
            Label(self, text="Options"),
            row=3, column=0)
        grid(
            Checkbutton(self, text="show arrows", variable=self.int_arrow),
            row=3, column=1, sticky=W)

        self.btn_plot = grid(Button(self, text="Plot", command=self.plot),
            row=100, column=0, columnspan=2)

        self.txt_func.set("1.5-0.4*x**2")
        self.txt_x0.set("0.2")
        self.txt_n.set("20")

        # self.txt_func.set("3.86*x*(1-x)")
        # self.txt_x0.set("0.3")
        # self.txt_n.set("60")

    def plot(self):
        plt.figure("Cobweb Plot")
        plt.clf()
        try:
            x0 = float(self.txt_x0.get())
            n = int(self.txt_n.get())
            func_text = self.txt_func.get()
            func = eval("lambda x:" + func_text)
            func(x0)

            print('=' * 80)
            summary = "g(x)=%s @ x0=%g, n=%d" % (func_text, x0, n)
            print(summary)
            plot_fixedpoint(func, x0, n, 
                show_arrow=bool(self.int_arrow.get()))
        except:
            print(traceback.format_exc())
            plt.close('all')
            return
        plt.show()

if __name__ == '__main__':
    root = Tk()
    root.title("Fixed Point Iteration Plotter")
    root.minsize(width=350, height=100)
    Grid.columnconfigure(root, 0, weight=1)
    root.resizable(1,0)
    app = App(master=root)
    app.mainloop()
