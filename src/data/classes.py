from enum import Enum
from datetime import datetime

class FORMAT_TYPE(Enum):
    ANDROID = 0
    IPHONE = 1

class DATE_TYPE(Enum):
    MMDDYY = 0
    DDMMYY = 1

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


SPANISH_KEYWORDS = {
    "MEDIA_MSG" : ["(archivo adjunto)", "<adjunto:"],
    "OMMITED_MEDIA" : ["<Multimedia omitido>\n", "\u200eaudio omitido\n",
                        "\u200eimagen omitida\n", "\u200evideo omitido\n", "\u200esticker omitido\n"],
    "TEMPORAL_MEDIA" : ["null\n", 
                      "\u200eRecibiste un mensaje de visualización única. Para mayor privacidad, solo puedes abrirlo en tu teléfono.\n"],
    "OTHER_MEDIA" : [ "\u200eNo se puede mostrar este mensaje aquí. Para verlo, abre WhatsApp en tu teléfono.\n",
                     ],
    "DELETED_MSG" : ["Se eliminó este mensaje.\n", "\u200eSe eliminó este mensaje.\n"],
    "EDITED_MSG" : ["Se editó este mensaje."]
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

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.messages = []
        self.m_ammount = 0
        self.a_ammount = 0
        self.actions = []
        self.mediaSent = {type:0 for type in MediaType}
        self.deletedMessages = 0
        self.editedMessages = 0




class Chat:
    members: list[Member] = []

    def addMember(self, name: str) -> int:
        id = len(self.members)
        member = Member(id=id,name=name)
        self.members.append(member)
        return id

    def addMessageChat(self, dt, msg:str, id: int, wE: bool=False, wD: bool=False, mT=MediaType.NONE):
        message = Message(dt,content=msg, wE=wE, wD=wD, mT=mT)
        self.members[id].addMessageMember(message)

    def getOrMakeUserId(self, name:str):
        for i in range(len(self.members)):
            mmb = self.members[i]
            if mmb.name == name:
                return i
        id = self.addMember(name)
        return id