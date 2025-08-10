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
        message = analizeChat(filename.get(), excludeAI=aistate.get())
        filepath = path.join(path.abspath(""),f"results_{path.basename(filename.get())}")
        with open(filepath, "w+") as f:
            f.write(message)
            f.close
        if language.get():
            warningText.set(f"Chatnalisis completed!\nRead it at {filepath}")
        else:
            warningText.set(f"Chatnálisis completado!\nSe encuentra en {filepath}")
    except Exception as e:
        warningText.set(e)


root = tk.Tk()
root.title("Chatnalizer (PROTOTYPE) version 0.2")
root.option_add("*tearOff", False)

root.columnconfigure(index=0, weight=1)
root.columnconfigure(index=1, weight=1)
root.columnconfigure(index=2, weight=1)
root.rowconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=1)
root.rowconfigure(index=2, weight=1)
root.rowconfigure(index=3, weight=1)
root.rowconfigure(index=4, weight=1)

# Import the tcl file
try:
    root.tk.call('source', f'appTheme/{THEME_FILE}')
    # Set the theme with the theme_use method
    ttk.Style().theme_use(THEME_NAME)

    # True = English. False = Spanish
    language = tk.BooleanVar(value=True)
    aistate = tk.BooleanVar()

    languageText = tk.StringVar(master=root,value="Change language")
    aitext = tk.StringVar(master=root, value="Exclude Meta AI")
    getFileText = tk.StringVar(master=root, value="Get file")
    filenameDisplay = tk.StringVar(master=root, value="No file selected.")
    chanalisisText = tk.StringVar(master=root,value="Start Chatnalisis")
    warningText = tk.StringVar(master=root, value="")

    def changeLanguage():
        language.set(not language.get())
        if language.get():
            languageText.set("Change language")
            chanalisisText.set("Start Chatnalisis")
            aitext.set("Exclude Meta AI")
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
            aitext.set("Excluir a Meta AI")
            warningText.set("Todavía no hay soporte de Chatnálisis en español.\nEl resultado estará en inglés.")
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
    
    button1.grid(row=0,column=1,padx=(0,0), pady=(30,5))
    fileText.grid(row=1,column=1,padx=(0,0),pady=(0,30))
    button2.grid(row=2,column=1,padx=(140,140),pady=(10,5))
    warningLabel = ttk.Label(root, textvariable=warningText, justify="center")
    warningLabel.grid(row=3,column=1,padx=(30,30),pady=(0,40))

    aibutton = ttk.Checkbutton(root,textvariable=aitext,variable=aistate)
    aibutton.grid(row=4,column=0,padx=(15,30),pady=(20,15))

    languagebutton = ttk.Button(root, textvariable=languageText,command=changeLanguage)
    languagebutton.grid(row=4,column=2,padx=(0,15),pady=(00,00))
    
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())

except Exception as e: # Make sure the application actualy shows something!
    errorText = ttk.Label(root, text=e)
    errorText.pack(padx=20,pady=20)
root.mainloop()