# CHATNALIZER

El chatnalizador analiza chats siguiendo el patrón **DD/MM/YYYY, HH:MM {Username}:**

[NUEVO] También detecta el patrón **[DD/MM/YY, HH:MM] {Username}:** que se usa en dispositivos de Apple (Mac y Apple)
___

## Cómo ejecutar

Desde la carpeta inicial, correr:

```$ python .\src\chatnalizer.py <ruta al archivo de texto>```

Donde la ruta tiene que ser el camino absoluto hacia el documento .txt
___

## Incoherencias conocidas

Si un nombre de usuario lleva el caracter ":", los mensajes de este usuario van a tener incoherencias. Se recomienda cambiar estos antes de usar el Chatnalizador

Idem con un nombre de usuario que por algún motivo tenga un fin de línea en su nombre.

Por supuesto que todos los mensajes que contengan algún patrón utilizado por el sistema tendrán incoherencias. En especial los mensajes que copian y pegan otros mensajes.
