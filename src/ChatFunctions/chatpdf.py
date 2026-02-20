from fpdf import FPDF
from fpdf.graphics_state import DeviceGray
from ChatFunctions.chatparser import parseChat
from ChatFunctions.chatfetcher import chatFetch
from ChatFunctions.chatnalisis import *
from ChatFunctions.chatgraphics import *
from misc.classes import DATE_TYPE, MediaType, ActionType
from os import path
from datetime import timedelta
from misc.keywords import AUTHOR_NAME, LANGUAGES, COLORS
from emoji import demojize
from time import time as clk #! as 'time' is also the constructor for the datetime "time", this function to time the computing of the program needed to be renamed


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
        groupChat = parseChat(messages, dStart=dateStart, dEnd=dateEnd, dateType=dateType, language=langauge, excludeAI=excludeAI)
        start = clk()
        wordCount, emojiCount = mostWordsByChatter(groupChat, caseSensitive)
        uniqueWord = getUncommonWordsPerChatter(wordCount)
        if len(groupChat.members.values()) > 2:
            mostTalkedDict = getMostTalkedTo(groupChat)
        messageCount, phraseCount = mostMessagesByChatter(groupChat, phraseList, caseSensitive)
        uniqueMsg = getUncommonMessagesPerChatter(messageCount)
        global_minute_ranking, personal_minute_ranking, global_date_ranking, personal_date_ranking, global_hour_ranking, personal_hour_ranking = getTimeDicts(groupChat)
        dStart, dEnd, dayPctg, pctgDict = getTimeStats(groupChat, dateStart, dateEnd)
        timeElapsed = clk() - start
        print(f"Analisis completed! Took {timeElapsed}")
        if includeMedia:
            mediaSentByChatter(groupChat)
            absChampionDict = getAbsoluteChampionPerMediaType(groupChat)
        makeMessagePie(groupChat)
        makeTimeStackplot(groupChat)
        makeHourRadarChart(global_hour_ranking, groupChat.messageAmount, language=langauge)
        makeHourRadarChartPerChatter(personal_hour_ranking, language=langauge)
        longest_streak = dEnd - dStart

        # The pdf wizardry begins here
        start = clk()
        c = FPDF(unit="cm")
        c.add_page()
        c.add_font("SegUI",fname="./internal/SegUIVar.ttf")
        c.set_font("SegUI", size=10)
        language = LANGUAGES[languageIndex]

        match language:
        # Before, the languages were divided and the next ~100 lines would be repeated but everything translated to spanish.
        # There has to be a better way, right?

            case _:

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
                    message = "A message has not been said at all hours.\nMissing hours:\n"
                    for i in range(24):
                        if not global_hour_ranking.get(i,0):
                            message += f"{i}hrs    "
                    c.multi_cell(0,LINE_SPACING,message, new_x="LMARGIN", new_y="NEXT")
                c.add_page()
                c.image("internal/total-time-stackplot.svg",w=c.epw,h=11)
                c.image("internal/messagePie.svg",w=9,h=9)
                c.image("internal/global-hour-ranking.svg", w=9, h=9)

                # Member's pages begin here

                mlist = list(groupChat.members.values())
                i = 0
                for user in mlist:
                    color = COLORS[i]
                    i += 1
                    i = i % len(COLORS)
                    # print(user.a_ammount)
                    if user.name != AUTHOR_NAME:
                        c.add_page()
                        c.set_text_color(color[0],color[1],color[2])
                        c.set_font(size=15)
                        c.cell(0, LINE_SPACING, user.name, align="C",new_x="LMARGIN", new_y="NEXT")
                        c.set_text_color(0)
                        c.set_font(size=10)
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
                        if len(mlist) > 2 and user.name in mostTalkedDict.keys():
                            message += f"Their most talked to chatter was {mostTalkedDict[user.name][0]} (answered {mostTalkedDict[user.name][1]} times)\n"

                        c.multi_cell(0,LINE_SPACING,message)
                        try:
                            c.add_page()
                            c.image(f"internal/{user.name}-time-stackplot.svg",w=c.epw,h=11)
                            c.image(f"internal/{user.name}-hour-ranking.svg", w=9, h=9)
                            if includeMedia:
                                c.image(f"internal/{user.name}-mediaSent.svg",w=9,h=9)
                        except:
                            continue


        try:
            c.output("results.pdf")
            timeElapsed = clk() - start
            print(f"PDF made! Took {timeElapsed}")
        except Exception as e:
            raise Exception("Exception while making pdf:" + e)
        return message
    



### Here is the spanish translation of the part that writes to the pdf

