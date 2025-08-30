from ChatFunctions.chatparser import parseChat
from ChatFunctions.chatfetcher import chatFetch
from ChatFunctions.chatnalisis import *
from misc.classes import DATE_TYPE, MediaType, ActionType
from os import path
from misc.keywords import AUTHOR_NAME


def analizeChat(filename: str, dateStart: datetime, dateEnd: datetime, excludeAI:bool, caseSensitive:bool, phraseList, dateType: str) -> str:

    for dt in DATE_TYPE:
        if dateType == dt.value:
            break
    else:
        raise ValueError("Date format not selected.")

    if not filename: raise ValueError("File not selected.")
    _, ext = path.splitext(filename)
    if ext != ".txt":
        raise ValueError("File must be .txt!")
    else:    
        messages = chatFetch(filename)
        if messages == []:
            message = "Either the file is empty, or there was an error fetching the file."
        else:
            groupChat = parseChat(messages, dStart=dateStart, dEnd=dateEnd, dateType=dateType)

            
            wordCount, emojiCount = mostWordsByChatter(groupChat, caseSensitive)
            uniqueWord = getUncommonWordsPerChatter(wordCount)
            messageCount, phraseCount = mostMessagesByChatter(groupChat, phraseList, caseSensitive)
            uniqueMsg = getUncommonMessagesPerChatter(messageCount)
            message = ''
            message += f"{groupChat.messageAmount} messages were sent.\n"
            message += "="*70 + "\n"
            mlist = groupChat.members
            for user in mlist:
                if (user.name != "Meta AI" or (not excludeAI)) and user.name != AUTHOR_NAME:
                    message += f"{user.name} has sent {user.m_ammount} messages ({((user.m_ammount / groupChat.messageAmount)*100):.2f}%).\n"

                    message += f"They deleted {user.deletedMessages} messages and edited {user.editedMessages}.\n"

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
                    if caseSensitive:
                        for phrase in phraseList:
                            message += f"They said '{phrase}' {phraseCount[user.name][phrase]} times.\n"
                    else:
                        for phrase in phraseList:
                            message += f"They said '{phrase.lower()}' {phraseCount[user.name][phrase]} times.\n"                        

                    for action in ActionType:
                        if user.actionsDone[action] > 1: 
                            message += f"{action.value} action was done {user.actionsDone[action]} times.\n"
                    
                    message += "="*70 + "\n"
            # try:
            #     mostMessagesByChatter(groupChat)
            # except Exception as e:
            #     print("Exception at mmbc:" + str(e))
            
        print("Parsing completed!")
        return message
    
if __name__ == "__main__":
    print("This shouldn't be run alone.")