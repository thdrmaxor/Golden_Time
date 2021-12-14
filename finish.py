import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import font as tkfont
TITLE_FONT = ("Helvetica", 18, "bold")

from pulsesensor import Pulsesensor
import time
import spidev
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from tkinter import ttk


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid(row=0, column=0)
        self.title_font = tkfont.Font(family='Helvetica', size=40, weight="bold", slant="italic")
        self.button_font = tkfont.Font(family='Helvetica', size=20, weight="bold", slant="italic")
        self.frames = {}

        for x in (StartPage, PageOne, PageTwo, PageThree):
            page_name = x.__name__
            frame = x(master=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):

        for frame in self.frames.values():
            frame.grid_remove()

        frame = self.frames[page_name]
        frame.grid()


class StartPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.width = 800
        self.height = 400
        controller.geometry("800x400")
        controller.resizable(True, True)

        imopen=Image.open('1.png')
        img=ImageTk.PhotoImage(imopen)
        canvas = Canvas(self, width=self.width, height=self.height)
        canvas.create_image(self.width / 2, self.height / 2, anchor=CENTER, image=img)
        self.img = img

        canvas.pack()

        button1 = Button(self, text="Press Start",height=3, width=21,
            relief="solid", font=controller.button_font,
            command=lambda: controller.show_frame("PageOne"))
        button2 =Button(self, text="Golden Time",
            relief="solid", font=controller.title_font,
           )


        button2.place(x=400, y=100)
        button1.place(x=400, y=200)

