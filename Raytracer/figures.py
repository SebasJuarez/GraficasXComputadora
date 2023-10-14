'''
Autor: Sebastian Juarez 21471

'''

import mathLibrary as numeritos
from math import tan, pi, atan2, acos

class Shape:
    def __init__(self, position, material):
        self.position = position
        self.material = material

    def intersect(self, origin, direction):
        return None

    def normal(self, point):
        raise NotImplementedError()
    
class Intercept:
    def __init__(self, distance, point, normal, obj, textureCoordinates):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.obj = obj
        self.textureCoordinates = textureCoordinates

class Sphere(Shape):
    def __init__(self, position, radius, material):
        super().__init__(position, material)
        self.radius = radius

    def intersect(self, origin, direction):
        L = numeritos.numeritos.twoVecSubstraction(self.position, origin)
        lengthL = numeritos.numeritos.vecNormSimple(L)
        tca = numeritos.dot_product(L, direction)
        d = (lengthL ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1

        if t0 < 0:
            return None
        
        point = numeritos.twoVecSum(origin, numeritos.valVecMultiply(t0, direction))
        normal = numeritos.numeritos.twoVecSubstraction(point, self.position)
        normal = numeritos.vecNorm(normal)
        
        u = 0.5 + (atan2(normal[2], normal[0]) / (2 * pi))
        v = (acos(normal[1]) / pi)

        return Intercept(distance=t0,
                         point=point,
                         normal=normal,
                         obj=self,
                         textureCoordinates=(u, v))
    
class Plane(Shape):
    def __init__(self, position, normal, material):
        super().__init__(position, material)
        self.normal = numeritos.vecNorm(normal)

    def intersect(self, origin, direction):
        denominator = numeritos.dot_product(direction, self.normal)

        if abs(denominator) <= 0.0001:
            return None

        t = numeritos.dot_product(numeritos.numeritos.twoVecSubstraction(self.position, origin), self.normal) / denominator

        if t < 0:
            return None
        
        point = numeritos.twoVecSum(origin, numeritos.valVecMultiply(t, direction))

        return Intercept(distance=t,
                         point=point,
                         normal=self.normal,
                         obj=self,
                         textureCoordinates=None)
    
class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        super().__init__(position, normal, material)
        self.radius = radius

    def intersect(self, origin, direction):
        intercept = super().intersect(origin, direction)

        if intercept is None:
            return None

        if numeritos.numeritos.vecNormSimple(numeritos.numeritos.twoVecSubstraction(intercept.point, self.position)) > self.radius:
            return None

        return Intercept(
            distance=intercept.distance,
            point=intercept.point,
            normal=self.normal,
            obj=self,
            textureCoordinates=None
        )
    
class AABB(Shape):
    def __init__(self, position, size, material):
        super().__init__(position, material)
        self.size = size
        self.planes = []

        leftPlane = Plane(
            numeritos.twoVecSum(self.position, (-size[0] / 2, 0, 0)),
            (-1, 0, 0),
            self.material
        )
        rightPlane = Plane(
            numeritos.twoVecSum(self.position, (size[0] / 2, 0, 0)),
            (1, 0, 0),
            self.material
        )
        bottomPlane = Plane(
            numeritos.twoVecSum(self.position, (0, -size[1] / 2, 0)),
            (0, -1, 0),
            self.material
        )
        topPlane = Plane(
            numeritos.twoVecSum(self.position, (0, size[1] / 2, 0)),
            (0, 1, 0),
            self.material
        )
        backPlane = Plane(
            numeritos.twoVecSum(self.position, (0, 0, -size[2] / 2)),
            (0, 0, -1),
            self.material
        )
        frontPlane = Plane(
            numeritos.twoVecSum(self.position, (0, 0, size[2] / 2)),
            (0, 0, 1),
            self.material
        )

        self.planes.append(leftPlane)
        self.planes.append(rightPlane)
        self.planes.append(bottomPlane)
        self.planes.append(topPlane)
        self.planes.append(backPlane)
        self.planes.append(frontPlane)

        # BOUNDS
        bias = 0.001
        self.boundsMin = [position[i] - (bias + size[i] / 2) for i in range(3)]
        self.boundsMax = [position[i] + (bias + size[i] / 2) for i in range(3)]

    def intersect(self, origin, direction):
        intersect = None
        t = float('inf')
        u = 0
        v = 0

        for plane in self.planes:
            planeIntersect = plane.intersect(origin, direction)
            if planeIntersect is not None:
                planePoint = planeIntersect.point
                if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0]:
                    if self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1]:
                        if self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:
                            if planeIntersect.distance < t:
                                t = planeIntersect.distance
                                intersect = planeIntersect

                                if abs(plane.normal[0]) > 0:
                                    u = (planePoint[1] - self.boundsMin[1]) / (self.size[1] + 0.002)
                                    v = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + 0.002)
                                if abs(plane.normal[1]) > 0:
                                    u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + 0.002)
                                    v = (planePoint[2] - self.boundsMin[2]) / (self.size[2] + 0.002)
                                if abs(plane.normal[2]) > 0:
                                    u = (planePoint[0] - self.boundsMin[0]) / (self.size[0] + 0.002)
                                    v = (planePoint[1] - self.boundsMin[1]) / (self.size[1] + 0.002)

        if intersect is None:
            return None

        return Intercept(
            distance=t,
            point=intersect.point,
            normal=intersect.normal,
            obj=self,
            textureCoordinates=(u, v)
        )

