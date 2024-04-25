from gravithon.Body import *
from gravithon.Circle import Circle
from gravithon.errors import *


class Line(Body2D):
    # y=mx+n
    def __init__(self, name: str,
                 slope: float,
                 color: str = None):
        super().__init__(name, None, color)

        self.slope = slope

    def __str__(self):
        return super().__str__() + \
            '\n' + \
            f'  Equation:  y = {self.slope}x + {"n" if self.position is None else self.y_intercept()}'

    def area(self):
        # line has no area
        return None

    def y_intercept(self):
        if self.position is None:
            raise Exception('Line has no position')
        else:
            # n=y-mx
            x = self.position[0]
            y = self.position[1]
            return y - self.slope * x

    def solve(self, x):
        # y=mx+n
        return self.slope * x + self.y_intercept()

    def general_form(self):
        # y=mx+n

        # Ax+By+C:
        # A=m
        # B=-1
        # C=n
        A = self.slope
        B = -1
        C = self.y_intercept()

        return A, B, C

    def is_touching(self, other: Body):
        distance = self.distance(other)  # also checks dimensions

        if isinstance(other, Circle):
            return distance <= other.radius
        elif isinstance(other, Line):
            # if lines are not parallel they have an intersection
            return self.slope != other.slope
        else:
            raise BodyNotSupportedError(other)

    def distance(self, other: Body):
        if not isinstance(other, Body2D):
            raise DimensionsError(self.name, self.dimensions, other.name, other.dimensions)

        if isinstance(other, Circle):
            A, B, C = self.general_form()
            formulas.distance_between_point_and_line(self.position[0], self.position[1], A, B, C)
            return formulas.distance(self.position, other.position)

        elif isinstance(other, Line):
            # there is no distance between lines
            raise BodyNotSupportedError(other)

        else:
            raise BodyNotSupportedError(other)
