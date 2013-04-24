# softimage_foot_roll.py (c) 2013 Scott Wilson (ProperSquid)
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
Date 4/23/2013
"""

bones_list = []
pivot_list = []

pick_bones = True
pick_pivots = False

def set_object_zero(object_name):
  data_container = '{o_name}_data'.format(o_name = object_name)
	object_parent = str(Application.GetValue(object_name).parent)
	Application.GetPrim('Null', data_container)
	Application.MatchTransform(data_container, object_name, 'siSRT', '')
	Application.ParentObj(data_container, object_name)
	if Application.ActiveSceneRoot.Name != object_parent:
		Application.ParentObj(object_parent, data_container)
	Application.SetValue("{null_object}.visibility.viewvis".format(null_object = data_container), False, "")
	Application.SetValue("{null_object}.visibility.rendvis".format(null_object = data_container), False, "")

while pick_bones == True:
	picked_obj = Application.PickElement('', 'Select Bone', 'Next')
	if picked_obj(0) == 0:
		bones_list = []
		pick_bones = False
	elif picked_obj(0) == 1: # Picked Bone
		bones_list.append(picked_obj(2))
	elif picked_obj(0) == 2: # Go to next step (select pivots)
		pick_pivots = True
		pick_bones = False

if pick_pivots == True:
	for sel_pivots in ('Select Toe Pivot', 'Select Heel Pivot', 'Select Outer Pivot', 'Select Inner Pivot'):
		pivot_list.append(Application.PickElement('', sel_pivots, '')(2))

for bones in bones_list:
	pivot_name = 'pv_{b_name}'.format(b_name = bones)
	pivot_data_name = 'pv_{b_name}_data'.format(b_name = bones)
	pivot_parent_name = 'pv_{b_parent}'.format(b_parent = str(bones.parent))
	up_vector_name = 'up_{b_name}'.format(b_name = bones)
	bone_length = Application.GetValue('{b_name}.length'.format(b_name = bones))
	
	if bones.parent.type == 'root':
		Application.GetPrim('Null', 'pv_ankle')
		Application.MatchTransform('pv_ankle', bones, 'siSRT', '')
	
	Application.GetPrim('Null', pivot_name)
	Application.GetPrim('Null', up_vector_name)
	Application.ParentObj(pivot_name, up_vector_name)
	for child in bones.children:
		Application.MatchTransform(pivot_name, child, 'siSRT', '')
		Application.MatchTransform(up_vector_name, bones, 'siSRT', '')
		Application.Translate(up_vector_name, 0, 1.0, 0, "siRelative", "siLocal", "siObj", "siXYZ", "", "", "", "", "", "", "", "", "", 0, "")

for bones in bones_list:
	pivot_name = 'pv_{b_name}'.format(b_name = bones)
	pivot_data_name = 'pv_{b_name}_data'.format(b_name = bones)
	pivot_parent_name = 'pv_{b_parent}'.format(b_parent = str(bones.parent))
	
	if bones.parent.type == 'root':
		Application.ParentObj(pivot_name, 'pv_ankle')
		Application.ApplyCns('Position', bones.parent, 'pv_ankle', '')
		set_object_zero('pv_ankle')

	else:
		Application.ParentObj(pivot_name, pivot_parent_name)
		Application.ApplyCns('Position', bones, pivot_parent_name, '')
	
		for child in bones.children:
			if child.type == 'eff':
				Application.ApplyCns('Position', child, pivot_name, '')
				toe_bone = pivot_data_name
				
	set_object_zero(pivot_name)
	
	Application.ApplyOp('SkeletonUpVector', '{b_name};up_{b_name}'.format(b_name = bones), 3, 'siPersistentOperation', '', 0)

Application.ParentObj(pivot_list[0], pivot_list[2]) # Parent: toe, Child: outer foot
Application.ParentObj(pivot_list[2], pivot_list[3]) # Parent: outer foot, Child: inner foot
Application.ParentObj(pivot_list[3], pivot_list[1]) # Parent: inner foot, Child: heel
Application.ParentObj(pivot_list[1], toe_bone) # Parent: heel, Child: toe bone

for pivot in pivot_list:
	set_object_zero(pivot)
