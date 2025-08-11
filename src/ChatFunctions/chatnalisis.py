from misc.classes import Chat, datetime
from misc.keywords import WORDS_TO_IGNORE, MESSAGES_TO_IGNORE
from unicodedata import category
import emoji

def mostWordsByChatter(chat: Chat):
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
                word = word.lower()
                if word and word not in WORDS_TO_IGNORE:
                    wordDict[word] = wordDict.get(word,0) + 1
                    emojis = emoji.emoji_list(word)
                    if emojis:
                        for emojiData in emojis:
                            actualEmoji = emojiData["emoji"]
                            emojiDict[actualEmoji] = emojiDict.get(actualEmoji, 0) + 1
        globalWordDict[member] = wordDict
        globalEmojiDict[member] = emojiDict
    return globalWordDict, globalEmojiDict


def mostMessagesByChatter(chat: Chat, wordList = []):
    members = chat.members
    globalMessageDict = {}
    if wordList:
        wordList = [m.lower() for m in wordList]
        wordListCount = {member.name : {m:0 for m in wordList} for member in members}
    else:
        wordListCount = {}
    for member in members:
        mDict = {}
        messages = member.messages
        for message in messages:
            actualMessage = str(message.content)
            actualMessage = "".join(ch for ch in actualMessage if category(ch)[0] != "C")
            actualMessage = actualMessage.lower()
            if actualMessage and actualMessage not in MESSAGES_TO_IGNORE:
                if actualMessage not in mDict.keys():
                    mDict[actualMessage] = 1
                else:
                    mDict[actualMessage] += 1
            for word in wordList:
                if word in actualMessage:
                    wordListCount[member.name][word] += 1
        globalMessageDict[member] = mDict
    return globalMessageDict, wordListCount


def getUncommonWordsPerChatter(wDict):
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



def getUncommonMessagesPerChatter(mDict):
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
    uniqueWordPerUser = {}
    for rare in rareList:
        timesUsedTotal = sum(mDict[member].get(rare[0],0) for member in mDict.keys())
        timesUsedChatter = mDict[rare[1]][rare[0]]
        if rare[1].name not in uniqueWordPerUser.keys():
            uniqueWordPerUser[rare[1].name] = [(rare[0],rare[2]*100, timesUsedTotal, timesUsedChatter, (timesUsedChatter / timesUsedTotal) * 100)]
        elif len(uniqueWordPerUser[rare[1].name]) <= 5:
            uniqueWordPerUser[rare[1].name].append((rare[0],rare[2]*100, timesUsedTotal, timesUsedChatter, (timesUsedChatter / timesUsedTotal) * 100))
    return uniqueWordPerUser


# Deprecated!
def filterChatByTime(gc: Chat, dateStart: datetime, dateEnd: datetime) -> Chat:
    for member in gc.members:
        newMessageList = []
        for message in member.messages:
            if (message.dtime >= dateStart) and (message.dtime <= dateEnd):
                newMessageList.append(message)
        gc.updateMessageListChat(msgl=newMessageList, member=member)
    return gc


if __name__ == "__main__":
    print("This shouldn't be run alone.")