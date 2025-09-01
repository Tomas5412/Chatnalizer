from ChatFunctions.chatparser import parseChat
from ChatFunctions.chatfetcher import chatFetch
from ChatFunctions.chatnalisis import *
from misc.classes import DATE_TYPE, MediaType, ActionType
from os import path
from datetime import timedelta
from misc.keywords import AUTHOR_NAME, LANGUAGES


def analizeChat(filename: str, dateStart: datetime, dateEnd: datetime, excludeAI:bool, caseSensitive:bool, phraseList, dateType: str, languageIndex:int) -> str:

    for dt in DATE_TYPE:
        if dateType == dt.value:
            break
    else:
        raise ValueError("Date format not selected.")

    if not filename: raise ValueError("File not selected.")

    _, ext = path.splitext(filename)

    if ext != ".txt": raise ValueError("File must be .txt!")  

    messages = chatFetch(filename)

    if messages == []:
        message = "Either the file is empty, or there was an error fetching the file."
    else:
        langauge = LANGUAGES[languageIndex]
        groupChat = parseChat(messages, dStart=dateStart, dEnd=dateEnd, dateType=dateType, language=langauge)
        wordCount, emojiCount = mostWordsByChatter(groupChat, caseSensitive)
        uniqueWord = getUncommonWordsPerChatter(wordCount)
        messageCount, phraseCount = mostMessagesByChatter(groupChat, phraseList, caseSensitive)
        uniqueMsg = getUncommonMessagesPerChatter(messageCount)
        global_minute_ranking, personal_minute_ranking, global_date_ranking, personal_date_ranking, global_hour_ranking, personal_hour_ranking = getTimeDicts(groupChat)
        dStart, dEnd, dayPctg, pctgDict = getTimeStats(groupChat, dateStart, dateEnd)
        longest_streak = dEnd - dStart
        message = ''
        message += f"{groupChat.messageAmount} messages were sent.\n"
        message += f"A message was sent {dayPctg*100:.2f}% of all days.\n"
        message += "="*70 + "\n"
        mlist = groupChat.members
        for user in mlist:
            print(user.a_ammount)
            if (user.name != "Meta AI" or (not excludeAI)) and user.name != AUTHOR_NAME:
                message += f"{user.name} has sent {user.m_ammount} messages ({((user.m_ammount / groupChat.messageAmount)*100):.2f}%).\n"

                message += f"They sent a message {pctgDict[user.name][0]*100:.2f}% of days ({pctgDict[user.name][1]} days).\n"
                message += f"They deleted {user.deletedMessages} messages and edited {user.editedMessages}.\n"

                max_date = max(personal_date_ranking[user.name], key=personal_date_ranking[user.name].get)
                message += f"The day with most messages by this chatter was {max_date.day}/{max_date.month}/{max_date.year}, at {personal_date_ranking[user.name][max_date]} messages.\n"

                if messageCount.get(user,{}):
                    maxMsg = max(messageCount[user], key= messageCount[user].get)
                    message += f"Their most sent message was '{maxMsg}'. It was said {messageCount[user][maxMsg]} times.\n"
                if emojiCount.get(user,{}):
                    maxEmoji = max(emojiCount[user], key=emojiCount[user].get)
                    message += f"Their most used emoji was {maxEmoji}. It was used {emojiCount[user][maxEmoji]} times.\n"
                if uniqueWord.get(user.name,{}):
                    message += "Here are their most unique words used:\n"
                    for wordData in uniqueWord[user.name]:
                        if wordData[4] != 100: # Excluse messages that had only been said by this chatter
                            message += f"\t'{wordData[0]}' was said {(wordData[1]):.1f}% more than the average by this user. They said it {wordData[3]} times ({(wordData[4]):.2f}% of total usage)\n"
                if uniqueMsg.get(user.name,{}):
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
                
        message += f"The longest streak was of {longest_streak.days} days, since {dStart} until {dEnd}.\n"
        most_message_day = max(global_date_ranking, key=global_date_ranking.get)
        message += f"The day with the most messages was {most_message_day}, at {global_date_ranking[most_message_day]} messages.\n"
        most_hour_day = max(global_minute_ranking, key=global_minute_ranking.get)
        message += f"The most preffered HOUR AND MINUTE for messaging was {most_hour_day}, at {global_minute_ranking[most_hour_day]} messages.\n"

        if len(global_hour_ranking) == 24: 
            message += "A message has been said at every hour!\n"
            if len(global_minute_ranking) == 60*24: 
                message += "A message has been said at EVERY POSSIBLE MINUTE! Congrats!\n"
            else:
                message += "Missing minutes:\n"
                for i in range(24):
                    for j in range(60):
                        checkTime = time(i,j)
                        if not global_minute_ranking.get(checkTime,0):
                            message += f"{i}:{j}\t"
        else:
            message += "Missing hours:\n"
            for i in range(24):
                if not global_hour_ranking.get(i,0):
                    message += f"{i}hrs\t"
        # try:
        #     mostMessagesByChatter(groupChat)
        # except Exception as e:
        #     print("Exception at mmbc:" + str(e))
        
    print("Parsing completed!")
    return message
    
if __name__ == "__main__":
    print("This shouldn't be run alone.")