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
			
