# LineworkToCollada-for-QGIS

LineworkToCollada.py:  A Python script for the QGIS processing framework

This script exports linework (polylines, and the edges of polygons) to a Collada file.


## Background:

3D visualization of real-world (or hypothetical) scenes may help individuals interpret geospatial information more easily than by presenting it on a 2D map.  3D visualization finds applications in planning, engineering, marketing, gaming, and other industries.  While many comprehensive software applications exist to aid in the development and publication of 3D visualizations, there is often a need to exchange data between software applications using standardized formats (“interoperability”).

This Python script is part of a simple 3D content production workflow based on QGIS (a free / open-source desktop GIS) and Trimble SketchUp (an inexpensive 3D drafting application).  Alternatively, one might also use other 3D modeling software, as well.

Some 3D visualizations involve terrain data, imagery, and other vector linework (polylines, polygons, mesh models, etc).  GIS software can view and manipulate most of these geospatial data sources.  While SketchUp can import a variety of file formats, common geospatial file types like Shapefile or Geodatabase are not supported (as of this writing).  SketchUp can import Collada (*.dae), an XML-based 3D asset interchange format.  So, content from the GIS system which can be converted to Collada may be imported and used in SketchUp.

QGIS has a “Processing” plugin framework that allows users with a basic knowledge of Python scripting to extent QGIS’s functionality.  The QGIS Processing framework takes much of the burden out of developing Python scripts for QGIS by handling the creation and behavior of the user interface for the user-developed script tools.  For example, if the script author specifies an input parameter as being a “vector” dataset, then the QGIS processing framework will automatically supply a drop-down list of vector layers in the user’s current project (when the script tool is loaded via the graphical user interface).

## Usage Tips:

Be sure to refer to the “Help” tab of the script’s user interface to read comments about each input / output parameter.  If this help information is not present, then ensure that you copied LineworkToCollada.py.help along with the main python script (LineworkToCollada.py).

If you are exporting multiple vector layers to Collada and want them to line up consistently in your 3D modeling software, you should pay careful attention to the coordinate systems of the GIS data.  You may want to project all the data into the same coordinate system before using this script.

A demonstration video with one possible use case for this script is available here: https://youtu.be/hhC8h4-kpe0 (link to video on YouTube).

## Installation:

There is no “installation” required; just copy the script file (LineworkToCollada.py) and its associated help document (LineworkToCollada.py.help) into your QGIS processing scripts folder.  On Windows 7, this folder can be found at C:\Users\username\\.qgis2\processing\scripts.  This may vary by operating system.  If you aren’t sure where to put QGIS Processing script files on your system, you can determine the proper location by using the “Create new script tool” (under QGIS Processing Toolbox > Scripts > Tools) ,and then check to see where QGIS would prompt you to save that script by default –that’s where you should put this script as well.

## Testing Notes:

This script, and its output, was tested using QGIS 2.14.1 and SketchUp 2016 on Windows 7.  It has not been tested with other platforms or software versions, but with any luck, it may work there as well.

## FAQ:

#### Q:  Why are you using QGIS?  Isn’t [fill-in-the-blank-with-your-preferred-GIS-software] better?
A:  QGIS was used for this demonstration because it is free, which reduces barriers that might exist for users who can’t afford the other software.

#### Q:  Why are you using SketchUp?  Doesn’t the professional version cost money?
A:  SketchUp is about as accessible as 3D drafting applications can be, and it’s very “snappy”.  Yes, the professional version costs money, but not a lot, relative to other software that is commonly used in the professional world.  Plus, there is a free version that you can use for individual learning.  Alternatively, you could try a free / open-source 3D modeling package like Blender.

#### Q:  Isn’t this really only a 2D or 2.5-D workflow?
A:  Yes; as of this writing, the QGIS API doesn’t expose access to actual vector geometry Z values.  This workflow is predicated on the existence of an attribute field to set a constant elevation on a per-feature basis.  In the future, if the QGIS API provides programmatic access to Z values, we should update this script accordingly.

#### Q: I have a drone / UAV and photogrammetric software that will produce a nice photo-textured mesh model automatically; why should I care about this?
A:  Certainly, the technology used to produce geo-specific 3D visualizations is advancing, and less manual work is required these days.  Of course, there may still be special circumstances in which you need to use a different workflow (sometimes the drone solution may not be an option).

#### Q:  I tried to use this script, but it didn’t work, or something bad happened, etc.
A:  The author of this script disclaims all liability.

#### Q:  This code is crufty, inelegant, brutish, and amateur.  This doesn’t fully comply with PEP8.  Why not use one of the many XML modules that are available for Python?  This code isn’t modular.  Why don’t you check for redundancy in the input data?  You spelled something wrong.  I don’t like your variable names.  Where’s the error handling?  I can do this better! Etc.
A:  You may be right.  This solution works for the specific purpose intended, and that’s all the effort that has been put into it for now.  From one perspective, the beauty of the QGIS Processing framework is that average people are empowered to put a solution into action (even if it wouldn’t stand up to professional software development scrutiny).  By putting this script on GitHub, it is possible that someone might contribute their improvements to address any perceived shortcomings.



