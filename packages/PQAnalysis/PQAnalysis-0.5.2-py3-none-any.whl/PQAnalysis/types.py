import numpy as np
import _io

from beartype.vale import Is
from typing import Annotated


Np2DNumberArray = Annotated[np.ndarray, Is[lambda array:
                                           array.ndim == 2 and
                                           (np.issubdtype(array.dtype, np.number))]]

Np1DNumberArray = Annotated[np.ndarray, Is[lambda array:
                                           array.ndim == 1 and
                                           (np.issubdtype(array.dtype, np.number)) or
                                           len(array) == 0]]

Np3x3NumberArray = Annotated[np.ndarray, Is[lambda array:
                                            array.ndim == 2 and
                                            array.shape == (3, 3) and
                                            (np.issubdtype(array.dtype, np.number))]]

Np2DIntArray = Annotated[np.ndarray, Is[lambda array:
                                        array.ndim == 2 and
                                        (np.issubdtype(array.dtype, np.integer))]]

Np1DIntArray = Annotated[np.ndarray, Is[lambda array:
                                        array.ndim == 1 and
                                        (np.issubdtype(array.dtype, np.integer)) or
                                        len(array) == 0]]

FILE = _io.TextIOWrapper
