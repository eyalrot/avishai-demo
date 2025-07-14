"""
Drawing library for vector graphics with Pydantic models.
"""

__version__ = "0.1.0"

# Export main components
from .types import ShapeType, BlendMode, LineCap, LineJoin, FillType, Units
from .styles import (
    RGBColor, RGBAColor, HSLColor, HexColor,
    LinearGradient, RadialGradient, PatternFill,
    FillProperties, StrokeProperties, Effects
)
from .shapes import Shape, Transform, StyleProperties
from .layers import Layer, LayerGroup, LayerManager
from .document import (
    CanvasSize, BackgroundProperties, DocumentMetadata, ViewSettings,
    ExportSettings, DrawingDocument
)

__all__ = [
    "ShapeType", "BlendMode", "LineCap", "LineJoin", "FillType", "Units",
    "RGBColor", "RGBAColor", "HSLColor", "HexColor",
    "LinearGradient", "RadialGradient", "PatternFill",
    "FillProperties", "StrokeProperties", "Effects",
    "Shape", "Transform", "StyleProperties",
    "Layer", "LayerGroup", "LayerManager",
    "CanvasSize", "BackgroundProperties", "DocumentMetadata", "ViewSettings",
    "ExportSettings", "DrawingDocument"
]