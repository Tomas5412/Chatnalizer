from misc.classes import Chat, datetime, Member
from misc.keywords import WORDS_TO_IGNORE, MESSAGES_TO_IGNORE
from unicodedata import category
from datetime import timedelta, time, date
import emoji



def mostWordsByChatter(chat: Chat, caseSensitive: bool) -> tuple[dict[Member, dict[str, int]], dict[Member, dict[str, int]]]:
    """
    Counts the number of words said by each chatter.
    
    Returns:
        tuple ((dict,dict)): Two dict of dicts. The keys are of Member type and the values are str:int dicts.
        
        For the second dict, the str keys are strictly emojis.
    """
    members = chat.members
    globalWordDict = {}
    globalEmojiDict = {}
    for member in members:
        wordDict = {}
        emojiDict = {}
        messages = member.messages
        for message in messages:
            actualMessage = str(message.content)
            actualMessage = "".join(ch for ch in actualMessage if category(ch)[0] != "C")
            # print(actualMessage)
            actualMessage = actualMessage.split()
            for word in actualMessage:
                if not caseSensitive:
                    word = word.lower()
                if word and (word not in WORDS_TO_IGNORE):
                    wordDict[word] = wordDict.get(word,0) + 1
                    emojis = emoji.emoji_list(word)
                    if emojis:
                        for emojiData in emojis:
                            actualEmoji = emojiData["emoji"]
                            emojiDict[actualEmoji] = emojiDict.get(actualEmoji, 0) + 1
        globalWordDict[member] = wordDict
        globalEmojiDict[member] = emojiDict
    return globalWordDict, globalEmojiDict


def mostMessagesByChatter(chat: Chat, wordList: list[str] = [], caseSensitive:bool=True) -> tuple[dict[Member, dict[str, int]], dict[Member, dict[str, int]]]:
    """
    Counts the number of messages said by each chatter.
    
    Returns:
        tuple ((dict,dict)): Two dict of dicts. The keys are of Member type and the values are str:int dicts.
        
        For the second dict, the str keys are strictly ones from the phrase list.
    """
    members = chat.members
    globalMessageDict = {}
    if wordList:
        wordListCount = {member.name : {m : 0 for m in wordList} for member in members}
    else:
        wordListCount = {}
    for member in members:
        mDict = {}
        messages = member.messages
        for message in messages:
            actualMessage = str(message.content)
            actualMessage = "".join(ch for ch in actualMessage if category(ch)[0] != "C")

            if not caseSensitive:
                actualMessage = actualMessage.lower()
            
            if actualMessage and (actualMessage not in MESSAGES_TO_IGNORE):
                if actualMessage not in mDict.keys():
                    mDict[actualMessage] = 1
                else:
                    mDict[actualMessage] += 1
            for word in wordList:
                if caseSensitive:
                    if word in actualMessage:
                        wordListCount[member.name][word] += 1
                else:
                    if word.lower() in actualMessage:
                        # print(word)
                        wordListCount[member.name][word] += 1
        globalMessageDict[member] = mDict
    return globalMessageDict, wordListCount


def getUncommonWordsPerChatter(wDict:dict) -> dict[str, list[tuple[str, float, int, int, float]]]:
    """
    Returns a dict with the five most "unique" words said by each chatter.
    
    The uniqueness factor is given by this formula:

    Uniqueness = (maxPctg - avPctg) / avPctg

    avPctg is the average of non-zero percentages (this is done to avoid rewarding words said by only one chatter)
    
    maxPctg corresponds to the highest percentage.

    Percentages are calculated normally: |times word is used| / |total words used|

    Returns:
        uniqueWordPerUser (dict): A dict whose keys are chat members, and whose values are lists of the 5 most unique words, with the following info: 
        [word, percentage of uniqueness, times the word was used, times the word was used by this chatter, percentage of times the chatter said the word]

    """

    # Can this function be changed to use IF-IDF instead? 
    # The benefits of the used formula is that it's descriptive. Can you reach a conclusion using only IF-IFD?
 
    pDict = {} # Proportion dict!
    for member, mwDict in wDict.items():
        n = len(mwDict)
        sDict = sorted(mwDict, key=mwDict.get)
        for word in sDict:
            proportion = mwDict[word] / member.m_ammount
            if word not in pDict.keys():
                pDict[word] = {member : proportion}
            else:
                pDict[word][member] = proportion
    rareList = []

    for word, mlist in pDict.items():
        maxMember = max(mlist, key=mlist.get)
        maxValue = mlist[maxMember]
        avPctg = 0
        for _, value in mlist.items():
            avPctg += value
        avPctg /= len(mlist)
        rarenessValue = (maxValue - avPctg) / avPctg
        rareList.append([word,maxMember,rarenessValue])
    rareList.sort(key=lambda x: x[2],reverse=True)
    uniqueWordPerUser = {}
    for rare in rareList:
        timesUsedTotal = sum(wDict[member].get(rare[0],0) for member in wDict.keys())
        timesUsedChatter = wDict[rare[1]][rare[0]]
        if rare[1].name not in uniqueWordPerUser.keys():
            uniqueWordPerUser[rare[1].name] = [(rare[0],rare[2]*100, timesUsedTotal, timesUsedChatter, (timesUsedChatter / timesUsedTotal) * 100)]
        elif len(uniqueWordPerUser[rare[1].name]) <= 5:
            uniqueWordPerUser[rare[1].name].append((rare[0],rare[2]*100, timesUsedTotal, timesUsedChatter, (timesUsedChatter / timesUsedTotal) * 100))
    return uniqueWordPerUser



