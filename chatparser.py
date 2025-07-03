from chatparseados.SojapostingT import messages
from data.classes import *

# First message is always null, plus we copy messages because we don't want to mess with it I suppose?



def parseHeader(header:str):
    divisions = header.split(",")
    m_date = divisions[0]

    day = ""
    day += (m_date[0])
    if m_date[1] in ["0","1","2","3","4","5","6","7","8","9"]: # I know how awful this is
        day += (m_date[1])
        m_date = m_date[3:]
    else: m_date = m_date[2:]

    month = ""
    month += (m_date[0])
    if m_date[1] in ["0","1","2","3","4","5","6","7","8","9"]: # I know how awful this is
        month += (m_date[1])
        m_date = m_date[3:]
    else: m_date = m_date[2:]
    year = m_date

    hourAndName = ""
    for j in range(1,len(divisions)):
        hourAndName += divisions[j]
    hourAndName = hourAndName.split("-",1)
    hour = hourAndName[0]
    name = hourAndName[1]
    hour = hour[1:-1]
    hour = hour.split(":")
    name = name[1:-1]
    return day, month, year, hour[0], hour[1], name

def parseMessage(message:str) -> str:
    # TODO: GET THIS TO WORK AAAAAAAAAAAAA
    return message


def parseChat(data):
    groupChat = Chat()

    chat = data[1:]
    messageCounter = 0
    holaCounter = 0
    eventCounter = 0
    events = []

    for i in range(0, len(chat), 2):
        header = chat[i]
        message = chat[i+1]
        if header[-1] == ":": 
            messageCounter += 1
            day, month, year, hour, minute, name = parseHeader(header)
            Pmessage = parseMessage(message)
            userId = groupChat.getOrMakeUserId(name)
            groupChat.addMessageChat(day, month, year, hour, minute, Pmessage, userId)
            if "hola" in message:
                holaCounter += 1

        else: 
            eventCounter += 1
            events.append(header)

    print(messageCounter, eventCounter)

    mlist = groupChat.members
    for i in range(len(mlist)):
        user = mlist[i]
        print(f"{user.name} mandó {user.m_ammount} mensajes")
        # for j in range(3):
        #     msg = user.messages[j]
        #     print(msg.day, msg.month, msg.year, msg.hour, msg.minute, msg.content)
    # print(events)



if __name__ == "__main__":
    parseChat(messages)