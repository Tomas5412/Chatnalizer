# from chatparseados import messages #! Fill with the correct file
from data.classes import *

def splitDateNameByFormat(header: str, fType:FORMAT_TYPE):
    if fType == FORMAT_TYPE.ANDROID:
        return header.split("-",maxsplit=1)
    elif fType == FORMAT_TYPE.IPHONE:
        division = header[1:]
        return division.split("]",maxsplit=1)

def parseHeaderAndriod(dateDiv, nameDiv):
    day = ""
    day += (dateDiv[0])
    if dateDiv[1] in ["0","1","2","3","4","5","6","7","8","9"]: # ? I know how awful this is, but isDigit(dateDiv[1]) doesn't work.
        day += (dateDiv[1])
        dateDiv = dateDiv[3:]
    else: dateDiv = dateDiv[2:]

    month = ""
    month += (dateDiv[0])
    if dateDiv[1] in ["0","1","2","3","4","5","6","7","8","9"]: # ? I know how awful this is, but isDigit(dateDiv[1]) doesn't work.
        month += (dateDiv[1])
        dateDiv = dateDiv[3:]
    else: dateDiv = dateDiv[2:]

    year = dateDiv[0:4]
    hour = dateDiv[6:8]
    minute = dateDiv[9:11]


    name = nameDiv[1:-1]
    return day, month, year, hour, minute, name

def parseHeaderIphone(dateDiv, nameDiv):
    day = ""
    day += (dateDiv[0])
    if dateDiv[1] in ["0","1","2","3","4","5","6","7","8","9"]: # ? I know how awful this is, but isDigit(dateDiv[1]) doesn't work.
        day += (dateDiv[1])
        dateDiv = dateDiv[3:]
    else: dateDiv = dateDiv[2:]

    month = ""
    month += (dateDiv[0])
    if dateDiv[1] in ["0","1","2","3","4","5","6","7","8","9"]: # ? I know how awful this is, but isDigit(dateDiv[1]) doesn't work.
        month += (dateDiv[1])
        dateDiv = dateDiv[3:]
    else: dateDiv = dateDiv[2:]

    year = dateDiv[0:2]
    hour = dateDiv[4:6]
    minute = dateDiv[7:9]


    name = nameDiv[1:-1]
    return day, month, year, hour, minute, name



def parseHeader(header:str, fType:FORMAT_TYPE):
    divisions = splitDateNameByFormat(header,fType)
    fDiv = divisions[0]
    sDiv = divisions[1]
    if fType == FORMAT_TYPE.ANDROID:
        day, month, year, hour, minute, name = parseHeaderAndriod(fDiv, sDiv)
        return day, month, year, hour, minute, name
    else:
        day, month, year, hour, minute, name = parseHeaderIphone(fDiv, sDiv)
        return day, month, year, hour, minute, name



def parseMessage(message:str) -> str:
    # TODO: GET THIS TO WORK AAAAAAAAAAAAA
    return message


def parseChat(data):
    groupChat = Chat()

    # First message is always null, plus we copy messages because we don't want to mess with it I suppose?
    chat = data[1:]
    messageCounter = 0
    holaCounter = 0
    eventCounter = 0
    events = []
    format = FORMAT_TYPE.ANDROID
    if(chat[0][0] == "["): 
        print("USANDO FORMATO IPHONE ...")
        format = FORMAT_TYPE.IPHONE

    for i in range(0, len(chat), 2):
        header = chat[i]
        message = chat[i+1]
        if header[-1] == ":": 
            messageCounter += 1
            day, month, year, hour, minute, name = parseHeader(header, format)
            Pmessage = parseMessage(message)
            userId = groupChat.getOrMakeUserId(name)
            groupChat.addMessageChat(day, month, year, hour, minute, Pmessage, userId)
            if "hola" in message:
                holaCounter += 1

        else: 
            eventCounter += 1
            events.append(header)

    print(f"Se enviaron {messageCounter} mensajes, con {eventCounter} 'Eventos de chat'")

    mlist = groupChat.members
    for i in range(len(mlist)):
        user = mlist[i]
        print(f"{user.name} mandó {user.m_ammount} mensajes. Sus primeros dos mensajes fueron:")
        for j in range(2):
            msg = user.messages[j]
            print(f"{msg.day}/{msg.month}/{msg.year} {msg.hour}:{msg.minute} {user.name} - {msg.content}")



if __name__ == "__main__":
    parseChat(messages)