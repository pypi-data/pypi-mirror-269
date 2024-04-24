from uuid import UUID
from org.iplatform.common.entities.permission.DevicePermission import DevicePermission
from org.iplatform.common.entities.permission.AreaPermission import AreaPermission
from org.iplatform.common.entities.permission.UserPermission import UserPermission
from org.iplatform.common.entities.permission.GroupPermission import GroupPermission
from org.iplatform.common.entities.permission.RolePermission import RolePermission
class Permission():
    """
    The Permission
    """
    def __init__(self, id: UUID = None, name: str = "", description: str = "", parent: object = None,
                  devicePermission: DevicePermission = DevicePermission(),
                  areaPermission: AreaPermission = AreaPermission(),
                  userPermission: UserPermission = UserPermission(),
                  groupPermission: GroupPermission = GroupPermission(),
                  rolePermission: RolePermission = RolePermission(),
                  ):
        """
        The constructor construct class

        Parameters:
        -----------
        id: UUID
            The identify of permission.
        name: str
            The name of permission.
        description: str
            The description about permission.
        devicePermission: DevicePermission
            The device permission.
        areaPermission: AreaPermission
            The area accessing permission.
        userPermission: UserPermission
            The User permission.
        groupPermission: GroupPermission
            The group permission.
        rolePermission: RolePermission
            The role permission.
        parent: object
            The entity contain itself
        """
        self.id = id
        self.parent = parent
        self.name = name
        self.description = description
        self.devicePermission = devicePermission
        self.areaPermission = areaPermission
        self.userPermission = userPermission
        self.groupPermission = groupPermission
        self.rolePermission = rolePermission
