from misc.classes import *
from misc.keywords import SPANISH_KEYWORDS, AUTHOR_NAME
from datetime import datetime

def splitDateNameByFormat(header: str, fType:FORMAT_TYPE):
    match fType:
        case FORMAT_TYPE.ANDROID:
            return header.split("-",maxsplit=1)
        case FORMAT_TYPE.IPHONE:
            division = header[1:]
            if division[0] == "[": division = division[1:]
            return division.split("]",maxsplit=1)
        case FORMAT_TYPE.OLD:
            division = header[1:]
            if division[0] == "[": division = division[1:]
            return division.split("]",maxsplit=1)


def getAction(actionDiv:str, kwords):
    name = ""
    victim = ""
    aType = ActionType.OTHER

    # This could've been a nested loop of ActionTypes (with the kwords keys being ActionTypes values)
    # However, the parsing of names and victims is different according to each type of action.
    # ? Perhaps there's a way to make this a nested loop, in a way that doesn't make the code completely unreadable

    for kick in kwords["KICKED_MSG"]: 
        if kick in actionDiv:
                name = actionDiv.split(kick)[0]
                victim = actionDiv.split(kick)[1]
                aType = ActionType.REMOVAL

    for add in kwords["ADDED_MSG"]:
        if add in actionDiv:
            name = actionDiv.split(add)[0]
            victim = actionDiv.split(add)[1]
            if victim[-1] == ".": victim = victim[:-1] # Some addition messages add an ending point. This is annoying and will cause edge bugs
            aType = ActionType.ADDITION
        
    for pin in kwords["PIN_MSG"]:
        if pin in actionDiv:
            name = actionDiv.replace(pin,"")
            victim = ""
            aType = ActionType.PIN

    for im_ch in kwords["CHANGE_LOGO"]:
        if im_ch in actionDiv:
            name = actionDiv.replace(im_ch,"")
            victim = ""
            aType = ActionType.I_CHANGE

    for desc_ch in kwords["CHANGE_DESCRIPTION"]:
        if desc_ch in actionDiv:
            name = actionDiv.replace(desc_ch,"")
            victim = ""
            aType = ActionType.D_CHANGE

    for name_ch in kwords["CHANGE_NAME"]:
        if name_ch in actionDiv:
            name = actionDiv.split(name_ch)[0]
            victim = ""
            aType = ActionType.N_CHANGE

    for s_del in kwords["SELF_DELETION"]:
        if s_del in actionDiv:
            name = actionDiv.replace(s_del, "")
            victim = ""
            aType = ActionType.S_REMOVAL

    for s_add in kwords["SELF_ADDITION"]:
        if s_add in actionDiv:
            name = actionDiv.replace(s_add,"")
            victim = ""
            aType = ActionType.S_ADDITION

    ### AUTHOR's action

    for a_kw in kwords["AUTHOR_DELETING"]:
        if a_kw in actionDiv:
            name = AUTHOR_NAME
            victim = actionDiv.replace(a_kw,"")
            aType = ActionType.REMOVAL    

    for a_kw in kwords["AUTHOR_DELETION"]:
        if a_kw in actionDiv:
            name = actionDiv.replace(a_kw,"")
            victim = AUTHOR_NAME
            aType = ActionType.REMOVAL    
    
    for a_kw in kwords["AUTHOR_SELF_REMOVAL"]:
        if a_kw in actionDiv:
            name = AUTHOR_NAME
            victim = ""
            aType = ActionType.S_REMOVAL    

    for a_kw in kwords["AUTHOR_ADDITION"]:
        if a_kw in actionDiv:
            name = actionDiv.replace(a_kw,"")
            victim = AUTHOR_NAME
            aType = ActionType.ADDITION    

    for a_kw in kwords["AUTHOR_ADDITION_UNKNOWN"]:
        if a_kw in actionDiv:
            name = AUTHOR_NAME
            victim = ""
            aType = ActionType.S_ADDITION    

    for a_kw in kwords["AUTHOR_S_ADDITION"]:
        if a_kw in actionDiv:
            name = AUTHOR_NAME
            victim = ""
            aType = ActionType.S_ADDITION

    for a_kw in kwords["AUTHOR_ADDING"]:
        if a_kw in actionDiv:
            name = AUTHOR_NAME
            victim = actionDiv.replace(a_kw,"")
            aType = ActionType.ADDITION    

    for a_kw in kwords["AUTHOR_PIN"]:
        if a_kw in actionDiv:
            name = AUTHOR_NAME
            victim = ""
            aType = ActionType.PIN


    if name:
        while name[0] == " " or name[0] == "\u200e": # This causes edge bugs to anyone that has contacts with starting whitespaces.
            name = name[1:]         # These edge bugs don't matter because people that has contacts with starting whitespaces have worse problems in their lives.
    
    if name and name[-1] == "\n":
        name = name[:-1]

    if victim:
        while victim[0] == " " or victim[0] == "\u200e":
            victim = victim[1:]
    
    if victim and victim[-1] == "\n":
        victim = victim[:-1]

    return name, victim, aType


