# Usage: python3 render_still.py <dir with scene.glb + shot.json> <out.png> [samples] [width]
# Renders the exact room scene with Blender's Cycles engine (pip install bpy). Free, CPU only.
import bpy, json, sys, math, os
from mathutils import Vector
d, out = sys.argv[1], sys.argv[2]
samples = int(sys.argv[3]) if len(sys.argv) > 3 else 160
width = int(sys.argv[4]) if len(sys.argv) > 4 else 1600
shot = json.load(open(os.path.join(d, 'shot.json')))
L = shot['lights']
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.join(d, 'scene.glb'))
B = lambda p: Vector((p[0], -p[2], p[1]))          # three.js (x,y,z) meters -> Blender (x,-z,y)
sc = bpy.context.scene
for o in list(sc.objects):
    if o.name.startswith('windowGlass'):
        bpy.data.objects.remove(o)                  # open the window so real light comes in
for o in sc.objects:
    if o.type == 'MESH':
        names = [m.name.split('.')[0] for m in o.data.materials if m]
        if any(n in ('lampOn', 'lampOff', 'can', 'fanLamp', 'clearGlass', 'blind') for n in names):
            o.visible_shadow = False
def emit(name, strength):
    for m in bpy.data.materials:
        if m.name.split('.')[0] == name and m.node_tree:
            for n in m.node_tree.nodes:
                if n.type == 'BSDF_PRINCIPLED':
                    n.inputs['Emission Strength'].default_value = strength
                    if strength > 0: n.inputs['Emission Color'].default_value = (1, .86, .68, 1) if name != 'screenOn' else (.06, .1, .22, 1)
emit('can', 12 if L['cans'] else 0); emit('fanLamp', 12 if L['fan'] else 0); emit('lampOn', 6); emit('screenOn', .1 if L['sun'] else .35)
for m in bpy.data.materials:
    if m.name.split('.')[0] == 'floor' and m.node_tree:
        for n in m.node_tree.nodes:
            if n.type == 'BSDF_PRINCIPLED': n.inputs['Roughness'].default_value = .45
def lamp(kind, loc, watts, color=(1, .84, .64), size=.06, spot=None, aim=None):
    ld = bpy.data.lights.new(kind, kind); ld.energy = watts; ld.color = color; ld.shadow_soft_size = size
    if spot: ld.spot_size = spot; ld.spot_blend = .6
    ob = bpy.data.objects.new(kind, ld); ob.location = loc; sc.collection.objects.link(ob)
    if aim is not None: ob.rotation_euler = (Vector(aim) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    return ob
world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True
bg = world.node_tree.nodes['Background']
if L['sun']:
    bg.inputs[0].default_value = (.8, .88, 1, 1); bg.inputs[1].default_value = 3.5
    w = shot['win']; inside = Vector((w['x'] - 2.6, -(w['z'] - .5), .1))
    s = lamp('SUN', (w['x'] + 2, -w['z'] - .3, w['y'] + 1.6), 2.4, (1, .93, .82), aim=inside); s.data.angle = math.radians(2)
else:
    bg.inputs[0].default_value = (.05, .08, .16, 1); bg.inputs[1].default_value = .15
if L['cans']:
    for c in shot['cans']: p = B(c); lamp('SPOT', p, 55, spot=math.radians(110), aim=(p.x, p.y, 0), size=.08)
if L['fan']: lamp('POINT', B(shot['fan']) - Vector((0, 0, .08)), 30, size=.09)
for l in shot['itemLights']:
    p = B(l['p'])
    if l['type'] == 'SpotLight': lamp('SPOT', p, 14, spot=math.radians(95), aim=(p.x - .1, p.y - .15, p.z - .37), size=.03)
    elif l['color'] == 0xdfe8ff: lamp('POINT', p, 2.5, (.8, .87, 1), size=.2)
    else: lamp('POINT', p, 16 if l['intensity'] > 2 else 6, size=.08)
c = shot['cam']; cd = bpy.data.cameras.new('cam'); cd.sensor_fit = 'VERTICAL'; cd.angle_y = math.radians(c['fov']); cd.clip_start = .05
cam = bpy.data.objects.new('cam', cd); cam.location = B(c['p']); cam.rotation_euler = (B(c['t']) - B(c['p'])).to_track_quat('-Z', 'Y').to_euler()
sc.collection.objects.link(cam); sc.camera = cam
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = samples; sc.cycles.use_denoising = True
sc.cycles.max_bounces = 8; sc.cycles.diffuse_bounces = 5; sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False
sc.render.resolution_x = width; sc.render.resolution_y = int(width / c['aspect']); sc.render.resolution_percentage = 100
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
sc.view_settings.exposure = 2.6 if L['sun'] else .9
sc.render.image_settings.file_format = 'JPEG' if out.lower().endswith('.jpg') else 'PNG'; sc.render.image_settings.quality = 90; sc.render.filepath = os.path.abspath(out)
bpy.ops.render.render(write_still=True); print('rendered', out)
