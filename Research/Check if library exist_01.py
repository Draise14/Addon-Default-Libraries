import bpy

for x in bpy.context.preferences.filepaths.asset_libraries.items():
    path = x[1].path 
    if path.endswith("Other"): #removes the last slash
        print("Found")
    else:
        print("Not found")