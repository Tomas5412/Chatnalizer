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

LANGUAGES = ["ENGLISH","SPANISH","PORTUGUESE"]

APP_KEYWORDS = {
    "SPANISH" : {
        "change_language" : "Cambiar lenguaje",
        "get_file_button" : "Buscar Archivo",
        "analysis_button" : "Chatnalizar!",
        "analysis_complete" : "Chatnálisis completado!\nSe encuentra en ",
        "unsopported_language_warning" : "Todavía no hay soporte de Chatnálisis en español!\nEl resultado estará en inglés.",
        "unselected_file" : "No se eligió un archivo.",
        "ai_exclusion" : "Excluir a Meta AI",
        "file_display" : "Archivo: ",
        "date_start" : "Desde:",
        "date_end" : "Hasta:"

    },
    "ENGLISH" : {
        "change_language" : "Change language",
        "get_file_button" : "Get file",
        "analysis_button" : "Chatnalize!",
        "analysis_complete" : "Chatnalisis completed!\nRead it at ",
        "unsopported_language_warning" : "",
        "unselected_file" : "Please select a file.",
        "ai_exclusion" : "Exclude Meta AI",
        "file_display" : "File: ",
        "date_start" : "Since:",
        "date_end" : "Up to:"
    },
    "PORTUGUESE" : {
        "change_language" : "Alterar idioma",
        "get_file_button" : "Obter arquivo",
        "analysis_button" : "Chatnalisar!",
        "analysis_complete" : "Chatnálise concluída!\n Localizado em ",
        "unsopported_language_warning" : "Não há suporte em português!\nOs resultados serão em inglês.",
        "unselected_file" : "Selecione arquivo.",
        "ai_exclusion" : "Excluda Meta AI",
        "file_display" : "Arquivo: ",
        "date_start" : "De:",
        "date_end" : "Até:"
    }
}



WORDS_TO_IGNORE = ["<multimedia","omitido>","null","omitido","omitida","sticker","audio","imagen","video","<se","mensaje.>","<adjunto:","votos)"]

MESSAGES_TO_IGNORE = ["imagen omitida", "audio omitido", "null", "<multimedia omitido>", "sticker omitido", "video omitido", "eliminaste este mensaje","ubicación en tiempo real compartida","esperando este mensaje"]