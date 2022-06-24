# Copy a file to a destination with shutil.copy()
import bpy
import shutil
import os
from pathlib import Path

# System Paths for later
user_path = Path(bpy.utils.resource_path('USER')).parent
local_path = Path(bpy.utils.resource_path('LOCAL')).parent
system_path = Path(bpy.utils.resource_path('SYSTEM')).parent

test_path = Path('E:\\\\3D stuff\\Bforartists\\Development\\Addons\\Addon-Default-Libraries\\')


print (user_path)
print (local_path)
print (system_path)
print (test_path)

shutil.copy(str(test_path)+'\\DEFAULT_LIBRARY.blend', str(test_path)+'\\Target\\')
shutil.copy(str(test_path)+'\\blender_assets.cats.txt', str(test_path)+'\\Target\\')

print("Copied")
