from gravithon import formulas


class Satellite:
    # Class for both artificial and natural satellites
    # TODO: make interface
    def __init__(self, rotation_period: float, orbital_radius: float, orbital_velocity: float):
        self.rotation_period = rotation_period
        self.orbital_radius = orbital_radius
        self.orbital_velocity = orbital_velocity

    def __str__(self):
        return '\n' + \
            f'  Rotation Period: {self.rotation_period} sec' + '\n' + \
            f'  Orbital Distance: {self.orbital_radius} m' + '\n' + \
            f'  Orbital Velocity: {self.orbital_velocity} m/sec' + '\n' + \
            f'  Orbital Period: {self.orbital_period()} sec'

    def orbital_period(self):
        return formulas.orbital_period(self.orbital_radius, self.orbital_velocity)
