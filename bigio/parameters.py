__author__ = 'atrimble'

properties = dict()


def get_property(name, default_value=None):
    if name in properties:
        return properties[name]
    else:
        return default_value


def set_property(name, value):
    properties[name] = value

