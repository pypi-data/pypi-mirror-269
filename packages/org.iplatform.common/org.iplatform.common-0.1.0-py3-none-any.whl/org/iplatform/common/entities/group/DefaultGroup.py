from enum import Enum, unique
@unique
class DefaultGroup(Enum):
    """
    A default groups list

    Attributes
    ----------
    AnomynousUsers = 1
    NonMemberUsers = 2
    """
    AnomynousUsers = 1
    NonMemberUsers = 2
    