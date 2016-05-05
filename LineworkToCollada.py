##Input_Linework=vector
##Elevation_Field=field Input_Linework
##Recenter_X=number 0.0
##Recenter_Y=number 0.0
##Recenter_Z=number 0.0
##Scale_Z=number 1.0
##Comments=string (user-definable comment)
##Output_File=output file


import qgis.core
import processing


def is_numeric(literal):
	"Function to return true if input literal is numeric"
	if literal is None:
		return False
	else:
		try:
			i = float(literal)
		except ValueError:
			return False
		else:
			return True

# Get the actual Vector Layer object
linework = processing.getObject(Input_Linework)

n = linework.featureCount()
progress.setText(str(n) + " features in Input Linework")

# linework.crs().mapUnits() should return an integer value
# QGIS units: 0 = meters, 1 = feet
# (other values also exist, but are not expected for typical use cases)
# (as per https://qgis.org/api/qgis_8h_source.html#l00155 --as of 4/30/2016)
units = "?"
if linework.crs().mapUnits() == 0:
	units = "meters"
elif linework.crs().mapUnits() == 1:
	units = "feet"
else:
	units = "?"

# Make a list to stage feature IDs, their vertex lists, and output elevations
# Each part within a multipart feature will be considered a separate geometry,
# for the purposes of exporting to Collada)
outputFeatures = []

# Count any errors when getting the feature elevation values
feat_elev_error_counter = 0

# Count the number of features;
# we will use this as part of the feature ID for each geometry instance
feat_counter = 0

progress.setText("Scanning over input features...")
for feat in processing.features(linework):
	feat_counter += 1
	
	geom_col = feat.geometry().asGeometryCollection()
	# The geom_col will be a list containing each "part" of the geometry
	# (if the geometry is single-part, then we expect len(geom_col) == 1)
	# We want to handle both polyline and polygon geometries
	
	part_counter = 0
	for geom_part in geom_col:
		part_counter += 1
		
		if len(geom_part.asPolyline()) > 0:
			# This part is a polyline
			vertexlist = []
			geom_vertexlist = geom_part.asPolyline()
			for vertex in geom_vertexlist:
				vertexlist.append([vertex.x(), vertex.y()])
				
			if Elevation_Field is not None and Elevation_Field != "":
				# User provided a field from which to obtain an elevation value for this feature
				feat_elev = 0
				try:
					feat_elev = feat[Elevation_Field]
					# If somehow the returned value was null / none, then just set to zero
					if feat_elev is None or is_numeric(feat_elev) is False:
						feat_elev = 0
				except:
					# Error getting the field value; leave elevation at zero and count this error
					feat_elev_error_counter += 1
					feat_elev = 0
					
				outputFeatures.append(["F" + str(feat_counter) + "P" + str(part_counter), vertexlist, feat_elev])
			else:
				# No elevation field; leave elevation at zero
				outputFeatures.append(["F" + str(feat_counter) + "P" + str(part_counter), vertexlist, 0])
			
		if len(geom_part.asPolygon()) > 0:
			# This part is a polygon (possibly with internal holes, denoted by additional rings)
			# If the polygon has internal holes, then len(geom_part.asPolygon()) > 1
			geom_pgon = geom_part.asPolygon()
			ring_counter = 0
			for geom_ring in geom_pgon:
				ring_counter += 1
				vertexlist = []
				for vertex in geom_ring:
					vertexlist.append([vertex.x(), vertex.y()])
					
				if Elevation_Field is not None and Elevation_Field != "":
					# User provided a field from which to obtain an elevation value for this feature
					feat_elev = 0
					try:
						feat_elev = feat[Elevation_Field]
						# If somehow the returned value was null / none, then just set to zero
						if feat_elev is None or is_numeric(feat_elev) is False:
							feat_elev = 0
					except:
						# Error getting the field value; leave elevation at zero and count this error
						feat_elev_error_counter += 1
						feat_elev = 0
						
					outputFeatures.append(["F" + str(feat_counter) + "P" + str(part_counter) + "R" + str(ring_counter), vertexlist, feat_elev])
				else:
					# No elevation field; leave elevation at zero
					outputFeatures.append(["F" + str(feat_counter) + "P" + str(part_counter) + "R" + str(ring_counter), vertexlist, 0])
					

