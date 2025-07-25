from chatparser import parseChat
from chatfetcher import chatFetch
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
from data.classes import MediaType




def analizeChat(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    if ext != ".txt":
        print("File must be .txt!")
    else:    
        messages = chatFetch(filename)
        if messages == []:
            message = "Either the file is empty, or there was an error fetching the file."
        else:
            groupChat = parseChat(messages)
            message = ''
            message += f"Se enviaron {groupChat.messageAmount} mensajes.\n"
            message += "="*70 + "\n"
            mlist = groupChat.members
            for user in mlist:
                message += f"{user.name} mandó {user.m_ammount} mensajes.\n"
                # if user.m_ammount > 5:
                #     for j in range(2):
                #         msg = user.messages[j]
                #         print(f"{msg.dtime} {user.name} - {repr(msg.content)}")
                message += f"Eliminó {user.deletedMessages} mensajes y editó {user.editedMessages}.\n"
                # print(user.mediaSent)
                message += f"Mandó {sum(user.mediaSent.values())} archivos multimedia. {user.mediaSent[MediaType.STICKER]} de ellos fueron stickers y {user.mediaSent[MediaType.T_MEDIA]} fueron temporales.\n"
                # print(f"{[message.content for message in user.messages if message.dtime.day == 6 and message.dtime.month == 6]}")
                message += "="*70 + "\n"
        print("Parsing completed!")
        return message