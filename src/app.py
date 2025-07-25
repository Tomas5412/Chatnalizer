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





# # Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
# filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
# print(filename)

if __name__ == "__main__":
    # print("File under construction! Use Chatnalizer for a primitve chatnalisis.")
    root = tk.Tk()
    # Import the tcl file
    root.tk.call('source', f'appTheme/{THEME_FILE}')
    # Set the theme with the theme_use method
    ttk.Style().theme_use(THEME_NAME)
    # A themed (ttk) button
    button = ttk.Button(root, text="Start Chatnalisis", command=startChatnalisis,  style="Accent.TButton")
    button.pack(pady=20)
    root.mainloop()