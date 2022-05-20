import re
from tkinter import *
import argparse
import tkinter as ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
import numpy as np
import enum
import tkinter.messagebox





class Errors(enum.Enum):
    VALID     = 0    # VALID STATE
    MIN_MAX   = 1    # X-MAX IS LESS THAN X-MIN
    INV_FUNC  = 2    # NON-VALID FUNCTION
    RNG_CAST  = 3    # NOT NUMERIC VALUES OF X-RANGE
    RNG_LIMIT = 4    # RANGE IS OVER THE LIMIT


class App(ttk.Tk):

    def __init__(self,enableTests):
        super().__init__()
        self.TEST_MODE = enableTests

        
        
        self.instructions_message = \
"""   
 Welcome To PolyPlot:
 You can now plot polynomial functions in one variable (x)  using PolyPlot
 
 Operations Allowed:
    1- Addition + 
    2- Subtraction - 
    3- Multiplication *
    4- Division /
    5- Power ^

 Minimum value of x is -10000 
 Maximum value of x is 10000
                    
"""
        
        
        self.title("PolyPlot")
        self.WIN_WIDTH    = 900
        self.WIN_HEIGHT   = 700
        self.X_MAX_RANGE  = 10000
        self.geometry(f"{self.WIN_WIDTH}x{self.WIN_HEIGHT}")
        self.resizable(0,0)
        self.buildUI()
        if self.TEST_MODE:
            self.runTests()
        


    def processInput(self):
        """Reads all the inputs and process them and check their validity"""

        #Check Min-Max Numeric Values:
        try:
            xmin = float(self.range_start.get())
            xmax = float(self.range_end.get())
        except:
            self.showError("Range Error","Range Values must be numeric")
            return Errors.RNG_CAST,"",""

        #Check Min-Max If They Exceeded The Limit
        if xmin<-1*self.X_MAX_RANGE or xmax>self.X_MAX_RANGE:
            self.showError("Range Error","Check The Range permitted in the instructions")
            return Errors.RNG_LIMIT,"",""

        #Check that Min-val is less than Max-val:
        if xmin>=xmax:
            self.showError("Range Error","Minimum value must be less than Maximum value of X")
            return Errors.MIN_MAX,"",""

        # Check Function Validity:
        expr = str(self.exp_field.get()).lower().replace('^', '**')
        try:
            if expr=="" or not bool(re.match(r"(?:[0-9-+*/^()x])+", expr)) or expr.count('x')==0:
                raise Exception()
            x = np.arange(xmin,xmax,step=0.01)
            y = eval(expr)
        except:
            self.showError("Invalid Function","Please enter a valid function. Check Instructions")
            return Errors.INV_FUNC,"",""

    
        return Errors.VALID,x,y


    def showError(self,title,mess):
        if not self.TEST_MODE:
            tkinter.messagebox.showerror(title,mess)

    def Plot(self):
        self.deleteFigureAndNavBar()
        """Plots the function within the range in spinboxes - called by plot button"""
        status,x,y = self.processInput()
        if status!=Errors.VALID:
            return
        fig = plt.Figure(figsize=(6,4), dpi=100)
        fig.patch.set_facecolor('gray')
        fig.patch.set_alpha(0.1)
        ax = fig.add_subplot()
        ax.set_facecolor('lightblue')
        ax.set_ylabel('F(x)')
        ax.set_xlabel('x')
        ax.grid(color='black',linewidth=0.1)
        ax.plot(x,y)
        self.CreateCanv(fig)

   

    def deleteFigureAndNavBar(self):
        """Delete the plotting widget - called by press clear button"""
        if hasattr(self,'nav_frame'):
            self.nav_frame.destroy()
        for slave in self.place_slaves():
            if(str(type(slave))=="<class 'tkinter.Canvas'>"):
                slave.destroy()

    

    def CreateCanv(self,fig):
        """" Create a widget for plotting on it """
        self.nav_frame = ttk.Frame(self)
        canvas = FigureCanvasTkAgg(fig,self)
        nav_bar = NavigationToolbar2Tk(canvas,self.nav_frame)  
        canv = canvas.get_tk_widget()
        nav_bar.grid(row=0,column=2,pady=5)
        canv.place(height=500,width=900,x=0,y=200) 
        self.nav_frame.pack()
        
            

   
    def buildUI(self):
        """Builds User Interface"""
        input_frame = Frame(self)

        input_frame.configure(height=500)

        exp_label = Label(input_frame,font=('arial',15,'bold'),text='F(x): ',bd=0,padx= 10,pady=10,fg='blue')
        exp_label.grid_configure(row=0,column=0,sticky='w')

        self.exp_field = Entry(input_frame, font=('arial',10),bd=5,width=self.WIN_WIDTH//8)
        self.exp_field.grid_configure(row=0,column=1,columnspan=10)

        #from label
        fromx_label = Label(input_frame,font=('arial',15,'bold'),text='From x: ',bd=0,padx=10,fg='blue')
        fromx_label.grid_configure(row=1,column=0,sticky='w')

        #start of the range of x
        start = StringVar()
        start.set('-100')
        self.range_start = Spinbox(input_frame, from_ = -self.X_MAX_RANGE, to = self.X_MAX_RANGE,bd=5,textvariable=start)
        self.range_start.grid_configure(row=1,column=1,sticky='w')

        #to label
        tox_label = Label(input_frame,font=('arial',15,'bold'),text='To x: ',bd=0,padx=10,fg='blue')
        tox_label.grid_configure(row=1,column=2,sticky='w')

        #end of the range of x
        end = StringVar()
        end.set('100')
        self.range_end = Spinbox(input_frame, from_ = -self.X_MAX_RANGE, to = self.X_MAX_RANGE,bd=5,textvariable=end)
        self.range_end.grid_configure(row=1,column=3,sticky='w')

        # plot button
        plot_button = Button(input_frame,text='Plot',width=10,bg='lightblue',command=self.Plot)
        plot_button.grid(row=1, column=4, padx=10, pady=15,sticky='e')

        plot_button = Button(input_frame, text='Clear',width=10,bg='red',command=self.deleteFigureAndNavBar)
        plot_button.grid(row=1, column=5, padx=10, pady=15,sticky='e')
        
        plot_button = Button(input_frame, text='Show Instructions',width=20,bg='lightgreen',command=self.showInstructions)
        plot_button.grid(row=2, column=0, padx=10, pady=15,sticky='w',columnspan=3)

        input_frame.pack() 

    def showInstructions(self):
        tkinter.messagebox.showinfo('Instructions',self.instructions_message)

    def runTests(self):
        self.exp_field.insert(0,"")
        status,x,y = self.processInput()
        if status==Errors.INV_FUNC:
            print("TEST 1 EMPTY_FUNCTION: PASSED")
        else:
            print("TEST 1 EMPTY_FUNCTION: FAILED")

        self.exp_field.insert(0,"mess")
        status,x,y = self.processInput()
        if status==Errors.INV_FUNC:
            print("TEST 2 INVALID_FUNC:   PASSED")
        else:
            print("TEST 2 INVALID_FUNC:   FAILED")
        self.exp_field.delete(0,10)

        self.exp_field.insert(0,"x")
        status,x,y = self.processInput()
        if status==Errors.VALID:
            print("TEST 3 VALID_FUNC:     PASSED")
        else:
            print("TEST 3 VALID_FUNC:     FAILED")

        self.range_start.delete(0,10)
        self.range_start.insert(0,"A")
        status,x,y = self.processInput()
        if status==Errors.RNG_CAST:
            print("TEST 4 INVALID_RANGE:  PASSED")
        else:
            print("TEST 4 INVALID_RANGE:  FAILED")


        self.range_start.delete(0,10)
        self.range_start.insert(0,"10")
        self.range_end.insert(0,"10000000")
        status,x,y = self.processInput()
        if status==Errors.RNG_LIMIT:
            print("TEST 5 RANGE_LIMIT:    PASSED")
        else:
            print("TEST 5 RANGE_LIMIT:    FAILED")

        self.range_start.delete(0,20)
        self.range_start.insert(0,"5")
        self.range_end.delete(0,20)
        self.range_end.insert(0,"-5")
        status,x,y = self.processInput()
        if status==Errors.MIN_MAX:
            print("TEST 6 MIN_MAX  :      PASSED")
        else:
            print("TEST 6 MIN_MAX  :      FAILED")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--test')
    args = parser.parse_args()
    if args.test == "true": 
        app = App(enableTests=True)
    else:
        app = App(enableTests=False)

    app.mainloop()



