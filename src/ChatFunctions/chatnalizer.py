from ChatFunctions.chatparser import parseChat
from ChatFunctions.chatfetcher import chatFetch
from ChatFunctions.chatnalisis import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from os import path
from misc.classes import MediaType


def analizeChat(filename: str, excludeAI: bool = False) -> str:
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
            wordCount, emojiCount = mostWordsByChatter(groupChat)
            uniqueWord = getUncommonWordsPerChatter(wordCount)
            messageCount, _ = mostMessagesByChatter(groupChat)
            uniqueMsg = getUncommonMessagesPerChatter(messageCount)
            message = ''
            message += f"{groupChat.messageAmount} messages were sent.\n"
            message += "="*70 + "\n"
            mlist = groupChat.members
            for user in mlist:
                if user.name != "Meta AI" or (not excludeAI):
                    message += f"{user.name} has sent {user.m_ammount} messages ({((user.m_ammount / groupChat.messageAmount)*100):.2f}%).\n"
                    # if user.m_ammount > 5:
                    #     for j in range(2):
                    #         msg = user.messages[j]
                    #         print(f"{msg.dtime} {user.name} - {repr(msg.content)}")
                    message += f"They deleted {user.deletedMessages} messages and edited {user.editedMessages}.\n"
                    # print(user.mediaSent)
                    if messageCount[user]:
                        maxMsg = max(messageCount[user], key= messageCount[user].get)
                        message += f"Their most sent message was '{maxMsg}'. It was said {messageCount[user][maxMsg]} times.\n"
                    if emojiCount[user]:
                        maxEmoji = max(emojiCount[user], key=emojiCount[user].get)
                        message += f"Their most used emoji was {maxEmoji}. It was used {emojiCount[user][maxEmoji]} times.\n"
                    if uniqueWord[user.name]:
                        message += "Here are their most unique words used:\n"
                        for wordData in uniqueWord[user.name]:
                            if wordData[4] != 100: # Excluse messages that had only been said by this chatter
                                message += f"\t'{wordData[0]}' was said {(wordData[1]):.1f}% more than the average by this user. They said it {wordData[3]} times ({(wordData[4]):.2f}% of total usage)\n"
                    if uniqueMsg[user.name]:
                        message += "Here are their most unique messages said:\n"
                        for messageData in uniqueMsg[user.name]:
                            if messageData[4] != 100:
                                message += f"\t'{messageData[0]}' was said {(messageData[1]):.1f}% more than the average by this user. They said it {messageData[3]} times ({(messageData[4]):.2f}% of total usage)\n"

                    message += f"They sent {sum(user.mediaSent.values())} media files. {user.mediaSent[MediaType.STICKER]} of them were stickers and {user.mediaSent[MediaType.T_MEDIA]} were once media.\n"
                    message += "="*70 + "\n"
            # try:
            #     mostMessagesByChatter(groupChat)
            # except Exception as e:
            #     print("Exception at mmbc:" + str(e))
            
        print("Parsing completed!")
        return message
    
if __name__ == "__main__":
    print("This shouldn't be run alone.")