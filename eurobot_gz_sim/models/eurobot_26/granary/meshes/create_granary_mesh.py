import bpy
import bmesh
import os

# === Einstellungen ===
image_path = r"/home/mblaich/ros2_ws/src/eurobot-simulation/eurobot_gazebo/models/eurobot_26/granary/vinyle_granary_2026.png"
export_path = r"/home/mblaich/ros2_ws/src/eurobot-simulation/eurobot_gazebo/models/eurobot_26/granary/textured_block.glb"

width_m = 1.770   # 1770 mm
depth_m = 0.450   # 450 mm
height_m = 0.055  # 55 mm

# === Szene vorbereiten ===
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# === Block erstellen ===
bpy.ops.mesh.primitive_cube_add(size=1)
obj = bpy.context.active_object
obj.name = "Textured_Block"
obj.scale = (width_m / 2, depth_m / 2, height_m / 2)

# === Material und Textur erstellen ===
mat = bpy.data.materials.new(name="TopTextureMaterial")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Alte Nodes löschen
for node in nodes:
    nodes.remove(node)

# Neue Nodes erstellen
output = nodes.new("ShaderNodeOutputMaterial")
bsdf = nodes.new("ShaderNodeBsdfPrincipled")
tex_image = nodes.new("ShaderNodeTexImage")
tex_coord = nodes.new("ShaderNodeTexCoord")

# Positionieren (nur für Übersicht im Shader-Editor)
tex_coord.location = (-600, 0)
tex_image.location = (-300, 0)
bsdf.location = (0, 0)
output.location = (300, 0)

# Textur laden
if os.path.exists(image_path):
    tex_image.image = bpy.data.images.load(image_path)
    tex_image.extension = 'REPEAT'  # erlaubt volle Koordinaten
else:
    raise FileNotFoundError(f"⚠️ Bild nicht gefunden: {image_path}")

# Shader verbinden
links.new(tex_coord.outputs["UV"], tex_image.inputs["Vector"])
links.new(tex_image.outputs["Color"], bsdf.inputs["Base Color"])
links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])

# Material zuweisen
obj.data.materials.append(mat)

# === UV-Mapping: 1px = 1mm, Ursprung links unten ===
bpy.context.view_layer.objects.active = obj
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(obj.data)
uv_layer = bm.loops.layers.uv.verify()

for face in bm.faces:
    if abs(face.normal.z) > 0.9:  # nur obere und untere Flächen
        for loop in face.loops:
            uv = loop[uv_layer].uv
            vert = loop.vert.co
            # Start bei linker unterer Ecke
            uv.x = (vert.x + (width_m) / 1.18) * 1  # 1 px = 1 mm
            uv.y = (vert.y + (depth_m) *1.105) * 1
    else:
        for loop in face.loops:
            loop[uv_layer].uv = (0.5, 0.5)

bmesh.update_edit_mesh(obj.data)
bpy.ops.object.mode_set(mode='OBJECT')

print("✅ Block mit Textur erzeugt!")

# === Export glTF (.glb) ===
export_dir = os.path.dirname(export_path)
if not os.path.exists(export_dir):
    os.makedirs(export_dir)
    print(f"📁 Exportordner erstellt: {export_dir}")

bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.context.view_layer.objects.active = obj

try:
    bpy.ops.export_scene.gltf(
        filepath=export_path,
        export_format='GLB',
        use_selection=True,
        export_yup=True,
        export_apply=True,
        export_materials='EXPORT',
        export_colors=True,
        export_texcoords=True,
        export_normals=True,
        export_image_format='AUTO',
        export_embed_images=True
    )
    print(f"✅ Export erfolgreich: {export_path}")
except Exception as e:
    print(f"❌ Export fehlgeschlagen: {e}")

