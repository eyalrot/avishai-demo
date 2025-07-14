"""
Tests for the component-based shape system.
"""

import pytest
from typing import Dict, Any

from drawing_lib.shapes import Shape, Transform, StyleProperties
from drawing_lib.types import ShapeType, InvalidGeometryError
from drawing_lib.styles import FillProperties, StrokeProperties, RGBColor


class TestTransform:
    """Test Transform model."""
    
    def test_default_transform(self) -> None:
        """Test default transform values."""
        transform = Transform()
        assert transform.x == 0.0
        assert transform.y == 0.0
        assert transform.rotation == 0.0
        assert transform.scale_x == 1.0
        assert transform.scale_y == 1.0
        assert transform.skew_x == 0.0
        assert transform.skew_y == 0.0
    
    def test_custom_transform(self) -> None:
        """Test custom transform values."""
        transform = Transform(
            x=10.0, y=20.0, rotation=45.0,
            scale_x=2.0, scale_y=1.5,
            skew_x=10.0, skew_y=-5.0
        )
        assert transform.x == 10.0
        assert transform.y == 20.0
        assert transform.rotation == 45.0
        assert transform.scale_x == 2.0
        assert transform.scale_y == 1.5
        assert transform.skew_x == 10.0
        assert transform.skew_y == -5.0
    
    def test_invalid_scale(self) -> None:
        """Test that zero or negative scale values are rejected."""
        with pytest.raises(ValueError):
            Transform(scale_x=0.0)
        
        with pytest.raises(ValueError):
            Transform(scale_y=-1.0)


class TestStyleProperties:
    """Test StyleProperties model."""
    
    def test_default_style(self) -> None:
        """Test default style properties."""
        style = StyleProperties()
        assert style.fill is None
        assert style.stroke is None
        assert style.effects is None
    
    def test_style_with_fill(self) -> None:
        """Test style with fill properties."""
        fill = FillProperties(color=RGBColor(r=255, g=0, b=0))
        style = StyleProperties(fill=fill)
        assert style.fill is not None
        assert style.fill.color.r == 255


