import os
from pathlib import Path

user_path = Path(bpy.utils.resource_path('USER')).parent
local_path = Path(bpy.utils.resource_path('LOCAL')).parent
system_path = Path(bpy.utils.resource_path('SYSTEM')).parent

print (user_path)
print (local_path)
print (system_path)

### ADD LIBRARIES, these can be based on relative paths from the installation
bpy.ops.preferences.asset_library_add(directory=str(local_path)+"\\customlibrary")
bpy.ops.preferences.asset_library_add(directory=str(local_path)+"\\anothercustomlibrary")



### SET NAME of library by path name iteratively 
for x in bpy.context.preferences.filepaths.asset_libraries.items():
    path = x[1].path 
    if path.endswith("\\"): #removes the last slash
        print(path.rstrip(path[-1])) #optional - just to see
        path = path.rstrip(path[-1]) #sets the path without the slash, useful for the next bit
    if x[0] != "": #skip if name not empty
        continue
    print(path.split("\\").pop()) #optional -  the last name of path
    library_name = path.split("\\").pop() # get the last name of the path
    x[1].name = library_name #set the name from the library_name


bpy.ops.wm.save_userpref()```

