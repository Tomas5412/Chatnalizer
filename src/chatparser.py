from data.classes import *
from datetime import datetime

def splitDateNameByFormat(header: str, fType:FORMAT_TYPE):
    if fType == FORMAT_TYPE.ANDROID:
        return header.split("-",maxsplit=1)
    elif fType == FORMAT_TYPE.IPHONE:
        division = header[1:]
        if division[0] == "[": division = division[1:]
        return division.split("]",maxsplit=1)

def parseHeaderAndriod(dateDiv, nameDiv, dType= DATE_TYPE.DDMMYY):
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

    year = int(dateDiv[0:4])
    hour = int(dateDiv[6:8])
    minute = int(dateDiv[9:11])

    day = int(day)
    month = int(month)
    # print(day, month, year, hour, minute)

    name = nameDiv[1:-1]
    if dType == DATE_TYPE.MMDDYY:
        return month, day, year, hour, minute, name
    else: return day, month, year, hour, minute, name

def parseHeaderIphone(dateDiv, nameDiv, dType=DATE_TYPE.DDMMYY):
    # print(dateDiv)
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

    year = int("20" + dateDiv[0:2]) #The Iphone functionality will break in 2100, Whoops!
    hour = int(dateDiv[4:6])
    minute = int(dateDiv[7:9])

    day = int(day)
    month = int(month)


    name = nameDiv[1:-1]

    if dType == DATE_TYPE.MMDDYY:
        return month, day, year, hour, minute, name
    else: return day, month, year, hour, minute, name


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



def parseMessage(message:str, kwords:dict=SPANISH_KEYWORDS):
    # TODO: GET THIS TO WORK AAAAAAAAAAAAA
    parsedMsg = message[1:]
    deleted = False
    edited = False
    mType = MediaType.NONE
    for kword in kwords["OMMITED_MEDIA"]:
        if parsedMsg == kword:
            mType = MediaType.OTHER
    for kword in kwords["DELETED_MSG"]:
        if parsedMsg == kword:
            deleted = True
            parsedMsg = ""
    for kword in kwords["EDITED_MSG"]:
        if kword in parsedMsg:
            edited = True
    for kword in kwords["TEMPORAL_MEDIA"]:
        if kword == parsedMsg:
            mType = MediaType.T_MEDIA
    for kword in kwords["MEDIA_MSG"]:
        if kword in parsedMsg:
            #Found one!
            for type in MediaType:
                if type in FILENAME_EXTENSIONS:
                    for ext in FILENAME_EXTENSIONS[type]:
                        if ext in parsedMsg:
                            mType = type
                            parsedMsg = parsedMsg[:-(len(kword)+1)]
    return edited, deleted, mType, parsedMsg


def parseChat(data, language:str="SPANISH"):
    groupChat = Chat()
    match language:
        case "SPANISH":
            languageDict = SPANISH_KEYWORDS
    # First message is always null
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
            dtime = datetime(day=day,month=month,year=year,hour=hour,minute=minute)
            wE,wD,mType, Pmessage = parseMessage(message,languageDict)
            userId = groupChat.getOrMakeUserId(name)
            groupChat.addMessageChat(dtime, Pmessage, userId, wE, wD, mType)

        else: 
            eventCounter += 1
            events.append(header)

    print(f"Se enviaron {messageCounter} mensajes, con {eventCounter} 'Eventos de chat'")
    print("="*70)
    mlist = groupChat.members
    for i in range(len(mlist)):
        user = mlist[i]
        print(f"{user.name} mandó {user.m_ammount} mensajes. Sus primeros dos mensajes fueron:")
        if user.m_ammount > 5:
            for j in range(2):
                msg = user.messages[j]
                print(f"{msg.dtime} {user.name} - {repr(msg.content)}")
        print(f"Este usuario eliminó {user.deletedMessages} mensajes y editó {user.editedMessages}.\n")
        print(user.mediaSent)
        print(f"Este usuario mandó {sum(user.mediaSent.values())} archivos multimedia. {user.mediaSent[MediaType.STICKER]} de ellos fueron stickers.")
        print("="*70)


if __name__ == "__main__":
    print("This shouldn't be ran alone.")
    # parseChat(messages)