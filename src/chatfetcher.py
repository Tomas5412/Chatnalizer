# coding=utf-8

# import matplotlib.pyplot as plt
import os
import re
# import emoji

CHAT_PATTERN = r'^([0-9]{1,2}/[0-9]{1,2}/[0-9]{4}, [0-9]{2}:[0-9]{2} - [^:\n]+[:\n])'

CHAT_PATTERN_IPHONE = r'^(\u200e*\[[0-9]{1,2}/[0-9]{1,2}/[0-9]{2}, [0-9]{2}:[0-9]{2}:[0-9]{2}\] [^:\n]+[:\n])'

def chatParse(parserRoute: str, fileName: str) -> int:
    chatnalizadorRoute = parserRoute
    chatFileName = f"chat\\{fileName}.txt"

    try:
        chatRouteAbs = os.path.join(chatnalizadorRoute, chatFileName)
        print(f"Fecthing from {chatRouteAbs}...")
        chatFile = open(chatRouteAbs)
        chat = chatFile.read()
        chatFile.close()
    except:
        print(f"Error reading file {chatFileName}. Make sure it exists")
        return 0


    # emojiFreeChat = emoji.demojize(chat)

    patternToUse = CHAT_PATTERN
    if chat[0] == "[":
        patternToUse = CHAT_PATTERN_IPHONE
    messages = re.split(pattern=patternToUse, string=chat, flags=re.MULTILINE)

    try:
        chatnalizatedPath = os.path.join(chatnalizadorRoute, f"chatparseados/{fileName}.py")
        with open(chatnalizatedPath, "w+") as f:
            f.write(f"messages = {messages}")
    except:
        print("Error writing to file")
        return 0
    return 1

if __name__ == "__main__":

    res = chatParse(os.path.abspath(""),"") #! Fill with correct file before using
    if res == 1:
        print("Fetch completed! Check chatparseados for the results")
    else:
        print("Whoops!")