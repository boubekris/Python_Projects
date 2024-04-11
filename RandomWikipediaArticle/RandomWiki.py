import requests
import tkinter
from tkinter import *
import tkinter
from functools import partial
from bs4 import BeautifulSoup

master = tkinter.Tk()
titlePage = Label(master, text='')
data = ''
S = requests.Session()
page = Text(master, height=13, width=50, font=(12))
sbV = Scrollbar(master, orient=VERTICAL)
sbH = Scrollbar(master, orient=HORIZONTAL)
title= ''
placeHolder = Text(master, height=13, width=50, background='light grey', font=(12))
placeHolder.config(state=DISABLED)


def showArticle():
    placeHolder.grid_forget()
    url = 'https://en.wikipedia.org/w/api.php'
    params = {
            'action': 'parse',
            'page': title,
            'format': 'json',
            'prop':'text',
            'redirects':''
        }
    response = S.get(url, params=params)
    dataPage = response.json()  
    article = dataPage['parse']['text']['*']


    printabletext = BeautifulSoup(article, features="lxml").get_text()
    
    sbV.grid(row=1, column=2, sticky=NS)
    sbH.grid(row=2, sticky=EW)
    
    page.config(yscrollcommand=sbV.set)
    page.config(xscrollcommand=sbH.set)
    
    sbV.config(command=page.yview)
    sbH.config(command=page.xview)
    
    page.grid(columnspan=2, row=1, column=0)
    page.config(state=NORMAL)
    page.delete("0.0", "end")
    page.insert(tkinter.END, printabletext)
    page.config(state=DISABLED)
    

def nextTitle():
    global title
    placeHolder.grid(columnspan=2, row=1, column=0)
    page.grid_forget()
    sbH.grid_forget()
    sbV.grid_forget()
    title = getRandomTitle()
    titlePage.config(text=title)
    


def getRandomTitle():
    url = 'https://en.wikipedia.org/wiki/Special:Random'
    response = S.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.find(class_="firstHeading").text


if __name__ == "__main__":
    params = {
            'action': 'query',
            'format': 'json',
            'list':'random',
            'rnlimit':'50',
        }
    
    
    title = getRandomTitle()   
    
    # Initialize UI    
    master.geometry('600x350')
    master.title('Random Article')
    
    #Add widgets
    titlePage.config(text= title)
    titlePage.grid(row=0, sticky=SW)
    
    placeHolder.grid(columnspan=2, row=1, column=0)

    nextTitleCallable = partial(nextTitle)
    showArticleCallable = partial(showArticle)
    
    #Add Submit button
    nextButton = Button(master, text="Next", command=nextTitleCallable)
    nextButton.grid(row=3, sticky=SW)

    submitButton = Button(master, text="Show Article", command=showArticleCallable)
    submitButton.grid(row=4, sticky=SW)
    
    master.mainloop()
