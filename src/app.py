from misc.keywords import APP_KEYWORDS,LANGUAGES
import tkinter as tk
from tkinter import ttk
# from tkinter import Tk
from tkinter.filedialog import askopenfilename
from ChatFunctions.chatnalizer import analizeChat
from os import path



THEME_FILE = "forest-dark.tcl"
THEME_NAME = "forest-dark"

def getFile():
    filename.set(askopenfilename())
    if filename.get():
        filenameDisplay.set(APP_KEYWORDS[LANGUAGES[languageV]]["file_display"] + filename.get())
    else:
        filenameDisplay.set(APP_KEYWORDS[LANGUAGES[languageV]]["unselected_file"])


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

    # 0 = English, 1 = Spanish
    language = tk.IntVar(value=0)
    languageV = language.get()
    aistate = tk.BooleanVar()
    languageText = tk.StringVar(master=root,value=APP_KEYWORDS[LANGUAGES[languageV]]["change_language"])
    aitext = tk.StringVar(master=root, value=APP_KEYWORDS[LANGUAGES[languageV]]["ai_exclusion"])
    getFileText = tk.StringVar(master=root, value=APP_KEYWORDS[LANGUAGES[languageV]]["get_file_button"])
    filenameDisplay = tk.StringVar(master=root, value=APP_KEYWORDS[LANGUAGES[languageV]]["unselected_file"])
    chanalisisText = tk.StringVar(master=root,value=APP_KEYWORDS[LANGUAGES[languageV]]["analysis_button"])
    warningText = tk.StringVar(master=root, value=APP_KEYWORDS[LANGUAGES[languageV]]["unsopported_language_warning"])
    filename = tk.StringVar()
    filename.set("")


    def changeLanguage():
        language.set((language.get() + 1) % len(LANGUAGES))
        languageV = language.get()
        languageText.set(APP_KEYWORDS[LANGUAGES[languageV]]["change_language"])
        aitext.set(APP_KEYWORDS[LANGUAGES[languageV]]["ai_exclusion"])
        getFileText.set(APP_KEYWORDS[LANGUAGES[languageV]]["get_file_button"])
        chanalisisText.set(APP_KEYWORDS[LANGUAGES[languageV]]["analysis_button"])
        warningText.set(APP_KEYWORDS[LANGUAGES[languageV]]["unsopported_language_warning"])
        if not filename.get():
            filenameDisplay.set(APP_KEYWORDS[LANGUAGES[languageV]]["unselected_file"])
        else:
            filenameDisplay.set(APP_KEYWORDS[LANGUAGES[languageV]]["file_display"] + filename.get())





    # Buttons
    
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