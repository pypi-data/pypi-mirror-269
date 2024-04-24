from uuid import UUID
class DevicePermission():
    """
    The Device Permission
    """
    def __init__(self,id: UUID = None, isCreatedDevice: bool = False,isEditedDevice: bool = False, isDeletedDevice: bool = False, isViewDevice: bool = True,
                  isSetDevice: bool = False, parent: object = None):
        """
        The constructor construct class

        Parameters:
        -----------
        isCreatedDevice: bool
            Is True if allow creating device, otherwise Fail.
        isEditedDevice: bool
            Is True if allow editing device, otherwise Fail.
        isDeletedDevice: bool
            Is True if allow deleting device, otherwise Fail.
        isViewDevice: bool
            Is True if allow viewing device, otherwise Fail.
        isSetDevice: bool
            Is True if allow device setting, otherwise Fail.
        parent: object
            The enti contain itself
        """
        self.id = id
        self.parent = parent
        self.isCreatedDevice = isCreatedDevice
        self.isEditedDevice = isEditedDevice
        self.isDeletedDevice = isDeletedDevice
        self.isViewDevice = isViewDevice
        self.isSetDevice = isSetDevice