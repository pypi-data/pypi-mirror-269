from __future__ import annotations

from gravithon import formulas
from gravithon.fields.Field import Field
from gravithon.fields.GravitationalField import GravitationalField
from gravithon.errors import *
from abc import ABC, abstractmethod

from numpy import array, ndarray


class Body(ABC):
    name: str
    mass: float
    position: ndarray
    velocity: ndarray
    color: str

    def __init__(self, name: str, mass: float, color: str = None):
        self.name = name
        NonPositiveValueError.validate_positivity(mass)
        self.mass = float(mass)
        self.position = None  # Body gets position when it's added to space
        self.velocity = None
        self.color = color

    def __str__(self):
        # TODO: better __str__ in all bodies?
        return \
                self.name + ':\n' + \
                f'  Mass: {self.mass} kg' + '\n' + \
                f'  Position: {self.position} m' + '\n' + \
                f'  Velocity: {self.velocity} m/s' + '\n' + \
                f'  Volume: {self.volume()} m^3' + '\n' + \
                f'  Density: {self.density()} kg/m^3'

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
    def volume(self):
        pass

    def density(self):
        return formulas.density(self.mass, self.volume())

    def distance(self, other: Body):
        return formulas.distance(self.position, other.position)

    def gravitational_field(self, distance: float):
        return formulas.gravitational_field(self.mass, distance)

    def gravitational_force(self, other: Body):
        # set force direction
        force = []
        for i in range(self.dimensions()):
            axis_distance = formulas.distance(self.position[i], other.position[i])
            force.append(axis_distance)
        force = array(force)

        # set force magnitude
        current_magnitude = formulas.magnitude(force)
        real_magnitude = self.gravitational_field(self.distance(other)) * other.mass

        force *= -(real_magnitude / current_magnitude)

        return force

    def __total_gravitational_force(self, space_dimensions: int, bodies: list, fields: list):
        force = array([0.0] * space_dimensions)

        for body in bodies:
            if body is not self:
                force += self.gravitational_force(body)

        for field in fields:
            if isinstance(field, GravitationalField):
                force += field.value * self.mass

        return force

    def calculate_total_force(self, space_dimensions: int, bodies: list, fields: list):
        return \
            self.__total_gravitational_force(space_dimensions, bodies, fields)

    def calculate_acceleration(self, space_dimensions: int, bodies: list, fields: list):
        F = self.calculate_total_force(space_dimensions, bodies, fields)
        return formulas.acceleration(F, self.mass)

    def dimensions(self):
        return len(self.position)
