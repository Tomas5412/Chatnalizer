import numpy as np
import matplotlib.dates as mdates
import matplotlib.units as munits
import datetime
import matplotlib.pyplot as plt
from misc.classes import Chat, Member, MediaType
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
    ax.set_axis_off()
    plt.savefig("internal/messagePie.png",transparent=False)

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


    for chatter, lists in listsPerChatter.items():
        fig, ax = plt.subplots()
        x, y = lists
        start = x[0]
        end = x[-1]
        time = np.arange(start, end, dtype='datetime64[D]')
        extended_y = []
        for date in time:
            if x[0] == date:
                extended_y.append(y[0])
                y = y[1:]
                x = x[1:]
            else:
                extended_y.append(0)
        ax.plot(time, extended_y)
        ax.set_title(chatter)
        plt.tight_layout()
        ax.tick_params(axis='both', which='major', labelsize=8)
        plt.savefig(f"internal/{chatter}-time-stackplot.svg",transparent=False)

    start = listsPerChatter[min(listsPerChatter, key=lambda x: listsPerChatter.get(x)[0][0])][0][0]
    end = listsPerChatter[max(listsPerChatter, key=lambda x: listsPerChatter.get(x)[0][-1])][0][-1]

    time = np.arange(start, end, dtype='datetime64[D]')
    extendedMessageCount = {}
    for date in time:
        for chatter, lists in listsPerChatter.items():
            if chatter not in extendedMessageCount.keys(): extendedMessageCount[chatter] = []
            if lists[0] and lists[0][0] == date:
                extendedMessageCount[chatter].append(lists[1][0] + 1) # See below for the reason of the +1
                lists[0] = lists[0][1:]
                lists[1] = lists[1][1:]
            else:
                extendedMessageCount[chatter].append(1) # Technically incorrect, but if the value is zero then a line is not drawn and the result is ugly. This means all graphics are off by 1.
    y = np.vstack([v for v in extendedMessageCount.values()])
    fig, ax = plt.subplots()
    ax.stackplot(time, y, labels=extendedMessageCount.keys())
    ax.legend(loc='upper left')
    ax.tick_params(axis='both', which='major', labelsize=8)
    plt.tight_layout()
    plt.savefig("internal/total-time-stackplot.svg",transparent=False)
    
def mediaSentByChatter(gc: Chat, language:str="SPANISH"):
    for member in gc.members:
        x = []
        labels = []
        for m_type in MediaType:
            if member.mediaSent.get(m_type,0):
                x.append(member.mediaSent[m_type])
                # x[0] -= member.mediaSent[m_type]
                labels.append(m_type.value)
        
        if x and labels:
            fig, ax = plt.subplots()
            ax.pie(x, labels=labels, labeldistance=None, radius=3, center=(4, 4), wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=False)
    
            ax.legend(loc="upper left")

            ax.set_title(member.name)

            ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
                ylim=(0, 8), yticks=np.arange(1, 8))
            ax.set_axis_off()
            plt.savefig(f"internal/{member.name}-mediaSent.png",transparent=False)
            # plt.show()


if __name__ == "__main__":
    gc = parseChat(messages)
    
    mediaSentByChatter(gc)
    # makeTimeStackplot(gc)