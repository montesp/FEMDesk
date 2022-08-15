# UICmv

Dentro de la carpeta, este comando es para correr el proyecto:

```bash
  python EF.py
```
Para modificar la interfaz, ingresa en el modo designer con:

```bash
  designer
```

Dentro de la interfaz del diseñador guardas tus cambios en el archivo `interfaz.ui`  y con el siguiente comando lo transforma al archivo `interfaz.py`


```bash
  pyuic5 -x interfaz.ui -o interfaz.py
```