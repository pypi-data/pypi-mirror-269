

from tendril.common.iotcore.exceptions import DeviceConfigValidationError


class DeviceContentValidationError(DeviceConfigValidationError):
    def __init__(self, id, name=None):
        self.id = id
        self.name = ''

    def __str__(self):
        return f"Error Validating Device Content {self.id} {self.name}: "


class CarouselContentValidationError(DeviceConfigValidationError):
    def __init__(self, id, name=None):
        self.id = id
        self.name = ''

    def __str__(self):
        return f"Error Validating Carousel Content {self.id} {self.name}: "


class DeviceContentNotRecognized(DeviceContentValidationError):
    status_code = 404

    def __str__(self):
        rv = super().__str__()
        rv += "Device Content Interest not found."
        return rv


class CarouselContentNotRecognized(CarouselContentValidationError):
    status_code = 404

    def __str__(self):
        rv = super().__str__()
        rv += "Carousel Content Interest not found."
        return rv


class DeviceContentNotReady(DeviceContentValidationError):
    status_code = 406

    def __init__(self, id, name, status):
        super().__init__(id, name)
        self.status = status

    def __str__(self):
        rv = super().__str__()
        rv += f"State is {self.status}, not ACTIVE."
        return rv


class CarouselContentNotReady(CarouselContentValidationError):
    status_code = 406

    def __init__(self, id, name, status):
        super().__init__(id, name)
        self.status = status

    def __str__(self):
        rv = super().__str__()
        rv += f"State is {self.status}, not ACTIVE."
        return rv


class DeviceContentUserUnauthorized(DeviceContentValidationError):
    status_code = 403

    def __init__(self, id, name, user):
        super().__init__(id, name)
        self.user = user

    def __str__(self):
        rv = super().__str__()
        rv += f"User {self.user} does not have access to this device content."
        return rv


class CarouselContentUserUnauthorized(CarouselContentValidationError):
    status_code = 403

    def __init__(self, id, name, user):
        super().__init__(id, name)
        self.user = user

    def __str__(self):
        rv = super().__str__()
        rv += f"User {self.user} does not have access to this carousel content."
        return rv
