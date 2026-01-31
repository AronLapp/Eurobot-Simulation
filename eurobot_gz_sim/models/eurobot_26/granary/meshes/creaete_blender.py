import bpy
import os

# === Einstellungen ===
# Pfad zum Bild (bitte Pfad anpassen, falls nötig)
image_path = r"/home/mblaich/ros2_ws/src/eurobot-simulation/eurobot_gazebo/models/eurobot_26/granary/vinyle_granary_2026.png"

# Maße in Metern (1 m = 1000 mm)
width = 1.770   # 1770 mm
depth = 0.450   # 450 mm
height = 0.055  # 55 mm

# === Szene vorbereiten ===
#bpy.ops.wm.read_factory_settings(use_empty=True)

# Quader erstellen
bpy.ops.mesh.primitive_cube_add(size=1)
obj = bpy.context.active_object
obj.name = "Textured_Block"
obj.scale = (width / 2, depth / 2, height / 2)

# === Material erstellen ===
mat = bpy.data.materials.new(name="TopTextureMaterial")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links
bsdf = nodes.get("Principled BSDF")

# Textur-Node
tex_image = nodes.new("ShaderNodeTexImage")

# Bild laden
if os.path.exists(image_path):
    tex_image.image = bpy.data.images.load(image_path)
else:
    print("⚠️ Bild nicht gefunden! Pfad prüfen:", image_path)

links.new(bsdf.inputs["Base Color"], tex_image.outputs["Color"])
obj.data.materials.append(mat)

# === UV-Mapping gezielt für große Flächen ===
bpy.context.view_layer.objects.active = obj
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(obj.data)

# UV-Layer anlegen
uv_layer = bm.loops.layers.uv.verify()

# Für jede Fläche prüfen, ob sie oben oder unten liegt
for face in bm.faces:
    # Normale prüfen (Z-Richtung)
    if abs(face.normal.z) > 0.9:
        for loop in face.loops:
            uv = loop[uv_layer].uv
            vert = loop.vert.co
            # Textur über volle Fläche strecken (X → U, Y → V)
            uv.x = (vert.x / width) + 0.5
            uv.y = (vert.y / depth) + 0.5
    else:
        # Seitenflächen bekommen neutrale UVs (z.B. schwarze Farbe)
        for loop in face.loops:
            loop[uv_layer].uv = (0.5, 0.5)

bmesh.update_edit_mesh(obj.data)
bpy.ops.object.mode_set(mode='OBJECT')

print("✅ Fertig! Nur obere und untere Flächen haben die gestreckte Textur.")
