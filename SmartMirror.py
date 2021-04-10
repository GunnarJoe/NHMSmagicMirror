# Smart Mirror Project
#
# Senior Capstone
# Gunnar Brown 
# Spring 2021
#
#
# This Project is supposed to develop a smart mirror for
# the computer Science department in Osborne at MNU. This mirror
# will be used as a greeting for people as they enter Osborne and can 
# be used to help people navigate the building easier.

#import all the classes we need. 
import tkinter
import tkinter.ttk
import webbrowser
import urllib
import locale
import threading
import time
import json
import traceback
import PIL
import random
import contextlib
from contextlib import contextmanager
from PIL import Image, ImageTk


LOCALE_LOCK =threading.Lock()



#standardizes the local area(sets area you are living in ex US , France, etc.)
@contextmanager
def setlocale(name):
    with LOCALE_LOCK:
        saved= locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

#class that opens a new window with a png of osbornes layout
class OsborneLayout(tkinter.Toplevel):
    def __init__(self,master=None):
        super().__init__(master=master)
        self.title("New Window")
        self.geometry("200x200")
        label=tkinter.Label(self,text="This is the new Window")
        label.pack()

#class that opens a new window with a png of professors room number
class ProfNum(tkinter.Toplevel):
    def __init__(self,master=None):
        super().__init__(master=master)
        self.title("New Window")
        self.geometry("200x200")
        label=tkinter.Label(self,text="This is the new Window")
        label.pack()


       

#class to display verses on screen
class Verse(tkinter.Frame):
    def __init__(self,parent):
        verses = ["Philippians 4:13 I Can Do All Things Through Christ Who Strengthens Me (Gunnar Brown)","Verse2","Verse3"]
     
        tkinter.Frame.__init__(self,parent,bg='black')
        self.text2 = tkinter.Label(self, compound=tkinter.CENTER, text="Professor Favorite Verses",font=('Helvetica', 30),fg='white',bg='black')
        self.text2.pack()

     
        self.text1 = tkinter.Label(self, compound = tkinter.CENTER, text= "", font=('Helvetica', 18), fg='white', bg='black')
        self.text1.pack()
        #function to choose random verse to display
        def on_after():
            randomverse=random.choice(verses)
            self.text1.configure(text=randomverse)
            self.text1.after(8000,on_after)

        #updates text every 5 seconds
        self.text1.after(8000,on_after)

        

#Buttons that will either open a new window to see osborne layout, or to open a new window
#that shows the professor room numbers
class MNUButton(tkinter.Frame):
    #Consructor
    def __init__(self,parent):
        tkinter.Frame.__init__(self,parent, bg = 'black')
        #images for buttons
        image1=Image.open('/home/pi/NHMSmagicMirror/Images/list.png')
        image2=Image.open('/home/pi/NHMSmagicMirror/Images/blueprint.png')
        test1=ImageTk.PhotoImage(image1)
        test2=ImageTk.PhotoImage(image2)
        labelimage1=tkinter.Label(image=test1)        
        labelimage2=tkinter.Label(image=test2)
        labelimage1.image=test1
        labelimage2.image=test2
        labelimage1.place(x=10,y=1000)
        labelimage2.place(x=1660,y=25)

        self.button1 = tkinter.Button(text ='Click Me For\n Professor Locations',bg='white', width=20)
        self.button1.place(x=50, y=1000)
        self.button1.bind("<Button>",lambda e: ProfNum(self))
        self.button2 = tkinter.Button(text='Click Me For \n Building Layout', bg='white',width=20)
        self.button2.place(x=1700, y=25)
        self.button2.bind("<Button>",lambda e: OsborneLayout(self))

