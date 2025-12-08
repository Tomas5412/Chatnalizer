import numpy as np
import matplotlib.dates as mdates
import matplotlib.units as munits
import datetime
import matplotlib.pyplot as plt
from misc.classes import Chat, Member
from misc.keywords import LANGUAGES, GRAPHIC_KEYWORDS
from ChatFunctions.chatparser import parseChat
from chatparseados.sojaposting import messages

def makeMessagePie(gc: Chat, langage:str="SPANISH"):
    # plt.style.use('_mpl-gallery')
    x = []
    labels = []
    for member in gc.members:
        if member.m_ammount:
            x.append(member.m_ammount)
            labels.append(member.name)

    # colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))

    # plot
    fig, ax = plt.subplots()
    ax.pie(x, labels=labels, labeldistance=None, radius=3, center=(4, 4),
           wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=False)
    
    ax.legend(loc="upper left")

    ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
           ylim=(0, 8), yticks=np.arange(1, 8))

    plt.show()

def makeTimeStackplot(gc:Chat, language:str="SPANISH"):
    listsPerChatter:dict[str,tuple[list[datetime.date],list[int]]] = {}
    for member in gc.members:
        dateList = []
        messageCount = []
        member.messages.sort(key=lambda x:x.dtime) #Just in case! This should not matter
        for message in member.messages:
            date = message.dtime
            if date.date() in dateList:
                messageCount[-1] += 1
            else:
                dateList.append(date.date())
                messageCount.append(1)
        if (dateList and messageCount): listsPerChatter[member.name] = [dateList, messageCount]

    start = listsPerChatter[min(listsPerChatter, key=lambda x: listsPerChatter.get(x)[0][0])][0][0]
    end = listsPerChatter[max(listsPerChatter, key=lambda x: listsPerChatter.get(x)[0][0])][0][0]
    everyDateList = []
    for chatter, lists in listsPerChatter.items():
        fig, ax = plt.subplots()
        # time = np.arange(start, end, dtype='datetime64[D]')
        x, y = lists
        ax.plot(x, y)
        ax.set_title(chatter)
        plt.show()
        everyDateList.extend(x)
    everyDateList = np.unique(everyDateList)
    extendedMessageCount = {}
    for date in everyDateList:
        for chatter, lists in listsPerChatter.items():
            if chatter not in extendedMessageCount.keys(): extendedMessageCount[chatter] = []
            if lists[0] and lists[0][0] == date:
                extendedMessageCount[chatter].append(lists[1][0])
                lists[0] = lists[0][1:]
                lists[1] = lists[1][1:]
            else:
                extendedMessageCount[chatter].append(0)
    y = np.vstack([v for v in extendedMessageCount.values()])
    fig, ax = plt.subplots()
    ax.stackplot(everyDateList, y, labels=extendedMessageCount.keys())
    ax.legend(loc='upper left')
    plt.show()
    


if __name__ == "__main__":
    gc = parseChat(messages)
    
    makeMessagePie(gc)
    # makeTimeStackplot(gc)