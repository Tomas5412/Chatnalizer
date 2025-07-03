# CHATNALIZER

El chatnalizador analiza chats siguiendo el patrón 'DD/MM/YYYY, HH:MM {Username} [: | \n]' (es decir, o un : o un fin de linea)

[NUEVO] También detecta el patrón [DD/MM/YY, HH:MM] {Username}:

## Instrucciones de uso primitivos

Como el esqueleto de la aplicación no está desarrollado, se tiene que correr cada parte por separado.

1. Crear la carpeta chat y chatparseados
2. Extraer el .txt del chat en la carpeta chat
3. Escribir el nombre de este archivo en chatfetcher.py
4. Ejecutar chatfetcher.py desde la terminal, parado en ./Chatnalizer/src
5. Se puede comprobar que, si está la carpeta chatparseados, se creará el archivo {fileName}.py
6. En chatparser.py, completar el import comentado agreando el nombre del archivo (sin el .py)
7. Correr chatparser.py para obtener los siguientes resultados parciales: **Mensajes totales, mensajes por persona, dos mensajes de ejemplo.**

## Incoherencias conocidas

Si un nombre de usuario lleva el caracter ":", los mensajes de este usuario van a tener incoherencias. Se recomienda cambiar estos antes de usar el Chatnalizador

Idem con un nombre de usuario que por algún motivo tenga un fin de línea en su nombre.

Por supuesto que todos los mensajes que contengan el patrón DD/MM/YYYY HH:MM tendrán incoherencias.

Debido a cuestiones relacionadas al lenguaje del sistema, todavía no se puede separar los eventos (cambio de nombres, eliminaciones, agregaciones...)

TODO:

* ... Complete the proyect
* Add multiple language support.
