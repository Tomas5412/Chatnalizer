from misc.classes import *
from misc.keywords import SPANISH_KEYWORDS, AUTHOR_NAME, ENGLISH_KEYWORDS, PORTUGUESE_KEYWORDS
from datetime import datetime
from unicodedata import category
from dateutil import parser
from time import time

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


def getAction(actionDiv:str, kwords:dict=SPANISH_KEYWORDS) -> tuple[str, str, ActionType]:
    name = ""
    victim = ""
    aType = ActionType.OTHER
    action = "".join(ch for ch in actionDiv if category(ch)[0] != "C")

    # This could've been a nested loop of ActionTypes (with the kwords keys being ActionTypes values)
    # However, the parsing of names and victims is different according to each type of action.
    # ? Perhaps there's a way to make this a nested loop, in a way that doesn't make the code completely unreadable

    for kick in kwords["KICKED_MSG"]: 
        if kick in action:
                name = action.split(kick)[0]
                victim = action.split(kick)[1]
                aType = ActionType.REMOVAL

    for add in kwords["ADDED_MSG"]:
        if add in action:
            selfless = False
            for selflessKw in kwords["ADDED_SELFLESS"]:
                if selflessKw in action:
                    selfless = True # Some additions don't register the adder. These ones will be ignored.
                    break
            if not selfless:
                name = action.split(add)[0]
                victim = action.split(add)[1]
                if victim[-1] == ".": victim = victim[:-1] # Some addition messages add an ending point. This is annoying and will cause edge bugs
                aType = ActionType.ADDITION
        
    for pin in kwords["PIN_MSG"]:
        if pin in action:
            name = action.replace(pin,"")
            victim = ""
            aType = ActionType.PIN

    for im_ch in kwords["CHANGE_LOGO"]:
        if im_ch in action:
            name = action.replace(im_ch,"")
            victim = ""
            aType = ActionType.I_CHANGE

    for desc_ch in kwords["CHANGE_DESCRIPTION"]:
        if desc_ch in action:
            name = action.replace(desc_ch,"")
            victim = ""
            aType = ActionType.D_CHANGE

    for name_ch in kwords["CHANGE_NAME"]:
        if name_ch in action:
            name = action.split(name_ch)[0]
            victim = ""
            aType = ActionType.N_CHANGE

    for s_del in kwords["SELF_DELETION"]:
        if s_del in action:
            name = action.replace(s_del, "")
            victim = ""
            aType = ActionType.S_REMOVAL

    for s_add in kwords["SELF_ADDITION"]:
        if s_add in action:
            name = action.replace(s_add,"")
            victim = ""
            aType = ActionType.S_ADDITION

    ### AUTHOR's action

    for a_kw in kwords["AUTHOR_DELETING"]:
        if a_kw in action:
            name = AUTHOR_NAME
            victim = action.replace(a_kw,"")
            aType = ActionType.REMOVAL    

    for a_kw in kwords["AUTHOR_DELETION"]:
        if a_kw in action:
            name = action.replace(a_kw,"")
            victim = AUTHOR_NAME
            aType = ActionType.REMOVAL    
    
    for a_kw in kwords["AUTHOR_SELF_REMOVAL"]:
        if a_kw in action:
            name = AUTHOR_NAME
            victim = ""
            aType = ActionType.S_REMOVAL    

    for a_kw in kwords["AUTHOR_ADDITION"]:
        if a_kw in action:
            name = action.replace(a_kw,"")
            victim = AUTHOR_NAME
            aType = ActionType.ADDITION    

    for a_kw in kwords["AUTHOR_ADDITION_UNKNOWN"]:
        if a_kw in action:
            name = AUTHOR_NAME
            victim = ""
            aType = ActionType.S_ADDITION    

    for a_kw in kwords["AUTHOR_S_ADDITION"]:
        if a_kw in action:
            name = AUTHOR_NAME
            victim = ""
            aType = ActionType.S_ADDITION

    for a_kw in kwords["AUTHOR_ADDING"]:
        if a_kw in action:
            name = AUTHOR_NAME
            victim = action.replace(a_kw,"")
            aType = ActionType.ADDITION    

    for a_kw in kwords["AUTHOR_PIN"]:
        if a_kw in action:
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
    dtime, _ = parseDate(dateDiv, dType=dType)
    name, victim, aType = getAction(actionDiv, kwords)
    return dtime, name, victim, aType


