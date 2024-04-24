from __future__ import annotations
from typing import List
from uuid import UUID
from org.iplatform.common.entities.role.Role import Role
class Group():
    """
    A class represent group
    """
    roleList: List[Role] = []
    """
        The role list of group
    """

    def __init__(self, id: UUID, name:str, description:str = "", parent: object = None) -> None:
        """
        A constructor construct group

        Parameters
        ----------
        id: UUID
            The indentifier of group.
        parent: object
            The parent of itself
        name: str
            The name of group.
        description: str
            The description about group.
        """
        self.id = id
        self.parent = parent
        self.name = name
        self.description = description
    """
    The method add new group

    Parameters:
    -----------
    group: Group
        The group to add.
    
    Return:
    -------
        Return True if add new group successful, otherwise False.
    """
    def addGroup(self, group: 'Group') -> bool:
        def add() -> bool:
            return True
        result = add()
        return result
    """
    The method remove group

    Parameter:
    ----------
    group: Group
        The group want to remove

    Return:
    -------
        Return True if remove successfully, otherwise False
    """
    def removeGroup(self, group: 'Group') -> bool:
        def remove() -> bool:
            return True
        result = remove()
        return result
    """
    The method modify group

    Parameter:
    ----------
    group: Group
        The group want to modify

    Return:
    -------
        Return True if modify successfully, otherwise False
    """
    def modifyGroup(self, group: 'Group') -> bool:
        def modify() -> bool:
            return True
        result = modify()
        return result
    """
    The method find group by name

    Parameter:
    ----------
    name: str
        The group name want to find

    Return:
    -------
        Return group list if group finded, otherwise empty list
    """
    def findGroupByName(self, name: str = "") -> list['Group']:
        def find() -> list['Group']:
            return []
        result = find()
        return result
    """
    The method find group by id

    Parameter:
    ----------
    id: str
        The group id want to find

    Return:
    -------
        Return group list if group finded, otherwise empty list
    """
    def findGroupById(self, id: str = "") -> list['Group']:
        def find() -> list['Group']:
            return []
        result = find()
        return result

