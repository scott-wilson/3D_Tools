# softimage_distributed_twist.py (c) 2013 Scott Wilson (ProperSquid)
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
Date 4/22/2013
"""
bones_list = []
control_obj = ''
distributed_twist = 3

pick_session = True

while pick_session == True:
  picked_obj = Application.PickElement('', 'Select Bone', 'Select Controller')
	if picked_obj(0) == 0:
		bones_list = []
		pick_session = False
	elif picked_obj(0) == 1: # Picked Bone
		bones_list.append(picked_obj(2))
	elif picked_obj(0) == 2: # Picked Controller
		control_obj = picked_obj(2)
		pick_session = False


		

bone_list_length = len(bones_list)
distributed_twist_tot_num = bone_list_length * distributed_twist
current_segment = 0



if bone_list_length > 0:
	side_input = Application.XSIInputBox('Please select the side of the model.', 'Side', 'left').lower()
	if side_input == '':
			bones_list = []
	while side_input not in ('left', 'right' ''):
		side_input = Application.XSIInputBox('Side not recognized. Please select the side of the model.', 'Error!', 'left').lower()
		if side_input == '':
			bones_list = []
	coord_input = Application.XSIInputBox('Please select the rotation axis of the controller.', 'Rotation Axis', 'x').lower()
	if coord_input == '':
			bones_list = []
	while coord_input not in ('x', 'y', 'z', ''):
		coord_input = Application.XSIInputBox('Coordinate not recognized! Please select the rotation axis of the controller.', 'Error!', 'x').lower()
		if coord_input == '':
			bones_list = []
	for bones in bones_list:
		segment = 0
		segment_number = 1
		for add_twist in range(distributed_twist):
			# Generate distributed twist objects
			segment_name = '{s_name}_{s_num}'.format(s_name = Application.GetValue('{b_obj}.name'.format(b_obj = bones)), s_num = segment_number)
			Application.GetPrim('Null', segment_name)
			Application.SetValue('{s_obj}.null.primary_icon'.format(s_obj = segment_name), 2, '')
			Application.SetValue('{s_obj}.null.size'.format(s_obj = segment_name), 0.2, '')
			Application.MatchTransform(segment_name, bones, 'siSRT', '')
			if side_input == 'left':
				Application.Translate(segment_name, segment, 0, 0, "siRelative", "siLocal", "siObj", "siXYZ", "", "", "", "", "", "", "", "", "", 0, "")
			else:
				Application.Translate(segment_name, -segment, 0, 0, "siRelative", "siLocal", "siObj", "siXYZ", "", "", "", "", "", "", "", "", "", 0, "")
			segment += Application.GetValue('{b_obj}.bone.length'.format(b_obj = bones))/distributed_twist
			segment_number += 1
			
			# Generate distributed twist data containers (zero out everything)
			data_container = '{s_name}_data'.format(s_name = segment_name)
			Application.GetPrim('Null', data_container)
			Application.MatchTransform(data_container, segment_name, 'siSRT', '')
			Application.ParentObj(data_container, segment_name)
			Application.SetValue("{null_object}.visibility.viewvis".format(null_object = data_container), False, "")
			Application.SetValue("{null_object}.visibility.rendvis".format(null_object = data_container), False, "")
			
			# Generate expressions to control distributed twist rotations
			distributed_twist_multiplier = float(current_segment) / float(distributed_twist_tot_num)
			Application.AddExpr('{s_obj}.kine.local.rotx'.format(s_obj = segment_name), '{c_obj}.kine.local.rot{coord} * {mult}'.format(c_obj = control_obj, coord = coord_input, mult = distributed_twist_multiplier), 1)
			current_segment += 1
			
			# Parent data container to bone
			Application.ParentObj(bones, data_container)