def parseActionAndriod(dateDiv:str, actionDiv:str, dType:DATE_TYPE=DATE_TYPE.DDMMYY, kwords:dict=SPANISH_KEYWORDS):
    dtime, _ = parseHeaderAndriod(dateDiv, dType=dType)
    name, victim, aType = getAction(actionDiv, kwords)
    return dtime, name, victim, aType


def parseHeaderAndriod(dateDiv, nameDiv="", dType:str= "DD/MM/YY"):
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

    name = nameDiv[1:-1] if nameDiv else ""

    if dType == DATE_TYPE.MMDDYY.value:
        return datetime(year=year, month=day, day=month, hour=hour, minute=minute), name
    else: return datetime(year=year, month=month, day=day, hour=hour, minute=minute), name

def parseHeaderIphone(dateDiv, nameDiv="", dType=DATE_TYPE.DDMMYY):
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


    name = nameDiv[1:-1] if nameDiv else ""

    if dType == DATE_TYPE.MMDDYY.value:
        return datetime(year=year, month=day, day=month, hour=hour, minute=minute), name
    else: return datetime(year=year, month=month, day=day, hour=hour, minute=minute), name

def parseHeaderOld(dateDiv, nameDiv="", dType=DATE_TYPE.DDMMYY):
    # print(dateDiv)
    hour = int(dateDiv[0:2])
    minute = int(dateDiv[3:5])

    dateDiv = dateDiv[7:]

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

    year = int(dateDiv[0:5])
    day = int(day)
    month = int(month)


    name = nameDiv[1:-1] if nameDiv else ""

    if dType == DATE_TYPE.MMDDYY.value:
        return datetime(year=year, month=day, day=month, hour=hour, minute=minute), name
    else: return datetime(year=year, month=month, day=day, hour=hour, minute=minute), name


def parseHeader(header:str, fType:FORMAT_TYPE, dtype:str):
    divisions = splitDateNameByFormat(header,fType)
    fDiv = divisions[0]
    sDiv = divisions[1]
    match fType:
        case FORMAT_TYPE.ANDROID:
            dtime, name = parseHeaderAndriod(fDiv, sDiv, dType=dtype)
            return dtime, name
        case FORMAT_TYPE.IPHONE:
            dtime, name = parseHeaderIphone(fDiv, sDiv, dType=dtype)
            return dtime, name
        case FORMAT_TYPE.OLD:
            dtime, name = parseHeaderOld(fDiv, sDiv, dType=dtype)
            return dtime, name

def parseAction(header:str, fType:FORMAT_TYPE=FORMAT_TYPE.ANDROID, dtype:str=DATE_TYPE.DDMMYY.value):
    divisions = splitDateNameByFormat(header,fType)
    fDiv = divisions[0]
    sDiv = divisions[1]
    match fType:
        case FORMAT_TYPE.ANDROID:
            dtime, name, victim, aType = parseActionAndriod(fDiv, sDiv, dType=dtype)
            return dtime, name, victim, aType
        case _:
            raise ValueError(f"Action found ({header}) in unsopported format type.")




    return 1,1,1,1,1,"",ActionType.PIN,None

def parseMessage(message:str, kwords:dict=SPANISH_KEYWORDS):
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
            parsedMsg = ""
    for kword in kwords["MEDIA_MSG"]:
        if kword in parsedMsg:
            #Found one!
            for type in MediaType:
                if type in FILENAME_EXTENSIONS:
                    for ext in FILENAME_EXTENSIONS[type]:
                        if ext in parsedMsg:
                            mType = type
                            parsedMsg = parsedMsg.replace(kword,"")
    return edited, deleted, mType, parsedMsg


def parseChat(data, dStart: datetime=datetime(2000,1,1), dEnd: datetime=datetime.now(), language:str="SPANISH", dateType: str="DD/MM/YY") -> Chat:
    groupChat = Chat()
    match language:
        case "SPANISH":
            languageDict = SPANISH_KEYWORDS
    # First message is always null?
    chat = data[1:]
    events = []
    format = FORMAT_TYPE.ANDROID
    if(chat[0][0] == "["): 
        if chat[0][2] == ":" or chat[0][3] == ":":
            print("USANDO FORMATO VIEJO ...")
            format = FORMAT_TYPE.OLD
        else:
            print("USANDO FORMATO IPHONE ...")
            format = FORMAT_TYPE.IPHONE

    for i in range(0, len(chat), 2):
        header = chat[i]
        message = chat[i+1]
        if header[-1] == ":": 
            dtime, name = parseHeader(header, format, dateType)
            if (dtime >= dStart) and (dtime <= dEnd):
                userId = groupChat.getOrMakeUserId(name)
                wE,wD,mType, Pmessage = parseMessage(message,languageDict)
                groupChat.addMessageChat(dtime, Pmessage, userId, wE, wD, mType)

        else:
            dtime, name, target, type = parseAction(header, format)
            if name:
                userId = groupChat.getOrMakeUserId(name)
                groupChat.addActionChat(dt=dtime,id=userId,atype=type,target=target)

    return groupChat


if __name__ == "__main__":
    print("This shouldn't be run alone.")