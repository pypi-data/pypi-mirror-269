from gravithon.Body import *
from gravithon.fields.Field import Field
from gravithon.errors import *
from gravithon.astronomy.Satellite import Satellite
from multipledispatch import dispatch
from numpy import array, ndarray, copy


class Space:
    def __init__(self, dimensions: int = 3, background_color: str = 'black', fps: float = 100):
        self.bodies = []
        self.fields = []
        self.dimensions = dimensions
        self.background_color = background_color
        self.time = 0.0
        self.step_duration = 1 / fps

    def __str__(self):
        string = ''

        # bodies count
        if len(self.bodies) == 0:
            string += f'No bodies\n'
        elif len(self.bodies) == 1:
            string += f'1 body:\n'
        else:
            string += f'{len(self.bodies)} bodies:\n'

        # bodies
        for body in self.bodies:
            # indent body's string
            for line in str(body).split('\n'):
                string += '  ' + line + '\n'

            string += '\n'

        # fields count
        if len(self.fields) == 0:
            string += f'No fields\n'
        elif len(self.fields) == 1:
            string += f'1 field:\n'
        else:
            string += f'{len(self.fields)} fields:\n'

        # fields
        for field in self.fields:
            # indent body's string
            for line in str(field).split('\n'):
                string += '  ' + line + '\n'

            string += '\n'

        # time
        string += f'Time: {self.time}'

        return string

    @dispatch(Body, ndarray, ndarray)
    def add_body(self, body: Body, position: ndarray, velocity: ndarray):
        # set velocity and position
        body.position = position.copy().astype(float)
        body.velocity = velocity.copy().astype(float)
        # connect 2d form's speed and velocity
        if isinstance(body, Body3D):
            body.two_dimensional.position = body.position
            body.two_dimensional.velocity = body.velocity

            if self.dimensions == 2:
                # body should be converted to space's dimensions
                body = body.two_dimensional

        # check dimensions
        if body.dimensions != self.dimensions:
            raise DimensionsError('Space', self.dimensions, body.name, body.dimensions)

        if len(position) != self.dimensions:
            # dimensions doesn't match
            raise DimensionsError('Space', self.dimensions, body.name + '\'s position', len(position))

        if velocity is not None and len(velocity) != self.dimensions:
            raise DimensionsError('Space', self.dimensions, body.name + '\'s velocity', len(velocity))

        # check if body has been already added
        for existing_body in self.bodies:
            if body.name == existing_body.name:
                raise BodyAlreadyExistError(body.name)

        self.bodies.append(body)

    @dispatch(Body, ndarray)
    def add_body(self, body: Body, position: ndarray):
        velocity = array([0] * self.dimensions)  # zero velocity
        self.add_body(body, position, velocity)

    @dispatch(Satellite, Body)
    def add_body(self, satellite: Satellite, parent: Body):
        """
        Add satellite in orbit around a parent
        """
        # if satellite is transformed to its 2d form, this method will save it's previous form
        save_satellite = satellite

        # check if parent is in space
        try:
            next(body for body in self.bodies if body.name == parent.name)
        except StopIteration:
            raise BodyNotFoundError(parent.name)

        # set position and velocity relative to parent
        position = parent.position.copy()
        position[0] += save_satellite.orbital_radius  # e.g. (in 3d spaces): [px+r py pz]
        velocity = parent.velocity.copy()
        velocity[1] += save_satellite.orbital_velocity  # e.g. (in 3d spaces): [v 0 0]

        if isinstance(satellite, Body):
            self.add_body(satellite, position, velocity)
        else:
            raise Exception('Satellite must be a body in order to be added to a space')

    def remove_body(self, body_name):
        # find body in bodies list
        try:
            body: Body = next(body for body in self.bodies if body.name == body_name)
        except StopIteration:
            raise BodyNotFoundError(body_name)

        # remove
        self.bodies.remove(body)

    def step(self, speed: float = 1.0):
        from gravithon.astronomy.Planets import Earth, Moon, Sun
        # increase speed
        self.time += self.step_duration * speed

        # move bodies
        for body in self.bodies:
            velocity = body.velocity.copy()
            velocity *= self.step_duration
            velocity *= speed
            body.move(velocity)

        # accelerate bodies
        for body in self.bodies:
            if body.mass is None:
                continue

            acceleration = body.calculate_acceleration(self.dimensions, self.bodies, self.fields)
            acceleration *= self.step_duration
            acceleration *= speed
            body.accelerate(acceleration)

        # collisions
        for body in self.bodies:
            for other in self.bodies:
                if body is other:
                    continue
                # check collision between bodies
                if body.is_touching(other):
                    print('collision!')  # TODO: collision

    def add_field(self, field: Field):
        # check dimensions
        if field.dimensions() < self.dimensions:
            # dimensions doesn't match
            raise DimensionsError('Space', self.dimensions, 'field', field.dimensions())

        if field.dimensions() > self.dimensions:
            # shorten field's dimensions to space's dimensions
            field.value = field.value[:self.dimensions]

        self.fields.append(field)

    def remove_field(self, field: Field):
        try:
            self.fields.remove(field)
        except ValueError:
            raise FieldNotFoundError()

    # TODO: space history


# 2d space
class Plane(Space):
    def __init__(self):
        super().__init__(dimensions=2)