def getUncommonMessagesPerChatter(mDict:dict) -> dict[str, list[tuple[str, float, int, int, float]]]:
    """
    Returns a dict with the five most "unique" messages said by each chatter.
    
    The uniqueness factor is given by this formula:

    Uniqueness = (maxPctg - avPctg) / avPctg

    avPctg is the average of non-zero percentages (this is done to avoid rewarding messages said by only one chatter)
    
    maxPctg corresponds to the highest percentage.

    Percentages are calculated normally: |times message is used| / |total messages used|

    Returns:
        uniqueMessagePerUser (dict): A dict whose keys are chat members, and whose values are lists of the 5 most unique messages, in the next order: 
        [percentage of uniqueness, times the message was used, times the message was used by this chatter, percentage of times the chatter said the message]

    """
    pDict = {} # Proportion dict!
    for member, mwDict in mDict.items():
        sDict = sorted(mwDict, key=mwDict.get)
        for word in sDict:
            proportion = mwDict[word] / member.m_ammount
            if word not in pDict.keys():
                pDict[word] = {member : proportion}
            else:
                pDict[word][member] = proportion
    rareList = []

    for word, mlist in pDict.items():
        maxMember = max(mlist, key=mlist.get)
        maxValue = mlist[maxMember]
        avPctg = 0
        for _, value in mlist.items():
            avPctg += value
        avPctg /= len(mlist)+1
        rarenessValue = (maxValue - avPctg) / avPctg
        rareList.append([word,maxMember,rarenessValue])
    rareList.sort(key=lambda x: x[2],reverse=True)
    uniqueMessagePerUser = {}
    for rare in rareList:
        timesUsedTotal = sum(mDict[member].get(rare[0],0) for member in mDict.keys())
        timesUsedChatter = mDict[rare[1]][rare[0]]
        if rare[1].name not in uniqueMessagePerUser.keys():
            uniqueMessagePerUser[rare[1].name] = [(rare[0],rare[2]*100, timesUsedTotal, timesUsedChatter, (timesUsedChatter / timesUsedTotal) * 100)]
        elif len(uniqueMessagePerUser[rare[1].name]) <= 5:
            uniqueMessagePerUser[rare[1].name].append((rare[0],rare[2]*100, timesUsedTotal, timesUsedChatter, (timesUsedChatter / timesUsedTotal) * 100))
    return uniqueMessagePerUser


def filterChatByTime(gc: Chat, dateStart: datetime, dateEnd: datetime) -> Chat:
    """
    Deprecated function, filters chat by two dates
    """
    for member in gc.members:
        newMessageList = []
        for message in member.messages:
            if (message.dtime >= dateStart) and (message.dtime <= dateEnd):
                newMessageList.append(message)
        gc.updateMessageListChat(msgl=newMessageList, member=member)
    return gc





def getTimeDicts(gc: Chat) -> tuple[dict[time,int], dict[str,dict[time,int]], 
                                    dict[datetime,int], dict[str,dict[datetime,int]], 
                                    dict[int,int], dict[str,dict[int,int]]]:
    '''
    wrapper function that calls all functions that return dicts.

    In order, these are: global minute ranking, personal minute ranking, global date ranking, personal date ranking, global hour ranking, personal hour ranking
    '''

    # Statistics variables are in snake_case because they're cuter that way (?
        
    messageList = []
    for member in gc.members:
        for message in member.messages:
            messageList.append((message.dtime, member.name))
        for action in member.actions:
            messageList.append((action.dtime, member.name))
    messageList.sort(key=lambda x:x[0])
    global_hm_ranking, global_h_ranking = getHourRanking(messageList=messageList)
    personal_hm_ranking = getHourAndMinuteRankingPerChatter(messageList)
    personal_h_ranking = getHourRankingPerChatter(messageList)
    global_date_ranking = getDayRanking(messageList)
    personal_date_ranking = getDayRankingPerChatter(messageList)
    return global_hm_ranking, personal_hm_ranking, global_date_ranking, personal_date_ranking, global_h_ranking, personal_h_ranking




def getHourRanking(messageList: list[tuple[datetime,str]]) -> tuple[dict[time,int], dict[int,int]]:
    hourAndMinutedict = {}
    hourDict = {}
    for element in messageList:
        elem_time = time(element[0].hour,element[0].minute)
        hourAndMinutedict[elem_time] = hourAndMinutedict.get(elem_time,0) + 1
        hourDict[elem_time.hour] = hourDict.get(elem_time.hour,0) + 1
    return hourAndMinutedict, hourDict

