from uuid import UUID
class RolePermission():
    """
    The Role Permission
    """
    def __init__(self,id: UUID = None, isAddedRole: bool = False, isEditedRole: bool = False, isDeletedRole: bool = False, parent: object = None):
        """
        The constructor construct class

        Parameters:
        -----------
        isAddedRole: bool
            Is True if allow adding Role, otherwise Fail.
        isEditedRole: bool
            Is True if allow editing Role, otherwise Fail.
        isDeletedRole: bool
            Is True if allow deleting Role, otherwise Fail.
        parent: object
            The entity contain itself
        """
        self.id = id
        self.parent = parent
        self.isAddedRole = isAddedRole
        self.isEditedRole = isEditedRole
        self.isDeletedRole = isDeletedRole