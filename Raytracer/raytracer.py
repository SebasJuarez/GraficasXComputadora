'''
Autor: Sebastian Juarez 21471

'''

import pygame
from pygame.locals import *

from rt import Raytracer
from figures import *
from lights import *
from materials import *

width = 300
height = 300

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

rayTracer = Raytracer(screen)
rayTracer.environmentMap = pygame.image.load("imagenes/fondo.jpg")
rayTracer.rtClearColor(0.25, 0.25, 0.25)
rayTracer.rtColor(1, 1, 1)


rayTracer.scene.append(
    Sphere(position=(0, 1.5, -5), radius=0.5, material=cell())
)
rayTracer.scene.append(
    Sphere(position=(0, -1.5, -5), radius=0.5, material=mirror())
)

rayTracer.scene.append(
    Sphere(position=(1.7, 1.5, -5), radius=0.5, material=glass())
)
rayTracer.scene.append(
    Sphere(position=(1.7, -1.5, -5), radius=0.5, material=diamond())
)

rayTracer.lights.append(
    AmbientLight(intensity=1)
)
rayTracer.lights.append(
    DirectionalLight(direction=(-1, -1, -1), intensity=0.5)
)
rayTracer.lights.append(
    PointLight(position=(0, 0, -4.5), intensity=1, color=(1, 0, 1))
)

rayTracer.lights.clear()
rayTracer.lights.append(
    AmbientLight(intensity=0.5)
)

rayTracer.scene.append(
    Sphere(position=(-1.7, 1.5, -5), radius=0.5, material=beach())
)

rayTracer.scene.append(
    Sphere(position=(-1.7, -1.5, -5), radius=0.5, material=room())
)

rayTracer.rtClear()
rayTracer.rtRender()

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

rect = pygame. Rect(0, 0, width, height)
sub = screen.subsurface(rect)
pygame.image.save(sub, "Resultado.png")

pygame.quit()