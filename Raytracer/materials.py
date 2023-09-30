'''
Autor: Sebastian Juarez 21471

'''
import pygame

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

class Material:
    def __init__(self, diffuse=(1, 1, 1), spec=1.0, Ks=0.0, ior=1.0, type=OPAQUE, texture=None):
        self.diffuse = diffuse
        self.spec = spec
        self.Ks = Ks
        self.ior = ior
        self.type = type
        self.texture = texture

def glass():
    return Material(diffuse=(0.8, 0.8, 0.8), spec=64, Ks=0.15, ior=1.5, type=TRANSPARENT)

def diamond():
    return Material(diffuse=(0.6, 0.6, 0.6), spec=128, Ks=0.2, ior=2.417, type=TRANSPARENT)

def mirror():
    return Material(diffuse=(0.8, 0.8, 0.8), spec=64, Ks=0.2, type=REFLECTIVE)

def blueMirror():
    return Material(diffuse=(0.2, 0.2, 0.8), spec=32, Ks=0.15, type=REFLECTIVE)

def beach():
    return Material(spec=256, Ks=0.01, texture=pygame.image.load("imagenes/beach.jpeg"))

def room():
    return Material(spec=256, Ks=0.01, texture=pygame.image.load("imagenes/room.jpg"))

def cell():
    return Material(spec=64, Ks=0.2, type=REFLECTIVE, texture=pygame.image.load("imagenes/cells.jpg"))

def brick():
    return Material(diffuse=(1.0, 0.3, 0.2), spec=8, Ks=0.01)

def grass():
    return Material(diffuse=(0.2, 0.8, 0.2), spec=32, Ks=0.1)

def water():
    return Material(diffuse=(0.2, 0.2, 0.8), spec=256, Ks=0.5)