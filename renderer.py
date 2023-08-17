from gl import Renderer
import shaders

print("Renderizando tu archivo .obj")
print("Esepera un segundo\n\n")

width = 1080
height = 720

modelFile = "models/model.obj"
textureFile = "textures/model.bmp"
exitFile = "photoshoots/mediumShot.bmp"

rend = Renderer(width, height)

rend.vertexShader = shaders.vertexShader
#rend.fragmentShader = shaders.fragmentShader
#rend.staticShader = shaders.staticShader
#rend.NebulaShader = shaders.NebulaShader

# ~~~~~ Medium Shot ~~~~~
rend.glLookAt(camPos = (0,0,-1), eyePos= (0,0,-5))

# ~~~~~ Low Angle ~~~~~
#rend.glLookAt(camPos = (0,-3,-2), eyePos= (0,0,-5))

# ~~~~~ High Angle ~~~~~
#rend.glLookAt(camPos = (0,3,-1), eyePos= (0,0,-5))

# ~~~~~ Dutch Angle ~~~~~
#rend.glLookAt(camPos = (-3,-2,-2), eyePos= (0,0,-5))
        
rend.glLoadModel(filename = modelFile,
                 textureName = textureFile,
                 translate = (0,0,-10),
                 rotate = (0, 0, 0),
                 scale = (3,3,3))

rend.glRender()

rend.glFinish(exitFile)
