# maya_version_save.py (c) 2013 Scott Wilson (ProperSquid)
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

"""
Created by Scott Wilson
Version 1.0
Date 1/23/2013
"""

from time import time
from os.path import split, join, exists, dirname, getctime
import maya.cmds as cmds

# 1. Save scene, and set environment variables.
if cmds.file(query = True, sceneName = True) == '':
    file_filters = "Maya ASCII (*.ma);;Maya Binary (*.mb)"
    get_save_settings = cmds.fileDialog2(fileFilter=multipleFilters, dialogStyle=2, returnFilter = True, selectFileFilter = 'Maya Binary (*.mb)')
    cmds.file(rename = get_save_settings[0])
    if get_save_settings[1] == 'Maya ASCII':
        cmds.file(save = True, type = 'mayaAscii')
    elif get_save_settings[1] == 'Maya Binary':
        cmds.file(save = True, type = 'mayaBinary')
else:
    cmds.file(save = True)
full_file_path = cmds.file(query = True, sceneName = True)
file_type = cmds.file(query = True, type = True)[0]
file_name = split(full_file_path)[1][:-3]
file_directory = dirname(full_file_path)

# 2. Check if 5 minutes has passed since last save. If it has, save new version. Else, just save.

previous_time = getctime(full_file_path)


if (time() - previous_time) >= 300: # Check if 5 minutes has passed (300 seconds).
	try: # Check if there is already a number at the end of the scene.
		version_number = int(file_name[-4:])
		version_number += 1
		append_number = ''
		for i in range(4 - len(str(version_number))):
			append_number += '0'
		append_number += str(version_number)
		new_file_name = file_name[:-4] + append_number
	except ValueError: # If there isn't, add a number.
		new_file_name = file_name + '-0001'
	#Application.SaveSceneAs(join(file_directory, new_file_name + '.scn'))
	if file_type == 'mayaAscii':
            cmds.file(rename = join(file_directory, new_file_name + '.ma'))
            cmds.file(save = True)
        elif file_type == 'mayaBinary':
            cmds.file(rename = join(file_directory, new_file_name + '.mb'))
            cmds.file(save = True)
