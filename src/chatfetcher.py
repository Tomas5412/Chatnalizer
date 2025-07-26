# coding=utf-8

# import matplotlib.pyplot as plt
from os import path
import re
# import emoji

CHAT_PATTERN = r'^([0-9]{1,2}/[0-9]{1,2}/[0-9]{4}, [0-9]{2}:[0-9]{2} - [^:\n]+[:\n])'

CHAT_PATTERN_IPHONE = r'^(\u200e*\[[0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}, [0-9]{2}:[0-9]{2}:[0-9]{2,4}\] [^:\n]+[:\n])'

CHAT_PATTERN_OLD = r'^(\u200e*\[[0-9]{1,2}:[0-9]{1,2}, [0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}\] [^:\n]+[:\n])'


def chatFetch(fileRoute: str, fileName = '') -> list[str]:

    try:
        # chatRouteAbs = os.path.join(chatnalizadorRoute, chatFileName)
        print(f"Fecthing from {fileRoute}...")
        chatFile = open(fileRoute)
        chat = chatFile.read()
        chatFile.close()
        print("Fetch completed! Parsing...")
    except Exception as e:
        print(e)
        print(f"Error reading file {fileRoute}. Make sure it exists")
        return []


    # emojiFreeChat = emoji.demojize(chat)

    patternToUse = CHAT_PATTERN

    if len(chat) < 4: raise ValueError("File does not contain chat.")

    if chat[0] == "[":
        if chat[2] == ":" or chat[3] == ":":
            patternToUse = CHAT_PATTERN_OLD
        else:
            patternToUse = CHAT_PATTERN_IPHONE
    messages = re.split(pattern=patternToUse, string=chat, flags=re.MULTILINE)

    if fileName != '': # This is deprecated, as it's never used.
        try:
            chatnalizatedPath = path.join(path.abspath(""), f"chatparseados/{fileName}.py")
            with open(chatnalizatedPath, "w+") as f:
                f.write(f"messages = {messages}")
        except:
            print("Error writing to file")
            return []
        
    if len(messages) == 1:
        raise ValueError("File does not contain chat.")
    return messages

if __name__ == "__main__":
    print("This shouldn't be ran alone.")