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

'''
Created by Scott Wilson
Version 1.0
Date 4/23/2013
'''

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
	Application.SetValue('{null_object}.visibility.viewvis'.format(null_object = data_container), False, '')
	Application.SetValue('{null_object}.visibility.rendvis'.format(null_object = data_container), False, '')

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
	for sel_pivots in ('Foot Pad', 'Select Toe Swivel', 'Select Heel Pivot', 'Select Outer Pivot', 'Select Inner Pivot'):
		pivot_list.append(Application.PickElement('', sel_pivots, '')(2))

if len(bones_list) and len(pivot_list) > 0:
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
		Application.SetValue('{pivot}.null.primary_icon'.format(pivot = pivot_name), 5, '')
		Application.GetPrim('Null', up_vector_name)
		Application.SetValue('{up_vector}.null.primary_icon'.format(up_vector = up_vector_name), 9, '')
		Application.SetValue('{up_vector}.null.size'.format(up_vector = up_vector_name), 0.5, '')
		Application.SetValue('{up_vector}.visibility.viewvis'.format(up_vector = up_vector_name), False, '')
		Application.SetValue('{up_vector}.visibility.rendvis'.format(up_vector = up_vector_name), False, '')
		Application.ParentObj(pivot_name, up_vector_name)
		
		for child in bones.children:
			Application.MatchTransform(pivot_name, child, 'siSRT', '')
			Application.MatchTransform(up_vector_name, bones, 'siSRT', '')
			Application.Translate(up_vector_name, 0, 1.0, 0, 'siRelative', 'siLocal', 'siObj', 'siXYZ', '', '', '', '', '', '', '', '', '', 0, '')
			if child.type == 'eff':
				Application.GetPrim('Null', 'pv_toe_cntr')
				Application.MatchTransform('pv_toe_cntr', bones, 'siSRT', '')
				Application.SetValue('pv_toe_cntr.null.primary_icon', 5, '')
				Application.SetValue('pv_toe_cntr.null.size', 1.5, '')
				Application.SetKeyableAttributes('pv_toe_cntr', 'kine.local.pos.posx,kine.local.pos.posy,kine.local.pos.posz,kine.local.scl.sclx,kine.local.scl.scly,kine.local.scl.sclz,kine.local.ori.euler.rotx,kine.local.ori.euler.roty', 'siKeyableAttributeNonKeyableVisible')
				Application.SetKeyableAttributes('pv_toe_cntr', 'kine.local.pos.posx,kine.local.pos.posy,kine.local.pos.posz,kine.local.scl.sclx,kine.local.scl.scly,kine.local.scl.sclz,kine.local.ori.euler.rotx,kine.local.ori.euler.roty', 'siKeyableAttributeClear')

		Application.SetKeyableAttributes(pivot_name, 'kine.local.pos.posx,kine.local.pos.posy,kine.local.pos.posz,kine.local.scl.sclx,kine.local.scl.scly,kine.local.scl.sclz,kine.local.ori.euler.rotx,kine.local.ori.euler.roty', 'siKeyableAttributeNonKeyableVisible')
		Application.SetKeyableAttributes(pivot_name, 'kine.local.pos.posx,kine.local.pos.posy,kine.local.pos.posz,kine.local.scl.sclx,kine.local.scl.scly,kine.local.scl.sclz,kine.local.ori.euler.rotx,kine.local.ori.euler.roty', 'siKeyableAttributeClear')
		
	for bones in bones_list:
		pivot_name = 'pv_{b_name}'.format(b_name = bones)
		pivot_data_name = 'pv_{b_name}_data'.format(b_name = bones)
		pivot_parent_name = 'pv_{b_parent}'.format(b_parent = str(bones.parent))
		
		if bones.parent.type == 'root':
			Application.ParentObj(pivot_name, 'pv_ankle')
			Application.ApplyCns('Position', bones.parent, 'pv_ankle', '')
			set_object_zero('pv_ankle')
			Application.SetValue('pv_ankle.visibility.viewvis', False, '')
			Application.SetValue('pv_ankle.visibility.rendvis', False, '')
			Application.SetValue('pv_ankle.kine.local.posxminactive', True, '')
			Application.SetValue('pv_ankle.kine.local.posxmaxactive', True, '')
			Application.SetValue('pv_ankle.kine.local.posyminactive', True, '')
			Application.SetValue('pv_ankle.kine.local.posymaxactive', True, '')
			Application.SetValue('pv_ankle.kine.local.poszminactive', True, '')
			Application.SetValue('pv_ankle.kine.local.poszmaxactive', True, '')
			Application.SetValue('pv_ankle.kine.local.posxminlimit', 0, '')
			Application.SetValue('pv_ankle.kine.local.posxmaxlimit', 0, '')
			Application.SetValue('pv_ankle.kine.local.posyminlimit', 0, '')
			Application.SetValue('pv_ankle.kine.local.posymaxlimit', 0, '')
			Application.SetValue('pv_ankle.kine.local.poszminlimit', 0, '')
			Application.SetValue('pv_ankle.kine.local.poszmaxlimit', 0, '')
			Application.SetValue('pv_ankle.kine.local.rotxminactive', True, '')
			Application.SetValue('pv_ankle.kine.local.rotxmaxactive', True, '')
			Application.SetValue('pv_ankle.kine.local.rotyminactive', True, '')
			Application.SetValue('pv_ankle.kine.local.rotymaxactive', True, '')
			Application.SetValue('pv_ankle.kine.local.rotzminactive', True, '')
			Application.SetValue('pv_ankle.kine.local.rotzmaxactive', True, '')
			Application.SetValue('pv_ankle.kine.local.rotxminlimit', 0, '')
			Application.SetValue('pv_ankle.kine.local.rotxmaxlimit', 0, '')
			Application.SetValue('pv_ankle.kine.local.rotyminlimit', 0, '')
			Application.SetValue('pv_ankle.kine.local.rotymaxlimit', 0, '')
			Application.SetValue('pv_ankle.kine.local.rotzminlimit', 0, '')
			Application.SetValue('pv_ankle.kine.local.rotzmaxlimit', 0, '')

		else:
			Application.ParentObj(pivot_name, pivot_parent_name)
			Application.ApplyCns('Position', bones, pivot_parent_name, '')
		
			for child in bones.children:
				if child.type == 'eff':
					Application.ApplyCns('Position', child, pivot_name, '')
					toe_bone = pivot_data_name
					Application.ParentObj(pivot_name, 'pv_toe_cntr')
					set_object_zero('pv_toe_cntr')
					Application.SetValue('pv_toe_cntr.kine.local.posxminactive', True, '')
					Application.SetValue('pv_toe_cntr.kine.local.posxmaxactive', True, '')
					Application.SetValue('pv_toe_cntr.kine.local.posyminactive', True, '')
					Application.SetValue('pv_toe_cntr.kine.local.posymaxactive', True, '')
					Application.SetValue('pv_toe_cntr.kine.local.poszminactive', True, '')
					Application.SetValue('pv_toe_cntr.kine.local.poszmaxactive', True, '')
					Application.SetValue('pv_toe_cntr.kine.local.posxminlimit', 0, '')
					Application.SetValue('pv_toe_cntr.kine.local.posxmaxlimit', 0, '')
					Application.SetValue('pv_toe_cntr.kine.local.posyminlimit', 0, '')
					Application.SetValue('pv_toe_cntr.kine.local.posymaxlimit', 0, '')
					Application.SetValue('pv_toe_cntr.kine.local.poszminlimit', 0, '')
					Application.SetValue('pv_toe_cntr.kine.local.poszmaxlimit', 0, '')
					Application.SetValue('pv_toe_cntr.kine.local.rotxminactive', True, '')
					Application.SetValue('pv_toe_cntr.kine.local.rotxmaxactive', True, '')
					Application.SetValue('pv_toe_cntr.kine.local.rotyminactive', True, '')
					Application.SetValue('pv_toe_cntr.kine.local.rotymaxactive', True, '')
					Application.SetValue('pv_toe_cntr.kine.local.rotzminactive', True, '')
					Application.SetValue('pv_toe_cntr.kine.local.rotzmaxactive', True, '')
					Application.SetValue('pv_toe_cntr.kine.local.rotxminlimit', 0, '')
					Application.SetValue('pv_toe_cntr.kine.local.rotxmaxlimit', 0, '')
					Application.SetValue('pv_toe_cntr.kine.local.rotyminlimit', 0, '')
					Application.SetValue('pv_toe_cntr.kine.local.rotymaxlimit', 0, '')
					Application.SetValue('pv_toe_cntr.kine.local.rotzminlimit', -90, '')
					Application.SetValue('pv_toe_cntr.kine.local.rotzmaxlimit', 90, '')
					
		set_object_zero(pivot_name)
		
		Application.SetValue('{pivot}.kine.local.posxminactive'.format(pivot = pivot_name), True, '')
		Application.SetValue('{pivot}.kine.local.posxmaxactive'.format(pivot = pivot_name), True, '')
		Application.SetValue('{pivot}.kine.local.posyminactive'.format(pivot = pivot_name), True, '')
		Application.SetValue('{pivot}.kine.local.posymaxactive'.format(pivot = pivot_name), True, '')
		Application.SetValue('{pivot}.kine.local.poszminactive'.format(pivot = pivot_name), True, '')
		Application.SetValue('{pivot}.kine.local.poszmaxactive'.format(pivot = pivot_name), True, '')
		Application.SetValue('{pivot}.kine.local.posxminlimit'.format(pivot = pivot_name), 0, '')
		Application.SetValue('{pivot}.kine.local.posxmaxlimit'.format(pivot = pivot_name), 0, '')
		Application.SetValue('{pivot}.kine.local.posyminlimit'.format(pivot = pivot_name), 0, '')
		Application.SetValue('{pivot}.kine.local.posymaxlimit'.format(pivot = pivot_name), 0, '')
		Application.SetValue('{pivot}.kine.local.poszminlimit'.format(pivot = pivot_name), 0, '')
		Application.SetValue('{pivot}.kine.local.poszmaxlimit'.format(pivot = pivot_name), 0, '')
		Application.SetValue('{pivot}.kine.local.rotxminactive'.format(pivot = pivot_name), True, '')
		Application.SetValue('{pivot}.kine.local.rotxmaxactive'.format(pivot = pivot_name), True, '')
		Application.SetValue('{pivot}.kine.local.rotyminactive'.format(pivot = pivot_name), True, '')
		Application.SetValue('{pivot}.kine.local.rotymaxactive'.format(pivot = pivot_name), True, '')
		Application.SetValue('{pivot}.kine.local.rotzminactive'.format(pivot = pivot_name), True, '')
		Application.SetValue('{pivot}.kine.local.rotzmaxactive'.format(pivot = pivot_name), True, '')
		Application.SetValue('{pivot}.kine.local.rotxminlimit'.format(pivot = pivot_name), 0, '')
		Application.SetValue('{pivot}.kine.local.rotxmaxlimit'.format(pivot = pivot_name), 0, '')
		Application.SetValue('{pivot}.kine.local.rotyminlimit'.format(pivot = pivot_name), 0, '')
		Application.SetValue('{pivot}.kine.local.rotymaxlimit'.format(pivot = pivot_name), 0, '')
		Application.SetValue('{pivot}.kine.local.rotzminlimit'.format(pivot = pivot_name), 0, '')
		Application.SetValue('{pivot}.kine.local.rotzmaxlimit'.format(pivot = pivot_name), 90, '')
		
		Application.ApplyOp('SkeletonUpVector', '{b_name};up_{b_name}'.format(b_name = bones), 3, 'siPersistentOperation', '', 0)

	Application.ParentObj(pivot_list[0], pivot_list[1]) # Parent: foot pad, Child: toe
	Application.ParentObj(pivot_list[1], pivot_list[3]) # Parent: toe, Child: outer foot
	Application.ParentObj(pivot_list[3], pivot_list[4]) # Parent: outer foot, Child: inner foot
	Application.ParentObj(pivot_list[4], pivot_list[2]) # Parent: inner foot, Child: heel
	Application.ParentObj(pivot_list[2], toe_bone) # Parent: heel, Child: toe bone
	
	# Toe Swivel
	Application.SetKeyableAttributes(pivot_list[1], 'kine.local.pos.posx,kine.local.pos.posy,kine.local.pos.posz,kine.local.scl.sclx,kine.local.scl.scly,kine.local.scl.sclz,kine.local.ori.euler.rotx,kine.local.ori.euler.rotz', 'siKeyableAttributeNonKeyableVisible')
	Application.SetKeyableAttributes(pivot_list[1], 'kine.local.pos.posx,kine.local.pos.posy,kine.local.pos.posz,kine.local.scl.sclx,kine.local.scl.scly,kine.local.scl.sclz,kine.local.ori.euler.rotx,kine.local.ori.euler.rotz', 'siKeyableAttributeClear')
	Application.SetValue('{pivot}.kine.local.posxminactive'.format(pivot = pivot_list[1]), True, '')
	Application.SetValue('{pivot}.kine.local.posxmaxactive'.format(pivot = pivot_list[1]), True, '')
	Application.SetValue('{pivot}.kine.local.posyminactive'.format(pivot = pivot_list[1]), True, '')
	Application.SetValue('{pivot}.kine.local.posymaxactive'.format(pivot = pivot_list[1]), True, '')
	Application.SetValue('{pivot}.kine.local.poszminactive'.format(pivot = pivot_list[1]), True, '')
	Application.SetValue('{pivot}.kine.local.poszmaxactive'.format(pivot = pivot_list[1]), True, '')
	Application.SetValue('{pivot}.kine.local.posxminlimit'.format(pivot = pivot_list[1]), 0, '')
	Application.SetValue('{pivot}.kine.local.posxmaxlimit'.format(pivot = pivot_list[1]), 0, '')
	Application.SetValue('{pivot}.kine.local.posyminlimit'.format(pivot = pivot_list[1]), 0, '')
	Application.SetValue('{pivot}.kine.local.posymaxlimit'.format(pivot = pivot_list[1]), 0, '')
	Application.SetValue('{pivot}.kine.local.poszminlimit'.format(pivot = pivot_list[1]), 0, '')
	Application.SetValue('{pivot}.kine.local.poszmaxlimit'.format(pivot = pivot_list[1]), 0, '')
	Application.SetValue('{pivot}.kine.local.rotxminactive'.format(pivot = pivot_list[1]), True, '')
	Application.SetValue('{pivot}.kine.local.rotxmaxactive'.format(pivot = pivot_list[1]), True, '')
	Application.SetValue('{pivot}.kine.local.rotyminactive'.format(pivot = pivot_list[1]), True, '')
	Application.SetValue('{pivot}.kine.local.rotymaxactive'.format(pivot = pivot_list[1]), True, '')
	Application.SetValue('{pivot}.kine.local.rotzminactive'.format(pivot = pivot_list[1]), True, '')
	Application.SetValue('{pivot}.kine.local.rotzmaxactive'.format(pivot = pivot_list[1]), True, '')
	Application.SetValue('{pivot}.kine.local.rotxminlimit'.format(pivot = pivot_list[1]), 0, '')
	Application.SetValue('{pivot}.kine.local.rotxmaxlimit'.format(pivot = pivot_list[1]), 0, '')
	Application.SetValue('{pivot}.kine.local.rotyminlimit'.format(pivot = pivot_list[1]), -90, '')
	Application.SetValue('{pivot}.kine.local.rotymaxlimit'.format(pivot = pivot_list[1]), 90, '')
	Application.SetValue('{pivot}.kine.local.rotzminlimit'.format(pivot = pivot_list[1]), 0, '')
	Application.SetValue('{pivot}.kine.local.rotzmaxlimit'.format(pivot = pivot_list[1]), 0, '')
	
	# Heel Pivot
	Application.SetKeyableAttributes(pivot_list[2], 'kine.local.pos.posx,kine.local.pos.posy,kine.local.pos.posz,kine.local.scl.sclx,kine.local.scl.scly,kine.local.scl.sclz,kine.local.ori.euler.roty,kine.local.ori.euler.rotz', 'siKeyableAttributeNonKeyableVisible')
	Application.SetKeyableAttributes(pivot_list[2], 'kine.local.pos.posx,kine.local.pos.posy,kine.local.pos.posz,kine.local.scl.sclx,kine.local.scl.scly,kine.local.scl.sclz,kine.local.ori.euler.roty,kine.local.ori.euler.rotz', 'siKeyableAttributeClear')
	Application.SetValue('{pivot}.kine.local.posxminactive'.format(pivot = pivot_list[2]), True, '')
	Application.SetValue('{pivot}.kine.local.posxmaxactive'.format(pivot = pivot_list[2]), True, '')
	Application.SetValue('{pivot}.kine.local.posyminactive'.format(pivot = pivot_list[2]), True, '')
	Application.SetValue('{pivot}.kine.local.posymaxactive'.format(pivot = pivot_list[2]), True, '')
	Application.SetValue('{pivot}.kine.local.poszminactive'.format(pivot = pivot_list[2]), True, '')
	Application.SetValue('{pivot}.kine.local.poszmaxactive'.format(pivot = pivot_list[2]), True, '')
	Application.SetValue('{pivot}.kine.local.posxminlimit'.format(pivot = pivot_list[2]), 0, '')
	Application.SetValue('{pivot}.kine.local.posxmaxlimit'.format(pivot = pivot_list[2]), 0, '')
	Application.SetValue('{pivot}.kine.local.posyminlimit'.format(pivot = pivot_list[2]), 0, '')
	Application.SetValue('{pivot}.kine.local.posymaxlimit'.format(pivot = pivot_list[2]), 0, '')
	Application.SetValue('{pivot}.kine.local.poszminlimit'.format(pivot = pivot_list[2]), 0, '')
	Application.SetValue('{pivot}.kine.local.poszmaxlimit'.format(pivot = pivot_list[2]), 0, '')
	Application.SetValue('{pivot}.kine.local.rotxminactive'.format(pivot = pivot_list[2]), True, '')
	Application.SetValue('{pivot}.kine.local.rotxmaxactive'.format(pivot = pivot_list[2]), True, '')
	Application.SetValue('{pivot}.kine.local.rotyminactive'.format(pivot = pivot_list[2]), True, '')
	Application.SetValue('{pivot}.kine.local.rotymaxactive'.format(pivot = pivot_list[2]), True, '')
	Application.SetValue('{pivot}.kine.local.rotzminactive'.format(pivot = pivot_list[2]), True, '')
	Application.SetValue('{pivot}.kine.local.rotzmaxactive'.format(pivot = pivot_list[2]), True, '')
	Application.SetValue('{pivot}.kine.local.rotxminlimit'.format(pivot = pivot_list[2]), -90, '')
	Application.SetValue('{pivot}.kine.local.rotxmaxlimit'.format(pivot = pivot_list[2]), 0, '')
	Application.SetValue('{pivot}.kine.local.rotyminlimit'.format(pivot = pivot_list[2]), 0, '')
	Application.SetValue('{pivot}.kine.local.rotymaxlimit'.format(pivot = pivot_list[2]), 0, '')
	Application.SetValue('{pivot}.kine.local.rotzminlimit'.format(pivot = pivot_list[2]), 0, '')
	Application.SetValue('{pivot}.kine.local.rotzmaxlimit'.format(pivot = pivot_list[2]), 0, '')
	
	# Outer Pivot
	Application.SetKeyableAttributes(pivot_list[3], 'kine.local.pos.posx,kine.local.pos.posy,kine.local.pos.posz,kine.local.scl.sclx,kine.local.scl.scly,kine.local.scl.sclz,kine.local.ori.euler.rotx,kine.local.ori.euler.roty', 'siKeyableAttributeNonKeyableVisible')
	Application.SetKeyableAttributes(pivot_list[3], 'kine.local.pos.posx,kine.local.pos.posy,kine.local.pos.posz,kine.local.scl.sclx,kine.local.scl.scly,kine.local.scl.sclz,kine.local.ori.euler.rotx,kine.local.ori.euler.roty', 'siKeyableAttributeClear')
	Application.SetValue('{pivot}.kine.local.posxminactive'.format(pivot = pivot_list[3]), True, '')
	Application.SetValue('{pivot}.kine.local.posxmaxactive'.format(pivot = pivot_list[3]), True, '')
	Application.SetValue('{pivot}.kine.local.posyminactive'.format(pivot = pivot_list[3]), True, '')
	Application.SetValue('{pivot}.kine.local.posymaxactive'.format(pivot = pivot_list[3]), True, '')
	Application.SetValue('{pivot}.kine.local.poszminactive'.format(pivot = pivot_list[3]), True, '')
	Application.SetValue('{pivot}.kine.local.poszmaxactive'.format(pivot = pivot_list[3]), True, '')
	Application.SetValue('{pivot}.kine.local.posxminlimit'.format(pivot = pivot_list[3]), 0, '')
	Application.SetValue('{pivot}.kine.local.posxmaxlimit'.format(pivot = pivot_list[3]), 0, '')
	Application.SetValue('{pivot}.kine.local.posyminlimit'.format(pivot = pivot_list[3]), 0, '')
	Application.SetValue('{pivot}.kine.local.posymaxlimit'.format(pivot = pivot_list[3]), 0, '')
	Application.SetValue('{pivot}.kine.local.poszminlimit'.format(pivot = pivot_list[3]), 0, '')
	Application.SetValue('{pivot}.kine.local.poszmaxlimit'.format(pivot = pivot_list[3]), 0, '')
	Application.SetValue('{pivot}.kine.local.rotxminactive'.format(pivot = pivot_list[3]), True, '')
	Application.SetValue('{pivot}.kine.local.rotxmaxactive'.format(pivot = pivot_list[3]), True, '')
	Application.SetValue('{pivot}.kine.local.rotyminactive'.format(pivot = pivot_list[3]), True, '')
	Application.SetValue('{pivot}.kine.local.rotymaxactive'.format(pivot = pivot_list[3]), True, '')
	Application.SetValue('{pivot}.kine.local.rotzminactive'.format(pivot = pivot_list[3]), True, '')
	Application.SetValue('{pivot}.kine.local.rotzmaxactive'.format(pivot = pivot_list[3]), True, '')
	Application.SetValue('{pivot}.kine.local.rotxminlimit'.format(pivot = pivot_list[3]), 0, '')
	Application.SetValue('{pivot}.kine.local.rotxmaxlimit'.format(pivot = pivot_list[3]), 0, '')
	Application.SetValue('{pivot}.kine.local.rotyminlimit'.format(pivot = pivot_list[3]), 0, '')
	Application.SetValue('{pivot}.kine.local.rotymaxlimit'.format(pivot = pivot_list[3]), 0, '')
	Application.SetValue('{pivot}.kine.local.rotzminlimit'.format(pivot = pivot_list[3]), -90, '')
	Application.SetValue('{pivot}.kine.local.rotzmaxlimit'.format(pivot = pivot_list[3]), 0, '')
	
	# Inner Pivot
	Application.SetKeyableAttributes(pivot_list[4], 'kine.local.pos.posx,kine.local.pos.posy,kine.local.pos.posz,kine.local.scl.sclx,kine.local.scl.scly,kine.local.scl.sclz,kine.local.ori.euler.rotx,kine.local.ori.euler.roty', 'siKeyableAttributeNonKeyableVisible')
	Application.SetKeyableAttributes(pivot_list[4], 'kine.local.pos.posx,kine.local.pos.posy,kine.local.pos.posz,kine.local.scl.sclx,kine.local.scl.scly,kine.local.scl.sclz,kine.local.ori.euler.rotx,kine.local.ori.euler.roty', 'siKeyableAttributeClear')
	Application.SetValue('{pivot}.kine.local.posxminactive'.format(pivot = pivot_list[4]), True, '')
	Application.SetValue('{pivot}.kine.local.posxmaxactive'.format(pivot = pivot_list[4]), True, '')
	Application.SetValue('{pivot}.kine.local.posyminactive'.format(pivot = pivot_list[4]), True, '')
	Application.SetValue('{pivot}.kine.local.posymaxactive'.format(pivot = pivot_list[4]), True, '')
	Application.SetValue('{pivot}.kine.local.poszminactive'.format(pivot = pivot_list[4]), True, '')
	Application.SetValue('{pivot}.kine.local.poszmaxactive'.format(pivot = pivot_list[4]), True, '')
	Application.SetValue('{pivot}.kine.local.posxminlimit'.format(pivot = pivot_list[4]), 0, '')
	Application.SetValue('{pivot}.kine.local.posxmaxlimit'.format(pivot = pivot_list[4]), 0, '')
	Application.SetValue('{pivot}.kine.local.posyminlimit'.format(pivot = pivot_list[4]), 0, '')
	Application.SetValue('{pivot}.kine.local.posymaxlimit'.format(pivot = pivot_list[4]), 0, '')
	Application.SetValue('{pivot}.kine.local.poszminlimit'.format(pivot = pivot_list[4]), 0, '')
	Application.SetValue('{pivot}.kine.local.poszmaxlimit'.format(pivot = pivot_list[4]), 0, '')
	Application.SetValue('{pivot}.kine.local.rotxminactive'.format(pivot = pivot_list[4]), True, '')
	Application.SetValue('{pivot}.kine.local.rotxmaxactive'.format(pivot = pivot_list[4]), True, '')
	Application.SetValue('{pivot}.kine.local.rotyminactive'.format(pivot = pivot_list[4]), True, '')
	Application.SetValue('{pivot}.kine.local.rotymaxactive'.format(pivot = pivot_list[4]), True, '')
	Application.SetValue('{pivot}.kine.local.rotzminactive'.format(pivot = pivot_list[4]), True, '')
	Application.SetValue('{pivot}.kine.local.rotzmaxactive'.format(pivot = pivot_list[4]), True, '')
	Application.SetValue('{pivot}.kine.local.rotxminlimit'.format(pivot = pivot_list[4]), 0, '')
	Application.SetValue('{pivot}.kine.local.rotxmaxlimit'.format(pivot = pivot_list[4]), 0, '')
	Application.SetValue('{pivot}.kine.local.rotyminlimit'.format(pivot = pivot_list[4]), 0, '')
	Application.SetValue('{pivot}.kine.local.rotymaxlimit'.format(pivot = pivot_list[4]), 0, '')
	Application.SetValue('{pivot}.kine.local.rotzminlimit'.format(pivot = pivot_list[4]), 0, '')
	Application.SetValue('{pivot}.kine.local.rotzmaxlimit'.format(pivot = pivot_list[4]), 90, '')

	for pivot in pivot_list:
		set_object_zero(pivot)
