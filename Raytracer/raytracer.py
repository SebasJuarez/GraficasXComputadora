'''
Autor: Sebastian Juarez 21471

'''

import pygame

from figures import *
from lights import *
from rt import *
from materials import *

width = 500
height = 500

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

rayTracer = Raytracer(screen)
rayTracer.environmentMap = pygame.image.load("imagenes/desert2.jpg")
rayTracer.rtClearColor(0.25, 0.25, 0.25)
rayTracer.rtColor(1, 1, 1)

# Piramide transparente
rayTracer.scene.append(
    Pyramid(position=(1.7, -0.9, -4), size=(1.5, 1.5, 1.5), material=glass())
)

# Piramide Reflectiva
rayTracer.scene.append(
    Pyramid(position=(-0.1, -1.3, -4), size=(1.3, 1.3, 1.3), material=Marmol())
)

# Piramide Opaca
rayTracer.scene.append(
    Pyramid(position=(-1.8, -1.7, -4), size=(1.3, 1.3, 1.3), material=Velvet())
)

# Piramide Reflectiva
rayTracer.scene.append(
    Pyramid(position=(-0.1, 0.9, -5), size=(1.8, 1.8, 1.8), material=Sky())
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

# rect = pygame. Rect(0, 0, width, height)
# sub = screen.subsurface(rect)
# pygame.image.save(sub, "Resultado.jpg")

pygame.quit()