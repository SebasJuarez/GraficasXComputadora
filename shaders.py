import math
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

def NebulaShader(**kwargs):
    texCoords = kwargs["texCoords"]

    # Calcula la distancia desde el centro de la nebulosa
    distance = math.sqrt((texCoords[0] - 0.5) ** 2 + (texCoords[1] - 0.5) ** 2)
    
    # Ajusta los parámetros para controlar la apariencia de la nebulosa
    brightness = 1.0 - distance * 2  # Cambia el brillo en función de la distancia al centro
    hue = (texCoords[0] + texCoords[1]) * 0.5  # Cambia el tono en función de las coordenadas

    # Convierte el color de HSL a RGB
    rgb_color = ml.hslToRgb(hue, 1.0, brightness)

    return rgb_color

def waterFragmentShader(**kwargs):
    texCoords = kwargs["texCoords"]
    time = kwargs["time"]

    # Escala el tamaño de las ondas
    uv = [texCoords[0] * 10.0, texCoords[1] * 10.0]

    # Calcula una perturbación basada en el tiempo
    offset = math.sin(uv[0] + uv[1] + time) * 0.1

    # Combina el color base con una variación basada en la perturbación
    baseColor = [0.0, 0.4, 0.8]
    waveColor = [0.0, 0.2, 0.6]

    # Combina el color base con la variación
    finalColor = [
        baseColor[0] + (waveColor[0] - baseColor[0]) * offset,
        baseColor[1] + (waveColor[1] - baseColor[1]) * offset,
        baseColor[2] + (waveColor[2] - baseColor[2]) * offset
    ]

    return finalColor