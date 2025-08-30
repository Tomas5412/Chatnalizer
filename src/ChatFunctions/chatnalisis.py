from misc.classes import Chat, datetime, Member
from misc.keywords import WORDS_TO_IGNORE, MESSAGES_TO_IGNORE
from unicodedata import category
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
        n = len(mwDict)
        # third_q = int(3*n/4) # Third quantile (Not useful anymore)
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

def getTimeStats(gc: Chat):
    messageList = []
    for member in gc.members:
        for message in member.messages:
            messageList.append((member.name, message.dtime))
        for action in member.actions:
            messageList.append((member.name, action.dtime))
    messageList.sort(key=lambda x:x[1])
    dStart, dEnd = getLongestStreak(messageList=messageList)


def getLongestStreak(messageList: list[tuple[datetime,str]]) -> tuple[datetime, datetime]:
    """
    Get the start and end date for the longest streak of consecutive messages in the chat.
    """
    current_day = messageList[0][0]
    
    return



if __name__ == "__main__":
    print("This shouldn't be run alone.")