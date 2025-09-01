from misc.keywords import APP_KEYWORDS,LANGUAGES
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter.filedialog import askopenfilename
from ChatFunctions.chatnalizer import analizeChat
from misc.classes import DATE_TYPE
from os import path
import datetime as dt
import tkcalendar as tkc


THEME_FILE = "forest-dark.tcl"
THEME_NAME = "forest-dark"

ROW_AMMOUNT = 5 # + 1 (including 0th row)
COLUMN_AMMOUNT = 2 # + 1

def getFile():
    filename.set(askopenfilename())
    if filename.get():
        filenameDisplay.set(APP_KEYWORDS[LANGUAGES[languageV]]["file_display"] + filename.get())
    else:
        filenameDisplay.set(APP_KEYWORDS[LANGUAGES[languageV]]["unselected_file"])


def startChatnalisis():
    try:
        if dStartState.get():
            try:
                dStart = dateStart.get_date()
                dStart = dt.datetime(day=dStart.day, month=dStart.month, year=dStart.year, hour=0, minute=0)
            except Exception as e:
                print(f"Exception in date fetch '{e}'. defaulting to no lower bound.")
                dStart = dt.datetime(2009,2,1)
        else:
            dStart = dt.datetime(2009,2,1)

        if dEndState.get():
            try:
                dEnd = dateEnd.get_date()
                dEnd = dt.datetime(day=dEnd.day, month=dEnd.month, year=dEnd.year, hour=23, minute=59)
            except Exception as e:
                print(f"Exception in date fetch '{e}'. defaulting to no upper bound.")
                dEnd = dt.datetime.now()
        else:
            dEnd = dt.datetime.now()

        if dEnd < dStart: raise ValueError("End date occurs sooner than start, sillyhead!")

        dType = dateFormat.get()
        if dType not in [t.value for t in DATE_TYPE]: dType = "DD/MM/YY"
        message = analizeChat(filename.get(), excludeAI=aistate.get(), dateStart=dStart, dateEnd=dEnd, dateType=dType, phraseList=wordList, caseSensitive=caseSensitive.get(), languageIndex=language.get())
        filepath = path.join(path.abspath(""),f"results_{path.basename(filename.get())}")
        with open(filepath, "w+") as f:
            f.write(message)
            f.close

        warningText.set(APP_KEYWORDS[LANGUAGES[language.get()]]["analysis_complete"] + filepath)
    
    except KeyError as e:
        print(e)
        warningText.set("Key error: " + str(e))
    except ValueError as e:
        print(e)
        warningText.set("Value error: " + str(e))
    except Exception as e:
        print(e)
        warningText.set(e)

root = tk.Tk()
root.title("Chatnalizer (PROTOTYPE) version 0.2")
root.option_add("*tearOff", False)
# chatnalizerLogo = tk.PhotoImage(file="chatnalizerLogo.png") # The world is not ready...
# root.wm_iconphoto(True, chatnalizerLogo)

italic = tkFont.Font(root, family="Arial", size=10, slant="italic")

