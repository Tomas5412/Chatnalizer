import tkinter as tk
from tkinter import ttk, font
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from ChatFunctions.chatnalizer import analizeChat
from os import path



THEME_FILE = "forest-dark.tcl"
THEME_NAME = "forest-dark"

def getFile():
    filename.set(askopenfilename())
    if filename.get():
        if language.get():
            filenameDisplay.set("File: " + filename.get())
        else:
            filenameDisplay.set("Archivo: " + filename.get())
    else:
        if language.get():
            filenameDisplay.set("No file selected.")
        else:
            filenameDisplay.set("No se eligió un archivo.")


def startChatnalisis():
    try:
        message = analizeChat(filename.get())
        filepath = path.join(path.abspath(""),f"results_{path.basename(filename.get())}")
        with open(filepath, "w+") as f:
            f.write(message)
            f.close
        if language.get():
            warningText.set(f"Chatnalisis completed! Read it at {filepath}")
        else:
            warningText.set(f"Chatnálisis completado! Se encuentra en {filepath}")
    except Exception as e:
        warningText.set(e)


root = tk.Tk()
root.title("Chatnalizer (PROTOTYPE) version 0.1")
root.option_add("*tearOff", False)

root.columnconfigure(index=0, weight=1)
root.columnconfigure(index=1, weight=1)
root.columnconfigure(index=2, weight=1)
root.rowconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=1)
root.rowconfigure(index=2, weight=1)

# Import the tcl file
try:
    root.tk.call('source', f'appTheme/{THEME_FILE}')
    # Set the theme with the theme_use method
    ttk.Style().theme_use(THEME_NAME)

    # True = English. False = Spanish
    language = tk.BooleanVar()
    language.set(True)

    languageText = tk.StringVar(master=root,value="Change language")
    getFileText = tk.StringVar(master=root, value="Get file")
    filenameDisplay = tk.StringVar(master=root, value="No file selected.")
    chanalisisText = tk.StringVar(master=root,value="Start Chatnalisis")
    warningText = tk.StringVar(master=root, value="")

    def changeLanguage():
        language.set(not language.get())
        if language.get():
            languageText.set("Change language")
            chanalisisText.set("Start Chatnalisis")
            getFileText.set("Get file")
            warningText.set("")
            if filenameDisplay.get() == "No se eligió un archivo.":
                filenameDisplay.set("No file selected.")
            else:
                filenameDisplay.set("File: " + filename.get())
        else:
            languageText.set("Cambiar lenguaje")
            chanalisisText.set("Empezar Chatnálisis")
            getFileText.set("Obtener archivo")
            warningText.set("Todavía no hay soporte de Chatnálisis en español: el resultado estará en inglés.")
            if filenameDisplay.get() == "No file selected.": 
                filenameDisplay.set("No se eligió un archivo.")
            else:
                filenameDisplay.set("Archivo: " + filename.get())


    # Buttons
    filename = tk.StringVar()
    filename.set("")
    
    button1 = ttk.Button(root, textvariable=getFileText, command=getFile)
    fileText = ttk.Label(root,textvariable=filenameDisplay)
    button2 = ttk.Button(root, textvariable=chanalisisText, command=startChatnalisis,  style="Accent.TButton")
    
    button1.pack(padx=200,pady=(40,1))
    fileText.pack(padx=1,pady=1)
    button2.pack(padx=200,pady=(40,1))
    warningLabel = ttk.Label(root, textvariable=warningText, justify="center")
    warningLabel.pack(padx=1,pady=(10,40))

    languagebutton = ttk.Button(root, textvariable=languageText,command=changeLanguage)
    languagebutton.pack(padx=(370,50),pady=(10,15))

except Exception as e: # Make sure the application actualy shows something!
    errorText = ttk.Label(root, text=e)
    errorText.pack(padx=20,pady=20)
root.mainloop()