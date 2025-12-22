from fpdf import FPDF
from ChatFunctions.chatparser import parseChat
from ChatFunctions.chatfetcher import chatFetch
from ChatFunctions.chatnalisis import *
from ChatFunctions.chatgraphics import *
from misc.classes import DATE_TYPE, MediaType, ActionType
from os import path
from datetime import timedelta
from misc.keywords import AUTHOR_NAME, LANGUAGES
from emoji import demojize

#    from reportlab.pdfgen import canvas
#    c = canvas.Canvas("hello.pdf")
#    from reportlab.lib.units import inch
#    # move the origin up and to the left
#    c.translate(inch,inch)
#    # define a large font
#    c.setFont("Helvetica", 80)
#    # choose some colors
#    c.setStrokeColorRGB(0.2,0.LINE_SPACING,0.3)
#    c.setFillColorRGB(1,0,1)
#    # draw a rectangle
#    c.rect(inch,inch,6*inch,9*inch, fill=1)
#    # make text go straight up
#    c.rotate(90)
#    # change color
#    c.setFillColorRGB(0,0,0.77)
#    # say hello (note after rotate the y coord needs to be negative!)
#    c.drawString(3*inch, -3*inch, "Hello World")
#    c.showPage()
#    c.save()




def analizeChat(filename: str, config: dict[str,bool]) -> str:

    LINE_SPACING = 0.5
    MAX_MISSING_MINUTES = 60

    # All the config variables are extracted at once.
    
    dateType = config["dateType"]
    languageIndex = config["languageIndex"]
    dateStart = config["dateStart"]
    dateEnd = config["dateEnd"]
    caseSensitive = config["caseSensitive"]
    phraseList = config["phraseList"]
    excludeAI = config["excludeAI"]
    includeMedia = config["includeMedia"]

    if dateType not in {dt.value for dt in DATE_TYPE}:
        raise ValueError("Date format not selected.")

    if not filename: raise ValueError("File not selected.")

    _, ext = path.splitext(filename)

    if ext != ".txt": raise ValueError("File must be .txt!")  

    messages = chatFetch(filename)

    if messages == []:
        message = "Either the file is empty, or there was an error fetching the file."
    else:
        # Initialization
        langauge = LANGUAGES[languageIndex]
        groupChat = parseChat(messages, dStart=dateStart, dEnd=dateEnd, dateType=dateType, language=langauge)
        wordCount, emojiCount = mostWordsByChatter(groupChat, caseSensitive)
        uniqueWord = getUncommonWordsPerChatter(wordCount)
        mostTalkedDict = getMostTalkedTo(groupChat)
        messageCount, phraseCount = mostMessagesByChatter(groupChat, phraseList, caseSensitive)
        uniqueMsg = getUncommonMessagesPerChatter(messageCount)
        global_minute_ranking, personal_minute_ranking, global_date_ranking, personal_date_ranking, global_hour_ranking, personal_hour_ranking = getTimeDicts(groupChat)
        dStart, dEnd, dayPctg, pctgDict = getTimeStats(groupChat, dateStart, dateEnd)
        if includeMedia:
            mediaSentByChatter(groupChat)
            absChampionDict = getAbsoluteChampionPerMediaType(groupChat)
        makeMessagePie(groupChat)
        makeTimeStackplot(groupChat)
        longest_streak = dEnd - dStart

        # The pdf wizardry begins here

        c = FPDF(unit="cm")
        c.add_page()
        c.add_font("SegUI",fname="./internal/SegUIVar.ttf")
        c.set_font("SegUI", size=10)
        c.cell(0,LINE_SPACING,f"{groupChat.messageAmount} messages were sent.", new_x="LMARGIN", new_y="NEXT")
        c.cell(0,LINE_SPACING,f"A message was sent {dayPctg*100:.2f}% of all days.", new_x="LMARGIN", new_y="NEXT")
        if includeMedia:
            c.cell(0,LINE_SPACING,f"{groupChat.mediaSentAmount} media were sent.", new_x="LMARGIN", new_y="NEXT")

        c.cell(0,LINE_SPACING,f"The longest streak was of {longest_streak.days} days, since {dStart} until {dEnd}.", new_x="LMARGIN", new_y="NEXT")
        most_message_day = max(global_date_ranking, key=global_date_ranking.get)
        c.cell(0,LINE_SPACING,f"The day with the most messages was {most_message_day}, at {global_date_ranking[most_message_day]} messages.", new_x="LMARGIN", new_y="NEXT")
        
        most_hour_day = max(global_minute_ranking, key=global_minute_ranking.get)
        if includeMedia:
            for m_type in absChampionDict.keys():
                if len(absChampionDict[m_type]) == 1:
                    champion = absChampionDict[m_type][0]
                    c.cell(0,LINE_SPACING,f"The chatter that has sent most {m_type.value}s is {champion.name} ({champion.mediaSent[m_type]} times)", new_x="LMARGIN", new_y="NEXT")
                else:
                    champions = absChampionDict[m_type]
                    message = ""
                    for champ in champions[:-1]:
                        message += f"{champ.name}, "
                    message += f"and {champions[-1]} were tied in sending the most {m_type.value}s ({champions[-1].mediaSent[m_type]} times)"
                    c.cell(0,LINE_SPACING,message, new_x="LMARGIN", new_y="NEXT")

            # message += "="*70 + "\n"
        
        c.cell(0,LINE_SPACING,f"The most preffered HOUR AND MINUTE for messaging was {most_hour_day}, at {global_minute_ranking[most_hour_day]} messages.", new_x="LMARGIN", new_y="NEXT")

        if len(global_hour_ranking) == 24: 
            c.cell(0,LINE_SPACING,"A message has been said at every hour!", new_x="LMARGIN", new_y="NEXT")
            if len(global_minute_ranking) == 60*24: 
                c.cell(0,LINE_SPACING,"A message has been said at EVERY POSSIBLE MINUTE! Go outside!", new_x="LMARGIN", new_y="NEXT")
            else:
                message = ""
                message += "Missing minutes:\n"
                missingMinutes = 0
                for i in range(24):
                    for j in range(60):
                        checkTime = time(i,j)
                        if not global_minute_ranking.get(checkTime,0):
                            message += f"{i}:{j}    "
                            missingMinutes += 1
                if missingMinutes <= MAX_MISSING_MINUTES:
                    c.multi_cell(0,LINE_SPACING,message, new_x="LMARGIN", new_y="NEXT")
                else:
                    c.cell(0,LINE_SPACING,f"{missingMinutes} missing minutes!", new_x="LMARGIN", new_y="NEXT")
        else:
            message = "Missing hours:\n"
            for i in range(24):
                if not global_hour_ranking.get(i,0):
                    message += f"{i}hrs    "
            c.multi_cell(0,LINE_SPACING,message, new_x="LMARGIN", new_y="NEXT")
        # c.add_page()
        c.image("internal/total-time-stackplot.svg",w=c.epw,h=9.5)
        c.image("internal/messagePie.svg",w=9,h=9)

        # Member's pages begin here

        mlist = groupChat.members
        for user in mlist:
            print(user.a_ammount)
            if (user.name != "Meta AI" or (not excludeAI)) and user.name != AUTHOR_NAME:
                c.add_page()
                message = ""
                message += f"{demojize(user.name)} has sent {user.m_ammount} messages ({((user.m_ammount / groupChat.messageAmount)*100):.2f}%).\n"

                message += f"They sent a message {pctgDict[user.name][0]*100:.2f}% of days ({pctgDict[user.name][1]} days).\n"
                message += f"They deleted {user.deletedMessages} messages and edited {user.editedMessages}.\n"
                try:
                    max_date = max(personal_date_ranking[user.name], key=personal_date_ranking[user.name].get)
                    message += f"The day with most messages by this chatter was {max_date.day}/{max_date.month}/{max_date.year}, at {personal_date_ranking[user.name][max_date]} messages.\n"
                except:
                    continue

                if messageCount.get(user,{}):
                    maxMsg = max(messageCount[user], key= messageCount[user].get)
                    message += f"Their most sent message was '{demojize(maxMsg)}'. It was said {messageCount[user][maxMsg]} times.\n"
                if emojiCount.get(user,{}):
                    maxEmoji = max(emojiCount[user], key=emojiCount[user].get)
                    message += f"Their most used emoji was {demojize(maxEmoji)}. It was used {emojiCount[user][maxEmoji]} times.\n"
                if uniqueWord.get(user.name,{}):
                    message += "Here are their most unique words used:\n"
                    for wordData in uniqueWord[user.name]:
                        if wordData[4] != 100: # Excluse messages that had only been said by this chatter
                            message += f"    '{demojize(wordData[0])}' was said {(wordData[1]):.1f}% more than the average by this user. They said it {wordData[3]} times ({(wordData[4]):.2f}% of total usage)\n"
                if uniqueMsg.get(user.name,{}):
                    message += "Here are their most unique messages said:\n"
                    for messageData in uniqueMsg[user.name]:
                        if messageData[4] != 100:
                            message += f"    '{demojize(messageData[0])}' was said {(messageData[1]):.1f}% more than the average by this user. They said it {messageData[3]} times ({(messageData[4]):.2f}% of total usage)\n"

                if includeMedia:
                    message += f"They sent {sum(user.mediaSent.values())} media files. {user.mediaSent[MediaType.STICKER]} of them were stickers and {user.mediaSent[MediaType.T_MEDIA]} were once media.\n"
                if caseSensitive:
                    for phrase in phraseList:
                        message += f"They said '{demojize(phrase)}' {phraseCount[user.name][phrase]} times.\n"
                else:
                    for phrase in phraseList:
                        message += f"They said '{demojize(phrase.lower())}' {phraseCount[user.name][phrase]} times.\n"                        

                for action in ActionType:
                    if user.actionsDone[action] > 1: 
                        message += f"{action.value} action was done {user.actionsDone[action]} times.\n"
                if user.name in mostTalkedDict.keys():
                    message += f"Their most talked to chatter was {mostTalkedDict[user.name][0]} (answered {mostTalkedDict[user.name][1]} times)\n"
                
                c.multi_cell(0,LINE_SPACING,message)
                try:
                    c.add_page()
                    c.image(f"internal/{user.name}-time-stackplot.svg",w=c.epw,h=9.5)
                    if includeMedia:
                        c.image(f"internal/{user.name}-mediaSent.svg",w=9,h=9)
                except:
                    continue


        try:
            c.output("results.pdf")
        except Exception as e:
            raise Exception("Exception while making pdf:" + e)
        return message