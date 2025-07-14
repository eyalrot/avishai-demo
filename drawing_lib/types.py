"""Core type definitions and enums for the drawing library."""

from enum import Enum
from typing import Any, Dict, Union
import uuid


class ShapeType(str, Enum):
    """Enumeration of all supported shape types."""
    
    RECTANGLE = "rectangle"
    CIRCLE = "circle"
    ELLIPSE = "ellipse"
    LINE = "line"
    POLYLINE = "polyline"
    POLYGON = "polygon"
    PATH = "path"
    GROUP = "group"


class BlendMode(str, Enum):
    """Enumeration of blend modes for shape rendering."""
    
    NORMAL = "normal"
    MULTIPLY = "multiply"
    SCREEN = "screen"
    OVERLAY = "overlay"
    DARKEN = "darken"
    LIGHTEN = "lighten"
    COLOR_DODGE = "color-dodge"
    COLOR_BURN = "color-burn"
    HARD_LIGHT = "hard-light"
    SOFT_LIGHT = "soft-light"
    DIFFERENCE = "difference"
    EXCLUSION = "exclusion"


class LineCap(str, Enum):
    """Enumeration of line cap styles."""
    
    BUTT = "butt"
    ROUND = "round"
    SQUARE = "square"


class LineJoin(str, Enum):
    """Enumeration of line join styles."""
    
    MITER = "miter"
    ROUND = "round"
    BEVEL = "bevel"


class FillType(str, Enum):
    """Enumeration of fill types."""
    
    SOLID = "solid"
    LINEAR_GRADIENT = "linear-gradient"
    RADIAL_GRADIENT = "radial-gradient"
    PATTERN = "pattern"


class Units(str, Enum):
    """Enumeration of measurement units."""
    
    PIXELS = "px"
    MILLIMETERS = "mm"
    INCHES = "in"
    POINTS = "pt"
    CENTIMETERS = "cm"


# Type aliases for common use cases
ID = str
Coordinate = float
Color = str  # Hex color like "#FF0000" or named color
GeometryDict = Dict[str, Any]


def generate_id() -> ID:
    """Generate a unique string-based ID for performance optimization."""
    return str(uuid.uuid4())


class DrawingLibraryError(Exception):
    """Base exception for all drawing library errors."""
    pass


class InvalidGeometryError(DrawingLibraryError):
    """Raised when shape geometry validation fails."""
    pass


class InvalidTransformError(DrawingLibraryError):
    """Raised when transform validation fails."""
    pass


class InvalidStyleError(DrawingLibraryError):
    """Raised when style property validation fails."""
    pass