class TestShapeGeometryValidation:
    """Test shape geometry validation for different shape types."""
    
    def test_rectangle_valid_geometry(self) -> None:
        """Test valid rectangle geometry."""
        geometry = {"width": 100.0, "height": 50.0}
        shape = Shape(type=ShapeType.RECTANGLE, geometry=geometry)
        assert shape.type == ShapeType.RECTANGLE
        assert shape.geometry["width"] == 100.0
        assert shape.geometry["height"] == 50.0
    
    def test_rectangle_with_corner_radius(self) -> None:
        """Test rectangle with corner radius."""
        geometry = {"width": 100.0, "height": 50.0, "corner_radius": 10.0}
        shape = Shape(type=ShapeType.RECTANGLE, geometry=geometry)
        assert shape.geometry["corner_radius"] == 10.0
    
    def test_rectangle_invalid_geometry(self) -> None:
        """Test invalid rectangle geometry."""
        # Missing required fields
        with pytest.raises(InvalidGeometryError, match="Rectangle requires"):
            Shape(type=ShapeType.RECTANGLE, geometry={"width": 100.0})
        
        # Invalid width
        with pytest.raises(InvalidGeometryError, match="width must be a positive number"):
            Shape(type=ShapeType.RECTANGLE, geometry={"width": -10.0, "height": 50.0})
        
        # Invalid height
        with pytest.raises(InvalidGeometryError, match="height must be a positive number"):
            Shape(type=ShapeType.RECTANGLE, geometry={"width": 100.0, "height": 0.0})
        
        # Invalid corner radius
        with pytest.raises(InvalidGeometryError, match="Corner radius must be a non-negative number"):
            Shape(type=ShapeType.RECTANGLE, geometry={"width": 100.0, "height": 50.0, "corner_radius": -5.0})
    
    def test_circle_valid_geometry(self) -> None:
        """Test valid circle geometry."""
        geometry = {"radius": 25.0}
        shape = Shape(type=ShapeType.CIRCLE, geometry=geometry)
        assert shape.geometry["radius"] == 25.0
    
    def test_circle_invalid_geometry(self) -> None:
        """Test invalid circle geometry."""
        # Missing radius
        with pytest.raises(InvalidGeometryError, match="Circle requires radius"):
            Shape(type=ShapeType.CIRCLE, geometry={})
        
        # Invalid radius
        with pytest.raises(InvalidGeometryError, match="radius must be a positive number"):
            Shape(type=ShapeType.CIRCLE, geometry={"radius": -10.0})
    
    def test_ellipse_valid_geometry(self) -> None:
        """Test valid ellipse geometry."""
        geometry = {"rx": 30.0, "ry": 20.0}
        shape = Shape(type=ShapeType.ELLIPSE, geometry=geometry)
        assert shape.geometry["rx"] == 30.0
        assert shape.geometry["ry"] == 20.0
    
    def test_ellipse_invalid_geometry(self) -> None:
        """Test invalid ellipse geometry."""
        # Missing required fields
        with pytest.raises(InvalidGeometryError, match="Ellipse requires"):
            Shape(type=ShapeType.ELLIPSE, geometry={"rx": 30.0})
        
        # Invalid rx
        with pytest.raises(InvalidGeometryError, match="rx must be a positive number"):
            Shape(type=ShapeType.ELLIPSE, geometry={"rx": 0.0, "ry": 20.0})
    
    def test_line_valid_geometry(self) -> None:
        """Test valid line geometry."""
        geometry = {"x1": 0.0, "y1": 0.0, "x2": 100.0, "y2": 50.0}
        shape = Shape(type=ShapeType.LINE, geometry=geometry)
        assert shape.geometry["x1"] == 0.0
        assert shape.geometry["y1"] == 0.0
        assert shape.geometry["x2"] == 100.0
        assert shape.geometry["y2"] == 50.0
    
    def test_line_invalid_geometry(self) -> None:
        """Test invalid line geometry."""
        # Missing required fields
        with pytest.raises(InvalidGeometryError, match="Line requires"):
            Shape(type=ShapeType.LINE, geometry={"x1": 0.0, "y1": 0.0, "x2": 100.0})
        
        # Invalid coordinate type
        with pytest.raises(InvalidGeometryError, match="must be a number"):
            Shape(type=ShapeType.LINE, geometry={"x1": "0", "y1": 0.0, "x2": 100.0, "y2": 50.0})
    
    def test_polyline_valid_geometry(self) -> None:
        """Test valid polyline geometry."""
        geometry = {"points": [[0.0, 0.0], [50.0, 25.0], [100.0, 0.0]]}
        shape = Shape(type=ShapeType.POLYLINE, geometry=geometry)
        assert len(shape.geometry["points"]) == 3
    
    def test_polyline_invalid_geometry(self) -> None:
        """Test invalid polyline geometry."""
        # Missing points
        with pytest.raises(InvalidGeometryError, match="Polyline requires points array"):
            Shape(type=ShapeType.POLYLINE, geometry={})
        
        # Too few points
        with pytest.raises(InvalidGeometryError, match="must have at least 2 points"):
            Shape(type=ShapeType.POLYLINE, geometry={"points": [[0.0, 0.0]]})
        
        # Invalid point format
        with pytest.raises(InvalidGeometryError, match="must be \\[x, y\\] coordinate"):
            Shape(type=ShapeType.POLYLINE, geometry={"points": [[0.0], [50.0, 25.0]]})
    
    def test_polygon_valid_geometry(self) -> None:
        """Test valid polygon geometry."""
        geometry = {"points": [[0.0, 0.0], [50.0, 0.0], [25.0, 50.0]]}
        shape = Shape(type=ShapeType.POLYGON, geometry=geometry)
        assert len(shape.geometry["points"]) == 3
    
    def test_polygon_invalid_geometry(self) -> None:
        """Test invalid polygon geometry."""
        # Too few points
        with pytest.raises(InvalidGeometryError, match="must have at least 3 points"):
            Shape(type=ShapeType.POLYGON, geometry={"points": [[0.0, 0.0], [50.0, 0.0]]})
    
    def test_path_valid_geometry(self) -> None:
        """Test valid path geometry."""
        geometry = {"path_data": "M 10,10 L 50,50 Q 100,10 150,50"}
        shape = Shape(type=ShapeType.PATH, geometry=geometry)
        assert "path_data" in shape.geometry
    
    def test_path_invalid_geometry(self) -> None:
        """Test invalid path geometry."""
        # Missing path_data
        with pytest.raises(InvalidGeometryError, match="Path requires path_data"):
            Shape(type=ShapeType.PATH, geometry={})
        
        # Empty path_data
        with pytest.raises(InvalidGeometryError, match="must be a non-empty string"):
            Shape(type=ShapeType.PATH, geometry={"path_data": ""})
        
        # Invalid path command
        with pytest.raises(InvalidGeometryError, match="must start with a valid SVG path command"):
            Shape(type=ShapeType.PATH, geometry={"path_data": "X 10,10"})
    
    def test_group_valid_geometry(self) -> None:
        """Test valid group geometry."""
        geometry = {"children": ["shape1", "shape2", "shape3"]}
        shape = Shape(type=ShapeType.GROUP, geometry=geometry)
        assert len(shape.geometry["children"]) == 3
    
    def test_group_empty_children(self) -> None:
        """Test group with empty children."""
        geometry = {"children": []}
        shape = Shape(type=ShapeType.GROUP, geometry=geometry)
        assert len(shape.geometry["children"]) == 0
    
    def test_group_invalid_geometry(self) -> None:
        """Test invalid group geometry."""
        # Missing children
        with pytest.raises(InvalidGeometryError, match="Group requires children array"):
            Shape(type=ShapeType.GROUP, geometry={})
        
        # Invalid child type
        with pytest.raises(InvalidGeometryError, match="must be a shape ID string"):
            Shape(type=ShapeType.GROUP, geometry={"children": ["shape1", 123]})


