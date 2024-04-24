from uuid import UUID
class Coordinate():
    """
    The coordinate of entity containt latitude, longtitude, altitude.
    """
    def __init__(self, id: UUID, name: str ="", description: str = "", latitude: float = 0.0, longtitude: float = 0.0, altitude: float = 0.0, parent: object = None) -> None:
        self.id = id
        self.parent = parent
        self.name = name
        self.description = description
        self.latitude = latitude
        self.longtitude = longtitude
        self.altitude = altitude