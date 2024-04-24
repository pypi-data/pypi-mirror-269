from uuid import UUID
class Manufacturer():
    """
    The manufacturer of anything
    """
    def __init__(self, id: UUID = None, name: str = "", organization: str = "", description: str = "", parent: object = None) -> None:
        self.id = id
        self.parent = parent
        self.name = name
        self.organization = organization
        self.description = description