class TestShapeProperties:
    """Test shape properties and methods."""
    
    def test_shape_defaults(self) -> None:
        """Test default shape property values."""
        geometry = {"width": 100.0, "height": 50.0}
        shape = Shape(type=ShapeType.RECTANGLE, geometry=geometry)
        
        assert shape.visible is True
        assert shape.locked is False
        assert shape.name is None
        assert shape.id is not None  # Generated ID
        assert shape.transform is not None
        assert isinstance(shape.transform, Transform)
        assert shape.style is not None
        assert isinstance(shape.style, StyleProperties)
    
    def test_shape_with_custom_properties(self) -> None:
        """Test shape with custom properties."""
        geometry = {"radius": 25.0}
        transform = Transform(x=10.0, y=20.0)
        fill = FillProperties(color=RGBColor(r=255, g=0, b=0))
        style = StyleProperties(fill=fill)
        
        shape = Shape(
            type=ShapeType.CIRCLE,
            geometry=geometry,
            transform=transform,
            style=style,
            visible=False,
            locked=True,
            name="My Circle"
        )
        
        assert shape.visible is False
        assert shape.locked is True
        assert shape.name == "My Circle"
        assert shape.transform.x == 10.0
        assert shape.style.fill.color.r == 255
    
    def test_rectangle_bounds(self) -> None:
        """Test bounding box calculation for rectangle."""
        geometry = {"width": 100.0, "height": 50.0}
        transform = Transform(x=10.0, y=20.0)
        shape = Shape(type=ShapeType.RECTANGLE, geometry=geometry, transform=transform)
        
        bounds = shape.get_bounds()
        assert bounds == (10.0, 20.0, 110.0, 70.0)  # (min_x, min_y, max_x, max_y)
    
    def test_circle_bounds(self) -> None:
        """Test bounding box calculation for circle."""
        geometry = {"radius": 25.0}
        transform = Transform(x=50.0, y=50.0)
        shape = Shape(type=ShapeType.CIRCLE, geometry=geometry, transform=transform)
        
        bounds = shape.get_bounds()
        assert bounds == (25.0, 25.0, 75.0, 75.0)
    
    def test_line_bounds(self) -> None:
        """Test bounding box calculation for line."""
        geometry = {"x1": 10.0, "y1": 20.0, "x2": 50.0, "y2": 5.0}
        shape = Shape(type=ShapeType.LINE, geometry=geometry)
        
        bounds = shape.get_bounds()
        assert bounds == (10.0, 5.0, 50.0, 20.0)
    
    def test_polyline_bounds(self) -> None:
        """Test bounding box calculation for polyline."""
        geometry = {"points": [[10.0, 20.0], [50.0, 5.0], [30.0, 40.0]]}
        shape = Shape(type=ShapeType.POLYLINE, geometry=geometry)
        
        bounds = shape.get_bounds()
        assert bounds == (10.0, 5.0, 50.0, 40.0)


class TestShapeSerialization:
    """Test shape JSON serialization and deserialization."""
    
    def test_rectangle_serialization(self) -> None:
        """Test rectangle serialization round-trip."""
        geometry = {"width": 100.0, "height": 50.0, "corner_radius": 5.0}
        shape = Shape(type=ShapeType.RECTANGLE, geometry=geometry, name="Test Rectangle")
        
        # Serialize to JSON
        json_data = shape.model_dump()
        
        # Deserialize back
        shape2 = Shape.model_validate(json_data)
        
        assert shape2.type == ShapeType.RECTANGLE
        assert shape2.geometry["width"] == 100.0
        assert shape2.geometry["height"] == 50.0
        assert shape2.geometry["corner_radius"] == 5.0
        assert shape2.name == "Test Rectangle"
    
    def test_complex_shape_serialization(self) -> None:
        """Test complex shape with styling serialization."""
        geometry = {"radius": 25.0}
        fill = FillProperties(color=RGBColor(r=255, g=128, b=64))
        stroke = StrokeProperties(color=RGBColor(r=0, g=0, b=0), width=2.0)
        style = StyleProperties(fill=fill, stroke=stroke)
        transform = Transform(x=50.0, y=50.0, rotation=45.0)
        
        shape = Shape(
            type=ShapeType.CIRCLE,
            geometry=geometry,
            style=style,
            transform=transform,
            name="Styled Circle"
        )
        
        # Serialize to JSON
        json_data = shape.model_dump()
        
        # Deserialize back
        shape2 = Shape.model_validate(json_data)
        
        assert shape2.type == ShapeType.CIRCLE
        assert shape2.style.fill.color.r == 255
        assert shape2.style.stroke.width == 2.0
        assert shape2.transform.rotation == 45.0
        assert shape2.name == "Styled Circle"