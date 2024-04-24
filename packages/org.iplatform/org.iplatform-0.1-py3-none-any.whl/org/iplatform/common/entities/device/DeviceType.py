from enum import Enum, unique
@unique
class DeviceType(Enum):
    """
    A enumeration device type list

    Attributes
    ----------
    Default = 1
    Sensor = 2
    NetworkDevice = 3
    """
    Default = 1
    Sensor = 2
    NetworkDevice = 3
    