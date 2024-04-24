from gravithon.astronomy.Planets import *
from gravithon.Space import Space
from gravithon.Screen import Screen
from gravithon.units import time
from numpy import array, ndarray

DIMENSIONS = 2  # TODO: 3?


class SolarSystem(Space):
    def __init__(self):
        super().__init__(DIMENSIONS)

        # Create space
        self.space = Space(dimensions=DIMENSIONS, fps=100)

        # Add sun
        self.space.add_body(Sun, array([130000000000, 0]))
        # Add planets
        self.space.add_body(Mercury, Sun)
        self.space.add_body(Venus, Sun)
        self.space.add_body(Earth, Sun)
        self.space.add_body(Mars, Sun)
        self.space.add_body(Jupiter, Sun)
        self.space.add_body(Saturn, Sun)
        self.space.add_body(Uranus, Sun)
        self.space.add_body(Pluto, Sun)
        # Add moon
        self.space.add_body(Moon, Earth)

    def run(self):
        print(self.space)
        Screen(self.space, speed=1000000).show()


if __name__ == '__main__':
    SolarSystem().run()
