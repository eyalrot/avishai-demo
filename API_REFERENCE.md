# Drawing Library API Reference

## Overview

The Drawing Library provides a comprehensive Python API for creating, manipulating, and exporting vector graphics. Built on Pydantic for robust data validation and type safety, it supports complex drawing operations with layers, styling, and transforms.

## Core Architecture

### Module Structure

```
drawing_lib/
├── __init__.py          # Main exports
├── types.py             # Core types and enums
├── styles.py            # Color and styling system
├── shapes.py            # Shape definitions and validation
├── layers.py            # Layer management system
└── document.py          # Document model and operations
```

## Core Types (`types.py`)

### ID Type
```python
ID = str  # UUID-based string identifiers
```

### Enums

#### Units
```python
class Units(str, Enum):
    PIXELS = "px"
    INCHES = "in"
    MILLIMETERS = "mm"
    CENTIMETERS = "cm"
    POINTS = "pt"
```

#### ShapeType
```python
class ShapeType(str, Enum):
    RECTANGLE = "rectangle"
    CIRCLE = "circle"
    ELLIPSE = "ellipse"
    LINE = "line"
    POLYGON = "polygon"
    PATH = "path"
    GROUP = "group"
    TEXT = "text"
```

#### BlendMode
```python
class BlendMode(str, Enum):
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
```

### Utility Functions

#### generate_id()
```python
def generate_id() -> ID:
    """Generate a unique string ID using UUID4."""
```

#### validate_color_value()
```python
def validate_color_value(value: int) -> int:
    """Validate RGB color value (0-255)."""
```

## Styling System (`styles.py`)

### Colors

#### RGBColor
```python
class RGBColor(BaseModel):
    r: int = Field(..., ge=0, le=255)
    g: int = Field(..., ge=0, le=255) 
    b: int = Field(..., ge=0, le=255)
    
    def to_hex(self) -> str:
        """Convert to hex format (#RRGGBB)."""
    
    def to_tuple(self) -> Tuple[int, int, int]:
        """Convert to RGB tuple."""
    
    @classmethod
    def from_hex(cls, hex_color: str) -> 'RGBColor':
        """Create from hex string."""
```

#### HSLColor
```python
class HSLColor(BaseModel):
    h: float = Field(..., ge=0.0, le=360.0)  # Hue
    s: float = Field(..., ge=0.0, le=100.0)  # Saturation
    l: float = Field(..., ge=0.0, le=100.0)  # Lightness
    
    def to_rgb(self) -> RGBColor:
        """Convert to RGB color."""
```

### Fill Properties

#### FillType
```python
class FillType(str, Enum):
    SOLID = "solid"
    GRADIENT_LINEAR = "gradient-linear"
    GRADIENT_RADIAL = "gradient-radial"
    PATTERN = "pattern"
```

#### FillProperties
```python
class FillProperties(BaseModel):
    type: FillType = FillType.SOLID
    color: Color
    opacity: float = Field(1.0, ge=0.0, le=1.0)
    
    # Gradient properties (when type is gradient)
    gradient_stops: Optional[List[GradientStop]] = None
    gradient_start: Optional[Tuple[float, float]] = None
    gradient_end: Optional[Tuple[float, float]] = None
```

### Stroke Properties

#### StrokeProperties
```python
class StrokeProperties(BaseModel):
    color: Color
    width: float = Field(1.0, gt=0.0)
    opacity: float = Field(1.0, ge=0.0, le=1.0)
    line_cap: LineCap = LineCap.ROUND
    line_join: LineJoin = LineJoin.ROUND
    dash_array: Optional[List[float]] = None
    dash_offset: float = 0.0
```

#### LineCap
```python
class LineCap(str, Enum):
    BUTT = "butt"
    ROUND = "round"
    SQUARE = "square"
```

#### LineJoin
```python
class LineJoin(str, Enum):
    MITER = "miter"
    ROUND = "round"
    BEVEL = "bevel"
```

### Style Properties

#### StyleProperties
```python
class StyleProperties(BaseModel):
    fill: Optional[FillProperties] = None
    stroke: Optional[StrokeProperties] = None
    
    def has_fill(self) -> bool:
        """Check if style has fill."""
    
    def has_stroke(self) -> bool:
        """Check if style has stroke."""
```

## Shape System (`shapes.py`)

### Transform

