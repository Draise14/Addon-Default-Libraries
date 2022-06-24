import bpy

import requests

url = 'https://github.com/Draise14/Addon-Default-Libraries/raw/main/DEFAULT_LIBRARY.blend'

myfile = requests.get(url)

open('C:////Users//drais//Downloads/DEFAULT_LIBRARY.blend', 'wb').write(myfile.content)

print("Downloaded")