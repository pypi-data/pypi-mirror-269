from gravithon.Body import *
from gravithon.errors import *
from numpy import pi


class Circle(Body2D):
    def __init__(self, name: str, mass: float, radius: float, color: str = None):
        super().__init__(name, mass, color)

        NonPositiveValueError.validate_positivity(radius)
        self.radius = float(radius)

    def __str__(self):
        return super().__str__() + \
            '\n' + \
            f'  Radius: {self.radius} m'

    def area(self):
        return pi * (self.radius ** 2)

    def is_touching(self, other: Body):
        from gravithon.Line import Line

        distance = self.distance(other)  # also checks dimensions

        if isinstance(other, Circle):
            return distance <= self.radius + other.radius
        elif isinstance(other, Line):
            self.distance(other)
        else:
            raise BodyNotSupportedError(other)

    def distance(self, other: Body):
        from gravithon.Line import Line

        if not isinstance(other, Body2D):
            raise DimensionsError(self.name, self.dimensions, other.name, other.dimensions)

        if isinstance(other, Circle):
            return formulas.distance(self.position, other.position)

        elif isinstance(other, Line):
            A, B, C = other.general_form()
            return formulas.distance_between_point_and_line(self.position[0], self.position[1], A, B, C)

        else:
            raise BodyNotSupportedError(other)