#### Transform
```python
class Transform(BaseModel):
    x: float = 0.0
    y: float = 0.0
    rotation: float = 0.0
    scale_x: float = 1.0
    scale_y: float = 1.0
    skew_x: float = 0.0
    skew_y: float = 0.0
    
    def apply_translation(self, dx: float, dy: float) -> 'Transform':
        """Apply translation."""
    
    def apply_rotation(self, angle: float) -> 'Transform':
        """Apply rotation in degrees."""
    
    def apply_scale(self, sx: float, sy: float = None) -> 'Transform':
        """Apply scaling."""
    
    def to_matrix(self) -> List[List[float]]:
        """Convert to transformation matrix."""
```

### Shape Model

#### Shape
```python
class Shape(BaseModel):
    id: ID = Field(default_factory=generate_id)
    type: ShapeType
    geometry: Dict[str, Any]  # Shape-specific geometry
    style: Optional[StyleProperties] = None
    transform: Transform = Field(default_factory=Transform)
    visible: bool = True
    locked: bool = False
    name: Optional[str] = None
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """Get shape bounding box (min_x, min_y, max_x, max_y)."""
    
    def set_position(self, x: float, y: float) -> None:
        """Set shape position."""
    
    def move_by(self, dx: float, dy: float) -> None:
        """Move shape by offset."""
```

### Geometry Specifications

#### Rectangle Geometry
```python
{
    "width": float,      # Required, > 0
    "height": float,     # Required, > 0
    "corner_radius": float  # Optional, >= 0
}
```

#### Circle Geometry
```python
{
    "radius": float  # Required, > 0
}
```

#### Ellipse Geometry
```python
{
    "rx": float,  # Required, > 0 (horizontal radius)
    "ry": float   # Required, > 0 (vertical radius)
}
```

#### Line Geometry
```python
{
    "x1": float,  # Start point X
    "y1": float,  # Start point Y
    "x2": float,  # End point X
    "y2": float   # End point Y
}
```

#### Polygon Geometry
```python
{
    "points": List[List[float]]  # [[x1, y1], [x2, y2], ...]
}
```

#### Path Geometry
```python
{
    "path_data": str  # SVG path data (e.g., "M 0,0 L 100,100")
}
```

## Layer System (`layers.py`)

### Layer

#### Layer
```python
class Layer(BaseModel):
    id: ID = Field(default_factory=generate_id)
    name: str
    shapes: List[Union[Shape, ID]] = Field(default_factory=list)
    z_index: int = 0
    visible: bool = True
    locked: bool = False
    opacity: float = Field(1.0, ge=0.0, le=1.0)
    blend_mode: BlendMode = BlendMode.NORMAL
    parent_id: Optional[ID] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def add_shape(self, shape: Union[Shape, ID]) -> None:
        """Add shape to layer."""
    
    def remove_shape(self, shape_id: ID) -> bool:
        """Remove shape from layer."""
    
    def get_shape_count(self) -> int:
        """Get number of shapes in layer."""
    
    def is_empty(self) -> bool:
        """Check if layer has no shapes."""
    
    def find_shape_by_id(self, shape_id: ID) -> Optional[Shape]:
        """Find shape by ID."""
```

### Layer Group

#### LayerGroup
```python
class LayerGroup(BaseModel):
    id: ID = Field(default_factory=generate_id)
    name: str
    children: List[Union[Layer, 'LayerGroup']] = Field(default_factory=list)
    z_index: int = 0
    visible: bool = True
    locked: bool = False
    expanded: bool = True
    opacity: float = Field(1.0, ge=0.0, le=1.0)
    blend_mode: BlendMode = BlendMode.NORMAL
    parent_id: Optional[ID] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def add_child(self, child: Union[Layer, 'LayerGroup']) -> None:
        """Add child layer or group."""
    
    def remove_child(self, child_id: ID) -> bool:
        """Remove child by ID."""
    
    def get_all_layers(self, recursive: bool = True) -> List[Layer]:
        """Get all layers in group."""
    
    def find_layer_by_id(self, layer_id: ID) -> Optional[Layer]:
        """Find layer by ID."""
    
    def find_group_by_id(self, group_id: ID) -> Optional['LayerGroup']:
        """Find group by ID."""
```

### Layer Manager

