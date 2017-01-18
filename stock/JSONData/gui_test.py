from tkinter import *
from pandastable import Table, TableModel
# import sys
# sys.path.append('../')
import tdx_data_Day as tdd

code = '999999'
df = tdd.get_tdx_Exp_day_to_df(code, type='f', start=None, end=None, dl=30, newdays=None)

class TestApp(Frame):
    """Basic test frame for the table"""
    def __init__(self, parent=None):
        self.parent = parent
        Frame.__init__(self)
        self.main = self.master
        self.main.geometry('800x600+200+100')
        self.main.title('Table app')
        f = Frame(self.main)
        f.pack(fill=BOTH,expand=1)
        # df = TableModel.getSampleData()
        self.table = pt = Table(f, dataframe=df,
                                showtoolbar=True, showstatusbar=True)
        pt.show()
        return

app = TestApp()
app.mainloop()