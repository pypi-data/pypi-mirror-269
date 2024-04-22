"""
A module containing the InfoFileReader class.

...

Classes
-------
InfoFileReader
    A class to read info files.
"""

from beartype.typing import Tuple, Dict

from .base import BaseReader
from ..traj import MDEngineFormat, MDEngineFormatError


class InfoFileReader(BaseReader):
    """
    A class to read info files.

    Parameters
    ----------
    BaseReader : BaseReader
        A base class for all readers.

    Attributes
    ----------
    filename : str
        The name of the file to read from.
    format : MDEngineFormat
        The format of the info file. Default is MDEngineFormat.PIMD_QMCF.
    """

    def __init__(self, filename: str, format: MDEngineFormat | str = MDEngineFormat.PIMD_QMCF) -> None:
        """
        Initializes the InfoFileReader with the given filename.

        Parameters
        ----------
        filename : str
            The name of the file to read from.
        format : MDEngineFormat | str, optional
            The format of the info file. Default is MDEngineFormat.PIMD_QMCF.
        """
        super().__init__(filename)

        self.format = MDEngineFormat(format)

    def read(self) -> Tuple[Dict, Dict | None]:
        """
        Reads the info file.

        Returns
        -------
        dict
            The information strings of the info file as a dictionary.
            The keys are the names of the information strings. The values are the
            corresponding data entry (columns in energy file).
        dict
            The units of the info file as a dictionary. The keys are the names of the
            information strings. The values are the corresponding units.
        """
        if self.format == MDEngineFormat.PIMD_QMCF:
            return self.read_pimd_qmcf()
        elif self.format == MDEngineFormat.QMCFC:
            return self.read_qmcfc()

    def read_pimd_qmcf(self) -> Tuple[Dict, Dict]:
        """
        Reads the info file in pimd-qmcf format.

        Returns
        -------
        dict
            The information strings of the info file as a dictionary.
            The keys are the names of the information strings. The values are the
            corresponding data entry (columns in energy file).
        dict
            The units of the info file as a dictionary. The keys are the names of the
            information strings. The values are the corresponding units.

        Raises
        ------
        MDEngineFormatError
            If the info file is not in pimd-qmcf format.
        """
        info = {}
        units = {}

        with open(self.filename, "r") as file:

            lines = file.readlines()

            entry_counter = 0

            for line in lines[3:-2]:
                line = line.split()

                if len(line) == 8:
                    info[line[1]] = entry_counter
                    units[line[1]] = line[3]
                    entry_counter += 1
                    info[line[4]] = entry_counter
                    units[line[4]] = line[6]
                    entry_counter += 1
                else:
                    raise MDEngineFormatError(
                        f"Info file {self.filename} is not in pimd-qmcf format.")

        return info, units

    def read_qmcfc(self) -> Tuple[Dict, None]:
        """
        Reads the info file in qmcfc format.

        Returns
        -------
        dict
            The information strings of the info file as a dictionary.
            The keys are the names of the information strings. The values are the
            corresponding data entry (columns in energy file).
        None
            For the qmcfc format, no units are given.

        Raises
        ------
        MDEngineFormatError
            If the info file is not in qmcfc format.
        """
        info = {}

        with open(self.filename, "r") as file:

            lines = file.readlines()

            entry_counter = 0

            for line in lines[3:-2]:
                line = line.split()

                if len(line) == 6:
                    info[line[1]] = entry_counter
                    entry_counter += 1
                    info[line[3]] = entry_counter
                    entry_counter += 1
                elif len(line) == 7:
                    info[' '.join(line[1:3])] = entry_counter
                    entry_counter += 1
                    info[line[4]] = entry_counter
                    entry_counter += 1
                else:
                    raise MDEngineFormatError(
                        f"Info file {self.filename} is not in qmcfc format.")

        return info, None
