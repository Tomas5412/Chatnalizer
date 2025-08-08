from chatparser import parseChat
from chatfetcher import chatFetch
from chatnalisis import mostMessagesByChatter
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from os import path
from data.classes import MediaType


def analizeChat(filename: str) -> str:
    if not filename: raise ValueError("File not selected.")
    _, ext = path.splitext(filename)
    if ext != ".txt":
        raise ValueError("File must be .txt!")
    else:    
        messages = chatFetch(filename)
        if messages == []:
            message = "Either the file is empty, or there was an error fetching the file."
        else:
            groupChat = parseChat(messages)
            message = ''
            message += f"{groupChat.messageAmount} messages were sent.\n"
            message += "="*70 + "\n"
            mlist = groupChat.members
            for user in mlist:
                message += f"{user.name} has sent {user.m_ammount} messages.\n"
                # if user.m_ammount > 5:
                #     for j in range(2):
                #         msg = user.messages[j]
                #         print(f"{msg.dtime} {user.name} - {repr(msg.content)}")
                message += f"They deleted {user.deletedMessages} messages and edited {user.editedMessages}.\n"
                # print(user.mediaSent)
                message += f"They sent {sum(user.mediaSent.values())} media files. {user.mediaSent[MediaType.STICKER]} of them were stickers and {user.mediaSent[MediaType.T_MEDIA]} were once media.\n"
                message += "="*70 + "\n"
            # try:
            #     mostMessagesByChatter(groupChat)
            # except Exception as e:
            #     print("Exception at mmbc:" + str(e))
            
        print("Parsing completed!")
        return message