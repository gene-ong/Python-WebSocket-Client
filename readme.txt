To create a .exe file from python script (.py), make sure that pyinstaller is installed (pip install pyinstaller), then perform the following in a cmd prompt -

Pyinstaller -w -F -i [icon file location] [you_python_file]
-w  removes window
-F  only makes one .exe file
-I  adds icon association to .exe, file must be a .ico (find some http://goo.gl/EfpGDo)

ToDO:
- update to work with 1664 pixel matrix