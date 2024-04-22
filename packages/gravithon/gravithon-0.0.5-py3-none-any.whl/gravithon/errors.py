class BodyNotFoundError(Exception):
    def __init__(self, name: str):
        message = f'Body "{name}" is not in space'
        super().__init__(message)


class BodyAlreadyExistError(Exception):
    def __init__(self, name: str):
        message = f'A body named "{name}" already exists in this space'
        super().__init__(message)


class FieldNotFoundError(Exception):
    def __init__(self):
        message = f'Field is not in space'
        super().__init__(message)


class DimensionsError(Exception):
    def __init__(self, body1_name: str, body1_dimensions: int, body2_name: str, body2_dimensions: int):
        message = f'{body1_name} has {body1_dimensions} dimensions, but {body2_name} has {body2_dimensions} dimensions'
        super().__init__(message)


class NegativeValueError(Exception):
    def __init__(self, name: str):

        if name is None:
            message = f'Variable must not be negative'
        else:
            message = f'Variable {name} must not be negative'

        super().__init__(message)

    @staticmethod
    def validate_negativity(value: float, name: str = None):
        """
        Throw exception if value is negative
        :param value:value to check
        :param name:name of variable to validate
        :return:None
        """
        if value < 0:
            raise NegativeValueError(name)


class NonPositiveValueError(Exception):
    def __init__(self, name: str = None):
        if name is None:
            message = f'Variable must be positive'
        else:
            message = f'Variable {name} must be positive'

        super().__init__(message)

    @staticmethod
    def validate_positivity(value: float, name: str = None):
        """
        Throw exception if value is negative
        :param value:value to check
        :param name:name of variable to validate
        :return:None
        """
        if not value > 0:
            raise NonPositiveValueError(name)
