from enum import Enum

class FORMAT_TYPE(Enum):
    ANDROID = 0
    IPHONE = 1

class ActionType(Enum):
    ADDITION = "addition" #Addition of other
    S_ADDITION = "s_addition" #Addition of self "via link"
    REMOVAL = "removal" #Removal of other
    S_REMOVAL = "s_removal" #Self removal
    D_CHANGE = "d_change" #Description change
    I_CHANGE = "i_change" #Icon change
    PIN = "pin"

class MediaType(Enum):
    VIDEO = "video"
    PHOTO = "photo"
    GIF = "gif" #pronounced with a hard G
    AUDIO = "audio"
    T_MEDIA = "t_media" #temporal media
    LOCATION = "location"
    SURVEY = "survey"
    EVENT = "event"
    OTHER = "other" #pdf, code, txt...
    NONE = "none"

# class MessageFlag(Enum):
#     NONE = 0
#     EDITED = 1
#     DELETED = 2
#     MEDIA = 3
#     MEDIA_EDITED = 4


class Event:
    # user: str 
    # This class belongs inside of Member.
    minute: int
    hour: int
    day: int
    month: int
    year: int

    def __init__(self, d, m, y,hour,minute):
        self.day = d
        self.month = m
        self.year = y
        self.hour = hour
        self.minute = minute
        


class Message(Event):
    content: str
    mType: MediaType = MediaType.NONE
    wasEdited: bool = False
    wasDeleted: bool = False

    def __init__(self, d, m, y,hour,minute, content:str, wE: bool=False, wD: bool=False, mT=MediaType.NONE):
        Event.__init__(self, d,m,y,hour,minute)
        self.content = content
        self.wasDeleted = wD
        self.wasEdited = wE
        self.mType = mT



class Action(Event):
    type: ActionType
    target: str = None

    def __init__(self, d, m, y,hour,minute, type: ActionType, target: str=None):
        Event.__init__(self, d,m,y,hour,minute)
        self.type = type
        self.target = target



class Member:
    id: int
    name: str
    m_ammount: int
    messages: list[Message]
    a_ammount: int
    actions: list[Action]
    mediaSent: dict[MediaType, int]

    def addMessageMember(self, msg:Message):
        self.m_ammount += 1
        self.messages.append(msg)
        if msg.mType != MediaType.NONE:
            self.mediaSent[msg.mType] += 1

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.messages = []
        self.m_ammount = 0
        self.a_ammount = 0
        self.actions = []
        self.mediaSent = {type:0 for type in MediaType}




class Chat:
    members: list[Member] = []

    def addMember(self, name: str) -> int:
        id = len(self.members)
        member = Member(id=id,name=name)
        self.members.append(member)
        return id

    def addMessageChat(self, d, m, y, hour, minute, msg:Message, id: int, wE: bool=False, wD: bool=False, mT=MediaType.NONE):
        message = Message(d,m,y,hour,minute,content=msg, wE=wE, wD=wD, mT=mT)
        self.members[id].addMessageMember(message)

    def getOrMakeUserId(self, name:str):
        for i in range(len(self.members)):
            mmb = self.members[i]
            if mmb.name == name:
                return i
        id = self.addMember(name)
        return id