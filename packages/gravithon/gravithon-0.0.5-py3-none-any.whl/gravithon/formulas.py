import numpy.linalg

from gravithon.constants.astrophisics import *
from math import sqrt, pi
from numpy import array, ndarray
from multipledispatch import dispatch


# TODO: order formulas
def sphere_volume(r):
    """
    Calculate sphere's volume
    :param r: radius
    :return: volume
    """
    return (4 / 3) * pi * (r ** 3)


def gravity(m1: float, m2: float, r: float):
    return (G * m1 * m2) / (r ** 2)


def acceleration(F: ndarray, m: float):
    """
    calculate body's acceleration
    :param F: total force
    :param m: mass
    :return: acceleration
    """
    return F / m


def magnitude(v: ndarray):
    """
    calculate vector's magnitude
    :param v: vector
    :return: magnitude
    """
    return numpy.linalg.norm(v)


@dispatch(ndarray, ndarray)
def distance(p1, p2):
    return magnitude(p1 - p2)


@dispatch(float, float)
def distance(p1, p2):
    return p1 - p2


def orbital_period(r: float, v: float):
    """
    Calculate the amount of time a satellite takes to complete one orbit around it's parent
    :param r: radius - distance from parent
    :param v: orbital speed
    :return: period time [seconds]
    """
    return (2 * pi * r) / (v)


def gravitational_field(M: float, r: float):
    """
    Calculate the gravitational field's magnitude of an object in specific distance
    :param M: mass
    :param r: radius - distance from mass center
    :return: gravitational field's magnitude
    """
    return (G * M) / (r ** 2)


def density(m: float, V: float):
    """
    Calculate body's density
    :param m: mass
    :param V: volume
    :return: density
    """
    return m / V
