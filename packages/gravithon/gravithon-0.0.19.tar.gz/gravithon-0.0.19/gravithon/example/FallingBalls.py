from gravithon.Sphere import Sphere
from gravithon.Line import Line
from gravithon.Space import Space
from gravithon.units.length import *
from gravithon.units.mass import *
from gravithon.astronomy.Planets import Earth
from gravithon.Screen import Screen
from gravithon.fields.GravitationalField import GravitationalField
from numpy import array, ndarray

# TODO: change to SOlar System file structure
DIMENSIONS = 2

# switch to 3d space class
# Create space
space = Space(dimensions=DIMENSIONS, fps=100)

space.add_body(
    Sphere(
        "Ball1",
        10000000000000 * kg,
        50 * cm,
        color='green'
    ),
    array([1 * m, 6 * m]))

space.add_body(
    Sphere(
        "Ball2",
        10000000000000 * kg,
        20 * cm,
        color='red'
    ),
    array([10 * m, 9 * m]))

space.add_body(
    Line(
        "Ground",
        0,
        'brown'
    )
    , array([0, 0])
)

space.add_field(GravitationalField(
    array([0, -Earth.surface_gravity(), 0])
))

print(space)
Screen(space, time=3).show()
