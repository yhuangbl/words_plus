#!/usr/bin/python
from Tkinter import *
import urllib
import json

# app functions

def get_words(query):
    # datamuse api, sp: spelling constraints, return 1000 words
    api = "https://api.datamuse.com/words?max=1000&sp="
    url = ''.join([api, query])
    # find the length of the given word
    word = list(query)
    word = [w for w in word if w.isalpha()]
    curr = ''.join(word).encode('utf-8')
    # get result in json
    result = json.loads(urllib.urlopen(url).read())
    words = set()
    # parse json
    for r in result:
        temp = r["word"].encode('utf-8')
        # ignore phrases, only words
        if not (' ' in temp):
            words.add(temp)
    
    return (words, curr)


def find_words(words, letters, curr, constraint=None):
    result = ""
    if "?" in letters:
        wildcard = True
        wildcard_used = False
    else:
        wildcard = False
        wildcard_used = False
    if constraint is not None:
        max_len = len(curr)+constraint
        words = [w for w in words if len(w) <= max_len]

    for word in words:
        letters_temp = letters+list(curr)
        flag = True
        for l in word:
            if len(letters_temp)>0:
                if l not in letters_temp:
                    if wildcard and not wildcard_used:
                        # pass this time
                        wildcard_used = True
                    else:
                        flag = False
                        break
                else:
                    letters_temp.remove(l)
            else:
                flag = False
                break
        if flag:
            result = " ".join([result, word])
    return result


# UI part

class App:
    def __init__(self,master):
        frame = Frame(master, height=100, width=100, borderwidth=15)
        frame.pack()

        # some texts
        Label(frame, text="Enter your query: ").grid(row=0, sticky=W)
        Label(frame, text="What tiles of letters do you have now?").grid(row=1, sticky=W)
        Label(frame, text="(seperate them with comma! use \"?\" for wildcard. e.g. v,f,b,l,k)").grid(row=2, sticky=W)
        self.error = Label(frame)
        self.error.grid(row=2, column=1)
        Label(frame, text="How many empty cells do you have before/after your desire position? (optional)").grid(row=3, sticky=W)
        Label(frame, text="\n The results we find for you:").grid(row=5, sticky=W)
        self.answer = Message(frame, width=500)
        self.answer.grid(row=6)

        # input fields
        self.e1 = Entry(frame)
        self.e2 = Entry(frame)
        self.e3 = Entry(frame)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=3, column=1)

        # enter button; press enter to call functions
        self.b = Button(frame, text="ENTER", command=self.search).grid(row=4, column=1, sticky=W)
        # reset button; press to clear all messages and inputs
        self.reset = Button(frame, text="RESET", command=self.reset).grid(row=4, column=0, sticky=E)

    def reset(self):
        self.e1.delete(0, 'end')
        self.e2.delete(0, 'end')
        self.e3.delete(0, 'end')
        self.error.config(text="")
        self.answer.config(text="")
    
    def check_input(self, letters):
        for l in letters:
            # if it's not a letter
            if not l.isalpha():
                return False
            # if it's multiple letters
            elif len([a for a in l]) != 1:
                return False
        return True

    def search(self):
        # get the inputs
        query = self.e1.get().lower()
        letters = self.e2.get()
        letters_list = [x.strip().lower().encode('utf-8') for x in letters.split(',')]

        if query == "" or len(letters_list) <= 0:
            self.answer.config(text="please fill in all mandatory fields", fg="red")

        if self.check_input(letters_list):
            constraint = self.e3.get()
            # search all words using api
            words, curr = get_words(query)
            # refine results
            if constraint != "":
                result = find_words(words, letters_list, curr, int(constraint))
            else:
                result = find_words(words, letters_list, curr, None)
            if result != "":
                self.answer.config(text=result)
            else:
                self.answer.config(text="oops! no word found :(", fg="red")
        else:
            self.error.config(text="invalid input!", fg="red")



root = Tk()
root.wm_title("words+")
app = App(root)            
root.mainloop()
