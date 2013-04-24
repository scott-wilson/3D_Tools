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
Version 1.1
Date 3/20/2013
"""

from time import time
from os.path import split, join, exists, dirname, getctime
from shutil import copyfile
import maya.cmds as cmds

# 1. Save scene, and set environment variables.
if cmds.file(query = True, sceneName = True) == None:
    file_filters = "Maya ASCII (*.ma);;Maya Binary (*.mb)"
    get_save_settings = cmds.fileDialog2(fileFilter=file_filters, dialogStyle=2, returnFilter = True, selectFileFilter = 'Maya Binary (*.mb)')
    cmds.file(rename = get_save_settings[0])
    if get_save_settings[1] == 'Maya ASCII':
        cmds.file(save = True, type = 'mayaAscii')
        file_ext = '.ma'
    elif get_save_settings[1] == 'Maya Binary':
        cmds.file(save = True, type = 'mayaBinary')
        file_ext = '.mb'
else:
    cmds.file(save = True)
    full_file_path = cmds.file(query = True, sceneName = True)
    file_type = cmds.file(query = True, type = True)[0]
    file_name = split(full_file_path)[1][:-3]
    file_directory = dirname(full_file_path)
    file_ext = split(full_file_path)[1][-3:]
    
    # 2. Check if 5 minutes has passed since last save. If it has, duplicate.
    
    version_number = '-0001'
    old_version_number = version_number
    while exists(join(file_directory, file_name + version_number + file_ext)):
        old_version_number = version_number
        version_number = int(version_number[1:])
        version_number += 1
        append_number = ''
        for i in range(4 - len(str(version_number))):
            append_number += '0'
        append_number += str(version_number)
        version_number = '-' + append_number
        
    try:
        previous_time = getctime(join(file_directory, file_name + old_version_number + file_ext))
        
    except WindowsError:
        previous_time = getctime(full_file_path)
        
    if(time() - previous_time) >= 300:
        new_file_name = file_name + version_number
        copyfile(join(file_directory, file_name + file_ext), join(file_directory, new_file_name + file_ext))
