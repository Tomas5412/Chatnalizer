
SPANISH_KEYWORDS = {
    # Message stuff
    "MEDIA_MSG" : ["(archivo adjunto)"],
    "OMMITED_MEDIA" : ["<Multimedia omitido>", "audio omitido", "imagen omitida", "video omitido", "sticker omitido",],
    "TEMPORAL_MEDIA" : ["null", 
                      "Recibiste un mensaje de visualización única. Para mayor privacidad, solo puedes abrirlo en tu teléfono.",""],
    "OTHER_MEDIA" : ["No se puede mostrar este mensaje aquí. Para verlo, abre WhatsApp en tu teléfono.",
                     ],
    "DELETED_MSG" : ["Se eliminó este mensaje."],
    "SELF_DELETED_MSG" : ["Eliminaste este mensaje."],
    "EDITED_MSG" : ["<Se editó este mensaje.>"],
    # Action stuff
    "KICKED_MSG" : [" eliminó a "],
    "ADDED_MSG" : [" añadió a "],
    "ADDED_SELFLESS" : ["Se añadió a "],
    "PIN_MSG" : [" fijó un mensaje."],
    "CHANGE_LOGO" : [" cambió el ícono de este grupo"],
    "CHANGE_NAME" : [" cambió el nombre del grupo de "],
    "CHANGE_DESCRIPTION" : [" cambió la descripción del grupo."],
    "SELF_ADDITION" : [" se unió usando el enlace de invitación de este grupo"],
    "SELF_DELETION" : [" salió del grupo."],
    ## The "Author" is the one that exported the chat: their actions are in first person.
    "AUTHOR_DELETING" : ["Eliminaste a "],
    "AUTHOR_DELETION" : [" te eliminó."],
    "AUTHOR_SELF_REMOVAL" : ["Saliste del grupo"],
    "AUTHOR_ADDITION" : [" te añadió"],
    "AUTHOR_ADDITION_UNKNOWN" : ["Se te añadió al grupo."],
    "AUTHOR_S_ADDITION" : ["Te uniste mediante el enlace de invitación de este grupo."],
    "AUTHOR_ADDING": ["Añadiste a "],
    "AUTHOR_PIN" : ["Fijaste un mensaje."],
}

ENGLISH_KEYWORDS = {
    # Message stuff
    "MEDIA_MSG" : ["(file attached)"],
    "OMMITED_MEDIA" : ["<Media omitted>","<media omitted>", "<Media omitted>"],
    "TEMPORAL_MEDIA" : ["", "<media omitted>"],
    "OTHER_MEDIA" : [],
    "DELETED_MSG" : ["This message was deleted"],
    "SELF_DELETED_MSG" : ["You deleted this message"],
    "EDITED_MSG" : ["<This message was edited>"],
    # Action stuff
    "KICKED_MSG" : ["  removed "],
    "ADDED_MSG" : [" added "],
    "ADDED_SELFLESS" : [],
    "PIN_MSG" : [" pinned a message"],
    "CHANGE_LOGO" : [" changed this group's icon"],
    "CHANGE_NAME" : [" changed the group name from "],
    "CHANGE_DESCRIPTION" : [" changed the group description"],
    "SELF_ADDITION" : [" joined using this group's invite link"],
    "SELF_DELETION" : [" left"],
    ## The "Author" is the one that exported the chat: their actions are in first person.
    "AUTHOR_DELETING" : ["You removed "],
    "AUTHOR_DELETION" : [" removed you"],
    "AUTHOR_SELF_REMOVAL" : ["You left"],
    "AUTHOR_ADDITION" : [" added you"],
    "AUTHOR_ADDITION_UNKNOWN" : ["You were added"],
    "AUTHOR_S_ADDITION" : ["You joined using this group's invite link"],
    "AUTHOR_ADDING": ["You added "],
    "AUTHOR_PIN" : ["You pinned a message"],
}

PORTUGUESE_KEYWORDS = {
    # Message stuff
    "MEDIA_MSG" : ["(arquivo anexado)"],
    "OMMITED_MEDIA" : ["<Mídia oculta>"],
    "TEMPORAL_MEDIA" : [""],
    "OTHER_MEDIA" : [],
    "DELETED_MSG" : ["Mensagem apagada"],
    "SELF_DELETED_MSG" : [], # Portuguese doesn't distinguish
    "EDITED_MSG" : ["<Mensagem editada>"],
    # Action stuff
    "KICKED_MSG" : [" removeu "],
    "ADDED_MSG" : [" adicionou "],
    "ADDED_SELFLESS" : [],
    "PIN_MSG" : [" fixou uma mensagem"],
    "CHANGE_LOGO" : [" mudou a imagem deste grupo."],
    "CHANGE_NAME" : [" mudou o nome do grupo de "],
    "CHANGE_DESCRIPTION" : [" mudou a descrição do grupo"],
    "SELF_ADDITION" : [" entrou usando o link de convite deste grupo"],
    "SELF_DELETION" : [" saiu"],
    ## The "Author" is the one that exported the chat: their actions are in first person.
    "AUTHOR_DELETING" : ["Você removeu "],
    "AUTHOR_DELETION" : [" removeu você"],
    "AUTHOR_SELF_REMOVAL" : ["Você saiu"],
    "AUTHOR_ADDITION" : [" adicionou você"],
    "AUTHOR_ADDITION_UNKNOWN" : ["Você foi adicionado(a)"],
    "AUTHOR_S_ADDITION" : ["Você entrou usando o link de convite do grupo"],
    "AUTHOR_ADDING": ["Você adicionou "],
    "AUTHOR_PIN" : ["Você fixou uma mensagem"],
}


            # The "Author" is the one that exported the chat: their actions are in first person.
AUTHOR_NAME = "AUTHOR RAAAAAAAAAA" 
            # ... the scream is there to avoid name conflicts, since "AUTHOR" could be a valid contact name.


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
        "media_warning" : "Actual media files not required.\nOnly that it was exported with media.",
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

GRAPHIC_KEYWORDS = []

META_AI_NAME = "Meta AI"

WORDS_TO_IGNORE = ["<multimedia","omitido>","null","omitido","omitida","sticker","audio","imagen","video","<se","mensaje.>","<adjunto:","votos)"]

MESSAGES_TO_IGNORE = ["imagen omitida", "audio omitido", "null", "<multimedia omitido>", "sticker omitido", "video omitido", "eliminaste este mensaje","ubicación en tiempo real compartida","esperando este mensaje"]

COLORS = [
    (0xFF,0,0),
    (0xFF,0x87,0),
    (0xFF,0xD3,0),
    (0xDE,0xFF,0x0A),
    (0xA1,0xFF,0x0A),
    (0x0A,0xFF,0x99),
    (0x0A,0xEF,0xFF),
    (0x14,0x7D,0xF5),
    (0X58,0x0a,0xff),
    (0xbe,0x0a,0xff)
]