try:
    # START STUFF
    root.tk.call('source', f'appTheme/{THEME_FILE}')
    ttk.Style().theme_use(THEME_NAME)
    root.resizable(False, False)

    # VARIABLES

    language = tk.IntVar(value=0)
    languageV = language.get()
    aistate = tk.BooleanVar(master=root)
    dStartState = tk.BooleanVar(master=root, value=False)
    dEndState = tk.BooleanVar(master=root, value= False)
    dStartText = tk.StringVar(master=root, value=APP_KEYWORDS[LANGUAGES[languageV]]["date_start"])
    dateFormatComboboxText = tk.StringVar(master=root, value= "DD/MM/YY")
    dateFormatLabelText = tk.StringVar(master=root, value=APP_KEYWORDS[LANGUAGES[languageV]]["date_format"])
    dEndText = tk.StringVar(master=root, value=APP_KEYWORDS[LANGUAGES[languageV]]["date_end"])
    languageText = tk.StringVar(master=root,value=APP_KEYWORDS[LANGUAGES[languageV]]["change_language"])
    aitext = tk.StringVar(master=root, value=APP_KEYWORDS[LANGUAGES[languageV]]["ai_exclusion"])
    getFileText = tk.StringVar(master=root, value=APP_KEYWORDS[LANGUAGES[languageV]]["get_file_button"])
    filenameDisplay = tk.StringVar(master=root, value=APP_KEYWORDS[LANGUAGES[languageV]]["unselected_file"])
    chanalisisText = tk.StringVar(master=root,value=APP_KEYWORDS[LANGUAGES[languageV]]["analysis_button"])
    warningText = tk.StringVar(master=root, value=APP_KEYWORDS[LANGUAGES[languageV]]["unsopported_language_warning"])
    wordListAddText = tk.StringVar(root, value=APP_KEYWORDS[LANGUAGES[languageV]]["word_list_add"])
    wordListShowText = tk.StringVar(root, value=APP_KEYWORDS[LANGUAGES[languageV]]["word_list_show"])
    filename = tk.StringVar()
    caseSensitive = tk.BooleanVar(root)
    caseSensitiveText = tk.StringVar(root, value=APP_KEYWORDS[LANGUAGES[languageV]]["case_sensitive"])
    includeMediaText = tk.StringVar(root, value=APP_KEYWORDS[LANGUAGES[languageV]]["include_media"])
    mediaWarningText = tk.StringVar(root, value=APP_KEYWORDS[LANGUAGES[languageV]]["media_warning"])
    wordListExplainerText = tk.StringVar(root, value=APP_KEYWORDS[LANGUAGES[languageV]]["list_explainer"])
    includeMedia = tk.BooleanVar()
    wordList = []
    filename.set("")

    # FUNCTIONS

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
        wordListAddText.set(APP_KEYWORDS[LANGUAGES[languageV]]["word_list_add"])
        wordListShowText.set(APP_KEYWORDS[LANGUAGES[languageV]]["word_list_show"])        
        dateFormatLabelText.set(APP_KEYWORDS[LANGUAGES[languageV]]["date_format"])
        caseSensitiveText.set(value=APP_KEYWORDS[LANGUAGES[languageV]]["case_sensitive"])
        includeMediaText.set(APP_KEYWORDS[LANGUAGES[languageV]]["include_media"])
        mediaWarningText.set(APP_KEYWORDS[LANGUAGES[languageV]]["media_warning"])
        wordListExplainerText.set(APP_KEYWORDS[LANGUAGES[languageV]]["list_explainer"])
        if not filename.get():
            filenameDisplay.set(APP_KEYWORDS[LANGUAGES[languageV]]["unselected_file"])
        else:
            filenameDisplay.set(APP_KEYWORDS[LANGUAGES[languageV]]["file_display"] + filename.get())

    def enableStart():
        if dStartState.get():
            dateStart.config(state="normal")
            dateStart.set_date(dt.date.today())
        else:
            dateStart.config(state="disabled")
        return
    
    def enableEnd():
        if dEndState.get():
            dateEnd.config(state="normal")
            dateEnd.set_date(dt.date.today())
        else:
            dateEnd.config(state="disabled")
        return

    def addWordList():
        word = wordListAdder.get()
        if word:
            print(f"Adding '{word}'...")
            wordList.append(word)
            wordListAdder.delete(0,tk.END)
        return

    def showWordList():
        wListWindow = tk.Toplevel(main)
        wListWindow.title("Phrase list")

        if wordList:
            wordFrame = ttk.LabelFrame(wListWindow, text="Phrase List:")

            def deleteRowAndRemoveWord(row):
                widgetRow = wordFrame.grid_slaves(row)
                wordList.remove(widgetRow[1].cget("text"))
                widgetRow[1].destroy()
                widgetRow[0].destroy()

            wordRow = 0
            for word in wordList:
                wordLabel = ttk.Label(wordFrame, text=word)
                deleteButton = ttk.Button(wordFrame, text=APP_KEYWORDS[LANGUAGES[language.get()]]["destroy"], style="Accent.TButton")
                wordLabel.grid(row=wordRow, column=0, padx=(10,5))
                deleteButton.grid(row=wordRow, column=1, padx=(0,10), pady=(20))
                deleteButton.config(command=lambda r=deleteButton.grid_info()["row"] : deleteRowAndRemoveWord(r))
                wordRow += 1

            wordFrame.grid(padx=40, pady=40)
        else:
            noWord = ttk.Label(wListWindow, text=APP_KEYWORDS[LANGUAGES[language.get()]]["no_word"], justify="center")
            noWord.pack(padx=50,pady=50)

        wListWindow.minsize(wListWindow.winfo_width(), wListWindow.winfo_height())
        return

    # APP WIDGETS

    ## Main frame
    main = ttk.Frame(root)
    main.grid()

    for i in range(ROW_AMMOUNT):
       main.rowconfigure(index=i, weight=1)
    for i in range(COLUMN_AMMOUNT):
        main.columnconfigure(index=i, weight=1)

    ## Main buttons

    buttonFrame = ttk.Frame(main)
    buttonFrame.grid(row=0,column=1, rowspan=3) # Rows 0, 1, 2

    button1 = ttk.Button(buttonFrame, textvariable=getFileText, command=getFile)
    button1.grid(row=0,column=1,padx=(0,0), pady=(30,5))

    fileText = ttk.Label(buttonFrame,textvariable=filenameDisplay)
    fileText.grid(row=1,column=1,padx=(0,0),pady=(0,30))
    
    button2 = ttk.Button(buttonFrame, textvariable=chanalisisText, command=startChatnalisis,  style="Accent.TButton")
    button2.grid(row=2,column=1,padx=(140,140),pady=(10,5))
    
    warningLabel = ttk.Label(buttonFrame, textvariable=warningText, justify="center")
    warningLabel.grid(row=3,column=1,padx=(30,30),pady=(0,20))

    ## Word List

    wordListSeparator = ttk.LabelFrame(main, text="Phrase List")
    wordListSeparator.grid(row=0, column= 2, rowspan=5, padx=(0,10), pady=(10,15),sticky="NE")

    wordListAdder = ttk.Entry(wordListSeparator)
    wordListAdder.grid(row=1,column=0, padx=0, pady=10, columnspan=2)
    wordListAdder.bind("<Return>",lambda x: addWordList())

    wordListExplainer = ttk.Label(wordListSeparator, textvariable=wordListExplainerText, font=italic, foreground="gray", justify="center")
    wordListExplainer.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    wordListAddButton = ttk.Button(wordListSeparator, textvariable=wordListAddText, command=addWordList, style="Accent.TButton")
    wordListShowButton = ttk.Button(wordListSeparator, textvariable=wordListShowText, command=showWordList)

    wordListAddButton.grid(row=2, column=0, padx=(20,10),pady=(0,10))
    wordListShowButton.grid(row=2, column=1, padx=(0,20), pady=(0,10))



    ## Date selection

    dateSeparator = ttk.LabelFrame(main, text="Filter by date")
    dateSeparator.grid(row=0, column=0, rowspan=3, pady=(10,15), padx=(20,20))

    dateStart = tkc.DateEntry(dateSeparator, mindate=dt.date(2009,2,1), maxdate=dt.datetime.now(), showothermonthdays=False, date_pattern="dd/mm/yy", state="disabled", showweeknumbers=False)
    dateStart.grid(row=0, column=0, pady=(10,0))

    dateEnd = tkc.DateEntry(dateSeparator, mindate=dt.date(2009,2,1), maxdate=dt.datetime.now(), showothermonthdays=False, date_pattern="dd/mm/yy", state="disabled", showweeknumbers=False)
    dateEnd.grid(row=2, column=0, padx=15)

    dStartButton = ttk.Checkbutton(dateSeparator, textvariable=dStartText, variable=dStartState, command=enableStart)
    dStartButton.grid(row=1, column=0,pady=(0,30), padx=15)

    dEndButton = ttk.Checkbutton(dateSeparator, textvariable=dEndText, command=enableEnd, variable= dEndState)
    dEndButton.grid(row=3,column=0,pady=(0,10), padx=15)

    # Analysis config (bottom mid)

    analysisConfig = ttk.Frame(main)

    includeMediaButton = ttk.Checkbutton(analysisConfig, textvariable=includeMediaText, variable=includeMedia, state="disabled")
    includeMediaButton.grid(row=0, column=0, pady=(10,0))

    mediaWarningLabel = ttk.Label(analysisConfig, textvariable=mediaWarningText, justify="center", font=italic, foreground="grey")
    mediaWarningLabel.grid(row=1, pady=(0,5))

    caseSensitiveButton = ttk.Checkbutton(analysisConfig, textvariable=caseSensitiveText, variable=caseSensitive)
    caseSensitiveButton.grid(row=2, column=0, pady=5)

    aibutton = ttk.Checkbutton(analysisConfig,textvariable=aitext,variable=aistate)
    aibutton.grid(row=3,column=0,padx=0,pady=(5,15))

    analysisConfig.grid(row=4, rowspan=3, column= 1) # rows 3, 4, 5

    ## Misc buttons (bottom left)

    miscSeparator = ttk.Frame(main)
    miscSeparator.grid(row=2,column=0, pady=(0,10), rowspan=3, columnspan=2, sticky="SW")

    dateFormat = ttk.Combobox(miscSeparator,textvariable=dateFormatComboboxText, state="readonly",values=[fmt.value for fmt in DATE_TYPE])
    dateFormat.grid(row=1,column=0, padx=(20,0))
    
    dateFormatLabel = ttk.Label(miscSeparator, textvariable=dateFormatLabelText)
    dateFormatLabel.grid(row=0, column=0,pady=(00,0))
    
    languagebutton = ttk.Button(main, textvariable=languageText,command=changeLanguage)
    languagebutton.grid(row=5,column=2,padx=(0,10),pady=(00,25), sticky="SE")


    # END STUFF    
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())

except Exception as e: # Make sure the application actualy shows something!
    try:
        main.grid_remove()
    except:
        pass
    errorText = ttk.Label(root, text=f"Fatal error: {e}")
    errorText.grid(row=0,column=0, padx=10, pady=10)

root.mainloop()