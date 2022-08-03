# ##### BEGIN GPL LICENSE BLOCK #####
#
#  <Template script for an asset library addon. Download and instructions on my GitHub page.>
#    Copyright (C) <2022>  <Blender Defender> <https://www.github.com/BlenderDefender>
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# -----------------------------------------------------------------------------
# ! IMPORTANT! READ THIS WHEN SETTING UP THE LIBRARY
# This template can be used for your free and commercial asset libraries, according to the GPL.
# After you have created your asset files and downloaded this template, do the following steps:
# 1. Make sure that this file is called __init__.py It MUST be this exact name.
# 2. Create a folder named however you like. A pattern like asset-library-name is recommended.
# 3. Replace the addon name [Asset Library Name] in line 47 and 59 with your library name.
# 4. Replace the author [Your Name] in line 48 with your name or pseudonym.
# 5. Add a link to the documentation of your library in line 51 and for reporting issues in line 52
# 6. (Optional, recommended) Implement Super Addon Manager to support automatic updates.
#    To do this, follow the documentation found at https://www.example.com/todo and paste the Endpoint URL
#    in line 54
# -----------------------------------------------------------------------------

import bpy
from bpy.types import (
    AddonPreferences,
    Context,
    Preferences,
    UILayout,
)

from os import path as p

bl_info = {
    "name": "Bforartists Default Asset Library",
    "author": "Draise",
    "version": (1, 0, 0),
    "blender": (3, 2, 1),
    "doc_url": "",
    "tracker_url": "",
    # Please go to https://www.example.com/todo to implement support for automatic library updates:
    "endpoint_url": "",
    "category": "Import-Export"
}

# Configure the display name of your Library here:
LIB_NAME = "Target"


# Custom Paths
user_path = Path(bpy.utils.resource_path('USER')).parent
local_path = Path(bpy.utils.resource_path('LOCAL')).parent
system_path = Path(bpy.utils.resource_path('SYSTEM')).parent



# Running code, don't change if not necessary!
# -----------------------------------------------------------------------------

# # safe_bl_idname = re.sub("\s", "_", re.sub("[^\w\s]", "", LIB_NAME)).lower()


class LIBADDON_APT_preferences(AddonPreferences):
    bl_idname = __package__

    def draw(self, context: Context):
        layout: UILayout = self.layout

        # Display addon inormation: Library name and Version.
        addon_version = bl_info['version']

        layout.label(
            text=f"{LIB_NAME} - Version {'.'.join(map(str, addon_version))}")

        # Make sure, Super Addon Manager is supported with the current addon before showing the notice.
        # is_sam = "endpoint_url" in bl_info.keys(
        # ) and bl_info["endpoint_url"] != ""
        is_sam = False  # ! Disabled until Super Addon Manager releases.

        # Show the notice, that this addon can be updated with Super Addon Manager.
        if is_sam and not "Super Addon Manager" in context.preferences.addons:
            layout.separator()
            layout.label(
                text="This addon can be updated automatically with Super Addon Manager.")
            layout.operator("wm.url_open", text="Learn more!",
                            icon="URL").url = "https//TODO"


def get_lib_path_index(prefs: Preferences):
    """Get the index of the library name or path for configuring them in the operator."""
    for index, lib in enumerate(prefs.filepaths.asset_libraries):
        if lib.path == p.dirname(__file__) or lib.name == LIB_NAME:
            return index
    return -1




def register_library():
    """Register the library in Blender, as long as the addon is enabled."""
    prefs = bpy.context.preferences

    index = get_lib_path_index(prefs)

    # In case the library doesn't exist in the preferences, create it.
    if index == -1:
        bpy.ops.preferences.asset_library_add(
            directory=p.dirname(__file__))
        index = get_lib_path_index(prefs)

    # Set the correct name and path of the library to avoid issues because of wrong paths.
    prefs.filepaths.asset_libraries[index].name = LIB_NAME
    prefs.filepaths.asset_libraries[index].path = p.dirname(__file__)

    return


def unregister_library():
    """Remove the library from Blender, as soon as the addon is disabled."""
    prefs = bpy.context.preferences

    index = get_lib_path_index(prefs)
    print(index)

    if index == -1:
        return

    bpy.ops.preferences.asset_library_remove(index=index)


classes = (
    LIBADDON_APT_preferences,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.app.timers.register(register_library, first_interval=0.1)


def unregister():
    unregister_library()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    try:
        bpy.app.timers.unregister(register_library)
    except Exception:
        print("WARNING: Already unregistered register_library.")