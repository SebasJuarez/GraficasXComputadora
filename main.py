import pygame
import glm
import math
from pygame.locals import *
from OpenGL.GL import *

from Renderer import Renderer
from modeling import Model
from Shaders import *
from objmodel import Obj

width = 500
height = 500

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

# Enable depth testing
glEnable(GL_DEPTH_TEST)

# Specify the depth function
glDepthFunc(GL_LESS)

renderer = Renderer(screen)
renderer.setShader(vertex_shader, fragment_shader)

drag = False
oldPosition = None
models = False
actualShader = 0


def printMenu():

    print("\nModelos disponibles:")
    print("1. Una planta (presiona 1)")
    print("2. Un Creaneo (presiona 2)")
    print("3. El martillo de Thor (presiona 3)")
    print("4. Unos hongos (presiona 4)")
    print("Los shaders estan en las teclas G, H, J, K, L")
    print("Te puedes mover usando las teclas de las flechas")
    print("\tPuedes hacer zoom con la rueda del mouse")

def loadModel(objF):
    objDataF = []
    for face in objF.faces:
        if len(face) == 3:
            for vertexInfo in face:
                vertexID, texcoordID, normalID = vertexInfo
                vertex = objF.vertices[vertexID - 1]
                normals = objF.normals[normalID - 1]
                uv = objF.texcoords[texcoordID - 1]
                uv = [uv[0], uv[1]]
                objDataF.extend(vertex + uv + normals)
        elif len(face) == 4:
            for i in [0, 1, 2]:
                vertexInfo = face[i]
                vertexID, texcoordID, normalID = vertexInfo
                vertex = objF.vertices[vertexID - 1]
                normals = objF.normals[normalID - 1]
                uv = objF.texcoords[texcoordID - 1]
                uv = [uv[0], uv[1]]
                objDataF.extend(vertex + uv + normals)
            for i in [0, 2, 3]:
                vertexInfo = face[i]
                vertexID, texcoordID, normalID = vertexInfo
                vertex = objF.vertices[vertexID - 1]
                normals = objF.normals[normalID - 1]
                uv = objF.texcoords[texcoordID - 1]
                uv = [uv[0], uv[1]]
                objDataF.extend(vertex + uv + normals)
    return objDataF

obj = Obj("Models/plant.obj")
objData = loadModel(obj)
model = Model(objData)
model.loadTexture("Textures/plant.bmp")
model.loadNoiseTexture("Textures/velvet.jpg")

model.position.z = -2.4
model.position.y = 0
model.position.x = -0.3
model.rotation.y = 120
model.scale = glm.vec3(0.20, 0.20, 0.20)
model.lookAt = glm.vec3(model.position.x + 0.4, model.position.y + 2 , model.position.z - 2.4)
renderer.scene.append(model)
renderer.target = model.lookAt

renderer.lightIntensity = 0.8
renderer.dirLight = glm.vec3(0.0, 0.0, -1.0)

isRunning = True

movement_sensitive = 0.1
sensX = 1
sensY = 0.1
distance = abs(renderer.cameraPosition.z- model.position.z)
radius = distance
zoomSensitive = 0.5
angle = 0

