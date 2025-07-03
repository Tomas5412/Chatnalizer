# coding=utf-8

import matplotlib.pyplot as plt
import os
import re
import emoji

CHAT_PATTERN = r'^([0-9]{1,2}/[0-9]{1,2}/[0-9]{4}, [0-9]{2}:[0-9]{2} - [^:\n]+[:\n])'

def chatParse(parserRoute: str, fileName: str) -> int:
    chatnalizadorRoute = parserRoute
    chatFileName = f"chat/{fileName}.txt"

    try:
        chatRouteAbs = os.path.join(chatnalizadorRoute, chatFileName)
        chatFile = open(chatRouteAbs)
        chat = chatFile.read()
        chatFile.close()
    except:
        print(f"Error reading file chat/{chatFileName}. Make sure it exists")
        return 0


    # emojiFreeChat = emoji.demojize(chat)

    messages = re.split(pattern=CHAT_PATTERN, string=chat, flags=re.MULTILINE)

    try:
        chatnalizatedPath = os.path.join(chatnalizadorRoute, f"chatparseados/{fileName}.py")
        with open(chatnalizatedPath, "w+") as f:
            f.write(f"messages = {messages}")
    except:
        print("Error writing to file")
        return 0
    return 1

if __name__ == "__main__":
    # print(f"El camino es {os.path.abspath("")}") 
    res = chatParse(os.path.abspath(""),"SojapostingT")
    if res == 1:
        print("Fetched completed!")
    else:
        print("Whoops!")