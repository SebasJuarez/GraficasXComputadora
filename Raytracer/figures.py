'''
Autor: Sebastian Juarez 21471

'''

import mathLibrary as numeritos
from math import sqrt, tan, pi, atan2, acos, cos, sin
import math

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
        L = numeritos.twoVecSubstraction(self.position, origin)
        lengthL = numeritos.vecNormSimple(L)
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
        normal = numeritos.twoVecSubstraction(point, self.position)
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
        centroid = numeritos.calculateMean(vertices)
        super().__init__(centroid, material)
        self.vertices = vertices

    def intersect(self, origin, direction):
        edge1 = numeritos.twoVecSubstraction(self.vertices[1], self.vertices[0])
        edge2 = numeritos.twoVecSubstraction(self.vertices[2], self.vertices[0])
        normal = numeritos.twoVecCross(edge1, edge2)
        normal = numeritos.vecNorm(normal)

        denominator = numeritos.dot_product(normal, direction)

        if abs(denominator) <= 0.0001:
            return None

        t = (numeritos.dot_product(normal, self.vertices[0]) - numeritos.dot_product(normal, origin)) / denominator

        if t < 0:
            return None

        point = numeritos.twoVecSum(origin, numeritos.valVecMultiply(t, direction))

        edge0 = numeritos.twoVecSubstraction(self.vertices[0], self.vertices[2])
        edge1 = numeritos.twoVecSubstraction(self.vertices[1], self.vertices[0])
        edge2 = numeritos.twoVecSubstraction(self.vertices[2], self.vertices[1])

        normal0 = numeritos.twoVecCross(edge0, numeritos.twoVecSubstraction(point, self.vertices[2]))
        normal1 = numeritos.twoVecCross(edge1, numeritos.twoVecSubstraction(point, self.vertices[0]))
        normal2 = numeritos.twoVecCross(edge2, numeritos.twoVecSubstraction(point, self.vertices[1]))

        if (numeritos.dot_product(normal, normal0) >= 0 and
                numeritos.dot_product(normal, normal1) >= 0 and
                numeritos.dot_product(normal, normal2) >= 0):
            u = numeritos.dot_product(edge1, numeritos.twoVecSubstraction(point, self.vertices[0]))
            v = numeritos.dot_product(edge0, numeritos.twoVecSubstraction(point, self.vertices[2]))
            w = numeritos.dot_product(edge2, numeritos.twoVecSubstraction(point, self.vertices[1]))
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
    
class Cylinder(Shape):
    def __init__(self, position, radius, height, material, rotation_z=0.0):
        super().__init__(position, material)
        self.radius = radius
        self.height = height
        self.rotation_z = rotation_z  # Angle in radians

    def intersect(self, origin, direction):
        cos_theta = cos(-self.rotation_z)
        sin_theta = sin(-self.rotation_z)
        
        rotated_origin = numeritos.vecAdd(
            numeritos.valVecMultiply2(origin, cos_theta),
            numeritos.valVecMultiply2(numeritos.twoVecCross((0, 0, 1), origin), sin_theta)
        )
        rotated_direction = numeritos.vecAdd(
            numeritos.valVecMultiply2(direction, cos_theta),
            numeritos.valVecMultiply2(numeritos.twoVecCross((0, 0, 1), direction), sin_theta)
        )

        L = numeritos.twoVecSubstraction(rotated_origin, self.position)
        a = rotated_direction[0] * rotated_direction[0] + rotated_direction[2] * rotated_direction[2]
        b = 2 * (L[0] * rotated_direction[0] + L[2] * rotated_direction[2])
        c = L[0] * L[0] + L[2] * L[2] - self.radius * self.radius

        discriminant = b * b - 4 * a * c

        if discriminant < 0:
            return None

        t1 = (-b - sqrt(discriminant)) / (2 * a)
        t2 = (-b + sqrt(discriminant)) / (2 * a)

        if t1 > t2:
            t1, t2 = t2, t1

        y1 = L[1] + t1 * rotated_direction[1]
        y2 = L[1] + t2 * rotated_direction[1]

        if (y1 < 0 and y2 < 0) or (y1 > self.height and y2 > self.height):
            return None

        t = t1 if 0 <= y1 <= self.height else t2
        point = numeritos.vecAdd(rotated_origin, numeritos.valVecMultiply2(rotated_direction, t))

        if 0 <= y1 <= self.height:
            normal = numeritos.vecNorm(numeritos.twoVecSubstraction(point, numeritos.vecAdd(self.position, (0, 0, 0))))
        else:
            normal = numeritos.vecNorm(numeritos.twoVecSubstraction(point, numeritos.vecAdd(self.position, (0, self.height, 0))))

        rotated_normal = numeritos.vecAdd(
            numeritos.valVecMultiply2(normal, cos_theta),
            numeritos.valVecMultiply2(numeritos.twoVecCross((0, 0, 1), normal), -sin_theta)
        )

        return Intercept(distance=t, point=point, normal=rotated_normal, obj=self, textureCoordinates=None)

    def normal(self, point):
        if point[1] <= 0:
            return numeritos.vecNorm(numeritos.twoVecSubstraction(point, numeritos.vecAdd(self.position, (0, 0, 0))))
        elif point[1] >= self.height:
            return numeritos.vecNorm(numeritos.twoVecSubstraction(point, numeritos.vecAdd(self.position, (0, self.height, 0))))
        else:
            return numeritos.vecNorm(numeritos.twoVecSubstraction(point, numeritos.vecAdd(self.position, (0, point[1], 0))))