from enum import Enum
from datetime import datetime

class FORMAT_TYPE(Enum):
    ANDROID = 0
    IPHONE = 1
    OLD = -1

class DATE_TYPE(Enum):
    DDMMYY = "DD/MM/YY"
    MMDDYY = "MM/DD/YY"

class ActionType(Enum):
    ADDITION = "addition"
    S_ADDITION = "Self adition" #Addition of self via group link
    REMOVAL = "Removal"
    S_REMOVAL = "Self removal"
    D_CHANGE = "Description change"
    I_CHANGE = "Icon change"
    N_CHANGE = "Name change"
    PIN = "Pin"
    OTHER = "Other"

class MediaType(Enum):
    VIDEO = "video"
    PHOTO = "photo"
    STICKER = "sticker"
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

FILENAME_EXTENSIONS = {
    MediaType.STICKER : [".webp"],
    MediaType.AUDIO : [".opus", ".mp3"],
    MediaType.PHOTO : [".jpg",".png"],
    MediaType.VIDEO : [".mp4"],
    MediaType.GIF : [".gif"],

}



class Event:
    # This class belongs inside of Member.
    dtime : datetime

    def __init__(self, dt):
        self.dtime = dt
        


class Message(Event):
    content: str
    mType: MediaType = MediaType.NONE
    wasEdited: bool = False
    wasDeleted: bool = False

    def __init__(self, dt, content:str, wE: bool=False, wD: bool=False, mT=MediaType.NONE):
        Event.__init__(self, dt)
        self.content = content
        self.wasDeleted = wD
        self.wasEdited = wE
        self.mType = mT



class Action(Event):
    type: ActionType
    target: str = None

    def __init__(self, dt, type: ActionType, target: str=None):
        Event.__init__(self, dt)
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
    actionsDone: dict[ActionType, int]
    deletedMessages : int
    editedMessages : int

    def addMessageMember(self, msg:Message):
        self.m_ammount += 1
        self.messages.append(msg)
        if msg.mType != MediaType.NONE:
            self.mediaSent[msg.mType] += 1
        if msg.wasDeleted:
            self.deletedMessages += 1
        if msg.wasEdited:
            self.editedMessages += 1

    def addActionMember(self, act:Action):
        self.a_ammount += 1
        if act.type != ActionType.OTHER:
            self.actionsDone[act.type] += 1
        self.actions.append(act)

    # Deprecated function.
    def updateMessageListMember(self, msgl: list[Message]):
        del self.messages
        self.messages = msgl
        for type in MediaType: # Flush the MediaType dict.
            self.mediaSent[type] = 0
        self.editedMessages = 0
        self.deletedMessages = 0
    
        for msg in msgl:
            if msg.mType != MediaType.NONE:
                self.mediaSent[msg.mType] += 1
            if msg.wasDeleted:
                self.deletedMessages += 1
            if msg.wasEdited:
                self.editedMessages += 1
        self.m_ammount = len(msgl) # Refresh the message amount



    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.messages = []
        self.m_ammount = 0
        self.a_ammount = 0
        self.actions = []
        self.mediaSent = {type:0 for type in MediaType}
        self.actionsDone = {act:0 for act in ActionType}
        self.deletedMessages = 0
        self.editedMessages = 0




class Chat:
    members: list[Member]
    messageAmount: int
    events: list[Event]
    eventAmount: int

    def addMember(self, name: str) -> int:
        id = len(self.members)
        member = Member(id=id,name=name)
        self.members.append(member)
        return id

    def addMessageChat(self, dt, msg:str, id: int, wE: bool=False, wD: bool=False, mT=MediaType.NONE):
        message = Message(dt,content=msg, wE=wE, wD=wD, mT=mT)
        self.members[id].addMessageMember(message)
        self.messageAmount += 1

    # Deprecated function.
    def updateMessageListChat(self, msgl: list[Message], member: Member):
        self.messageAmount -= member.m_ammount
        member.updateMessageListMember(msgl)
        self.messageAmount += member.m_ammount

    def getOrMakeUserId(self, name:str):
        for i in range(len(self.members)):
            mmb = self.members[i]
            if mmb.name == name:
                return i
        id = self.addMember(name)
        return id
    
    def addActionChat(self, id: int, dt: datetime, atype: ActionType, target: str=None):
        act = Action(dt=dt, type=atype,target=target)
        self.members[id].addActionMember(act)
        self.eventAmount += 1
    
    def __init__(self):
        self.members = []
        self.messageAmount = 0
        self.events = []
        self.eventAmount = 0