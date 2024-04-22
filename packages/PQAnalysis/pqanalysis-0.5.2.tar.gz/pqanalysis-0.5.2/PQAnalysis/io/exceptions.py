"""
A module containing different exceptions related to the io subpackage.

...

Classes
-------
BoxWriterError
    Exception raised for errors related to the BoxWriter class
FrameReaderError
    Exception raised for errors related to the FrameReader class
MoldescriptorReaderError
    Exception raised for errors related to the MoldescriptorReader class
RestartFileReaderError
    Exception raised for errors related to the RestartFileReader class
RestartFileWriterError
    Exception raised for errors related to the RestartFileWriter class
TrajectoryReaderError
    Exception raised for errors related to the TrajectoryReader class
"""

from ..exceptions import PQException


class BoxWriterError(PQException):
    """
    Exception raised for errors related to the BoxWriter class
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class FrameReaderError(PQException):
    """
    Exception raised for errors related to the FrameReader class
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class MoldescriptorReaderError(PQException):
    """
    Exception raised for errors related to the MoldescriptorReader class
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class RestartFileReaderError(PQException):
    """
    Exception raised for errors related to the RestartFileReader class
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class RestartFileWriterError(PQException):
    """
    Exception raised for errors related to the RestartFileWriter class
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class TrajectoryReaderError(PQException):
    """
    Exception raised for errors related to the TrajectoryReader class
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
