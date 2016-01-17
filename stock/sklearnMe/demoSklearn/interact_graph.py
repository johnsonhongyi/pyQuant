from Tkinter import *
from random import *

import matplotlib

matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

numberOfFrames = eval(str(input('Number of frames to be crated: ')))

x = []
y = []


class app(Tk):
    def __init__(self):

        Tk.__init__(self)
        self.geometry('800x600')
        self.frames = []
        self.currentPage = 0
        self.figs = []
        self.axeslist = []
        self.canvaslist = []

        def nextpage():

            try:
                frame = self.frames[self.currentPage + 1]
                frame.tkraise()
                self.currentPage += 1
            except:
                pass

        def backpage():

            if self.currentPage == 0:
                pass
            else:

                frame = self.frames[self.currentPage - 1]
                frame.tkraise()
                self.currentPage -= 1

        def DrawOn():

            def onclick(event):
                self.axeslist[self.currentPage].hlines(event.ydata, event.xdata - 0.1, event.xdata + 0.1,
                                                       colors='r', linestyle='solid')
                self.canvaslist[self.currentPage].show()
                print(event.xdata, event.ydata)

            for i in self.figs:
                i.canvas.mpl_connect('button_press_event', onclick)

        for i in range(int(numberOfFrames)):
            frame = Frame(self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames.append(frame)
            fig = plt.figure()
            self.figs.append(fig)
            ax = self.figs[i].add_subplot(111)
            self.axeslist.append(ax)

            for j in range(2):
                x.append(randint(1, 10))
                y.append(randint(1, 10))

            plt.plot(x, y)
            canvas1 = FigureCanvasTkAgg(self.figs[i], self.frames[i])
            self.canvaslist.append(canvas1)
            self.canvaslist[i].get_tk_widget().pack(fill='both', expand=True)
            toolbar = NavigationToolbar2TkAgg(self.canvaslist[i], self.frames[i])
            toolbar.update()
            self.canvaslist[i]._tkcanvas.pack(fill='both', expand=True)
            label = Label(self.frames[i], text='Page %d' % (i + 1))
            label.pack()
            Next = Button(self.frames[i], text='Next', command=nextpage)
            Next.pack(side=LEFT)
            Back = Button(self.frames[i], text='Back', command=backpage)
            Back.pack(side=LEFT)
            Draw = Button(self.frames[i], text='Draw', command=DrawOn)
            Draw.pack(side=LEFT)

        self.frames[0].tkraise()


run = app()
run.mainloop()
