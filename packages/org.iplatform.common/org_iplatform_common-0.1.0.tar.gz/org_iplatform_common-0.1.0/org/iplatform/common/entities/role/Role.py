from __future__ import annotations
from org.iplatform.common.entities.permission.DevicePermission import DevicePermission
from org.iplatform.common.entities.permission.AreaPermission import AreaPermission
from org.iplatform.common.entities.permission.UserPermission import UserPermission
from org.iplatform.common.entities.permission.GroupPermission import GroupPermission
from org.iplatform.common.entities.permission.RolePermission import RolePermission
from org.iplatform.common.entities.permission.Permission import Permission
from uuid import UUID
class Role():
    """
    A class represent role of User/ Group
    """
    def __init__(self, id: UUID = None, name:str = "", description:str = "", parent: object = None,permission: Permission = Permission()) -> None:
        """
        A constructor construct role

        Parameters
        ----------
        id: UUID
            The indentifier of role.
        parent: object
            The parent of itself
        name: str
            The name of role.
        description: str
            The description about role.
        permission: Permission
            The allowing permission.
        """
        self.id = id
        self.parent = parent
        self.name = name
        self.description = description
        self.permission = permission
    def addRole(self, role: 'Role') -> bool:
        def add() -> bool:
            return True
        result = add()
        return result
    def removeRole(self, role: 'Role') -> bool:
        def remove() -> bool:
            return True
        result = remove()
        return result
    def modifyRole(self, role: 'Role') -> bool:
        def modify() -> bool:
            return True
        result = modify()
        return result
    def modifyDevicePermission(self, devicePermission: 'DevicePermission') -> bool:
        def modify() -> bool:
            return True
        result = modify()
        return result
    def modifyAreaPermission(self, areaPermission: 'AreaPermission') -> bool:
        def modify() -> bool:
            return True
        result = modify()
        return result
    def modifyUserPermission(self, userPermission: 'UserPermission') -> bool:
        def modify() -> bool:
            return True
        result = modify()
        return result
    def modifyGroupPermission(self, groupPermission: 'GroupPermission') -> bool:
        def modify() -> bool:
            return True
        result = modify()
        return result
    def modifyRolePermission(self, rolePermission: 'RolePermission') -> bool:
        def modify() -> bool:
            return True
        result = modify()
        return result
    