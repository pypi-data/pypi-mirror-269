from gravithon.Body import *
from gravithon.errors import *


class Sphere(Body):
    def volume(self):
        return formulas.sphere_volume(self.radius)

    def __init__(self, name: str, mass: float, radius: float, color: str = None):
        super().__init__(name, mass, color)

        NonPositiveValueError.validate_positivity(radius)
        self.radius = float(radius)

    def __str__(self):
        return super().__str__() + \
            '\n' + \
            f'  Radius: {self.radius} m'
