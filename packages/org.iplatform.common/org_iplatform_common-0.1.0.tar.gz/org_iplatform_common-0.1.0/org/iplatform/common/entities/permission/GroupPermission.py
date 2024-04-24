from uuid import UUID
class GroupPermission():
    """
    The Group Permission
    """
    def __init__(self,id: UUID = None, isAddedGroup: bool = False, isEditedGroup: bool = False, isDeletedGroup: bool = False, parent: object = None):
        """
        The constructor construct class

        Parameters:
        -----------
        isAddedGroup: bool
            Is True if allow adding Group, otherwise Fail.
        isEditedGroup: bool
            Is True if allow editing Group, otherwise Fail.
        isDeletedGroup: bool
            Is True if allow deleting Group, otherwise Fail.
        parent: object
            The entity contain itself
        """
        self.id = id
        self.parent = parent
        self.isAddedGroup = isAddedGroup
        self.isEditedGroup = isEditedGroup
        self.isDeletedGroup = isDeletedGroup