#dispalys the NHMS banner on top of screen
class MNUimage(tkinter.Frame):
    def __init__(self,parent):
        tkinter.Frame.__init__(self,parent, bg = 'black')
        image1=Image.open('/home/pi/NHMSmagicMirror/Images/NHMSbanner.png')
        test=ImageTk.PhotoImage(image1)
        label1=tkinter.Label(image=test,bg='black')
        label1.image=test
        label1.place(x=650,y=0)
        image2=Image.open('/home/pi/NHMSmagicMirror/Images/MNU.jpg')
        test2=ImageTk.PhotoImage(image2)
        label2=tkinter.Label(image=test2,bg='black')
        label2.image=test2
        label2.place(x=1760,y=975)

#class that displays the date and time in the top left corner
class Time(tkinter.Frame):
    #constructor for the class
    def __init__(self,parent):
        tkinter.Frame.__init__(self,parent,bg ='black')
        #initialize time label
        self.time1=''
        self.timeLbl = tkinter.Label(self, font=('Helvetica', 28),fg='white', bg='black')
        self.timeLbl.pack(side=tkinter.TOP)
        #initialize day 
        self.day1 =''
        self.dayOWLb1 = tkinter.Label(self,text=self.day1, font=('Helvetica', 16),fg='white',bg='black' )
        self.dayOWLb1.pack(side=tkinter.TOP)
        #initialize date
        self.date1=''
        self.dateLbl= tkinter.Label(self, text=self.date1, font=('Helvetica', 16), fg='white', bg='black')
        self.dateLbl.pack(side=tkinter.TOP)
        self.tick()

    def tick(self):
        with setlocale(''):
            time2 = time.strftime('%I:%M %p') #hour in 12h format
            day2= time.strftime('%A')
            date2= time.strftime("%b %d, %Y")
            #if time string changes update it
            if time2 != self.time1:
                self.time1=time2
                self.timeLbl.config(text=time2)
            #if day changes it updates
            if day2!= self.day1:
                self.day1=day2
                self.dayOWLb1.config(text=day2)
            #if date changes it updates
            if date2!= self.date1:
                self.date1=date2
                self.dateLbl.config(text=date2)
            #Function calls itself every 500 ms
            self.timeLbl.after(500, self.tick)

#class that creates the welcome to osborne greeting
class Greeting(tkinter.Frame):
    #constructor for class
    def __init__(self,parent):
        tkinter.Frame.__init__(self,parent)
        self.text = tkinter.Label(self, compound = tkinter.CENTER, text= "Welcome to Osborne!", font=('Helvetica', 44), fg='white', bg='black')
        self.text.pack()
        
#creates the main homescreen window for the program.       
class FullScreen:
    #init is a constructor for the class
    def __init__(self):
        #set up for black background uses tkinter public class to create background
        #self is used to access the instance of a class 
        self.tk = tkinter.Tk()
        self.tk.configure(background = 'black')
    
        #sections the screen into a top and bottom section
        self.topFrame = tkinter.Frame(self.tk, background = 'black')
        self.bottomFrame = tkinter.Frame(self.tk, background = 'black')
        self.topFrame.pack(side = tkinter.TOP, fill=tkinter.BOTH, expand= tkinter.YES)
        self.bottomFrame.pack(side = tkinter.BOTTOM, fill=tkinter.BOTH, expand= tkinter.YES)
        self.state=False
        self.tk.attributes("-fullscreen",True)
 
        
        #Display Button
        self.button = MNUButton(self.bottomFrame)
        self.button.pack(side=tkinter.BOTTOM,anchor=tkinter.SE)

        #Display Greeting 
        self.greeting = Greeting(self.topFrame)
        self.greeting.pack(side=tkinter.BOTTOM, anchor=tkinter.S)

        
        #Display Time and Date
        self.time = Time(self.topFrame)
        self.time.pack(side=tkinter.TOP, anchor=tkinter.NW)

        #Display MNU logo
        self.image = MNUimage(self.topFrame)
        self.image.pack(side=tkinter.TOP, anchor=tkinter.NE)

       
        #Display Verses on screen
        self.verses = Verse(self.bottomFrame)
        self.verses.pack(side=tkinter.TOP)

       
        
#runs the main program and calls the fullscreen function
if __name__ == '__main__':
    window = FullScreen()
    window.tk.mainloop()         

