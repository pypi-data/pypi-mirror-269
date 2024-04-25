from gravithon.Body import *
from gravithon.Circle import Circle
from gravithon.errors import *
from numpy import pi


class Sphere(Body3D):

    def __init__(self, name: str, mass: float, radius: float, color: str = None):
        super().__init__(name, mass, color)

        NonPositiveValueError.validate_positivity(radius)
        self.radius = float(radius)

        self.__two_dimensional = Circle(self.name, self.mass, self.radius, self.color)

    def __str__(self):
        return super().__str__() + \
            '\n' + \
            f'  Radius: {self.radius} m'

    @property
    def two_dimensional(self):
        return self.__two_dimensional

    def volume(self):
        return (4 / 3) * pi * (self.radius ** 3)

    def is_touching(self, other: Body):
        distance = self.distance(other)  # also checks dimensions

        if isinstance(other, Sphere):
            return distance <= self.radius + other.radius
        else:
            raise BodyNotSupportedError(other)
        """
        # TODO: Plane/Board
        elif isinstance(other, Line):
            self.distance(other)"""

    def distance(self, other: Body):
        if not isinstance(other, Body3D):
            raise DimensionsError(self.name, self.dimensions, other.name, other.dimensions)

        if isinstance(other, Sphere):
            return formulas.distance(self.position, other.position)
        else:
            raise BodyNotSupportedError(other)
        '''
        # TODO: Plane/Board
        elif isinstance(other, Line):
            A, B, C = other.general_form()
            formulas.distance_between_point_and_line(self.position[0], self.position[1], A, B, C)'''
