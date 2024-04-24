from uuid import UUID
class UserPermission():
    """
    The User Permission
    """
    def __init__(self,id: UUID = None, isAddedUser: bool = False, isEditedUser: bool = False, isDeletedUser: bool = False, parent: object = None):
        """
        The constructor construct class

        Parameters:
        -----------
        isAddedUser: bool
            Is True if allow adding User, otherwise Fail.
        isEditedUser: bool
            Is True if allow editing User, otherwise Fail.
        isDeletedUser: bool
            Is True if allow deleting User, otherwise Fail.
        parent: object
            The entity contain itself
        """
        self.id = id
        self.parent = parent
        self.isAddedUser = isAddedUser
        self.isEditedUser = isEditedUser
        self.isDeletedUser = isDeletedUser