from __future__ import annotations
from typing import List
from org.iplatform.common.entities.user.User import User
from org.iplatform.common.entities.group.Group import Group
from org.iplatform.common.entities.role.Role import Role
class IPlatform():
    """
    The IPlatform
    """
    userList: List[User] = []
    groupList: List[Group] = []
    roleList: List[Role] = []
    def __init__(self, name: str = "IPlatform", description: str = "", parent: object = None) -> None:
        self.parent = parent
        self.name = name
        self.description = description
    def addUser(self,user: User) -> bool:
        def add() -> bool:
            return True
        result = add()
        return result
    def removeUser(self,user: User) -> bool:
        def remove() -> bool:
            return True
        result = remove()
        return result
    def modifyUser(self,user: User) -> bool:
        def modify() -> bool:
            return True
        result = modify()
        return result
    def addGroup(self,group: Group) -> bool:
        def add() -> bool:
            return True
        result = add()
        return result
    def removeGroup(self,group: Group) -> bool:
        def remove() -> bool:
            return True
        result = remove()
        return result
    def modifyGroup(self,group: Group) -> bool:
        def modify() -> bool:
            return True
        result = modify()
        return result
    def addRole(self,role: Role) -> bool:
        def add() -> bool:
            return True
        result = add()
        return result
    def removeRole(self,role: Role) -> bool:
        def remove() -> bool:
            return True
        result = remove()
        return result
    def modifyRole(self,role: Role) -> bool:
        def modify() -> bool:
            return True
        result = modify()
        return result