printMenu()
while isRunning:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Enable polygon offset
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(1.0, 1.0)

    deltaTime = clock.tick(60) / 1000.0
    renderer.elapsedTime += deltaTime
    keys = pygame.key.get_pressed()

    renderer.cameraPosition.x = math.sin(math.radians(angle)) * radius + model.position.x
    renderer.cameraPosition.z = math.cos(math.radians(angle)) * radius + model.position.z

    if keys[K_RIGHT]:
        model.rotation.y += deltaTime * 50
    if keys[K_LEFT]:
        model.rotation.y -= deltaTime * 50
    if keys[K_UP]:
        if (model.rotation.x <= 45):
            model.rotation.x += deltaTime * 50
    if keys[K_DOWN]:
        if (model.rotation.x >= -100):
            model.rotation.x -= deltaTime * 50
    if keys[K_PLUS]:
        if (model.position.z <= 0):
            model.position.z += 0.1
    if keys[K_MINUS]:
        if (model.position.z >= -10):
            model.position.z -= 0.1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            if event.key == pygame.K_m:
                printMenu()
            if event.key == pygame.K_g:
                renderer.setShader(vertex_shader, fragment_shader)

            if event.key == pygame.K_h:
                actualShader = 1
                renderer.setShader(vertex_shader, stroboscopic_fragment_shader)

            if event.key == pygame.K_j:
                actualShader = 2
                renderer.setShader(vertex_shader, tv_noise_fragment_shader)

            if event.key == pygame.K_k:
                actualShader = 3
                renderer.setShader(vertex_shader, distorsioned_fragment_shader)

            if event.key == pygame.K_l:
                actualShader = 4
                renderer.setShader(vertex_shader, anime_style_fragment_shader)

            if event.key == pygame.K_1:
                models = False
                renderer.scene.clear()
                obj = Obj("Models/plant.obj")
                objData = loadModel(obj)
                model = Model(objData)
                model.loadTexture("Textures/plant.bmp")
                model.loadNoiseTexture("Textures/velvet.jpg")
                model.position.z = -2.4
                model.position.y = 0
                model.position.x = -0.3
                model.rotation.y = 120
                model.scale = glm.vec3(0.20, 0.20, 0.20)
                model.lookAt = glm.vec3(model.position.x + 0.4, model.position.y + 2 , model.position.z - 2.4)
                renderer.target = model.lookAt
                renderer.scene.append(model)
                
            if event.key == pygame.K_2:
                models = False
                renderer.scene.clear()
                obj = Obj("Models/skull.obj")
                objData = loadModel(obj)
                model = Model(objData)
                model.loadTexture("Textures/skull.bmp")
                model.loadNoiseTexture("Textures/velvet.jpg")
                model.rotation.x = -90
                model.scale = glm.vec3(0.05, 0.05, 0.05)
                model.lookAt = glm.vec3(model.position.x, model.position.y + 0.4, model.position.z)
                renderer.target = model.lookAt
                renderer.scene.append(model)

            if event.key == pygame.K_3:
                models = False
                renderer.scene.clear()
                obj = Obj("Models/thor.obj")
                objData = loadModel(obj)
                model = Model(objData)
                model.loadTexture("Textures/thor.bmp")
                model.loadNoiseTexture("Textures/velvet.jpg")
                model.rotation.x = -90
                model.scale = glm.vec3(0.8,0.8,0.8)
                model.lookAt = glm.vec3(model.position.x, model.position.y, model.position.z)
                renderer.target = model.lookAt
                renderer.scene.append(model)

            if event.key == pygame.K_4:
                models = True
                renderer.scene.clear()
                obj = Obj("Models/hongo.obj")
                objData = loadModel(obj)
                model = Model(objData)
                model.loadTexture("Textures/hongo.bmp")
                model.loadNoiseTexture("Textures/velvet.jpg")
                model.scale = glm.vec3(0.03, 0.03, 0.03)
                model.lookAt = glm.vec3(model.position.x, model.position.y + 0.6, model.position.z)
                renderer.target = model.lookAt
                renderer.scene.append(model)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                drag = True
                oldPosition = pygame.mouse.get_pos()

            elif event.button == 4:
                if radius > distance * 0.5:
                    radius -= zoomSensitive             

            elif event.button == 5:
                if radius < distance * 1.5:
                    radius += zoomSensitive

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  
                drag = False

        elif event.type == pygame.MOUSEMOTION:
            if drag:
                new_position = pygame.mouse.get_pos()
                deltax = new_position[0] - oldPosition[0]
                deltay = new_position[1] - oldPosition[1]
                angle += deltax * -sensX

                if angle > 360:
                    angle = 0

                if distance > renderer.cameraPosition.y + deltay * -sensY and distance * -1.5 < renderer.cameraPosition.y + deltay * -sensY:
                    renderer.cameraPosition.y += deltay * -sensY

                oldPosition = new_position
            

    renderer.updateViewMatrix()
    renderer.render()
    # Disable polygon offset
    glDisable(GL_POLYGON_OFFSET_FILL)
    pygame.display.flip()

pygame.quit()