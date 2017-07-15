#!/usr/bin/python
from Tkinter import *
import urllib
import json

# app functions

def get_words(query):
    # datamuse api, sp: spelling constraints
    api = "https://api.datamuse.com/words?sp="
    url = ''.join([api, query])
    # find the length of the given word
    word = list(query)
    word = [w for w in word if w.isalpha()]
    curr = ''.join(word)
    # get result in json
    result = json.loads(urllib.urlopen(url).read())

    words = set()
    # parse json
    for r in result:
        words.add(r["word"])
    return (words, curr)


def find_words(words, letters, curr, constraint=None):
    result = ""
    if constraint is not None:
        max_len = len(curr)+constraint
        words = [w for w in words if len(w) <= max_len]
    letters.extend(list(curr))
    for word in words:
        flag = True
        for l in word:
            if l not in letters:
                flag = False
        if flag:
            result = " ".join([result, word])
    return result


# words = get_words("*case")
# find_words(words[0], ['v', 'f', 'b', 'l', 'k'], words[1], 5)

def callback():
    print "click!"

# UI part

class App:
    def __init__(self,master):
        frame = Frame(master, height=100, width=100, borderwidth=15)
        frame.pack()

        # some texts
        Label(frame, text="Enter your query: ").grid(row=0, sticky=W)
        Label(frame, text="What tiles of letters do you have now?").grid(row=1, sticky=W)
        Label(frame, text="(seperate them with comma! e.g. v,f,b,l,k)").grid(row=2, sticky=W)
        Label(frame, text="How many empty cells do you have before/after your desire position?").grid(row=3, sticky=W)
        Label(frame, text="\n The results we find for you:").grid(row=5, sticky=W)
        self.answer = Label(frame)
        self.answer.grid(row=6)

        # input fields
        self.e1 = Entry(frame)
        self.e2 = Entry(frame)
        self.e3 = Entry(frame)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=3, column=1)

        # enter button; press enter to call functions
        self.b = Button(frame, text="ENTER", command=self.search).grid(row=4)

    def search(self):
        # get the inputs
        query = self.e1.get()
        letters = self.e2.get()
        letters_list = [x.strip() for x in letters.split(',')]
        constraint = self.e3.get()
        # search all words using api
        words, curr = get_words(query)
        # refine results
        result = find_words(words, letters_list, curr, int(constraint))
        if result != "":
            self.answer.config(text=result)
        else:
            self.answer.config(text="oops! no word found :(", fg="red")



root = Tk()
root.wm_title("words+")
app = App(root)            
root.mainloop()
