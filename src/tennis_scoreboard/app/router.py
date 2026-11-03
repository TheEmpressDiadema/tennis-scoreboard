import re
import logging
from dataclasses import dataclass
from typing import Callable


@dataclass
class Route:

    pattern: re.Pattern
    handler: str
    