from uuid import UUID
from typing import List, TypeVar
from org.iplatform.common.entities.device.Device import Device
from org.iplatform.common.entities.group.Group import Group
T = TypeVar('T', Device)
class Entities():
    deviceList: List[Device] = []
    groupList: List[Group] = []
    def __init__(self, id: UUID = None, name: str = "", description: str = "", parent: object = None) -> None:
        self.id = id
        self.parent = parent
        self.name = name
        self.description = description
    def addDevice(self, device: Device) -> bool:
        def add() -> bool:
            return True
        result = add()
        return result
    def removeDevice(self, device: Device) -> bool:
        def remove() -> bool:
            return True
        result = remove()
        return result
    def modifyDevice(self, device: Device) -> bool:
        def modify() -> bool:
            return True
        result = modify()
        return result
    def addGroup(self, group: Group) -> bool:
        def add() -> bool:
            return True
        result = add()
        return result
    def removeGroup(self, group: Group) -> bool:
        def remove() -> bool:
            return True
        result = remove()
        return result
    def modifyGroup(self, group: Group) -> bool:
        def modify() -> bool:
            return True
        result = modify()
        return result
    def findDeviceByName(self, name: str) -> List[Device]:
        def find() -> List[Device]:
            return []
        result = find()
        return result
    def findDeviceById(self, id: UUID) -> List[Device]:
        def find() -> List[Device]:
            return []
        result = find()
        return result
    def findGroupByName(self, name: str) -> List[Group]:
        def find() -> List[Group]:
            return []
        result = find()
        return result
    def findGroupById(self, id: UUID) -> List[Group]:
        def find() -> List[Group]:
            return []
        result = find()
        return result