progress.setText("Opening output file...")
with open(Output_File, "w") as outfile:
		
	# Begin the output file
	outfile.write("""<?xml version="1.0" encoding="UTF-8" standalone="no" ?>""" + "\n")
	outfile.write("""<COLLADA xmlns="http://www.collada.org/2005/11/COLLADASchema" version="1.4.1">""" + "\n")
	outfile.write("""<asset>""" + "\n")
	outfile.write("<contributor>" + "\n")
	outfile.write("<authoring_tool>LineworkToCollada python script for QGIS processing framework</authoring_tool>" + "\n")
	if Comments is not None:
		if len(Comments) != 0:
			outfile.write("<comments>" + Comments.replace("<", "_lt_").replace(">", "_gt_") + "</comments>" + "\n")
	outfile.write("</contributor>" + "\n")
	
	if units == "meters":
		outfile.write("""<unit meter="1" name="meter" />""" + "\n")
	elif units == "feet":
		outfile.write("""<unit meter="0.3048" name="foot" />""" + "\n")
	else:
		outfile.write("""<unit meter="1" name="unknown" />""" + "\n")
		
	outfile.write("""<up_axis>Z_UP</up_axis>""" + "\n")
	outfile.write("""</asset>""" + "\n")
	
	
	# Library of visual scenes
	outfile.write("""<library_visual_scenes>""" + "\n")
	outfile.write("""<visual_scene id="Scene1">""" + "\n")
	outfile.write("""<node name="ExportedPolylines">""" + "\n")
	
	for i in range(0, len(outputFeatures)):
		outfile.write("<instance_geometry url=\"#" + str(outputFeatures[i][0]) + "\" />" + "\n")
	
	outfile.write("""</node>""" + "\n")
	outfile.write("""</visual_scene>""" + "\n")
	outfile.write("""</library_visual_scenes>""" + "\n")
	
	
	# Library of geometries
	outfile.write("""<library_geometries>""" + "\n")
	progress.setText("Writing geometries...")
	for i in range(0, len(outputFeatures)):
		outfile.write("<geometry id=\"" + str(outputFeatures[i][0]) + "\">" + "\n")
		outfile.write("<mesh>" + "\n")
		outfile.write("<source id=\"" + str(outputFeatures[i][0]) + "Src1\">" + "\n")
		outfile.write("<float_array id=\""+ str(outputFeatures[i][0]) + "Src1FltAry1\" count=\"" + str(3 * len(outputFeatures[i][1])) + "\">" + "\n")
		for j in range(0, len(outputFeatures[i][1])):
			currentvertex = outputFeatures[i][1][j]

			# currentvertex is a python list of [x,y]; our output vertex format should be a string:  "x y z"
			if Scale_Z == 1.0:
				# Leave the z values' scale alone (but recenter as specified by the user)
				outputvertex = str(currentvertex[0] - Recenter_X) + " " + str(currentvertex[1] - Recenter_Y) + " " + str(float(outputFeatures[i][2]) - Recenter_Z)
			else:
				# We will multiply the z values by the scale factor (but only after first applying any user-defined recentering along that axis)
				outputvertex = str(currentvertex[0] - Recenter_X) + " " + str(currentvertex[1] - Recenter_Y) + " " + str((float(outputFeatures[i][2]) - Recenter_Z) * Scale_Z)
			
			outfile.write(outputvertex + " \n")

		outfile.write("</float_array>" + "\n")
		outfile.write("<technique_common>" + "\n")
		outfile.write("<accessor count=\"" + str(len(outputFeatures[i][1])) + "\" source=\"#" + str(outputFeatures[i][0]) + "Src1FltAry1\" stride=\"3\">" + "\n")

		outfile.write("""<param name="X" type="float" />""" + "\n")
		outfile.write("""<param name="Y" type="float" />""" + "\n")
		outfile.write("""<param name="Z" type="float" />""" + "\n")

		outfile.write("</accessor>" + "\n")
		outfile.write("</technique_common>" + "\n")
		outfile.write("</source>" + "\n")

		outfile.write("<vertices id=\"" + str(outputFeatures[i][0]) + "Src1v1\">" + "\n")
		outfile.write("<input semantic=\"POSITION\" source=\"#" + str(outputFeatures[i][0]) + "Src1\" />" + "\n")
		outfile.write("</vertices>" + "\n")
		outfile.write("<lines count=\"" + str(len(outputFeatures[i][1]) - 1) + "\">" + "\n")
		outfile.write("<input offset=\"0\" semantic=\"VERTEX\" source=\"#" + str(outputFeatures[i][0]) + "Src1v1\" />" + "\n")
		outfile.write("<p>" + "\n")

		for j in range(0, len(outputFeatures[i][1])-1):
			outfile.write(str(j) + " " + str(j+1) + " \n")
			
		outfile.write("</p>" + "\n")
		outfile.write("</lines>" + "\n")
		outfile.write("</mesh>" + "\n")
		outfile.write("</geometry>" + "\n")
		
	outfile.write("</library_geometries>" + "\n")
	outfile.write("<scene>" + "\n")
	outfile.write("<instance_visual_scene url=\"#Scene1\" />" + "\n")
	outfile.write("</scene>\n")
	outfile.write("</COLLADA>\n")
	
	# Final messages (for debugging):
	if feat_elev_error_counter > 0:
		outfile.write("<!-- Error getting elevation for " + str(feat_elev_error_counter) + " feature [parts]. --/>\n")

	outfile.close()
				
progress.setInfo("Done exporting linework to Collada.")
