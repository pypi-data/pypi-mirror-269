from enum import Enum, unique


@unique
class Environment(Enum):
    """
    Enumeration of possible environments.

    Each environment is represented by a unique constant value that can be accessed as an attribute
    of the class.

    Attributes:
        Development: Development environment.
        Testing: Testing environment.
        Staging: Staging environment.
        Production: Production environment.
        DevCore: Development Core environment.
    """

    Development = 0
    Testing = 1
    Staging = 2
    Production = 3
    DevCore = 4
