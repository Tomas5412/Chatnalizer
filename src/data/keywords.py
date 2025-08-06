SPANISH_KEYWORDS = {
    "MEDIA_MSG" : ["(archivo adjunto)"],
    "OMMITED_MEDIA" : ["<Multimedia omitido>", "audio omitido", "imagen omitida", "video omitido", "sticker omitido",],
    "TEMPORAL_MEDIA" : ["null", 
                      "Recibiste un mensaje de visualización única. Para mayor privacidad, solo puedes abrirlo en tu teléfono."],
    "OTHER_MEDIA" : ["No se puede mostrar este mensaje aquí. Para verlo, abre WhatsApp en tu teléfono.",
                     ],
    "DELETED_MSG" : ["Se eliminó este mensaje."],
    "EDITED_MSG" : ["<Se editó este mensaje.>"]
}

FILENAME_EXTENSIONS = {
    "STICKER" : [".webp"],
    "AUDIO" : [".opus", ".mp3"],
    "PHOTO" : [".jpg",".png"],
    "VIDEO" : [".mp4"]

}


WORDS_TO_IGNORE = ["<multimedia","omitido>","null","omitido","omitida","sticker","audio","imagen","video","<se","mensaje.>","<adjunto:"]

MESSAGES_TO_IGNORE = ["imagen omitida", "audio omitido", "null", "<multimedia omitido>", "sticker omitido", "video omitido", "eliminaste este mensaje","ubicación en tiempo real compartida","esperando este mensaje"]