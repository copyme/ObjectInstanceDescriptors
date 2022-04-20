# Author: Kacper Pluta - kacper.pluta@inria.fr
# Works on any platform on which Blender works too. The command may have to be adjusted with respect to the local paths see CHANGE ME section.

# The FBX classes are extracted and saved to separate PLY files.

# Linux: blender --background --python fbx_class_extractor.py
# Windows PowerShell: & 'C:\Program Files\Blender Foundation\Blender 3.1\blender.exe' --background --python fbx_class_extractor.py

# You will need to adjust the CHANGE ME section!


import bpy
import os
 
# CHANGE ME - BEGIN

# get the path and make a new folder for the exported meshes
path = bpy.path.abspath(os.environ['USERPROFILE'] + '\\fbx-ply-export')
FBXfile = os.environ['USERPROFILE'] + '\\Documents\\Project\\Données\\Batiment_ifc-convert.fbx'

# path = bpy.path.abspath('/user/kpluta/home/plyexport/')
# FBXfile = bpy.path.abspath('/user/kpluta/home/Downloads/H0022.fbx')

# CHANGE ME - END

if not os.path.exists(path):
    os.makedirs(path)
    
# remove init. cube
try:
    object_to_delete = bpy.data.objects['Cube']
    bpy.data.objects.remove(object_to_delete, do_unlink=True)
except:
  print("Cube does not exist!")     
    
# read bfx
bpy.ops.import_scene.fbx(filepath = FBXfile)


# export everything
ply_path=os.path.join(path, 'fbx2ply-all.ply')
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.export_mesh.ply(filepath=ply_path, use_selection=True, axis_forward='Y', axis_up='Z')

# # iterate over named objects
#collect objects to save
# bpy.ops.object.select_all(action='DESELECT')
# bpy.ops.object.select_by_type(type='MESH')
# names = [o.name for o in bpy.context.selected_objects]

# # deselect all
# bpy.ops.object.select_all(action='DESELECT')
# for name in names:
    # # select the object
    # obj = bpy.data.objects[name]
    # bpy.context.view_layer.objects.active = obj
    # obj.select_set(True)

    # # export object with its name as file name
    # ply_path = os.path.join(path, name + '.ply')

    # bpy.ops.export_mesh.ply(filepath=ply_path, use_selection=True, axis_forward='-Y', axis_up='Z')
    # # deselect
    # obj.select_set(False)
