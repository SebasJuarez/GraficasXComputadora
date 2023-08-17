import math
import random
import mathLibrary as ml

def waterEffect(time, position):
    frequency = 1.0  # Ajusta la frecuencia de las ondas
    amplitude = 0.1  # Ajusta la amplitud de las ondas
    
    wave_x = position[0] + time * frequency
    wave_y = position[1] + time * frequency
    
    displacement = amplitude * (math.sin(wave_x) + math.cos(wave_y))
    
    return displacement

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
    texture = kwargs["texture"]
    time = kwargs["time"]  # Nuevo parámetro para el tiempo
    
    if texture != None:
        color = texture.getColor(texCoords[0], texCoords[1])
    else:
        color = (1, 1, 1)
    
    # Aplica el efecto de ondas en el agua
    displacement = waterEffect(time, texCoords)
    texCoords = [texCoords[0], texCoords[1] + displacement]
    
    # Aplica el efecto de distorsión para simular el agua
    distortion_intensity = 0.05  # Ajusta este valor para controlar la intensidad de la distorsión
    noise = random.uniform(-distortion_intensity, distortion_intensity)
    texCoords = [texCoords[0] + noise, texCoords[1] + noise]
    
    # Obtén el color de la textura después de aplicar la distorsión
    color = texture.getColor(texCoords[0], texCoords[1])
    
    return color

def invertColorShader(**kwargs):
    texCoords = kwargs["texCoords"]
    texture = kwargs["texture"]

    if texture != None:
        color = texture.getColor(texCoords[0], texCoords[1])
    else:
        color = (1, 1, 1)
    
    # Invierte los canales de color
    inverted_color = (
        1.0 - color[0],
        1.0 - color[1],
        1.0 - color[2]
    )
    
    return inverted_color