# case "SPANISH":
#                 c.set_font(size=15)
#                 c.cell(0,LINE_SPACING,f"General", new_x="LMARGIN", new_y="NEXT", align="C")
#                 c.set_font(size=10)
#                 c.cell(0,LINE_SPACING,f"Se enviaron {groupChat.messageAmount} mensajes.", new_x="LMARGIN", new_y="NEXT")
#                 c.cell(0,LINE_SPACING,f"El tamaño promedio de mensaje es de {(sum([m.avgMessageLength for m in groupChat.members.values()]) / len(groupChat.members.values())):.2f} letras por mensaje.", new_x="LMARGIN", new_y="NEXT")
#                 c.cell(0,LINE_SPACING,f"Al menos un mensaje se envió el {dayPctg*100:.2f}% de todos los días.", new_x="LMARGIN", new_y="NEXT")
#                 if includeMedia:
#                     c.cell(0,LINE_SPACING,f"Se enviaron {groupChat.mediaSentAmount} archivos multimedia.", new_x="LMARGIN", new_y="NEXT")
        
#                 c.cell(0,LINE_SPACING,f"La mayor racha de días fue de {longest_streak.days}, desde {dStart} hasta {dEnd}.", new_x="LMARGIN", new_y="NEXT")
#                 most_message_day = max(global_date_ranking, key=global_date_ranking.get)
#                 c.cell(0,LINE_SPACING,f"El día con la mayor cantidad de mensajes fue {most_message_day}, con {global_date_ranking[most_message_day]} messages.", new_x="LMARGIN", new_y="NEXT")
                
#                 most_hour_day = max(global_minute_ranking, key=global_minute_ranking.get)
#                 if includeMedia:
#                     for m_type in absChampionDict.keys():
#                         if len(absChampionDict[m_type]) == 1:
#                             champion = absChampionDict[m_type][0]
#                             c.cell(0,LINE_SPACING,f"La persona que mandó más {m_type.value}s es {champion.name} ({champion.mediaSent[m_type]} veces)", new_x="LMARGIN", new_y="NEXT")
#                         else:
#                             champions = absChampionDict[m_type]
#                             message = ""
#                             for champ in champions[:-1]:
#                                 message += f"{champ.name}, "
#                             message += f"y {champions[-1]} empataron al mandar la mayor cantidad de {m_type.value}s ({champions[-1].mediaSent[m_type]} veces)"
#                             c.cell(0,LINE_SPACING,message, new_x="LMARGIN", new_y="NEXT")
        
#                     # message += "="*70 + "\n"
                
#                 c.cell(0,LINE_SPACING,f"La HORA Y MINUTO con más mensajes fue {most_hour_day}, con {global_minute_ranking[most_hour_day]} mensajes.", new_x="LMARGIN", new_y="NEXT")
        
#                 if len(global_hour_ranking) == 24: 
#                     c.cell(0,LINE_SPACING,"¡Se mandó un mensaje en cada hora!", new_x="LMARGIN", new_y="NEXT")
#                     if len(global_minute_ranking) == 60*24: 
#                         c.cell(0,LINE_SPACING,"¡Se mandó un mensaje en CADA minuto! ¡Toquen pasto!", new_x="LMARGIN", new_y="NEXT")
#                     else:
#                         message = ""
#                         message += "No se mandó un mensaje en cada minuto.\nMinutos faltantes:\n"
#                         missingMinutes = 0
#                         for i in range(24):
#                             for j in range(60):
#                                 checkTime = time(i,j)
#                                 if not global_minute_ranking.get(checkTime,0):
#                                     message += f"{i}:{j}    "
#                                     missingMinutes += 1
#                         if missingMinutes <= MAX_MISSING_MINUTES:
#                             c.multi_cell(0,LINE_SPACING,message, new_x="LMARGIN", new_y="NEXT")
#                         else:
#                             c.cell(0,LINE_SPACING,f"¡Faltan {missingMinutes} minutos!", new_x="LMARGIN", new_y="NEXT")
#                 else:
#                     message = "No se mandó un mensaje en cada hora.\nHoras faltantes:\n"
#                     for i in range(24):
#                         if not global_hour_ranking.get(i,0):
#                             message += f"{i}hrs    "
#                     c.multi_cell(0,LINE_SPACING,message, new_x="LMARGIN", new_y="NEXT")
#                 c.add_page()
#                 c.image("internal/total-time-stackplot.svg",w=c.epw,h=11)
#                 c.image("internal/messagePie.svg",w=9,h=9)
#                 c.image("internal/global-hour-ranking.svg", w=9, h=9)
        
#                 # Member's pages begin here
        
