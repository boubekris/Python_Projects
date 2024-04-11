from gtts import gTTS
from playsound import playsound
from tkinter import *
import tkinter
from functools import partial


#Text to Speech method
def tts(text):
    # The text that you want to convert to audio
    mytext = text.get()
    language = 'fr'
    
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("tts.mp3")
    
    playsound('tts.mp3')


if __name__ == "__main__":
    # Initialize UI
    master = tkinter.Tk()
    master.geometry('400x150')
    master.title('Text To Speech')

    #Add widgets
    Label(master, text='Text to be converted').grid(row=0)
    text = Entry(master)
    text.grid(row=0, column=1)

    #Define Text To speech call
    printDetailsCallable = partial(tts, text)
    
    #Add Submit button
    submitButton = Button(master, text="Submit", command=printDetailsCallable)
    submitButton .grid(row=1, column=1) 
    
    master.mainloop()