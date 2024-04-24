from uuid import UUID
class AreaPermission():
    """
    The Area Permission
    """
    def __init__(self,id: UUID = None, enableAdministration: bool = False, enableUsers: bool = False, enableGroups: bool = False,
                 enableRoles: bool = False, enableEditUser: bool = False, enableEditGroup: bool = False, enableEditRole: bool = False, parent: object = None):
        """
        The constructor construct class

        Parameters:
        -----------
        enableAdministration: bool
            Is True if allow accessing Administration area, otherwise Fail.
        enableUsers: bool
            Is True if allow accessing Users area, otherwise Fail.
        enableGroups: bool
            Is True if allow accessing Groups area, otherwise Fail.
        enableRoles: bool
            Is True if allow accessing Roles area, otherwise Fail.
        enableEditUser: bool
            Is True if allow user editing area, otherwise Fail.
        enableEditGroup: bool
            Is True if allow group editing area, otherwise Fail.
        enableEditRole: bool
            Is True if allow role editing area, otherwise Fail.
        parent: object
            The entity contain itself
        """
        self.id = id
        self.parent = parent
        self.enableAdministration = enableAdministration
        self.enableUsers = enableUsers
        self.enaleGroups = enableGroups
        self.enableRoles = enableRoles
        self.enableEditUser = enableEditUser
        self.enableEditGroup = enableEditGroup
        self.enableEditRole = enableEditRole