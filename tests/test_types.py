"""Test the core types module."""

import pytest
from drawing_lib.types import (
    ShapeType, BlendMode, LineCap, LineJoin, FillType, Units,
    generate_id, DrawingLibraryError, InvalidGeometryError,
    InvalidTransformError, InvalidStyleError
)


def test_shape_type_enum() -> None:
    """Test ShapeType enum values."""
    assert ShapeType.RECTANGLE.value == "rectangle"
    assert ShapeType.CIRCLE.value == "circle"
    assert ShapeType.ELLIPSE.value == "ellipse"
    assert ShapeType.LINE.value == "line"
    assert ShapeType.POLYLINE.value == "polyline"
    assert ShapeType.POLYGON.value == "polygon"
    assert ShapeType.PATH.value == "path"
    assert ShapeType.GROUP.value == "group"
    
    # Test all enum values are present
    expected_shapes = {
        "rectangle", "circle", "ellipse", "line", 
        "polyline", "polygon", "path", "group"
    }
    actual_shapes = {shape.value for shape in ShapeType}
    assert actual_shapes == expected_shapes


def test_blend_mode_enum() -> None:
    """Test BlendMode enum values."""
    assert BlendMode.NORMAL.value == "normal"
    assert BlendMode.MULTIPLY.value == "multiply"
    assert BlendMode.SCREEN.value == "screen"
    assert BlendMode.OVERLAY.value == "overlay"


def test_line_cap_enum() -> None:
    """Test LineCap enum values."""
    assert LineCap.BUTT.value == "butt"
    assert LineCap.ROUND.value == "round"
    assert LineCap.SQUARE.value == "square"


def test_line_join_enum() -> None:
    """Test LineJoin enum values."""
    assert LineJoin.MITER.value == "miter"
    assert LineJoin.ROUND.value == "round"
    assert LineJoin.BEVEL.value == "bevel"


def test_fill_type_enum() -> None:
    """Test FillType enum values."""
    assert FillType.SOLID.value == "solid"
    assert FillType.LINEAR_GRADIENT.value == "linear-gradient"
    assert FillType.RADIAL_GRADIENT.value == "radial-gradient"
    assert FillType.PATTERN.value == "pattern"


def test_units_enum() -> None:
    """Test Units enum values."""
    assert Units.PIXELS.value == "px"
    assert Units.MILLIMETERS.value == "mm"
    assert Units.INCHES.value == "in"
    assert Units.POINTS.value == "pt"
    assert Units.CENTIMETERS.value == "cm"


def test_generate_id() -> None:
    """Test ID generation system."""
    id1 = generate_id()
    id2 = generate_id()
    
    # IDs should be strings
    assert isinstance(id1, str)
    assert isinstance(id2, str)
    
    # IDs should be unique
    assert id1 != id2
    
    # IDs should not be empty
    assert len(id1) > 0
    assert len(id2) > 0


def test_exception_hierarchy() -> None:
    """Test custom exception classes."""
    # Test base exception
    base_error = DrawingLibraryError("Base error")
    assert str(base_error) == "Base error"
    
    # Test specific exceptions inherit from base
    assert issubclass(InvalidGeometryError, DrawingLibraryError)
    assert issubclass(InvalidTransformError, DrawingLibraryError)
    assert issubclass(InvalidStyleError, DrawingLibraryError)
    
    # Test specific exceptions can be raised
    with pytest.raises(InvalidGeometryError):
        raise InvalidGeometryError("Geometry error")
    
    with pytest.raises(InvalidTransformError):
        raise InvalidTransformError("Transform error")
    
    with pytest.raises(InvalidStyleError):
        raise InvalidStyleError("Style error")