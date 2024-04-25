from dataclasses import dataclass

from dnv.onecompute.flowmodel import TypeMeta


@dataclass(init=True)
class FileSpecification(TypeMeta):
    """
    A class representing a file specification, which includes information about whether the file
    is located in a shared folder, its filename, and the directory in which it is stored.

    Attributes:
        sharedfolder (bool): A boolean value indicating whether the file is stored in a shared
            folder.
        filename (str): The name of the file.
        directory (str): The name of the directory in which the file is stored.

    Methods:
        type(): A method that returns an empty string. This method is provided for compatibility
            with other classes that inherit from TypeMeta.
    """

    sharedfolder: bool
    filename: str
    directory: str

    @property
    def type(self) -> str:
        return ""
