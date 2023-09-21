'''
Autor: Sebastian Juarez 21471

'''

import pygame
from pygame.locals import *

from rt import Raytracer
from figures import *
from lights import *
from materials import *

width = 500
height = 500

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

rayTracer = Raytracer(screen)
rayTracer.rtClearColor(0.2, 0.2, 0.5)
rayTracer.rtColor(1, 1, 1)

# Cuerpo del muñeco
rayTracer.scene.append(Sphere(position = (0, 1.7, -7), radius = 1.2, material = snow()))
rayTracer.scene.append(Sphere(position = (0, 0.2, -7), radius = 1.4, material = snow()))
rayTracer.scene.append(Sphere(position = (0, -1.5, -7), radius = 1.6, material = snow()))

# Cara del muñeco

    # Nariz
rayTracer.scene.append(Sphere(position = (0, 1.2, -5), radius = 0.15, material=  carrot()))
    # Botones de la boca
rayTracer.scene.append(Sphere(position = (0.15, 0.9, -5), radius = 0.06, material=  black_metal()))
rayTracer.scene.append(Sphere(position = (-0.15, 0.9, -5), radius = 0.06, material=  black_metal()))
rayTracer.scene.append(Sphere(position = (0, 0.9, -5), radius = 0.06, material=  black_metal()))
rayTracer.scene.append(Sphere(position = (0.29, 1.0, -5), radius = 0.06, material=  black_metal()))
rayTracer.scene.append(Sphere(position = (-0.29, 1.0, -5), radius = 0.06, material=  black_metal()))
    # Ojos
rayTracer.scene.append(Sphere(position = (0.19, 1.13, -4), radius = 0.11, material=  stone()))
rayTracer.scene.append(Sphere(position = (-0.19, 1.13, -4), radius = 0.11, material=  stone()))

#Botones del muñeco
rayTracer.scene.append(Sphere(position = (0, 0.3, -5), radius = 0.15, material=  black_metal()))
rayTracer.scene.append(Sphere(position = (0, -0.4, -5), radius = 0.20, material=  black_metal()))
rayTracer.scene.append(Sphere(position = (0, -1.1, -5), radius = 0.25, material=  black_metal()))

# Iluminación del muñeco
rayTracer.lights.append(AmbientLight(intensity=0.9))
rayTracer.lights.append(DirectionalLight(direction=(-0.5, -1, 1), intensity=1, color=(0.9, 1, 0.1)))
rayTracer.lights.append(PointLight(position=(2.5, -1, -5), intensity=0.7, color=(1, 0, 0)))

isRunning = True

while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    rayTracer.rtClear()
    rayTracer.rtRender()
    pygame.display.flip()

pygame.quit()