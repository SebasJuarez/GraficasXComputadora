import struct
import mathLibrary as ml
from math import pi, sin, cos, tan
from obj import Obj
from texture import Texture
POINTS = 0
LINES = 1
TRIANGLES = 2
QUADS = 3

def char(c):
    #1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    #2 bytes
    return struct.pack('=h', w)

def dword(d):
    #4 bytes
    return struct.pack('=l', d)

def color(r, g, b):
    # Asegura que los valores estén en el rango correcto
    r = max(0, min(255, int(r * 255)))
    g = max(0, min(255, int(g * 255)))
    b = max(0, min(255, int(b * 255)))
    
    return bytes([r, g, b])

class Model(object):
    def __init__(self, filename, translate = (0,0,0), rotate = (0,0,0), scale = (1,1,1)):
        
        model = Obj(filename)

        self.vertices = model.vertices
        self.texcoords = model.texcoords
        self.normals = model.normals
        self.faces = model.faces

        self.translate = translate
        self.rotate = rotate
        self.scale = scale

    def LoadTexture(self, textureName):
        self.texture = Texture(textureName)



class Renderer(object):
    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.glClearColor(0.5,0.5,0.5)
        self.glClear()

        self.glColor(1,1,1)

        self.objects = []

        self.vertexShader = None
        self.fragmentShader = None

        self.primitiveType = TRIANGLES

        self.vertexBuffer=[ ]

        self.activeTexture = None
        
        self.glViewPort(0,0,self.width,self.height)
        self.glCamMatrix()
        self.glProjectionMatrix()

    def glAddVertices(self, vertices):
        for vert in vertices:
            self.vertexBuffer.append(vert)

    def glPrimitiveAssembly(self,tVerts, tTexCoords, tNormals):
        primitives = [ ]
        if self.primitiveType == TRIANGLES:
            for i in range(0,len(tVerts), 3):
                
                #Verts
                verts =[]
                verts.append(tVerts[i])
                verts.append(tVerts[i+1])
                verts.append(tVerts[i+2])
                #TexCoords
                texCoords = []
                texCoords.append(tTexCoords[i])
                texCoords.append(tTexCoords[i+1])
                texCoords.append(tTexCoords[i+2])
                #Normals
                normals = []
                normals.append(tNormals[i])
                normals.append(tNormals[i+1])
                normals.append(tNormals[i+2])

                triangle = [verts, texCoords, normals]

                primitives.append(triangle)
        
        return primitives
    
    def glDirectionalLight(self, dlLight):
        self.directionalLight = dlLight

    def glClearColor(self, r, g, b):
        # Establecer el color de fondo
        self.clearColor = color(r,g,b)


    def glColor(self, r, g, b):
        # Establecer el color default de rederización.
        self.currColor = color(r,g,b)


    def glClear(self):
        # Se crea la tabla de pixeles del tamaño width*height.
        # Se le asigna a cada pixel el color de fondo.
        self.pixels = [[self.clearColor for y in range(self.height)]
                       for x in range(self.width)]

        # Se crea otra tabla para el Z Buffer. Aquí se guarda la profundidad
        # de cada pixel, con el valor máximo de profundidad inicial.
        self.zbuffer = [[float('inf') for y in range(self.height)]
                       for x in range(self.width)]


    def glPoint(self, x, y, clr = None):
        # Si el valor de X y Y está dentro del ancho y alto del framebuffer,
        # dibujar el punto en la posición (x,y) del FrameBuffer.
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[x][y] = clr or self.currColor


    def glTriangle(self, verts, texCoords, normals):
        A = verts[0]
        B = verts[1]
        C = verts[2]
        minX = round(min(A[0], B[0], C[0]))
        maxX = round(max(A[0], B[0], C[0]))
        minY = round(min(A[1], B[1], C[1]))
        maxY = round(max(A[1], B[1], C[1]))

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                if (0 <= x < self.width) and (0 <= y < self.height):
                    P = (x, y)
                    bCoords = ml.barycentricCoords(A, B, C, P)
                    u, v, w = bCoords

                    if all(0 <= val <= 1 for val in bCoords):
                        z = u * A[2] + v * B[2] + w * C[2]
                        
                        if z < self.zbuffer[x][y]:
                            self.zbuffer[x][y] = z
                            
                            texCoord = (
                                u * texCoords[0][0] + v * texCoords[1][0] + w * texCoords[2][0],
                                u * texCoords[0][1] + v * texCoords[1][1] + w * texCoords[2][1]
                            )

                            if self.fragmentShader:
                                shaderColor = self.fragmentShader(
                                    texture=self.activeTexture,
                                    texCoords=texCoord,
                                    normals=(
                                        u * normals[0][0] + v * normals[1][0] + w * normals[2][0],
                                        u * normals[0][1] + v * normals[1][1] + w * normals[2][1],
                                        u * normals[0][2] + v * normals[1][2] + w * normals[2][2]
                                    ),
                                    dLight=self.directionalLight,
                                    bCoords=bCoords
                                )
                            else:
                                shaderColor = (1, 1, 1)

                            texColor = self.activeTexture.getColor(texCoord[0], texCoord[1])

                            finalColor = (
                                texColor[0] * shaderColor[0],
                                texColor[1] * shaderColor[1],
                                texColor[2] * shaderColor[2]
                            )

                            self.glPoint(x, y, color(finalColor[0], finalColor[1], finalColor[2]))

    #Frustum: lo que esta dentro de el, se renderiza.
    def glViewPort(self,x,y,width,height):
        self.vpX = x
        self.vpY = y
        self.vpWidth = width
        self.vpHeight = height
        
        self.vpMatrix = [[self.vpWidth/2,0,0,self.vpX+self.vpWidth/2],
                        [0,self.vpHeight/2,0,self.vpY+self.vpHeight/2],
                        [0,0,0.5,0.5],
                        [0,0,0,1]]

    def glCamMatrix(self, translate = (0,0,0), rotate = (0,0,0)):
        #Crea matrix de camara
        self.camMatrix = self.glModelMatrix(translate, rotate)
        
        #Matriz de vista es igual a la inversa de la camara
        self.viewMatrix = ml.matInverse(self.camMatrix)
          
    def glLookAt(self, camPos = (0,0,0), eyePos = (0,0,0)):
        worldUp = (0,1,0)
        
        forward = ml.vecNorm(ml.twoVecSubstraction(camPos, eyePos))
        right = ml.vecNorm(ml.twoVecProduct(worldUp, forward))
        up = ml.vecNorm(ml.twoVecProduct(forward, right))
        
        self.camMatrix = [[right[0],up[0],forward[0],camPos[0]],
                          [right[1],up[1],forward[1],camPos[1]],
                          [right[2],up[2],forward[2],camPos[2]],
                          [0,0,0,1]]
        
        self.viewMatrix = ml.matInverse(self.camMatrix)
        
    def glProjectionMatrix(self, fov = 60, n = 0.1, f = 1000):
        aspectRatio = self.vpWidth/self.vpHeight
        
        t = tan((fov*pi/180)/2)*n
        
        r = t*aspectRatio
        
        self.projectionMatrix = [[n/r,0,0,0],
                                [0,n/t,0,0],
                                [0,0,-(f+n)/(f-n),(-2*f*n)/(f-n)],
                                [0,0,-1,0]]
    
    def glModelMatrix(self, translate = (0,0,0), rotate = (0,0,0), scale = (1,1,1)):

        # Matriz de traslación
        translation = [ [1,0,0,translate[0]],
                        [0,1,0,translate[1]],
                        [0,0,1,translate[2]],
                        [0,0,0,1] ]

        # Matrix de rotación
        rotMat = self.glRotationMatrix(rotate[0], rotate[1], rotate[2])

        # Matriz de escala
        scaleMat = [[scale[0],0,0,0],
                    [0,scale[1],0,0],
                    [0,0,scale[2],0],
                    [0,0,0,1]]
        
        # Se multiplican las tres para obtener la matriz del objeto final
        return ml.nMatProduct([translation, rotMat, scaleMat])

    def glRotationMatrix(self, pitch = 0, yaw = 0, roll = 0):
        # Convertir a radianes
        pitch *= pi/180
        yaw *= pi/180
        roll *= pi/180

        # Creamos la matriz de rotación para cada eje.
        pitchMat = [[1,0,0,0],
                    [0,cos(pitch),-sin(pitch),0],
                    [0,sin(pitch),cos(pitch),0],
                    [0,0,0,1]]

        yawMat = [ [cos(yaw),0,sin(yaw),0],
                    [0,1,0,0],
                    [-sin(yaw),0,cos(yaw),0],
                    [0,0,0,1] ]

        rollMat = [ [cos(roll),-sin(roll),0,0],
                    [sin(roll),cos(roll),0,0],
                    [0,0,1,0],
                    [0,0,0,1] ]

        # Se multiplican las tres matrices para obtener la matriz de rotación final
        return ml.nMatProduct([pitchMat, yawMat, rollMat])

    def glLine(self, v0, v1, clr = None):
        # Bresenham line algorith
        # y = m*x + b

        x0 = int(v0[0])
        x1 = int(v1[0])
        y0 = int(v0[1])
        y1 = int(v1[1])

        # Si el punto 0 es igual al punto 1, solo dibujar un punto
        if x0 == x1 and y0 == y1:
            self.glPoint(x0,y0)
            return

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        # Si la linea tiene pendiente mayor a 1 o menor a -1
        # intercambiamos las x por las y, y se dibuja la linea
        # de manera vertical en vez de horizontal
        if steep:
            x0, y0 = y0,x0
            x1, y1 = y1,x1

        # Si el punto inicial en X es mayor que el punto final en X,
        # intercambiamos los puntos para siempre dibujar de 
        # izquierda a derecha
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)


        offset = 0
        limit = 0.5
        m = dy/dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                # Dibujar de manera vertical
                self.glPoint(y, x, clr or self.currColor)
            else:
                # Dibujar de manera horizontal
                self.glPoint(x, y, clr or self.currColor)

            offset += m

            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1

                limit += 1


    def glLoadModel(self, filename, textureName, translate = (0,0,0), rotate = (0,0,0), scale = (1,1,1)):
        # Se crea el modelo y le asignamos su textura
        model = Model(filename, translate, rotate, scale)
        model.LoadTexture(textureName)

        # Se agrega el modelo al listado de objetos
        self.objects.append( model )


    def glRender(self):
        transformedVerts = []
        texCoords = []
        normals = []

        for model in self.objects:

            self.activeTexture = model.texture
            mMatrix = self.glModelMatrix(model.translate, model.rotate ,model.scale)

            for face in model.faces:
                vertCount = len(face)
                v0=model.vertices[face[0][0] -1]
                v1=model.vertices[face[1][0] -1]
                v2=model.vertices[face[2][0] -1]
                if vertCount == 4:
                    v3=model.vertices[face[3][0] -1]

                if self.vertexShader:
                    v0=self.vertexShader(v0, 
                                         modelMatrix=mMatrix,
                                         viewMatrix=self.viewMatrix,
                                         projectionMatrix=self.projectionMatrix,
                                         vpMatrix=self.vpMatrix)
                    
                    v1=self.vertexShader(v1, 
                                         modelMatrix=mMatrix,
                                         viewMatrix=self.viewMatrix,
                                         projectionMatrix=self.projectionMatrix,
                                         vpMatrix=self.vpMatrix)
                    
                    v2=self.vertexShader(v2, 
                                         modelMatrix=mMatrix,
                                         viewMatrix=self.viewMatrix,
                                         projectionMatrix=self.projectionMatrix,
                                         vpMatrix=self.vpMatrix)
                    if vertCount == 4:
                        v3=self.vertexShader(v3, 
                                         modelMatrix=mMatrix,
                                         viewMatrix=self.viewMatrix,
                                         projectionMatrix=self.projectionMatrix,
                                         vpMatrix=self.vpMatrix)
                
                transformedVerts.append(v0)
                transformedVerts.append(v1)
                transformedVerts.append(v2)

                if vertCount == 4:
                    transformedVerts.append(v0)
                    transformedVerts.append(v2)
                    transformedVerts.append(v3)

                vt0=model.texcoords[face[0][1] -1]
                vt1=model.texcoords[face[1][1] -1]
                vt2=model.texcoords[face[2][1] -1]

                if vertCount == 4:
                    vt3=model.texcoords[face[3][1] -1]

                texCoords.append(vt0)
                texCoords.append(vt1)
                texCoords.append(vt2)

                if vertCount == 4:
                    texCoords.append(vt0)
                    texCoords.append(vt2)
                    texCoords.append(vt3)
                
                #normales del modelo
                vn0=model.normals[face[0][2] -1]
                vn1=model.normals[face[1][2] -1]
                vn2=model.normals[face[2][2] -1]

                if vertCount == 4:
                    vn3=model.normals[face[3][2] -1]

                normals.append(vn0)
                normals.append(vn1)
                normals.append(vn2)

                if vertCount == 4:
                    normals.append(vn0)
                    normals.append(vn2)
                    normals.append(vn3)

        primitives = self.glPrimitiveAssembly(transformedVerts, texCoords, normals)

        for prim in primitives:
            if self.primitiveType == TRIANGLES:
                self.glTriangle(prim[0], prim[1], prim[2])
                
    def glBackgroundTexture(self, filename):
        self.background = Texture(filename)

    def clearBackground(self):
        self.glClear()

        if self.background:
            for x in range(self.vpX, self.vpX+self.vpWidth+1):
                for y in range(self.vpY, self.vpY+self.vpHeight+1):
                    u=(x-self.vpX)/self.vpWidth
                    v=(y-self.vpY)/self.vpHeight
                    texColor = self.background.getColor(u, v)
                    if texColor:
                        self.glPoint(x,y,color(texColor[0],texColor[1],texColor[2]))
        


    def glFinish(self, filename):
        # Esta función crea una textura BMP de 24 bits y la rellena 
        # con la tabla de pixeles. Este será nuestro FrameBuffer final.

        with open(filename, "wb") as file:
            # Header
            file.write(char("B"))
            file.write(char("M"))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])

            print("\nBMP creado con éxito!")