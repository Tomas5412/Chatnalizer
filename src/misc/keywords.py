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
        "date_end" : "Hasta:",
        "analyzing" : "...Chatnalizando...",
        "date_format" : "Formato de fecha",
        "word_list_add" : "Añadir",
        "word_list_show" : "Editar lista",
        "no_word" : "La lista de frases está vacía.",
        "destroy" : "Borrar",
        "case_sensitive" : "Distinguir mayús. de minús.",
        "include_media" : "Incluir análisis de media",
        "media_warning" : "No se requieren los archivos.\nSolo que se haya exportado con media.",
        "list_explainer" : "Cuenta la cantidad de veces\nque cada miembro dice la frase o palabra."


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
        "date_end" : "Up to:",
        "analyzing" : "...Chatnalizing...",
        "date_format" : "Date format",
        "word_list_add" : "Add",
        "word_list_show" : "Edit list",
        "no_word" : "No phrase in phrase list.",
        "destroy" : "Delete",
        "case_sensitive" : "Case sensitive",
        "include_media" : "Include media analysis",
        "media_warning" : "Actual files not required.\nOnly that it was exported with media.",
        "list_explainer" : "Counts the number of times\neach member says the phrase or word."
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
        "date_end" : "Até:",
        "analyzing" : "...Chatnalisando...",
        "date_format" : "Formato de data",
        "word_list_add" : "Adicionar",
        "word_list_show" : "Editar lista",
        "no_word" : "A lista de frases está vazia",
        "destroy" : "Excluir",
        "case_sensitive" : "Distingue maiús. de minús.",
        "include_media" : "Incluir análise de mídia",
        "media_warning" : "Os arquivos não são necessários.\nBasta que tenham sido exportados con a mídia.",
        "list_explainer" : "Conta o número de vezes\nque cada membro diz a frase ou palavra."
    }
}



WORDS_TO_IGNORE = ["<multimedia","omitido>","null","omitido","omitida","sticker","audio","imagen","video","<se","mensaje.>","<adjunto:","votos)"]

MESSAGES_TO_IGNORE = ["imagen omitida", "audio omitido", "null", "<multimedia omitido>", "sticker omitido", "video omitido", "eliminaste este mensaje","ubicación en tiempo real compartida","esperando este mensaje"]