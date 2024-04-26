
from typing import List
from typing import NewType

from dataclasses import dataclass

from pyorthogonalrouting.Common import NOT_SET_INT


@dataclass
class Size:
    """
    A size construct
    """
    width:  int = NOT_SET_INT
    height: int = NOT_SET_INT


Sizes = NewType('Sizes', List[Size])
