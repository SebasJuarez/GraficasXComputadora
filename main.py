import pygame
import glm
from pygame.locals import *

from modeling import modeling
from Renderer import Renderer
from Shaders import *
from objmodel import objmodel


width = 960
height = 540

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE)

clock = pygame.time.Clock()

renderer = Renderer(screen)
renderer.setShader(vertex_shader, fragment_shader)
obj = objmodel("Models/Plant/plant.obj")
objData = []

for face in obj.faces:
    if len(face) == 3:
        for vertexInfo in face:
            vertexID, texcoordID, normalID = vertexInfo
            vertex = obj.vertices[vertexID - 1]
            normals = obj.normals[normalID - 1]
            uv = obj.texcoords[texcoordID - 1]
            uv = [uv[0], uv[1]]
            objData.extend(vertex + uv + normals)
    elif len(face) == 4:
        for i in [0, 1, 2]:
            vertexInfo = face[i]
            vertexID, texcoordID, normalID = vertexInfo
            vertex = obj.vertices[vertexID - 1]
            normals = obj.normals[normalID - 1]
            uv = obj.texcoords[texcoordID - 1]
            uv = [uv[0], uv[1]]
            objData.extend(vertex + uv + normals)
        for i in [0, 2, 3]:
            vertexInfo = face[i]
            vertexID, texcoordID, normalID = vertexInfo
            vertex = obj.vertices[vertexID - 1]
            normals = obj.normals[normalID - 1]
            uv = obj.texcoords[texcoordID - 1]
            uv = [uv[0], uv[1]]
            objData.extend(vertex + uv + normals)


model = modeling(objData)
model.loadTexture("Models/Plant/plant.png")
model.position.z = -1
model.position.y = 0
model.scale = glm.vec3(0.01, 0.01, 0.01)
renderer.scene.append(model)
FPS = 60

isRunning = True
while isRunning:
    deltaTime = clock.tick(FPS) / 1000.0
    renderer.elapsedTime += deltaTime
    keys = pygame.key.get_pressed()

    if keys[K_RIGHT]:
        model.position.x += deltaTime
    if keys[K_LEFT]:
        model.position.x -= deltaTime
    if keys[K_UP]:
        model.position.y += deltaTime
    if keys[K_DOWN]:
        model.position.y -= deltaTime
    if keys[K_SPACE]:
        model.position.z += deltaTime
    if keys[K_LSHIFT]:
        model.position.z -= deltaTime

    if keys[K_d]:
        model.rotation.y += deltaTime * 50
    if keys[K_a]:
        model.rotation.y -= deltaTime * 50
    if keys[K_w]:
        model.rotation.x += deltaTime * 50
    if keys[K_s]:
        model.rotation.x -= deltaTime * 50

    if keys[K_q]:
        if renderer.fatness > 0:
            renderer.fatness -= deltaTime
    if keys[K_e]:
        if renderer.fatness < 1:
            renderer.fatness += deltaTime

    # Handle quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            if event.key == pygame.K_f:
                renderer.toggleFilledMode()
            # Handle Shaders
            if event.key == K_0:
                renderer.setShader(vertex_shader, fragment_shader)
            if event.key == K_1:
                renderer.setShader(vertex_shader, dirtAndDamage_fragment_shader)

    renderer.updateViewMatrix()
    renderer.render()
    pygame.display.flip()

pygame.quit()