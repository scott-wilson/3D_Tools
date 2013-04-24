# softimage_set_object_new_zero.py (c) 2013 Scott Wilson (ProperSquid)
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
Date 1/11/2013
"""

objects_list = []

for object in Application.Selection:
  objects_list.append(object)

if objects_list > 0:
	for object in objects_list:
		Application.GetPrim("Null", "", "", "")
		new_null = Application.GetValue(Application.Selection(0))
		Application.MatchTransform(new_null, object, "siSRT", "")
		if Application.ActiveSceneRoot.Name != object.parent.Name:
			Application.ParentObj(object.parent, new_null)
		Application.ParentObj(new_null, object)
		Application.SetValue("{null_object}.visibility.viewvis".format(null_object = new_null), False, "")
		Application.SetValue("{null_object}.visibility.rendvis".format(null_object = new_null), False, "")
		Application.SetValue("{null_object}.Name".format(null_object = new_null), "{object_name}_home".format(object_name = object), "")
		