#### LayerManager
```python
class LayerManager(BaseModel):
    root_group: LayerGroup = Field(default_factory=lambda: LayerGroup(name="Root"))
    active_layer_id: Optional[ID] = None
    
    def create_layer(self, name: str, **kwargs) -> Layer:
        """Create new layer."""
    
    def create_group(self, name: str, **kwargs) -> LayerGroup:
        """Create new layer group."""
    
    def delete_layer(self, layer_id: ID) -> bool:
        """Delete layer by ID."""
    
    def get_all_layers(self) -> List[Layer]:
        """Get all layers in manager."""
    
    def get_visible_layers(self) -> List[Layer]:
        """Get only visible layers."""
    
    def get_layers_by_z_order(self) -> List[Layer]:
        """Get layers sorted by z-index."""
    
    def get_layer_count(self) -> int:
        """Get total number of layers."""
    
    def set_active_layer(self, layer_id: ID) -> bool:
        """Set active layer."""
    
    def get_active_layer(self) -> Optional[Layer]:
        """Get active layer."""
```

## Document System (`document.py`)

### Canvas and Background

#### CanvasSize
```python
class CanvasSize(BaseModel):
    width: float = Field(..., gt=0.0)
    height: float = Field(..., gt=0.0)
    units: Units = Units.PIXELS
    
    def to_pixels(self, dpi: float = 96.0) -> Tuple[float, float]:
        """Convert to pixels."""
    
    def get_aspect_ratio(self) -> float:
        """Get width/height ratio."""
```

#### BackgroundProperties
```python
class BackgroundProperties(BaseModel):
    color: Optional[Color] = None
    transparent: bool = True
    image_url: Optional[str] = None
    image_opacity: float = Field(1.0, ge=0.0, le=1.0)
```

### Document Metadata

#### DocumentMetadata
```python
class DocumentMetadata(BaseModel):
    title: str = "Untitled Document"
    description: Optional[str] = None
    author: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime = Field(default_factory=datetime.now)
    version: str = "1.0"
    app_version: str = "0.1.0"
    custom_properties: Dict[str, Any] = Field(default_factory=dict)
    
    def update_modified_time(self) -> None:
        """Update modified timestamp."""
```

### Settings

#### ViewSettings
```python
class ViewSettings(BaseModel):
    zoom_level: float = Field(1.0, gt=0.0)
    pan_x: float = 0.0
    pan_y: float = 0.0
    show_grid: bool = False
    show_rulers: bool = True
    show_guides: bool = True
    snap_to_grid: bool = False
    snap_to_guides: bool = True
    grid_size: float = Field(10.0, gt=0.0)
    grid_color: Color = Field(default_factory=lambda: RGBColor(r=200, g=200, b=200))
```

#### ExportSettings
```python
class ExportSettings(BaseModel):
    default_format: str = "svg"
    dpi: float = Field(96.0, gt=0.0)
    quality: float = Field(0.9, ge=0.0, le=1.0)
    include_metadata: bool = True
    transparent_background: bool = True
```

### Main Document

#### DrawingDocument
```python
class DrawingDocument(BaseModel):
    id: ID = Field(default_factory=generate_id)
    canvas: CanvasSize
    background: BackgroundProperties = Field(default_factory=BackgroundProperties)
    layer_manager: LayerManager = Field(default_factory=LayerManager)
    metadata: DocumentMetadata = Field(default_factory=DocumentMetadata)
    view_settings: ViewSettings = Field(default_factory=ViewSettings)
    export_settings: ExportSettings = Field(default_factory=ExportSettings)
    
    # Core methods
    def get_total_shape_count(self) -> int:
        """Get total shapes in document."""
    
    def get_canvas_bounds(self) -> Tuple[float, float, float, float]:
        """Get canvas bounds."""
    
    def get_canvas_center(self) -> Tuple[float, float]:
        """Get canvas center point."""
    
    # Document management
    def update_metadata(self, **kwargs: Any) -> None:
        """Update metadata fields."""
    
    def set_canvas_size(self, width: float, height: float, units: Units = Units.PIXELS) -> None:
        """Set canvas dimensions."""
    
    # Layer operations
    def create_layer(self, name: str, **kwargs: Any) -> Layer:
        """Create new layer."""
    
    def create_layer_group(self, name: str, **kwargs: Any) -> LayerGroup:
        """Create new layer group."""
    
    # Utility methods
    def get_document_info(self) -> Dict[str, Any]:
        """Get document summary."""
    
    def validate_document(self) -> Dict[str, List[str]]:
        """Validate document integrity."""
    
    def cleanup_empty_layers(self) -> int:
        """Remove empty layers."""
    
    def duplicate(self, new_title: Optional[str] = None) -> 'DrawingDocument':
        """Create document copy."""
    
    # Factory methods
    @classmethod
    def create_new(
        cls,
        title: str = "New Document",
        width: float = 800.0,
        height: float = 600.0,
        units: Units = Units.PIXELS,
        author: Optional[str] = None
    ) -> 'DrawingDocument':
        """Create new document with defaults."""
    
    @classmethod
    def create_preset(cls, preset: str, **kwargs: Any) -> 'DrawingDocument':
        """Create document with preset dimensions."""
```

