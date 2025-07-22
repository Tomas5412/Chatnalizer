from chatparser import parseChat
from chatfetcher import chatFetch
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
from data.classes import MediaType




if __name__ == "__main__":
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    # print(filename)
    _, ext = os.path.splitext(filename)
    if ext != ".txt":
        print("File must be .txt!")
    else:    
        messages = chatFetch(filename)
        if messages == []:
            print("Either the file is empty, or there was an error fetching the file.")
        else:
            groupChat = parseChat(messages)
            print(f"Se enviaron {groupChat.messageAmount} mensajes, con {groupChat.eventAmount} 'Eventos de chat'")
            print("="*70)
            mlist = groupChat.members
            for user in mlist:
                print(f"{user.name} mandó {user.m_ammount} mensajes.")
                # if user.m_ammount > 5:
                #     for j in range(2):
                #         msg = user.messages[j]
                #         print(f"{msg.dtime} {user.name} - {repr(msg.content)}")
                print(f"Eliminó {user.deletedMessages} mensajes y editó {user.editedMessages}.")
                # print(user.mediaSent)
                print(f"Mandó {sum(user.mediaSent.values())} archivos multimedia. {user.mediaSent[MediaType.STICKER]} de ellos fueron stickers y {user.mediaSent[MediaType.T_MEDIA]} fueron temporales.")
                # print(f"{[message.content for message in user.messages if message.dtime.day == 6 and message.dtime.month == 6]}")
                print("="*70)