import tkinter as tk
from tkinter import ttk
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from chatnalizer import analizeChat
from os import path



THEME_FILE = "forest-dark.tcl"
THEME_NAME = "forest-dark"


def startChatnalisis():
    filename = askopenfilename()
    message = analizeChat(filename)
    try:
        filepath = path.join(path.abspath(""),"results.txt")
        with open(filepath, "w+") as f:
            f.write(message)
            f.close
    except Exception as e:
        print(e)


root = tk.Tk()
# Import the tcl file
root.tk.call('source', f'appTheme/{THEME_FILE}')
# Set the theme with the theme_use method
ttk.Style().theme_use(THEME_NAME)


# # Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
# filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
# print(filename)

# True = English. False = Spanish
language = tk.BooleanVar()
language.set(True)
languageText = tk.StringVar(master=root,value="Change language")
chanalisisText = tk.StringVar(master=root,value="Start Chatnalisis")

def changeLanguage():
    language.set(not language.get())
    if language.get():
        languageText.set("Change language")
        chanalisisText.set("Start Chatnalisis")
    else:
        languageText.set("Cambiar lenguaje")
        chanalisisText.set("Empezar Chatnálisis")

# print("File under construction! Use Chatnalizer for a primitve chatnalisis.")
# A themed (ttk) button
button = ttk.Button(root, textvariable=chanalisisText, command=startChatnalisis,  style="Accent.TButton")
button.pack(padx=40,pady=40)

languageutton = ttk.Button(root, textvariable=languageText, command=changeLanguage)
languageutton.pack(padx=40,pady=40)
root.mainloop()