class PageOne(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller

        frame1 = tk.Frame(self, relief="solid")
        frame1.grid(column=0, row=0)
        temp_button = tk.Button(frame1, text="Check Tempautre!", relief="solid", font=controller.button_font)
        pulse_button = tk.Button(frame1, text="Check heart rate!",width=15, font=controller.button_font, command=lambda: controller.show_frame("PageTwo"))
        graph_button = tk.Button(frame1, text="Check electrocardiogram!", font=controller.button_font, command=lambda: controller.show_frame("PageThree"))

        str = StringVar ()

        com1 = ttk.Combobox(frame1, textvariable=str, width=5)
        com1['value'] = ("Nomal","Low","High")
        com1.current(0)


        frame2 = tk.Frame(self, relief="solid")
        frame2.grid(column=1, row=0)


        blank_label = tk.Label(frame2, text= " ")
        warning1=Image.open('1.png')
        warning1_img=ImageTk.PhotoImage(warning1)
        warning1_label = tk.Label(frame2, image=warning1_img)
        blank_label.grid(column=0, row=1)
        warning1_label.grid(column=1, row=1)
        self.img = warning1_img

        temp_button.grid(column=0, row=1)
        pulse_button.grid(column=0, row=2)
        graph_button.grid(column=0, row=3)
        com1.grid(column=1, row=1)


class PageTwo(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller

        def BPM() :
            b=Tk()
            b.title("BPM")
            b.geometry("200x250")
            

            p = Pulsesensor()
            p.startAsyncBPM()
            N=0
            T=[]
            while True:
                bpm = p.BPM
                if N>9 :
                    break
                else :
                    T.append(bpm)
                    N=N+1
                time.sleep(1)
           
            b1=Label(b,text=' %s '% T)
            b1.pack()    
        
        frame1 = tk.Frame(self, relief="solid")
        frame1.grid(column=0, row=0)
        temp_button = tk.Button(frame1, text="Check Heart Rate!", relief="solid", font=controller.button_font)
        b1_label = tk.Label(frame1, text="   ", width=6)
        b2_label = tk.Label(frame1, text="   ", height=5)
        b3_label = tk.Label(frame1, text="   ", height=1)


        temp_button.grid(row=1, column=0)
        b1_label.grid(row=2, column=1)
        b2_label.grid(row=0, column=0)

        test_1 = tk.Checkbutton(frame1,text="50 ↓")
        test_1.grid()
        test_1 = tk.Checkbutton(frame1, text="50~60")
        test_1.grid()
        test_1 = tk.Checkbutton(frame1, text="60~70")
        test_1.grid()
        test_1 = tk.Checkbutton(frame1, text="70~80")
        test_1.grid()
        test_1 = tk.Checkbutton(frame1, text="80↑")
        test_1.grid()

        button1 = tk.Button(frame1, text="Search BPM for 10sec",
            command=BPM)
        button2 = tk.Button(self, text="Go to the start page",
            command=lambda: controller.show_frame("PageOne"))

        button1.grid(column=0, row=8)
        b3_label.grid(row=9, column=0)
        button2.grid(column=0, row=10)

        frame2 = tk.Frame(self, relief="solid")
        frame2.grid(column=1, row=0)
        b3_label = tk.Label(frame2, text="   ", height=1)

        b3_label.grid()

        blank_label = tk.Label(frame2, text=" ")
        warning1 = Image.open('warning1.png')
        warning1_img = ImageTk.PhotoImage(warning1)
        warning1_label = tk.Label(frame2, image=warning1_img)
        blank_label.grid(column=0, row=1)
        warning1_label.grid(column=1, row=1)
        self.img = warning1_img

class PageThree(tk.Frame):

    
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller

        def electrocardiogram():
            
            spi=spidev.SpiDev()
            spi.open(0,0)
            spi.max_speed_hz=500000
            def read_spi_adc(adcChannel):
              adcValue=0
              buff=spi.xfer2([1,(8 + adcChannel) << 4,0])
              adcValue = ((buff[1]&3)<<8)+buff[2]
              return adcValue

            x_num=100
            x=np.arange(x_num)
            y=np.empty(x_num)
            y[:]=np.NaN
            fig=plt.figure(figsize=[6.5,3])
            ax = plt.axes()
            ax = plt.axes(xlim=(0,x_num),ylim=(-500,1400))
            line,=ax.plot(x,y,lw=2)
            def init() :
             line.set_data([],[])
             return line,

            def animate(i) :
             global y
             y[i]= read_spi_adc(0)
             line.set_data(x,y)
             if i==x_num-1 :
               y[:]=np.NaN
               line.set_data(x,y)
               return line,


            ani=animation.FuncAnimation(fig,animate,init_func=init,frames=x_num,interval=1)
            plt.show()
        
        frame1 = tk.Frame(self, relief="solid")
        frame1.grid(column=0, row=0)
        topic_button = tk.Button(frame1, text="Check electrocardiogram!", relief="solid", font=controller.button_font)
        b1_label = tk.Label(frame1, text="   ", width=6)
        b2_label = tk.Label(frame1, text="   ", height=2)
        b3_label = tk.Label(frame1, text="   ", height=1)
        b4_label = tk.Label(frame1, text="   ", height=1)


        topic_button.grid(row=0, column=0)
        b1_label.grid(row=0, column=1)
        b2_label.grid(row=1, column=0)

        test_1 = tk.Checkbutton(frame1, text="Stable")
        test_1.grid(row=2, column=0)
        test_1 = tk.Checkbutton(frame1, text="Unstable")
        test_1.grid(row=3, column=0)


        b3_label.grid(row=4, column=0)


        button1 = tk.Button(frame1, text="Start",
            command=electrocardiogram)
        button2 = tk.Button(frame1, text="Go to the start page",
            command=lambda: controller.show_frame("PageOne"))
        button1.grid(column=0, row=5)
        b4_label.grid(row=6, column=0)
        button2.grid(column=0, row=7)


        frame2 = tk.Frame(self, relief="solid")
        frame2.grid(column=1, row=0)

        blank_label = tk.Label(frame2, text=" ")
        warning1 = Image.open('warning2.png')
        warning1_img = ImageTk.PhotoImage(warning1)
        warning1_label = tk.Label(frame2, image=warning1_img)
        blank_label.grid(column=0, row=1)
        warning1_label.grid(column=1, row=1)
        self.img = warning1_img


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()