def getHourAndMinuteRankingPerChatter(messageList: list[tuple[datetime,str]]) -> dict[str,dict[time,int]]:
    time_dict = {}
    for element in messageList:
        elem_name = element[1]
        elem_time = time(element[0].hour,element[0].minute)
        if elem_name in time_dict.keys():
            time_dict[elem_name][elem_time] = time_dict[elem_name].get(elem_time,0) + 1
        else: time_dict[elem_name] = {}
    return time_dict

def getHourRankingPerChatter(messageList: list[tuple[datetime,str]]) -> dict[str,dict[int,int]]:
    time_dict = {}
    for element in messageList:
        elem_name = element[1]
        elem_time = element[0].hour
        if elem_name in time_dict.keys():
            time_dict[elem_name][elem_time] = time_dict[elem_name].get(elem_time,0) + 1
        else: time_dict[elem_name] = {}
    return time_dict

def getDayRanking(messageList: list[tuple[datetime,str]]) -> dict[datetime,int]:
    # Statistics variables are in snake_case because they're cuter that way (?
    date_dict = {}
    for element in messageList:
        elem_date = date(year=element[0].year, month=element[0].month, day=element[0].day)
        date_dict[elem_date] = date_dict.get(elem_date,0) + 1
    return date_dict

def getDayRankingPerChatter(messageList: list[tuple[datetime,str]]) -> dict[str,dict[datetime,int]]:
    date_dict = {}
    for element in messageList:
        elem_name = element[1]
        elem_date = date(element[0].year,element[0].month, element[0].day)
        if elem_name in date_dict.keys():
            date_dict[elem_name][elem_date] = date_dict[elem_name].get(elem_date,0) + 1
        else: date_dict[elem_name] = {}
    return date_dict

def getLongestStreak(messageList: list[tuple[datetime,str]]) -> tuple[datetime, datetime]:
    """
    Get the start and end date for the longest streak of consecutive messages in the chat.
    """

    # Statistics variables are in snake_case because they're cuter that way (?

    highest_first_day = current_first_day = messageList[0][0].date()
    highest_last_day = current_last_day = messageList[0][0].date()
    highest_streak = current_streak = 0

    for elem in messageList:
        
        date = elem[0].date()
        
        if date == current_last_day: continue

        elif date == (current_last_day + timedelta(days=1)):
            current_streak += 1
            current_last_day = date
        else:
            if current_streak > highest_streak:
                highest_streak = current_streak
                highest_first_day = current_first_day
                highest_last_day = current_last_day
            current_streak = 0
            current_first_day = date
            current_last_day = date     
    else:
        if current_streak > highest_streak:
            highest_streak = current_streak
            highest_first_day = current_first_day
            highest_last_day = current_last_day    
    
    return highest_first_day, highest_last_day

def getDayPercentage(messageList: list[tuple[datetime,str]], dStart:datetime, dEnd:datetime) -> float:
    """
    Get the percentage of days a message was sent.
    """
    day_begin = messageList[0][0]
    day_count = 1
    for message in messageList:
        date = message[0]
        if date.date() != day_begin.date():
            day_count += 1
            day_begin = date
    last_day = messageList[-1][0] if dEnd.date() == datetime.now().date() else dEnd
    lifespan = last_day - (messageList[0][0] if dStart.year == 2009 else dStart)
    return day_count / (lifespan.days + 1)

def getDayPercentagePerChatter(messageList: list[tuple[datetime,str]], dStart=datetime(2009,2,1), dEnd=datetime(2000,1,1)) -> dict[str,tuple[float,int]]:
    """
    Get the percentage of days each chatter has sent a message.
    """
    dayBegins = {}
    dayIter = {}
    dayBegins[messageList[0][1]] = messageList[0][0]
    dayCounts = {}
    dayCounts[messageList[0][1]] = 1
    for message in messageList:
        if message[0].date() != dayIter.get(message[1],datetime(1,1,1)).date():
            dayIter[message[1]] = message[0]
            if not dayBegins.get(message[1],0):
                dayBegins[message[1]] = message[0]
            dayCounts[message[1]] = dayCounts.get(message[1],0) + 1

    lastDay = messageList[-1][0] if dEnd.date() == datetime.now().date() else dEnd
    pctgDict = {}
    for member, count in dayCounts.items():
        chatspan:timedelta = lastDay - (dayBegins[member] if dStart.year == 2009 else dStart)
        pctgDict[member] = (count / (chatspan.days + 1), count)
    return pctgDict

def getTimeStats(gc:Chat, dateStart:datetime, dateEnd:datetime):
    """
    Wrapper function that gets other time statistics.
    """
    messageList = []
    for member in gc.members:
        for message in member.messages:
            messageList.append((message.dtime, member.name))
        for action in member.actions:
            messageList.append((action.dtime, member.name))
    messageList.sort(key=lambda x:x[0])
    dStart, dEnd = getLongestStreak(messageList=messageList)
    dayPctg = getDayPercentage(messageList, dateStart, dateEnd)
    pctgDict = getDayPercentagePerChatter(messageList, dateStart, dateEnd)
    return dStart, dEnd, dayPctg, pctgDict



if __name__ == "__main__":
    print("This shouldn't be run alone.")
    