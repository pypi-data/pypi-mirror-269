from . import _frida


def get_frida_hooker(device_serial: str) -> _frida.FridaHooker:
    """
    Get an instance of _frida.FridaHooker.
    :param device_serial: The serial number of the device.
    :return: An instance of _frida.FridaHooker.
    """
    return _frida.FridaHooker(device_serial)

