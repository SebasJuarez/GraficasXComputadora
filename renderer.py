from gl import Renderer
import shaders

print("Renderizando tu archivo .obj")
print("Esepera un segundo\n\n")

width = 720
height = 360

exitFile = "photoshoots/Shader5.bmp"

rend = Renderer(width, height)

rend.glClearColor(0.5,0.5,0.5)
rend.glBackgroundTexture('./backgrounds/coffeeshop.bmp')
rend.clearBackground()

rend.vertexShader = shaders.vertexShader
# rend.fragmentShader = shaders.fragmentShader
#rend.staticShader = shaders.staticShader
#rend.NebulaShader = shaders.NebulaShader
#rend.waterFragmentShader = shaders.waterFragmentShader
#rend.invertColorShader = shaders.invertColorShader

# ~~~~~ Medium Shot ~~~~~
rend.glLookAt(camPos = (0,0,-1), eyePos= (0,0,-5))

# ~~~~~ Low Angle ~~~~~
#rend.glLookAt(camPos = (0,-3,-2), eyePos= (0,0,-5))

# ~~~~~ High Angle ~~~~~
#rend.glLookAt(camPos = (0,3,-1), eyePos= (0,0,-5))

# ~~~~~ Dutch Angle ~~~~~
#rend.glLookAt(camPos = (-3,-2,-2), eyePos= (0,0,-5))
#---------- Coffee Cups --------------------------------
rend.NebulaShader = shaders.NebulaShader  
rend.glDirectionalLight((0,1,0))     
rend.glLoadModel(filename = "models/coffee_cup_obj.obj",
                 textureName = "textures/Base_color.bmp",
                 translate = (-0.3,-0.75,-5),
                 rotate = (0, 0, 0),
                 scale = (0.6,0.6,0.6))

rend.glLoadModel(filename = "models/coffee_cup_obj.obj",
                 textureName = "textures/Base_color.bmp",
                 translate = (3.65,-0.75,-5),
                 rotate = (0, 0, 0),
                 scale = (0.6,0.6,0.6))
rend.glRender()
#------------- Pumpkin ----------------
rend.staticShader = shaders.staticShader
rend.glDirectionalLight((0,1,0))
rend.glLoadModel(filename = "models/Pumpkin.obj",
                 textureName = "textures/Pumpkin.bmp",
                 translate = (0.65,-0.03,0),
                 rotate = (0, 0, -180),
                 scale = (0.2,0.2,0.2))
rend.glRender()
#------------- Halloween Decorations --------------------------------
rend.fragmentShader = shaders.fragmentShader
rend.glDirectionalLight((0,1,0))
rend.glLoadModel(filename = "models/Halloween.obj",
                 textureName = "textures/Halloween.bmp",
                 translate = (-0.06,0.18,0),
                 rotate = (0, 0, -180),
                 scale = (1,1,1))
rend.glLoadModel(filename = "models/Halloween.obj",
                 textureName = "textures/Halloween.bmp",
                 translate = (-0.7,0.18,0),
                 rotate = (0, -20, -180),
                 scale = (1,1,1))
rend.glRender()
#-------------------- Doll -------------------------
rend.invertColorShader = shaders.invertColorShader
rend.glDirectionalLight((0,1,0))
rend.glLoadModel(filename = "models/muñeco.obj",
                 textureName = "textures/muñeco.bmp",
                 translate = (0.2,0.31,0),
                 rotate = (0, -20, -180),
                 scale = (2,2,2))
rend.glRender()
rend.glFinish(exitFile)
