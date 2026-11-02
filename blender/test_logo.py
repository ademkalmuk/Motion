# Blender test: 3D extruded "KALMUK" text, rendered headless with Eevee/Workbench.
# Usage: blender -b -P blender/test_logo.py -- out.png
import bpy, sys
out = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "/tmp/blender_test.png"
bpy.ops.wm.read_factory_settings(use_empty=True)
s = bpy.context.scene
s.render.resolution_x, s.render.resolution_y = 1080, 1920
bpy.ops.object.text_add(location=(0, 0, 0))
t = bpy.context.object; t.data.body = "KALMUK"; t.data.extrude = 0.15; t.data.align_x = 'CENTER'
mat = bpy.data.materials.new("blue"); mat.diffuse_color = (0.32, 0.64, 1, 1); t.data.materials.append(mat)
bpy.ops.object.camera_add(location=(0, -9, 1.5), rotation=(1.42, 0, 0)); s.camera = bpy.context.object
bpy.ops.object.light_add(type='SUN', location=(3, -3, 5))
s.render.engine = 'BLENDER_WORKBENCH'
s.render.filepath = out
bpy.ops.render.render(write_still=True)
