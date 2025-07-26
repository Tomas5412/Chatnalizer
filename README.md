# Chatnalizador

___

## Cómo ejecutar

Desde la carpeta inicial, correr:

```$ python .\src\app.py```

Y elegir el archivo que contenga el chat a analizar. El archivo **Debe ser** un archivo de texto .txt con codificación utf-8
___

## Patrones de hora detectados

- [DD/MM/YY, HH:MM]

- [HH:MM, DD/MM/YYYY]

- DD/MM/YYYY, HH:MM

___

## Incoherencias

Si un nombre de usuario lleva el caracter ":", los mensajes de ese usuario van a tener incoherencias. Se recomienda cambiar estos antes de usar el Chatnalizador

Idem con un nombre de usuario que por algún motivo malicioso tenga un fin de línea en su nombre.

Por supuesto que todos los mensajes que contengan algún patrón utilizado por el sistema tendrán incoherencias. En especial los mensajes que copian y pegan otros mensajes.
