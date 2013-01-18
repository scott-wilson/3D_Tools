"""
Created by Scott Wilson
Version 1.0
Date 1/15/2013
"""

from time import time
from os.path import split, join, exists, dirname

# 1. Save scene, and set environment variables.
Application.SaveScene()

version_file = join(Application.ActiveProject3.Path, 'version')
file_name = split(Application.ActiveProject3.ActiveScene.filename.value)[1][:-4]
file_directory = dirname(Application.ActiveProject3.ActiveScene.filename.value)

# 2. Check if the version management file exsits. If it doesn't, then make file.
if exists(version_file) == False:
  with open(version_file, 'w') as f:
		f.write(str(time()))

# 3. Check if 5 minutes has passed since last save. If it has, save new version. Else, just save.
with open(version_file) as f:
	previous_time = float(f.read())

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
	Application.SaveSceneAs(join(file_directory, new_file_name + '.scn'))
	
	with open(version_file, 'w') as f:
		f.write(str(time()))