class Triangle(Shape):
    def __init__(self, vertices, material):
        centroid = numeritos.vecMean(vertices)
        super().__init__(centroid, material)
        self.vertices = vertices

    def intersect(self, origin, direction):
        edge1 = numeritos.twoVecSubstraction(self.vertices[1], self.vertices[0])
        edge2 = numeritos.twoVecSubstraction(self.vertices[2], self.vertices[0])
        normal = numeritos.twoVecCross(edge1, edge2)
        normal = numeritos.vecNorm(normal)

        denominator = numeritos.twoVecDot(normal, direction)

        if abs(denominator) <= 0.0001:
            return None

        t = (numeritos.twoVecDot(normal, self.vertices[0]) - numeritos.twoVecDot(normal, origin)) / denominator

        if t < 0:
            return None

        point = numeritos.twoVecSum(origin, numeritos.valVecMultiply(t, direction))

        edge0 = numeritos.twoVecSubstraction(self.vertices[0], self.vertices[2])
        edge1 = numeritos.twoVecSubstraction(self.vertices[1], self.vertices[0])
        edge2 = numeritos.twoVecSubstraction(self.vertices[2], self.vertices[1])

        normal0 = numeritos.twoVecCross(edge0, numeritos.twoVecSubstraction(point, self.vertices[2]))
        normal1 = numeritos.twoVecCross(edge1, numeritos.twoVecSubstraction(point, self.vertices[0]))
        normal2 = numeritos.twoVecCross(edge2, numeritos.twoVecSubstraction(point, self.vertices[1]))

        if (numeritos.twoVecDot(normal, normal0) >= 0 and
                numeritos.twoVecDot(normal, normal1) >= 0 and
                numeritos.twoVecDot(normal, normal2) >= 0):
            u = numeritos.twoVecDot(edge1, numeritos.twoVecSubstraction(point, self.vertices[0]))
            v = numeritos.twoVecDot(edge0, numeritos.twoVecSubstraction(point, self.vertices[2]))
            w = numeritos.twoVecDot(edge2, numeritos.twoVecSubstraction(point, self.vertices[1]))
            det = u + v + w

            u = u / det
            v = w / det

            u *= 1
            v *= 1

            return Intercept(
                distance=t,
                point=point,
                normal=normal,
                obj=self,
                textureCoordinates=(u, v)
            )

        return None

    def normal(self, point):
        edge1 = numeritos.twoVecSubstraction(self.vertices[1], self.vertices[0])
        edge2 = numeritos.twoVecSubstraction(self.vertices[2], self.vertices[0])
        normal = numeritos.twoVecCross(edge1, edge2)
        normal = numeritos.vecNorm(normal)
        return normal

class Pyramid(Shape):
    def __init__(self, position, size, material):
        super().__init__(position, material)
        self.size = size
        
        width = size[0]
        height = size[1]
        depth = size[2]

        half_width = width / 2
        half_height = height / 2
        half_depth = depth / 2

        vertices = [
            numeritos.twoVecSum(position, (half_width, -half_height, half_depth)),
            numeritos.twoVecSum(position, (-half_width, -half_height, half_depth)),
            numeritos.twoVecSum(position, (-half_width, -half_height, -half_depth)),
            numeritos.twoVecSum(position, (half_width, -half_height, -half_depth)),
            numeritos.twoVecSum(position, (0, half_height, 0))
        ]

        self.triangles = [
            Triangle((vertices[0], vertices[1], vertices[4]), material),
            Triangle((vertices[1], vertices[2], vertices[4]), material),
            Triangle((vertices[2], vertices[3], vertices[4]), material),
            Triangle((vertices[3], vertices[0], vertices[4]), material),
            Triangle((vertices[0], vertices[1], vertices[2]), material)
        ]

    def intersect(self, origin, direction):
        intersect = None
        t = float('inf')

        for triangle in self.triangles:
            triangle_intersect = triangle.intersect(origin, direction)
            if triangle_intersect and triangle_intersect.distance < t:
                t = triangle_intersect.distance
                intersect = triangle_intersect

        if intersect:
            return Intercept(
                distance=intersect.distance,
                point=intersect.point,
                normal=intersect.normal,
                obj=self,
                textureCoordinates=intersect.textureCoordinates
            )
        else:
            return None

    def normal(self, point):
        normal_sum = (0.0, 0.0, 0.0)
        for triangle in self.triangles:
            normal_sum += triangle.normal(point)
        return normal_sum / len(self.triangles)