#                 mlist = list(groupChat.members.values())
#                 i = 0
#                 for user in mlist:
#                     color = COLORS[i]
#                     i += 1
#                     i = i % len(COLORS)
#                     # print(user.a_ammount)
#                     if user.name != AUTHOR_NAME:
#                         c.add_page()
#                         c.set_text_color(color[0],color[1],color[2])
#                         c.set_font(size=15)
#                         c.cell(0, LINE_SPACING, user.name, align="C",new_x="LMARGIN", new_y="NEXT")
#                         c.set_text_color(0)
#                         c.set_font(size=10)
#                         message = ""
#                         message += f"{demojize(user.name)} mandó {user.m_ammount} mensajes ({((user.m_ammount / groupChat.messageAmount)*100):.2f}%)\n"
#                         message += f"Su promedio fue de {user.avgMessageLength:.2f} letras por mensaje.\n"
        
#                         message += f"Mandó al menos un mensaje el {pctgDict[user.name][0]*100:.2f}% de los días ({pctgDict[user.name][1]} días).\n"
#                         message += f"Eliminó {user.deletedMessages} mensajes y editó {user.editedMessages}.\n"
#                         try:
#                             max_date = max(personal_date_ranking[user.name], key=personal_date_ranking[user.name].get)
#                             message += f"El día que mandó más mensajes fue el {max_date.day}/{max_date.month}/{max_date.year}, con {personal_date_ranking[user.name][max_date]} mensajes.\n"
#                         except:
#                             continue
                        
#                         if messageCount.get(user,{}):
#                             maxMsg = max(messageCount[user], key= messageCount[user].get)
#                             message += f"El mensaje que más mandó fue '{demojize(maxMsg)}'. ({messageCount[user][maxMsg]} veces)\n"
#                         if emojiCount.get(user,{}):
#                             maxEmoji = max(emojiCount[user], key=emojiCount[user].get)
#                             message += f"El emoji más usado fue {demojize(maxEmoji)} ({emojiCount[user][maxEmoji]} veces)\n"
#                         if uniqueWord.get(user.name,{}):
#                             message += "Las palabras más únicas:\n"
#                             for wordData in uniqueWord[user.name]:
#                                 if wordData[4] != 100: # Excluse messages that had only been said by this chatter
#                                     message += f"    '{demojize(wordData[0])}' fue dicho por esta persona un {(wordData[1]):.1f}% más que el promedio.\n"
#                                     #? Don't like the fully detailed version. Change?
#                                     # message += f"    '{demojize(wordData[0])}' fue dicho por esta persona un {(wordData[1]):.1f}% más que el promedio. They said it {wordData[3]} times ({(wordData[4]):.2f}% of total usage)\n"
#                         if uniqueMsg.get(user.name,{}):
#                             message += "Los mensajes más únicos:\n"
#                             for messageData in uniqueMsg[user.name]:
#                                 if messageData[4] != 100:
#                                     message += f"    '{demojize(messageData[0])}' fue dicho por esta persona un {(messageData[1]):.1f}% más que el promedio.\n"
#                                     #message += f"    '{demojize(messageData[0])}' was said {(messageData[1]):.1f}% more than the average by this user. They said it {messageData[3]} times ({(messageData[4]):.2f}% of total usage)\n"
        
#                         if includeMedia:
#                             message += f"Mandó {sum(user.mediaSent.values())} archivos multimedia:\n"
#                             for M_type in MediaType:
#                                 if M_type is not MediaType.NONE and user.mediaSent[M_type]:
#                                     message += f"   - {user.mediaSent[M_type]} {M_type.value}s.\n"
#                         if caseSensitive:
#                             for phrase in phraseList:
#                                 message += f"Escribió '{demojize(phrase)}' en {phraseCount[user.name][phrase]} mensajes.\n"
#                         else:
#                             for phrase in phraseList:
#                                 message += f"Escribió '{demojize(phrase.lower())}' en {phraseCount[user.name][phrase]} mensajes.\n"                        
        
#                         for action in ActionType:
#                             if user.actionsDone[action] > 1: 
#                                 message += f"Acción '{action.value}' fue hecha {user.actionsDone[action]} veces.\n"
#                         if len(mlist) > 2 and user.name in mostTalkedDict.keys():
#                             message += f"La persona con la que más habló fue {mostTalkedDict[user.name][0]} (respondió {mostTalkedDict[user.name][1]} veces)\n"
                        
#                         c.multi_cell(0,LINE_SPACING,message)
#                         try:
#                             c.add_page()
#                             c.image(f"internal/{user.name}-time-stackplot.svg",w=c.epw,h=11)
#                             c.image(f"internal/{user.name}-hour-ranking.svg", w=9, h=9)
#                             if includeMedia:
#                                 c.image(f"internal/{user.name}-mediaSent.svg",w=9,h=9)
#                         except:
#                             continue