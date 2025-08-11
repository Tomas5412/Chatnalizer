from misc.keywords import APP_KEYWORDS,LANGUAGES
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from ChatFunctions.chatnalizer import analizeChat
from misc.classes import DATE_TYPE
from os import path
import datetime as dt
import tkcalendar as tkc



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
        try:
            dStart = dateStart.get_date()
            dStart = dt.datetime(day=dStart.day, month=dStart.month, year=dStart.year, hour=0, minute=0)
        except Exception as e:
            print(e)
            dStart = dt.datetime(2009,2,1)
        try:
            dEnd = dateEnd.get_date()
            dEnd = dt.datetime(day=dEnd.day, month=dEnd.month, year=dEnd.year, hour=23, minute=59)
        except Exception as e:
            print(e)
            dEnd = dt.datetime.now()

        if dEnd < dStart: raise ValueError("End date occurs sooner than start, sillyhead!")

        message = analizeChat(filename.get(), excludeAI=aistate.get(), dateStart=dStart, dateEnd=dEnd)
        filepath = path.join(path.abspath(""),f"results_{path.basename(filename.get())}")
        with open(filepath, "w+") as f:
            f.write(message)
            f.close
        warningText.set(APP_KEYWORDS[LANGUAGES[language.get()]]["analysis_complete"] + filepath)
    except Exception as e:
        print(e)
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
root.rowconfigure(index=4, weight=1)

# Import the tcl file
try:
    root.tk.call('source', f'appTheme/{THEME_FILE}')
    # Set the theme with the theme_use method
    ttk.Style().theme_use(THEME_NAME)

    language = tk.IntVar(value=0)
    languageV = language.get()
    aistate = tk.BooleanVar(master=root)
    dStartState = tk.BooleanVar(master=root, value=False)
    dEndState = tk.BooleanVar(master=root, value= False)
    dStartText = tk.StringVar(master=root, value=APP_KEYWORDS[LANGUAGES[languageV]]["date_start"])
    dateFormatText = tk.StringVar(master=root, value= "Date Format")
    dEndText = tk.StringVar(master=root, value=APP_KEYWORDS[LANGUAGES[languageV]]["date_end"])
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
        dStartText.set(APP_KEYWORDS[LANGUAGES[languageV]]["date_start"])
        dEndText.set(APP_KEYWORDS[LANGUAGES[languageV]]["date_end"])
        if not filename.get():
            filenameDisplay.set(APP_KEYWORDS[LANGUAGES[languageV]]["unselected_file"])
        else:
            filenameDisplay.set(APP_KEYWORDS[LANGUAGES[languageV]]["file_display"] + filename.get())



    # Buttons
    
    button1 = ttk.Button(root, textvariable=getFileText, command=getFile)
    fileText = ttk.Label(root,textvariable=filenameDisplay)
    button2 = ttk.Button(root, textvariable=chanalisisText, command=startChatnalisis,  style="Accent.TButton")
    warningLabel = ttk.Label(root, textvariable=warningText, justify="center")
    aibutton = ttk.Checkbutton(root,textvariable=aitext,variable=aistate)
    languagebutton = ttk.Button(root, textvariable=languageText,command=changeLanguage)

    wordListSeparator = ttk.LabelFrame(root, text="Word List")

    wordListSeparator.grid(row=0, column= 2, rowspan=5)
    
    wordListAdder = ttk.Entry(wordListSeparator)
    wordListAdder.grid(row=0,column=0, padx=10, pady=10)

    def enableStart():
        # dStartState.set(not dStartState.get())
        if dStartState.get():
            dateStart.config(state="normal")
            dateStart.set_date(dt.date.today())
        else:
            dateStart.config(state="disabled")
        return
    
    def enableEnd():
        # dEndState.set(not dEndState.get())
        if dEndState.get():
            dateEnd.config(state="normal")
            dateEnd.set_date(dt.date.today())
        else:
            dateEnd.config(state="disabled")
        return
    
    dateStart = tkc.DateEntry(root, mindate=dt.date(2009,2,1), maxdate=dt.datetime.now(), showothermonthdays=False, date_pattern="dd/mm/yy", state="disabled")
    dateEnd = tkc.DateEntry(root, mindate=dt.date(2009,2,1), maxdate=dt.datetime.now(), showothermonthdays=False, date_pattern="dd/mm/yy", state="disabled")
    dStartButton = ttk.Checkbutton(root, textvariable=dStartText, variable=dStartState, command=enableStart)
    dEndButton = ttk.Checkbutton(root, textvariable=dEndText, command=enableEnd, variable= dEndState)

    dateFormat = ttk.Combobox(root,textvariable=dateFormatText, state="readonly",values=[fmt.value for fmt in DATE_TYPE])
    dateFormat.grid(row=4,column=0, padx=(20,0),pady=(20,0))


    button1.grid(row=0,column=1,padx=(0,0), pady=(30,5))
    fileText.grid(row=1,column=1,padx=(0,0),pady=(0,30))
    button2.grid(row=2,column=1,padx=(140,140),pady=(10,5))
    warningLabel.grid(row=3,column=1,padx=(30,30),pady=(0,20))
    aibutton.grid(row=5,column=0,padx=(15,30),pady=(20,15))
    languagebutton.grid(row=5,column=2,padx=(0,15),pady=(00,00))
    dateStart.grid(row=0, column=0, pady=(30,0))
    dateEnd.grid(row=2, column=0)
    dStartButton.grid(row=1, column=0,pady=(0,30))
    dEndButton.grid(row=3,column=0,pady=(0,20))


    
    
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())

except Exception as e: # Make sure the application actualy shows something!
    errorText = ttk.Label(root, text=e)
    errorText.pack(padx=20,pady=20)
root.mainloop()