def parseDate(dateDiv,nameDiv="",dType:str= "DD/MM/YY"):
    dayFirst = dType == "DD/MM/YY"
    date = parser.parse(dateDiv,dayfirst=dayFirst) #! Here's the perfomance bottleneck
    name = nameDiv[1:-1] if nameDiv else ""
    return date, name


def parseHeader(header:str, fType:FORMAT_TYPE, dtype:str):
    divisions = splitDateNameByFormat(header,fType)
    fDiv = divisions[0]
    sDiv = divisions[1]
    name = ""
    dtime = ""
    dtime, name = parseDate(fDiv, sDiv,dType=dtype)
    name = "".join(ch for ch in name if category(ch)[0] != "C")
    return dtime, name


def parseAction(header:str, fType:FORMAT_TYPE=FORMAT_TYPE.ANDROID, dtype:str=DATE_TYPE.DDMMYY.value, kwords=SPANISH_KEYWORDS):
    divisions = splitDateNameByFormat(header,fType)
    fDiv = divisions[0]
    sDiv = divisions[1]
    match fType:
        case FORMAT_TYPE.ANDROID:
            dtime, name, victim, aType = parseActionAndriod(fDiv, sDiv, dType=dtype, kwords=kwords)
            return dtime, name, victim, aType
        case _:
            raise ValueError(f"Action found ({header}) in unsopported format type.")




    return 1,1,1,1,1,"",ActionType.PIN,None

def parseMessage(message:str, kwords:dict=SPANISH_KEYWORDS):
    parsedMsg = message[1:]
    parsedMsg = "".join(ch for ch in parsedMsg if category(ch)[0] != "C")
    deleted = False
    edited = False
    mType = MediaType.NONE
    for kword in kwords["OMMITED_MEDIA"]:
        if parsedMsg in kword:
            mType = MediaType.OTHER
            parsedMsg = ""
            break
    for kword in kwords["DELETED_MSG"]:
        if parsedMsg == kword:
            deleted = True
            parsedMsg = ""
            break
    for kword in kwords["EDITED_MSG"]:
        if kword in parsedMsg:
            edited = True
            break
    for kword in kwords["TEMPORAL_MEDIA"]:
        if kword == parsedMsg:
            mType = MediaType.T_MEDIA
            parsedMsg = ""
            break
    for kword in kwords["MEDIA_MSG"]:
        if kword in parsedMsg:
            #Found one!
            for type in MediaType:
                if type in FILENAME_EXTENSIONS:
                    for ext in FILENAME_EXTENSIONS[type]:
                        if ext in parsedMsg:
                            mType = type
                            parsedMsg = parsedMsg.replace(kword,"")
                            break
            break

    for kword in kwords["SELF_DELETED_MSG"]:
        if kword == parsedMsg:
            deleted = True
            parsedMsg = ""
    return edited, deleted, mType, parsedMsg


def parseChat(data, dStart: datetime=datetime(2000,1,1), dEnd: datetime=datetime.now(), language:str="SPANISH", dateType: str="DD/MM/YY") -> Chat:
    start = time()
    groupChat = Chat()
    match language:
        case "SPANISH":
            languageDict = SPANISH_KEYWORDS
        case "ENGLISH":
            languageDict = ENGLISH_KEYWORDS
        case "PORTUGUESE":
            languageDict = PORTUGUESE_KEYWORDS

    # First message is always null?
    chat = data[1:]
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
                wE,wD, mType, Pmessage = parseMessage(message,languageDict)
                groupChat.addMessageChat(dtime, Pmessage, userId, wE, wD, mType)

        else:
            dtime, name, target, type = parseAction(header, format, kwords=languageDict)
            if name and (dtime >= dStart) and (dtime <= dEnd):
                userId = groupChat.getOrMakeUserId(name)
                groupChat.addActionChat(dt=dtime,id=userId,atype=type,target=target)
    parsingTime = time() - start
    print(f"Chat parsing completed! It took {parsingTime}.")
    return groupChat


if __name__ == "__main__":
    print("This shouldn't be run alone.")