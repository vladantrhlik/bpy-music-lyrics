import bpy
import json

FPS = bpy.context.scene.render.fps

project = "Men I Trust - Found me"

path = bpy.data.filepath
folders = path.split("\\")
project_folder = "\\".join(folders[:-1])

 
with open(f"{project_folder}\{project}\data.json") as f:
  data = json.load(f)["data"]
  
#light
bpy.ops.object.light_add(type='SUN', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

#camera 
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 15), rotation=(0,0,0), scale=(1, 1, 1))
cam = bpy.context.object

#background
bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1,1,1))
bg = bpy.context.object
bg.scale = (20,20,20)
bg.location = (8,-8,0)

x = 0 
space = 0.5
line_height = 1.5
part_spacing = 2
y = 0
frame = 1000/FPS # lenght of 1 frame in ms

def ms_to_frame(ms):
    return round(ms / frame)

def create_text(txt):
    bpy.ops.object.text_add()
    ob = bpy.context.object
    tcu = ob.data
    tcu.body = txt
    # Inherited Curve attributes
    tcu.extrude = 0.05
    return ob


shadow = True
shadow_mat = bpy.data.materials.new("shadow_mat")
shadow_mat.roughness = 1
shadow_mat.diffuse_color = (0,0,0,1)
shadow_offset = 0.02 

for p, part in enumerate(data):
    #set camera to default z
    f = ms_to_frame(part[0][0][1])
    cam.location.z = 15
    cam.keyframe_insert("location", index=2,frame = f)
    for l,line in enumerate(part):
        
        for w,word in enumerate(line):   
            # Create TextCurve object
            ob = create_text(word[0])
            
            #shadow
            if shadow:
                shadow_ob = create_text(word[0])
                shadow_ob.parent = ob
                shadow_ob.location = (shadow_offset,shadow_offset,-0.01)
                shadow_ob.data.materials.append(shadow_mat)
            #shadow material
            
            # material stuff
            mat = bpy.data.materials.new("mat_" + str(x) + str(y))
            mat.roughness = 1
            # animating color
            
            f = ms_to_frame(word[1])
            word_length = 30
            if w < len(line)-1:
                word_legth = ms_to_frame(line[w+1][1] - word[1])
            
            mat.diffuse_color = (1,1,1,1)
            mat.keyframe_insert("diffuse_color", frame=f-5)
            mat.keyframe_insert("diffuse_color", frame=f+word_legth+15)
            
            mat.diffuse_color = (0,0,0,1)
            mat.keyframe_insert("diffuse_color", frame=f )
            mat.keyframe_insert("diffuse_color", frame=f + word_legth)
            
            
            ob.data.materials.append(mat)
            
            # animating location
            ob.location.x = x
            ob.location.y = y
            ob.keyframe_insert("location", frame=f )
            
            ob.location.x = x
            ob.location.y = y-10
            ob.keyframe_insert("location", frame=f-50  )

            ob.location.y = 10

            #shadow
            shadow = bpy.data.objects.new('TextOwo', ob.data)
            shadow.parent = ob
            
            # updating scene to get right dimensions of word
            bpy.context.view_layer.update()
            
            
            #cam anim
            cam.location.x = x + ob.dimensions.x/2
            cam.location.y = y
            cam.keyframe_insert("location", frame = f)
            
            
            x+=ob.dimensions.x+space
        y-=line_height
        x = 0
    #camera transition between parts
    if p < len(data)-1:
        f = ms_to_frame((part[-1][-1][1] + data[p+1][0][0][1])/2)
        cam.location.z = 30
        print(f)
        cam.keyframe_insert("location", index=2,frame = f)
                
    y-=part_spacing