"""
Shape models implementing component-based design pattern.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
from pydantic import BaseModel, Field, model_validator

from .types import ShapeType, ID, Coordinate, InvalidGeometryError, generate_id
from .styles import FillProperties, StrokeProperties, Effects


class Transform(BaseModel):
    """Geometric transformation properties."""
    
    x: float = Field(0.0, description="X position")
    y: float = Field(0.0, description="Y position")
    rotation: float = Field(0.0, description="Rotation in degrees")
    scale_x: float = Field(1.0, gt=0.0, description="X scale factor")
    scale_y: float = Field(1.0, gt=0.0, description="Y scale factor")
    skew_x: float = Field(0.0, description="X skew in degrees")
    skew_y: float = Field(0.0, description="Y skew in degrees")


class StyleProperties(BaseModel):
    """Combined styling properties for shapes."""
    
    fill: Optional[FillProperties] = Field(None, description="Fill properties")
    stroke: Optional[StrokeProperties] = Field(None, description="Stroke properties")
    effects: Optional[Effects] = Field(None, description="Visual effects")


class Shape(BaseModel):
    """
    Unified shape model using component-based design.
    
    Uses a flexible geometry dictionary that is validated based on the shape type.
    This approach allows for maximum flexibility while maintaining type safety.
    """
    
    id: ID = Field(default_factory=generate_id, description="Unique shape identifier")
    type: ShapeType = Field(..., description="Type of shape")
    geometry: Dict[str, Any] = Field(..., description="Shape-specific geometry data")
    style: Optional[StyleProperties] = Field(default=None, description="Visual styling")
    transform: Optional[Transform] = Field(default=None, description="Geometric transformations")
    visible: bool = Field(True, description="Shape visibility")
    locked: bool = Field(False, description="Shape editing lock")
    name: Optional[str] = Field(None, description="Optional shape name")
    
    @model_validator(mode='after')
    def validate_geometry(self) -> 'Shape':
        """Validate geometry data matches shape type requirements."""
        # Initialize defaults if None
        if self.style is None:
            self.style = StyleProperties()  # type: ignore
        if self.transform is None:
            self.transform = Transform()  # type: ignore
        geometry = self.geometry
        shape_type = self.type
        
        if shape_type == ShapeType.RECTANGLE:
            self._validate_rectangle_geometry(geometry)
        elif shape_type == ShapeType.CIRCLE:
            self._validate_circle_geometry(geometry)
        elif shape_type == ShapeType.ELLIPSE:
            self._validate_ellipse_geometry(geometry)
        elif shape_type == ShapeType.LINE:
            self._validate_line_geometry(geometry)
        elif shape_type == ShapeType.POLYLINE:
            self._validate_polyline_geometry(geometry)
        elif shape_type == ShapeType.POLYGON:
            self._validate_polygon_geometry(geometry)
        elif shape_type == ShapeType.PATH:
            self._validate_path_geometry(geometry)
        elif shape_type == ShapeType.GROUP:
            self._validate_group_geometry(geometry)
        else:
            raise InvalidGeometryError(f"Unknown shape type: {shape_type}")
        
        return self
    
    def _validate_rectangle_geometry(self, geometry: Dict[str, Any]) -> None:
        """Validate rectangle geometry: requires width and height."""
        required_fields = {'width', 'height'}
        if not required_fields.issubset(geometry.keys()):
            raise InvalidGeometryError(f"Rectangle requires: {required_fields}")
        
        width = geometry.get('width')
        height = geometry.get('height')
        
        if not isinstance(width, (int, float)) or width <= 0:
            raise InvalidGeometryError("Rectangle width must be a positive number")
        if not isinstance(height, (int, float)) or height <= 0:
            raise InvalidGeometryError("Rectangle height must be a positive number")
        
        # Optional corner radius
        if 'corner_radius' in geometry:
            radius = geometry['corner_radius']
            if not isinstance(radius, (int, float)) or radius < 0:
                raise InvalidGeometryError("Corner radius must be a non-negative number")
    
    def _validate_circle_geometry(self, geometry: Dict[str, Any]) -> None:
        """Validate circle geometry: requires radius."""
        if 'radius' not in geometry:
            raise InvalidGeometryError("Circle requires radius")
        
        radius = geometry['radius']
        if not isinstance(radius, (int, float)) or radius <= 0:
            raise InvalidGeometryError("Circle radius must be a positive number")
    
    def _validate_ellipse_geometry(self, geometry: Dict[str, Any]) -> None:
        """Validate ellipse geometry: requires rx and ry."""
        required_fields = {'rx', 'ry'}
        if not required_fields.issubset(geometry.keys()):
            raise InvalidGeometryError(f"Ellipse requires: {required_fields}")
        
        rx = geometry['rx']
        ry = geometry['ry']
        
        if not isinstance(rx, (int, float)) or rx <= 0:
            raise InvalidGeometryError("Ellipse rx must be a positive number")
        if not isinstance(ry, (int, float)) or ry <= 0:
            raise InvalidGeometryError("Ellipse ry must be a positive number")
    
    def _validate_line_geometry(self, geometry: Dict[str, Any]) -> None:
        """Validate line geometry: requires start and end points."""
        required_fields = {'x1', 'y1', 'x2', 'y2'}
        if not required_fields.issubset(geometry.keys()):
            raise InvalidGeometryError(f"Line requires: {required_fields}")
        
        for field in required_fields:
            value = geometry[field]
            if not isinstance(value, (int, float)):
                raise InvalidGeometryError(f"Line {field} must be a number")
    
    def _validate_polyline_geometry(self, geometry: Dict[str, Any]) -> None:
        """Validate polyline geometry: requires points array."""
        if 'points' not in geometry:
            raise InvalidGeometryError("Polyline requires points array")
        
        points = geometry['points']
        if not isinstance(points, list) or len(points) < 2:
            raise InvalidGeometryError("Polyline must have at least 2 points")
        
        for i, point in enumerate(points):
            if not isinstance(point, (list, tuple)) or len(point) != 2:
                raise InvalidGeometryError(f"Point {i} must be [x, y] coordinate")
            if not all(isinstance(coord, (int, float)) for coord in point):
                raise InvalidGeometryError(f"Point {i} coordinates must be numbers")
    
    def _validate_polygon_geometry(self, geometry: Dict[str, Any]) -> None:
        """Validate polygon geometry: requires points array (closed shape)."""
        if 'points' not in geometry:
            raise InvalidGeometryError("Polygon requires points array")
        
        points = geometry['points']
        if not isinstance(points, list) or len(points) < 3:
            raise InvalidGeometryError("Polygon must have at least 3 points")
        
        for i, point in enumerate(points):
            if not isinstance(point, (list, tuple)) or len(point) != 2:
                raise InvalidGeometryError(f"Point {i} must be [x, y] coordinate")
            if not all(isinstance(coord, (int, float)) for coord in point):
                raise InvalidGeometryError(f"Point {i} coordinates must be numbers")
    
    def _validate_path_geometry(self, geometry: Dict[str, Any]) -> None:
        """Validate path geometry: requires path_data string."""
        if 'path_data' not in geometry:
            raise InvalidGeometryError("Path requires path_data")
        
        path_data = geometry['path_data']
        if not isinstance(path_data, str) or not path_data.strip():
            raise InvalidGeometryError("Path data must be a non-empty string")
        
        # Basic SVG path validation - starts with valid command
        valid_commands = {'M', 'm', 'L', 'l', 'H', 'h', 'V', 'v', 'C', 'c', 'S', 's', 'Q', 'q', 'T', 't', 'A', 'a', 'Z', 'z'}
        first_char = path_data.strip()[0]
        if first_char not in valid_commands:
            raise InvalidGeometryError("Path data must start with a valid SVG path command")
    
    def _validate_group_geometry(self, geometry: Dict[str, Any]) -> None:
        """Validate group geometry: requires children array."""
        if 'children' not in geometry:
            raise InvalidGeometryError("Group requires children array")
        
        children = geometry['children']
        if not isinstance(children, list):
            raise InvalidGeometryError("Group children must be an array")
        
        # Children can be empty for an empty group
        for i, child in enumerate(children):
            if not isinstance(child, str):
                raise InvalidGeometryError(f"Child {i} must be a shape ID string")
    
    def get_bounds(self) -> Optional[Tuple[float, float, float, float]]:
        """
        Calculate bounding box for the shape.
        
        Returns:
            Tuple of (min_x, min_y, max_x, max_y) or None if bounds cannot be calculated
        """
        geometry = self.geometry
        transform = self.transform or Transform()  # type: ignore
        
        # Calculate base bounds without transform
        base_bounds = self._calculate_base_bounds()
        if not base_bounds:
            return None
        
        min_x, min_y, max_x, max_y = base_bounds
        
        # Apply transform (simplified - only position for now)
        min_x += transform.x
        min_y += transform.y
        max_x += transform.x
        max_y += transform.y
        
        return (min_x, min_y, max_x, max_y)
    
    def _calculate_base_bounds(self) -> Optional[Tuple[float, float, float, float]]:
        """Calculate bounding box without transforms."""
        geometry = self.geometry
        
        if self.type == ShapeType.RECTANGLE:
            width = geometry['width']
            height = geometry['height']
            return (0.0, 0.0, width, height)
        
        elif self.type == ShapeType.CIRCLE:
            radius = geometry['radius']
            return (-radius, -radius, radius, radius)
        
        elif self.type == ShapeType.ELLIPSE:
            rx = geometry['rx']
            ry = geometry['ry']
            return (-rx, -ry, rx, ry)
        
        elif self.type == ShapeType.LINE:
            x1, y1, x2, y2 = geometry['x1'], geometry['y1'], geometry['x2'], geometry['y2']
            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)
            return (min_x, min_y, max_x, max_y)
        
        elif self.type in (ShapeType.POLYLINE, ShapeType.POLYGON):
            points = geometry['points']
            if not points:
                return None
            
            xs = [point[0] for point in points]
            ys = [point[1] for point in points]
            return (min(xs), min(ys), max(xs), max(ys))
        
        # PATH and GROUP bounds are more complex and would need additional implementation
        return None