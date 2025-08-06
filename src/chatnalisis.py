from data.classes import Chat
from chatparser import parseChat
from data.keywords import WORDS_TO_IGNORE, MESSAGES_TO_IGNORE
from unicodedata import category

def mostWordsByChatter(chat: Chat):
    members = chat.members
    globalWordDict = {}
    for member in members:
        wordDict = {}
        messages = member.messages
        for message in messages:
            actualMessage = str(message.content)
            actualMessage = "".join(ch for ch in actualMessage if category(ch)[0] != "C")
            # print(actualMessage)
            actualMessage = actualMessage.split()
            for word in actualMessage:
                word = word.lower()
                if word not in WORDS_TO_IGNORE:
                    if word not in wordDict.keys():
                        wordDict[word] = 1
                    else:
                        wordDict[word] += 1
        globalWordDict[member] = wordDict
        # cleanWordDict = {k:v for k,v in wordDict.items() if v > 10}
        # print(wordDict)
        # sDict = sorted(cleanWordDict, key=cleanWordDict.get, reverse=True)
        # print(f"{"="*50} Messages by {member}:" + "="*50)
        # for item in sDict:
        #     print(f"({item}, {cleanWordDict[item]}, {(cleanWordDict[item] / chat.messageAmount):.5f})")
        # print("="*120)
    return globalWordDict


def mostMessagesByChatter(chat: Chat, wordList = []):
    members = chat.members
    globalMessageDict = {}
    if wordList:
        wordList = [m.lower() for m in wordList]
        wordListCount = {member.name : {m:0 for m in wordList} for member in members}
    for member in members:
        mDict = {}
        messages = member.messages
        for message in messages:
            actualMessage = str(message.content)
            actualMessage = "".join(ch for ch in actualMessage if category(ch)[0] != "C")
            actualMessage = actualMessage.lower()
            # print(actualMessage)
            if actualMessage not in MESSAGES_TO_IGNORE:
                if actualMessage not in mDict.keys():
                    mDict[actualMessage] = 1
                else:
                    mDict[actualMessage] += 1
            for word in wordList:
                if word in actualMessage:
                    wordListCount[member.name][word] += 1
        globalMessageDict[member] = mDict
        # cleanMDict = {k:v for k,v in mDict.items() if v > 5}
        # print(cleanMDict)
        # sDict = sorted(cleanMDict, key=cleanMDict.get, reverse=True)
        # print(f"{"="*50} Messages by {member.name}:" + "="*50)
        # for item in sDict:
        #     print(f"({item}, {cleanMDict[item]}, {(cleanMDict[item] / chat.messageAmount):.5f})")
        # print("="*120)
    return globalMessageDict, wordListCount


def getUncommonWordsPerChatter(wDict):
    pDict = {} # Proportion dict!
    for member, mwDict in wDict.items():
        n = len(mwDict)
        third_q = int(3*n/4) # Third quantile
        print(third_q, n)
        # cleanDict = {k:v for k,v in mwDict.items() if v > 10}
        sDict = sorted(mwDict, key=mwDict.get)
        for word in sDict[third_q:]:
            # print(value)
            proportion = mwDict[word] / member.m_ammount
            if word not in pDict.keys():
                pDict[word] = {member.name : proportion}
            else:
                pDict[word][member.name] = proportion

    rareList = []

    for word, mlist in pDict.items():
        maxMember = max(mlist, key=mlist.get)
        maxValue = mlist[maxMember]
        percentage = 1
        for otherMember, value in mlist.items():
            if maxValue > 0 and otherMember != maxMember:
                percentage -= value / maxValue
        if maxValue > 0:
            rareList.append([word,maxMember,maxValue])
    rareList.sort(key=lambda x: x[2],reverse=True)
    uniqueWordPerUser = {}
    for rare in rareList:
        if rare[1] not in uniqueWordPerUser.keys():
            uniqueWordPerUser[rare[1]] = (rare[0],rare[2])
    return uniqueWordPerUser


if __name__ == "__main__":
    print("This shouldn't be ran alone (and doesn't work)")
    # gc = parseChat(messages)
    # wordDict = mostWordsByChatter(gc)
    # messageDict, holaList = mostMessagesByChatter(gc,["hola","alta gracia"])
    # something = getUncommonWordsPerChatter(wordDict)
    # print(something)
    # print(holaList)
    # print(messageDict)