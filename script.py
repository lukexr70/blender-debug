import bpy
import os

print("Starting Script")

# supported pairs of {ID type/section names: datablock parameter names}
known_datablock_names = {"/Camera": "cameras",
                              "/Collection": "collections",
                              "/Image": "images",
                              "/Light": "lights",
                              "/Material": "materials",
                              "/Mesh": "meshes",
                              "/Object": "objects",
                              "/Texture": "textures"}

load_from = "/Object"
path="/home/travis_frink/blender-debug/scene.blend"
with bpy.data.libraries.load(path) as (data_from, data_to):
    # check if defined ID is supported
    if load_from in known_datablock_names.keys():
        entities_to_load = getattr(data_from, known_datablock_names[load_from])
        # load entities
        for entity_to_load in entities_to_load:
            bpy.ops.wm.append(filepath=os.path.join(path, load_from, entity_to_load),
                              filename=entity_to_load,
                              directory=os.path.join(path + load_from))

bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
bpy.context.scene.cycles.device = 'GPU'
bpy.context.scene.render.engine = 'CYCLES'

for group in bpy.context.preferences.addons['cycles'].preferences.get_devices():
    for d in group:
        if "V100" in d.name:
            print(d.name)
            d.use = True

bpy.context.scene.render.threads = 0 
bpy.context.scene.render.tile_x = 1920 // 2
bpy.context.scene.render.tile_y = 1080 // 4
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 5
bpy.context.scene.frame_current=1
bpy.context.scene.render.filepath = "/home/travis_frink/blender-debug/output"

bpy.ops.render.render(animation=True,write_still=True)
