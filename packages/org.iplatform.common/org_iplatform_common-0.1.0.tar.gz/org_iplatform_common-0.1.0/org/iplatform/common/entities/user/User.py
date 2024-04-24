from __future__ import annotations
from typing import List
from org.iplatform.common.entities.language.Language import Language
from org.iplatform.common.entities.group.Group import Group
from org.iplatform.common.entities.role.Role import Role
from uuid import UUID
class User():
    """
    A class represent User Account
    """
    roleList: List[Role] = []
    def __init__(self, id: UUID, name:str, firstName: str, lastName:str, password:str,
                 description:str = "",email:str = "", language: Language = Language(), phoneNumber: str = "", parent: object = None) -> None:
        """
        A constructor construct user account

        Parameters
        ----------
        id: UUID
            The indentifier of user account.
        parent: object
            The parent of itself
        name: str
            The name of user.
        firstName: str
            The first name of user.
        lastName: str
            The last name of user.
        password: str
            The password for account.
        email: str
            The email of user.
        phoneNumber: str
            The phone number of user.
        language: Language
            The manipulate language for user [default: Language.Default]
        description: str
            The description about account.
        """
        self.id = id
        self.parent = parent
        self.name = name
        self.firstName = firstName
        self.lastName = lastName
        self.language = language
        self.__email = email
        self.__phoneNumber = phoneNumber
        self.__password = password
        self.description = description
    @property
    def email(self) -> str:
        return self.__email
    @email.setter
    def email(self, email: str) -> None:
        self.__email = email
    @property
    def phoneNumber(self) -> str:
        return self.__phoneNumber
    @phoneNumber.setter
    def phoneNumber(self, phoneNumber: str) -> None:
        self.__phoneNumber = phoneNumber
    @property
    def password(self) -> str:
        return self.__password
    @password.setter
    def password(self, pwd: str) -> None:
        self.__password = pwd
    """
    The method add user

    Parameter:
    ----------
    user: User
        The user to add
    
    Return:
    -------
        Return True is add successfully, otherwise False
    """
    def addUser(self, user: 'User') -> bool:
        # Function to add user:
        def add() -> bool:
            return True
        result = add()
        return result
    """
    The method remove user

    Parameter:
    ----------
    user: User
        The user to remove
    
    Return:
    -------
        Return True is add successfully, otherwise False
    """
    def removeUser(self, user: 'User') -> bool:
        # Function to remove user:
        def remove() -> bool:
            return True
        result = remove()
        return result
    """
    The method modify user

    Parameter:
    ----------
    user: User
        The user to modify
    
    Return:
    -------
        Return True is add successfully, otherwise False
    """
    def modifyUser(self,user: 'User') -> bool:
        #Function to modify user:
        def modify() -> bool:
            return True
        result = modify()
        return result
    """
    The method lock user

    Parameter:
    ----------
    user: User
        The user to lock
    
    Return:
    -------
        Return True is add successfully, otherwise False
    """
    def lockUser(self, user: 'User') -> bool:
        # Function to lock user:
        def lock() -> bool:
            return True
        result = lock()
        return result
    """
    The method unlock user

    Parameter:
    ----------
    user: User
        The user to unlock
    
    Return:
    -------
        Return True is add successfully, otherwise False
    """
    def unlockUser(self, user: 'User') -> bool:
        # Function to unlock user:
        def unlock() -> bool:
            return True
        result = unlock()
        return result
    """
    The method add user to group

    Parameter:
    ----------
    user: User
        The user to add
    group: Group
        The group that user add to
    
    Return:
    -------
        Return True is add successfully, otherwise False
    """
    def addToGroup(self, user: 'User', group: 'Group') -> bool:
        # Function to add user to specify group:
        def add() -> bool:
            return True
        result = add()
        return result
    """
    The method remove user from group

    Parameter:
    ----------
    user: User
        The user to remove
    group: Group
        The group that remove user out of
    
    Return:
    -------
        Return True is add successfully, otherwise False
    """
    def removeFromGroup(self, user: 'User', group: 'Group') -> bool:
        # Function to remove user from specify group:
        def remove() -> bool:
            return True
        result = remove()
        return result
    """
    The method lock user from group

    Parameter:
    ----------
    user: User
        The user to lock
    group: Group
        The group that lock user
    
    Return:
    -------
        Return True is add successfully, otherwise False
    """
    def lockFromGroup(self, user: 'User', group: 'Group') -> bool:
        # Function to lock user from specify group:
        def lock() -> bool:
            return True
        result = lock()
        return result
    """
    The method unlock user at group

    Parameters:
    ----------
    user: User
        The user to unlock
    group: Group
        The group that unlock user
    
    Return:
    -------
        Return True is add successfully, otherwise False
    """
    def unlockFromGroup(self, user: 'User', group: 'Group') -> bool:
        # Function to unlock user from specify group:
        def unlock() -> bool:
            return True
        result = unlock()
        return result
    """
    The method find groups that user joining

    Parameter:
    ----------
    user: User
        The user want to find
    
    Return:
    -------
        Return group list joining
    """
    def findJoinedGroups(self, user: 'User') -> list[Group]:
        # Function find list of joined group of user:
        def find() -> list:
            return []
        result = find()
        return result
    """
    The method find roles that user joining

    Parameter:
    ----------
    user: User
        The user want to find
    
    Return:
    -------
        Return role list joining
    """
    def findJoinedRoles(self, user: 'User') -> list[Role]:
        # Function find list of joined role of user:
        def find() -> list:
            return []
        result = find()
        return result