### Document Presets

Available presets for `create_preset()`:

- **web**: 1920x1080px (HD web graphics)
- **web_4k**: 3840x2160px (4K web graphics)
- **mobile**: 375x667px (mobile screen)
- **tablet**: 768x1024px (tablet screen)
- **print_letter**: 8.5x11 inches (US letter)
- **print_a4**: 210x297mm (A4 paper)
- **print_a3**: 297x420mm (A3 paper)
- **social_instagram**: 1080x1080px (Instagram post)
- **social_facebook**: 1200x630px (Facebook post)
- **social_twitter**: 1024x512px (Twitter header)

## Usage Examples

### Creating a Document

```python
from drawing_lib import DrawingDocument, Units

# Create with defaults
doc = DrawingDocument.create_new(title="My Drawing")

# Create with preset
doc = DrawingDocument.create_preset("web", title="Web Graphics")

# Create with custom dimensions
doc = DrawingDocument.create_new(
    title="Custom Document",
    width=1200.0,
    height=800.0,
    units=Units.PIXELS,
    author="Artist Name"
)
```

### Creating Shapes

```python
from drawing_lib import (
    Shape, ShapeType, RGBColor, FillProperties, 
    StrokeProperties, StyleProperties, Transform
)

# Define styling
fill = FillProperties(color=RGBColor(r=255, g=100, b=50))
stroke = StrokeProperties(color=RGBColor(r=0, g=0, b=0), width=2.0)
style = StyleProperties(fill=fill, stroke=stroke)

# Create rectangle
rectangle = Shape(
    type=ShapeType.RECTANGLE,
    geometry={"width": 100.0, "height": 60.0, "corner_radius": 5.0},
    style=style,
    transform=Transform(x=50.0, y=50.0),
    name="My Rectangle"
)

# Create circle
circle = Shape(
    type=ShapeType.CIRCLE,
    geometry={"radius": 25.0},
    style=StyleProperties(fill=FillProperties(color=RGBColor(r=50, g=150, b=255))),
    transform=Transform(x=200.0, y=100.0)
)
```

### Layer Management

```python
# Create layers
background = doc.create_layer("Background")
content = doc.create_layer("Content")

# Create layer group
ui_group = doc.create_layer_group("UI Elements")
buttons = doc.create_layer("Buttons", parent_group=ui_group)

# Add shapes to layers
background.add_shape(rectangle)
content.add_shape(circle)

# Layer operations
content.visible = False  # Hide layer
doc.layer_manager.set_active_layer(content.id)
```

### Serialization

```python
# Save to JSON
json_data = doc.model_dump_json(indent=2)
with open("document.json", "w") as f:
    f.write(json_data)

# Load from JSON
with open("document.json", "r") as f:
    json_data = f.read()
loaded_doc = DrawingDocument.model_validate_json(json_data)
```

## Error Handling

The library uses custom exceptions for validation:

```python
from drawing_lib.types import InvalidGeometryError

try:
    shape = Shape(
        type=ShapeType.RECTANGLE,
        geometry={"width": -10.0, "height": 50.0}  # Invalid negative width
    )
except InvalidGeometryError as e:
    print(f"Geometry error: {e}")
```

## Type Safety

The library is fully typed and works with mypy:

```bash
mypy your_drawing_script.py
```

All models use Pydantic validation for runtime type checking and data validation.

## Performance Considerations

- **Shape Creation**: O(1) for individual shapes, O(n) for batch operations
- **Layer Operations**: O(1) for direct access, O(n) for searches
- **Serialization**: Linear with document size
- **Memory Usage**: Approximately 1KB per shape for complex documents

See `performance.md` for detailed benchmarks and optimization guidelines.