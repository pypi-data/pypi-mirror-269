
from typing import List
from typing import NewType
from typing import cast

from dataclasses import dataclass

from pyorthogonalrouting.Common import NOT_SET_INT
from pyorthogonalrouting.Size import Size


@dataclass
class Rect(Size):
    """
    Represents a Rectangle by location and size
    """
    left: int = NOT_SET_INT
    top:  int = NOT_SET_INT


Rects = NewType('Rects', List[Rect])


NO_RECT: Rect = cast(Rect, None)
