""" Classwise Axes. """
import sys
import random
import matplotlib
matplotlib.use('QtAgg')
import numpy as np

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class CustomCanvas(FigureCanvasQTAgg):
    def __init__(self, width=5, height=4, dpi=100):
        self.data = np.random.rand(5, 25, 25)
        self.fig0 = PltFigure(self)
        self.fig1 = ImgFigure(self)
        super().__init__(self.fig0)
        self.fig0.set_canvas(self)
        self.fig1.set_canvas(self)

    def toggle_figure(self):
        if self.figure is self.fig0:
            self.figure = self.fig1
        else:
            self.figure = self.fig0


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.canvas = CustomCanvas(width=5, height=4, dpi=100)
        self.setCentralWidget(self.canvas)

        self._y = 0
        self.update_plot()

        self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        # Drop off the first y element, append a new one.
        self._y += 1
        print(self._y, end=", ", flush=True)
        if self._y % 10 == 0:
            self.canvas.toggle_figure()
            print("", flush=True)
        self.canvas.figure.plot()

        self.canvas.draw()


class ImgFigure(Figure):
    """ A basic figure using axes.imshow """
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        super().__init__(*args, **kwargs)
        self._t = 0
        self._dim = self.parent.data.shape[0]
        self._axes = self.add_subplot(111)
        self._plot = self._axes.imshow(self.parent.data[0])

    def plot(self):
        """ Set the new data. """
        self._t = (self._t + 1) % self._dim
        self._plot.set_data(self.parent.data[self._t])


class PltFigure(Figure):
    """ A basic figure using axes.plot """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self._t = 0
        self._dim = self.parent.data.shape[0]
        self._axes = self.add_subplot(111)
        self._plot = self._axes.plot(self.parent.data[0, :, 0])[0]

    def plot(self):
        """ Set the new data. """
        self._t = (self._t + 1) % self._dim
        self._plot.set_ydata(self.parent.data[self._t, :, 0])


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec()
