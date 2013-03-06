# blender_version_save.py (c) 2013 Scott Wilson (ProperSquid)
#
# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****

bl_info = {
    "name": "Version Save",
    "author": "Scott Wilson",
    "version": (1, 0, 0),
    "blender": (2, 65, 0),
    "location": "Info -> File Menu -> Save",
    "description": "Automatically create versions of saved file every 5 minutes",
    "warning": "",
    "category": "System"}

import bpy
from time import time
from os.path import split, join, exists, dirname, getctime
from os import rename
from shutil import copyfile

class VersionSave(bpy.types.Operator):
    bl_idname = 'file.version_save'
    bl_label = 'Version Save'
    
    def execute(self, context):
        # 1. Save scene, and set environment variables.
        if bpy.data.filepath == '':
            bpy.ops.wm.save_mainfile('INVOKE_AREA')
        else:
            bpy.ops.wm.save_as_mainfile('EXEC_AREA')
            self.full_file_path = bpy.data.filepath
            self.previous_time = getctime(self.full_file_path)
            self.file_name = split(self.full_file_path)[1][:-6]
            self.file_directory = dirname(self.full_file_path)
            # 2. Check if 5 minutes has passed since last save. If it has, save new version. Else, just save.
            if (time() - self.previous_time) >= 3: # Check if 5 minutes has passed (300 seconds).
#                try: # Check if there is already a number at the end of the scene.
#                    self.version_number = int(self.file_name[-4:])
#                    self.version_number += 1
#                    self.append_number = ''
#                    for i in range(4 - len(str(self.version_number))):
#                        self.append_number += '0'
#                    self.append_number += str(self.version_number)
#                    self.new_file_name = self.file_name[:-4] + self.append_number
#                except ValueError: # If there isn't, add a number.
#                    self.new_file_name = self.file_name + '-0001'
                self.version_number = '-0001'
                while exists(join(self.file_directory, self.file_name + self.version_number + '.blend')) == True:
                    self.version_number = int(self.version_number[1:])
                    self.version_number += 1
                    self.append_number = ''
                    for i in range(4 - len(str(self.version_number))):
                        self.append_number += '0'
                    self.append_number += str(self.version_number)
                    self.version_number = '-' + self.append_number
                self.new_file_name = self.file_name + self.version_number
#                bpy.ops.wm.save_as_mainfile(filepath = join(self.file_directory, self.new_file_name + '.blend'))
                copyfile(join(self.file_directory, self.file_name + '.blend'), join(self.file_directory, self.new_file_name + '.blend'))

        return {'FINISHED'}

# Registration

def register():
    bpy.utils.register_class(VersionSave)

def unregister():
    bpy.utils.unregister_class(VersionSave)

if __name__ == "__main__":
    register() 
