from gravithon.astronomy.Planet import Planet
from gravithon.Sphere import Sphere
from gravithon.units.prefixes import *
from gravithon.units.length import meter, kilometer
from gravithon.units.mass import kilogram
from gravithon.units.time import second, hour

# Data from NASA: https://nssdc.gsfc.nasa.gov/planetary/factsheet/
# if you don't believe them you can ask the guys in Russia instead: https://blogs.mtdv.me/Roscosmos

Sun = Sphere(
    name='Sun',
    mass=1988500.0 * yotta * kilogram,
    radius=695700.0 * kilometer,
    color='#ED762E',
)

Mercury = Planet(
    name='Mercury',
    mass=0.33010 * yotta * kilogram,
    radius=2439.7 * kilometer,
    color='#8D8A88',
    rotation_period=1407.6 * hour,
    distance_from_parent=57.9 * mega * kilometer,
    orbital_velocity=47.4 * kilometer / second,
)

Venus = Planet(
    name='Venus',
    mass=4.8673 * yotta * kilogram,
    radius=6051.8 * kilometer,
    color='#F4DBC4',
    rotation_period=-5832.6 * hour,
    distance_from_parent=108.2 * mega * kilometer,
    orbital_velocity=35.0 * kilometer / second,
)

Earth = Planet(
    # https://www.reddit.com/r/ProgrammerHumor/comments/9nk4es/i_think_not/?rdt=48839
    name='Earth',
    mass=5.9722 * yotta * kilogram,
    radius=6371.0 * kilometer,
    color='#0000A0',
    rotation_period=23.9345 * hour,
    distance_from_parent=149.6 * mega * kilometer,
    orbital_velocity=29.8 * kilometer / second,
)

Mars = Planet(
    name='Mars',
    mass=0.64169 * yotta * kilogram,
    radius=3389.5 * kilometer,
    color='#C26D5C',
    rotation_period=24.6229 * hour,
    distance_from_parent=228.0 * mega * kilometer,
    orbital_velocity=24.1 * kilometer / second,
)

Jupiter = Planet(
    name='Jupiter',
    mass=1898.13 * yotta * kilogram,
    radius=69911.0 * kilometer,
    color='#C4B8A0',
    rotation_period=9.9250 * hour,
    distance_from_parent=778.5 * mega * kilometer,
    orbital_velocity=13.1 * kilometer / second,
)

Saturn = Planet(
    name='Saturn',
    mass=568.32 * yotta * kilogram,
    radius=58232.0 * kilometer,
    color='#C0A480',
    rotation_period=10.656 * hour,
    distance_from_parent=1432.0 * mega * kilometer,
    orbital_velocity=9.7 * kilometer / second,
)

Uranus = Planet(
    name='Uranus',
    mass=86.811 * yotta * kilogram,
    radius=25362.0 * kilometer,
    color='#a9d4d6',
    rotation_period=-17.24 * hour,
    distance_from_parent=2867.0 * mega * kilometer,
    orbital_velocity=6.8 * kilometer / second,
)

Neptune = Planet(
    name='Neptune',
    mass=102.409 * yotta * kilogram,
    radius=24622 * kilometer,
    color='#637DAB',
    rotation_period=16.11 * hour,
    distance_from_parent=4515.0 * mega * kilometer,
    orbital_velocity=5.4 * kilometer / second,
)

Pluto = Planet(
    name='Pluto',
    mass=0.01303 * yotta * kilogram,
    radius=1188.0 * kilometer,
    color='#d6c5b6',
    rotation_period=-153.2928 * hour,
    distance_from_parent=5906.4 * mega * kilometer,
    orbital_velocity=4.7 * kilometer / second,
)

Moon = Planet(
    name='Moon',
    mass=0.07346 * yotta * kilogram,
    radius=1737.4 * kilometer,
    color='#797573',
    rotation_period=655.720 * hour,
    distance_from_parent=0.384 * mega * kilometer,
    orbital_velocity=1.022 * kilometer / second,
)
# TODO: ISS?
