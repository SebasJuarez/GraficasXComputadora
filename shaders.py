'''
 * Nombre: shaders.py
 * Programadora: Fernanda Esquivel (esq21542@uvg.edu.gt)
 * Lenguaje: Python
 * Recursos: VSCode
 * Historial: Finalizado el 16.07.2023 
              Modificado el 08.08.2023
 '''

import random
import mathLibrary as ml


def vertexShader(vertex, **kwargs):
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    vpMatrix = kwargs["vpMatrix"]

    vt = [vertex[0],
          vertex[1],
          vertex[2],
          1]

    mMat = ml.nMatProduct([vpMatrix, projectionMatrix, viewMatrix, modelMatrix])
    vt = ml.vecMatProduct(mMat, vt)

    vt = [vt[0]/vt[3],
          vt[1]/vt[3],
          vt[2]/vt[3]]

    return vt

def fragmentShader(**kwargs):
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]

    if texture != None:
        color = texture.getColor(texCoords[0], texCoords[1])
    else:
        color = (1,1,1)

    return color

def staticShader(**kwargs):
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]

    if texture != None:
        color = texture.getColor(texCoords[0], texCoords[1])
    else:
        color = (1, 1, 1)
    
    # Aplica el efecto de estática
    static_intensity = 0.4  # Ajusta este valor para controlar la intensidad de la estática
    
    # Genera un valor de ruido diferente para cada canal de color (r, g, b)
    noise_r = random.uniform(-static_intensity, static_intensity)
    noise_g = random.uniform(-static_intensity, static_intensity)
    noise_b = random.uniform(-static_intensity, static_intensity)
    
    # Aplica el ruido a cada canal de color
    static_color = (
        color[0] + noise_r,
        color[1] + noise_g,
        color[2] + noise_b
    )
    
    return static_color