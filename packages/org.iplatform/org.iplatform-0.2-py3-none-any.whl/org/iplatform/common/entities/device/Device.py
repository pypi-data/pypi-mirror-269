from __future__ import annotations
from org.iplatform.common.entities.entity.Entity import Entity
from org.iplatform.common.entities.device.DeviceType import DeviceType
from org.iplatform.common.entities.protocol.ProtocolType import ProtocolType
from org.iplatform.common.entities.user.User import User
from org.iplatform.common.entities.group.Group import Group
from org.iplatform.common.entities.role.Role import Role
from org.iplatform.common.entities.manufacturer.Manufacturer import Manufacturer
from uuid import UUID
from typing import List
class Device(Entity['Device']):
    def __init__(self, id: UUID = None, name: str = "", description: str = "",
                  model: str = "", seriesNumber: str = "", deviceType: DeviceType = DeviceType.Default,
                  protocolType: ProtocolType = ProtocolType.Default, manufacturer: Manufacturer = None, parent: object = None) -> None:
        super().__init__(id, name, description, parent)
        self.model = model
        self.seriesNumber =seriesNumber
        self.deviceType = deviceType
        self.protocolType = protocolType
        self.manufacturer = manufacturer
        self.parent = parent
    def addEntity(self, entity: Device) -> bool:
        return super().addEntity(entity)
    def removeEntity(self, entity: Device) -> bool:
        return super().removeEntity(entity)
    def modifyEntity(self, entity: Device) -> bool:
        return super().modifyEntity(entity)
    def findEntityByName(self, name: str) -> List[Device]:
        return super().findEntityByName(name)
    def findEntityByID(self, name: str) -> List[Device]:
        return super().findEntityByID(name)
    
    def addDevice(self, device: Device) -> bool:
        result = self.addEntity(device)
        return result
    def removeDevice(self, device: Device) -> bool:
        result = self.removeEntity(device)
        return result
    def modifyDevice(self, device: Device) -> bool:
        result = self.modifyEntity(device)
        return result
    def findDeviceByName(self, name: str) -> List[Device]:
        def find() -> List[Device]:
            return []
        result = find()
        return result
    def findDeviceById(self, id: str) -> List[Device]:
        def find() -> List[Device]:
            return []
        result = find()
        return result
    def findDeviceByType(self, deviceType: DeviceType = DeviceType.Default) -> List[Device]:
        def find() -> List[Device]:
            return []
        result = find()
        return result
    def findDeviceByModel(self, model: str = "") -> List[Device]:
        def find() -> List[Device]:
            return []
        result = find()
        return result
    def addOwnedMembers(self, userList: List[User], groupList: List[Group], roleList: List[Role]) -> bool:
        def add() -> bool:
            return True
        result = add()
        return result
    def removeOwnedMember(self, user: User) -> bool:
        def remove() -> bool:
            return True
        result = remove()
        return result
    def removeOwnedMember(self, group: Group) -> bool:
        def remove() -> bool:
            return True
        result = remove()
        return result
    def modifyOwnedMember(self, user: User, role: Role) -> bool:
        def modify() -> bool:
            return True
        result = modify()
        return result
    def modifyOwnedMember(self, group: Group, role: Role) -> bool:
        def modify() -> bool:
            return True
        result = modify()
        return result