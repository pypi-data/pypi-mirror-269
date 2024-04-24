from enum import Enum, unique
@unique
class ProtocolType(Enum):
    """
    A enumeration protocol type list

    Attributes
    ----------
    Default = 1
    Mqtt = 2
    Http = 3
    """
    Default = 1
    Mqtt = 2
    Http = 3
    