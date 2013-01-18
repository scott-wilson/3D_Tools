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
		Application.SetValue("{null_object}.Name".format(null_object = new_null), "{object_name}_data".format(object_name = object), "")
		
