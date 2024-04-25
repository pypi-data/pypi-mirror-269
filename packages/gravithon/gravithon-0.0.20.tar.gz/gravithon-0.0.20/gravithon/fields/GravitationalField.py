from gravithon.fields.Field import Field
from numpy import array, ndarray


class GravitationalField(Field):
    # Field of N/kg
    def __init__(self, value: ndarray):
        self.value = value

    def __str__(self):
        return super().__str__() \
            + 'N/kg' + '\n'
