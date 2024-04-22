"""
A module containing different exceptions related to the physicalData subpackage.

...

Classes
-------
EnergyError
    Exception raised for errors related to the Energy class
"""

from ..exceptions import PQException


class EnergyError(PQException):
    """
    Exception raised for errors related to the Energy class
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
