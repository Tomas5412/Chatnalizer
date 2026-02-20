# Chatnalizer

___

## How to run

First, make a virtual enviroment and install all dependencies:

```$ python -m venv .venv```

```$ python -m pip install -r ./requirements.txt```

Now activate the virtual enviroment and go to **the src directory**. There, run:

```$ python .\app.py```

*If an error shows up, make sure you're in the ./src directory (don't run ./src/app.py in the root directory! For some reason it doesn't work in the virtual enviroment).*

This should open the next window:

![App Screenshot](appScreenshot.png)

In order, from left to right:

- **Filter by date** lets you filter the chatnalisis by date. If the buttons are turned off, the analisis doesn't take into account the dates selected.

- Selecting the right **date format** is important! Whatsapp automatically exports english chats using MM/DD/YY, and spanish/portuguese ones using the normal format.

- To actually do an analisis, first **select the file** and then click **The big green button that says chatnalize.**

- WhatsApp has the option to export chats with or without media. If you exported with media, turn **media analysis** ON (the actual media files are not needed)

- **Case sensitivity** and **Exclude Meta AI from the analisis** are self explaining.

- If you add strings to the **Phrase List**, the final result will also show each person in how many messages they said each string.

- Set the language to the one the chat was imported!!! This is important since the keywords change accordingly.

___

## Detected hour patterns

- [DD/MM/YY, HH:MM]

- [HH:MM, DD/MM/YYYY]

- DD/MM/YYYY, HH:MM

___

## Warnings

Do not include chat members that have ":" in their name, or (for whatever reason) the end of line '\n' character.

Messages that have nested messages in their contents (like ones that copy and paste other messages) can count as more than one.
