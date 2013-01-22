# softimage_clean_skeleton.py (c) 2013 Scott Wilson (ProperSquid)
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
Date 1/9/2013
"""

selection = Application.Selection
size = 0.2

for obj in selection:
  if obj.Type == "root":
		obj_icon = obj.name + ".root.primary_icon"
		obj_size = obj.name + ".root.size"
		Application.SetValue(obj_icon, 2, "")
		Application.SetValue(obj_size, size, "")
		for child in obj.FindChildren("", "", "", False):
			if child.Type == "bone":
				child_solverangles = child.name + ".chain.solverangles"
				Application.SetValue(child_solverangles, 0, "")
			else:
				pass
	
	elif obj.Type == "eff":
		obj_icon = obj.name + ".eff.primary_icon"
		obj_size = obj.name + ".eff.size"
		Application.SetValue(obj_icon, 4, "")
		Application.SetValue(obj_size, size * 2, "")
		
	elif obj.Type == "null":
		obj_icon = obj.name + ".null.primary_icon"
		obj_size = obj.name + ".null.size"
		Application.SetValue(obj_icon, 1, "")
		Application.SetValue(obj_size, size * 2, "")
			
