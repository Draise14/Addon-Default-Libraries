import bpy
import os
import shutil

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



### SET NAME of library by path name iteratively 
# First check if it exists
for x in bpy.context.preferences.filepaths.asset_libraries.items():
    path = x[1].path 
    if path.endswith("Target"): 
        print("Found, will do nothing")
        variable = True
    else:
        print("Not found, let's register")
        variable = False

# Now that we did the check, we register it, or not. 
if variable == True:
    print("Already exists")
else: 
    print("Nope")
    bpy.ops.preferences.asset_library_add(directory=str(test_path)+'\\Target\\')        

bpy.ops.wm.save_userpref()