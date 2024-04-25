from __future__ import annotations

from gravithon import formulas
from gravithon.fields.GravitationalField import GravitationalField
from gravithon.errors import *
from abc import ABC, abstractmethod

from numpy import array, ndarray


class Body(ABC):
    name: str
    dimensions: int
    mass: float
    position: ndarray
    velocity: ndarray
    color: str

    def __init__(self, name: str, dimensions: int, mass: float, color: str = None):
        self.name = name
        self.dimensions = dimensions

        if mass is None:
            self.mass = None
        else:
            NonPositiveValueError.validate_positivity(mass)
            self.mass = float(mass)

        self.position = None  # Body gets position when it's added to space
        self.velocity = None
        self.color = color

    def __str__(self):
        return \
                self.name + ':\n' + \
                f'  Dimensions: {self.dimensions}' + '\n' + \
                ('' if self.mass is None else f'  Mass: {self.mass} kg' + '\n') + \
                f'  Position: {self.position} m' + '\n' + \
                f'  Velocity: {self.velocity} m/s'

    def move(self, velocity: ndarray):
        # check dimensions
        if len(self.position) != len(velocity):
            raise DimensionsError(self.name + '\'s position', len(self.position), 'velocity', len(velocity))

        self.position += velocity

    def accelerate(self, acceleration: ndarray):
        # check dimensions
        if len(self.velocity) != len(acceleration):
            raise DimensionsError(self.name + '\'s velocity', len(self.velocity), 'acceleration', len(acceleration))

        self.velocity += acceleration

    @abstractmethod
    def distance(self, other: Body):
        pass

    def gravitational_field(self, distance: float):
        return formulas.gravitational_field(self.mass, distance)

    def gravitational_force(self, other: Body):
        # set force direction
        force = []
        for i in range(self.dimensions):
            axis_distance = formulas.distance(self.position[i], other.position[i])
            force.append(axis_distance)
        force = array(force)

        # set force magnitude
        current_magnitude = formulas.magnitude(force)
        real_magnitude = self.gravitational_field(self.distance(other)) * other.mass

        force *= -(real_magnitude / current_magnitude)

        return force

    @abstractmethod
    def is_touching(self, other: Body):
        pass

    def calculate_total_force(self, space_dimensions: int, bodies: list, fields: list):
        force = array([0.0] * space_dimensions)

        for body in bodies:
            if body is not self \
                    and body.mass is not None:
                force += self.gravitational_force(body)

        for field in fields:
            if isinstance(field, GravitationalField):
                force += field.value * self.mass
            else:
                raise FieldNotSupportedError(field)

        return force

    def calculate_acceleration(self, space_dimensions: int, bodies: list, fields: list):
        F = self.calculate_total_force(space_dimensions, bodies, fields)
        return formulas.acceleration(F, self.mass)


class Body2D(Body, ABC):
    def __init__(self, name: str, mass: float, color: str = None):
        super().__init__(name, 2, mass, color)

    def __str__(self):
        return super().__str__() + \
            ('' if self.area() is None else '\n' + f'  Area: {self.area()} m^2')

    @abstractmethod
    def area(self):
        pass


class Body3D(Body, ABC):
    def __init__(self, name: str, mass: float, color: str = None):
        super().__init__(name, 3, mass, color)

    def __str__(self):
        return super().__str__() + \
            ('' if self.volume() is None else '\n' + f'  Volume: {self.volume()} m^3')

    @property
    @abstractmethod
    def two_dimensional(self):
        pass

    @abstractmethod
    def volume(self):
        pass

    def density(self):
        return formulas.density(self.mass, self.volume())
