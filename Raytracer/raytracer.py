'''
Autor: Sebastian Juarez 21471

'''

import pygame
from pygame.locals import *

from rt import *
from figures import *
from lights import *
from materials import *

width = 480
height = 480

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

rayTracer = Raytracer(screen)
rayTracer.rtClearColor(0.2, 0.2, 0.2)
rayTracer.rtColor(1, 1, 1)

rayTracer.scene.append(
    Plane(position=(0, -2, 0), normal=(0, 1, -0.2), material=floor())
)
rayTracer.scene.append(
    Plane(position=(0, 5, 0), normal=(0, 1, 0.2), material=ceiling())
)
rayTracer.scene.append(
    Plane(position=(4, 0, 0), normal=(1, 0, 0.2), material=wall())
)
rayTracer.scene.append(
    Plane(position=(-4, 0, 0), normal=(1, 0, -0.2), material=wall())
)
rayTracer.scene.append(
    Plane(position=(0, 0, 5), normal=(0, 0, 1), material=wall())
)

rayTracer.scene.append(
    Disk(position=(0, 0, -7), normal=(0, 0, 1), radius=1, material=mirror())
)

rayTracer.scene.append(
    AABB(position=(-1, 1, -5), size=(1, 1, 1), material=Velvet())
)
rayTracer.scene.append(
    AABB(position=(-1, -1, -5), size=(1, 1, 1), material=Marmol())
)
rayTracer.scene.append(
    AABB(position=(1, 1, -5), size=(1, 1, 1), material=Marmol())
)
rayTracer.scene.append(
    AABB(position=(1, -1, -5), size=(1, 1, 1), material=Sky())
)

rayTracer.lights.append(
    AmbientLight(intensity=0.7)
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