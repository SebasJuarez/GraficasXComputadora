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
rayTracer.environmentMap = pygame.image.load("imagenes/desert3.jpg")
rayTracer.rtClearColor(0.25, 0.25, 0.25)
rayTracer.rtColor(1, 1, 1)

# Piramide del fondo (Opacas)
rayTracer.scene.append(
    Pyramid(position=(1.9, -0.5, -6), size=(1.5, 1.5, 1.5), material=BlockPyramid())
)
rayTracer.scene.append(
    Pyramid(position=(1.0, -0.5, -7), size=(0.9, 0.9, 0.9), material=BlockPyramid())
)
rayTracer.scene.append(
    Pyramid(position=(0, -0.5, -6), size=(1.5, 1.5, 1.5), material=BlockPyramid())
)
rayTracer.scene.append(
    Pyramid(position=(-1.9, -0.5, -5), size=(1.2, 1.2, 1.2), material=BlockPyramid())
)

# Pipes de mario (Reflectivos)
rayTracer.scene.append(
    Cylinder(position=(1.7, -2.5, -4), radius=0.2, height=1.3, material=greenMirror(), rotation_z=0.0)
)
rayTracer.scene.append(
    Cylinder(position=(1.3, -2.5, -4), radius=0.2, height=0.8, material=greenMirror(), rotation_z=0.0)
)
rayTracer.scene.append(
    Cylinder(position=(1.0, -2.5, -4), radius=0.2, height=1.0, material=greenMirror(), rotation_z=0.0)
)
rayTracer.scene.append(
    Cylinder(position=(-0.8, -2.5, -4), radius=0.2, height=1.3, material=greenMirror(), rotation_z=0.0)
)
rayTracer.scene.append(
    Cylinder(position=(-1.8, -2.5, -4), radius=0.2, height=1.3, material=greenMirror(), rotation_z=0.0)
)

# Platillo volador (Cilindro Refractivo, Esfera opaca)
rayTracer.scene.append(
    Cylinder(position=(-0.7, 0.7, -4), radius=1.0, height=0.3, material=glass(), rotation_z=0.2)
)
rayTracer.scene.append(
    Sphere(position=(-1.1, 1.3, -5), radius=0.6, material=Sun())
)

rayTracer.lights.append(
    AmbientLight(intensity=0.7)
)

# Piramide Reflectiva
# rayTracer.scene.append(
#     Pyramid(position=(-0.1, -1.3, -4), size=(1.3, 1.3, 1.3), material=Marmol())
# )

# # Piramide Opaca
# rayTracer.scene.append(
#     Pyramid(position=(-1.8, -1.7, -4), size=(1.3, 1.3, 1.3), material=Velvet())
# )



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