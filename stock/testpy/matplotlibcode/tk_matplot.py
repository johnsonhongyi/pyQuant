#!/usr/bin/env python
import matplotlib
matplotlib.use('TkAgg')

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from tkFileDialog import askopenfilename
import ttk

import urllib2
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.finance import candlestick
import matplotlib.dates
matplotlib.rcParams.update({'font.size': 9})

eachStock = 'TSLA', 'AAPL'

# Frames  --------------------------------------------------------
root = Tk.Tk()
root.minsize(900,700)
main_frame = Tk.Frame(root)
main_frame.pack()

menu_frame = Tk.Frame(root)
menu_frame.pack()

tab_frame = Tk.Frame(root)
tab_frame.pack()

chart_frame = Tk.Frame(root)
chart_frame.pack()

statusbar_frame = Tk.Frame(root)
statusbar_frame.pack(side=Tk.BOTTOM, fill=Tk.BOTH, expand=True)
# -------------------------------------------------------------



# functions ---------------------------------------------
def NewFile():
    print "New File!"
def OpenFile():
    name = askopenfilename()
    print name
def About():
    print "This is a simple example of a menu"
# ----------------------------------------------------------

# Menu --------------------------------------------------------
menu = Tk.Menu(menu_frame)
root.config(menu=menu)
filemenu = Tk.Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=NewFile)
filemenu.add_command(label="Open...", command=OpenFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.destroy)

helpmenu = Tk.Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)
# ----------------------------------------------------------

# Drawing charts --------------------------------------------
def graphData(stock):
    try:
        stockFile = 'data.csv'

        date, closep, highp, lowp, openp, volume = np.loadtxt(stockFile,delimiter=',', unpack=True, converters={ 0: mdates.strpdate2num('%Y%m%d')})

        x = 0
        y = len(date)
        candleAr = []
        while x < y:
            appendLine = date[x],openp[x],closep[x],highp[x],lowp[x],volume[x]
            candleAr.append(appendLine)
            x+=1

        fig = plt.figure()
        ax1 = plt.subplot2grid((5,4), (0,0), rowspan=4, colspan=4)
        candlestick(ax1, candleAr, width=1, colorup='g', colordown='r')

        ax1.grid(True)
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.ylabel('Stock price')

        ax2 = plt.subplot2grid((5,4), (4,0), sharex=ax1, rowspan=1, colspan=4)
        ax2.bar(date, volume, color='red', align='center')
        ax2.grid(True)
        plt.ylabel('Volume')
        for label in ax2.xaxis.get_ticklabels():
            label.set_rotation(45)


        plt.xlabel('Date')
        plt.suptitle(stock+' Stock Price')
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.subplots_adjust(left=.09, bottom=.18, right=.94, top=.94, wspace=.20, hspace=0)
        plt.show()


    except Exception,e:
        print 'main loop', str(e)

graphData('TSLA')

from matplotlib.backends.backend_tkagg  import  FigureCanvasTkAgg
from matplotlib.figure                  import  Figure

class UiSuperFrame( Frame ):                    # The user interface:

    def __init__( self, master = None ):

        Frame.__init__( self, master )
        self.grid()
        self.fig        = Figure( ( 6, 6 ), dpi = 100 )
        canvas          = FigureCanvasTkAgg( self.fig, master = self )
        canvas.get_tk_widget().grid(                     row = 0, column = 0 )
        label           = Label(    self, text = 'TSLA, AAPL' )
        label.grid(                                      row = 1, column = 1 )
        #
        # .
        # ..
        # .... move the rest of GUI setup here ...

def TkDemo():                                  # Finally, set up <root> & start UI
    """ HELP:       Tk-GUI-MVC via a Class
        TESTS:      TkDemo()
        """
    root = Tk()
    root.title( 'TSLA/AAPL' )

    root.lift()

    app = UiSuperFrame( root )

    app.mainloop()
    pass