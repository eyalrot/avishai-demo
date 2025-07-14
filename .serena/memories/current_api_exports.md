# Drawing Library API Exports

## Complete Public API
The drawing library exports all major components through `drawing_lib.__init__.py`:

```python
from drawing_lib import (
    # Core Types and Enums
    ShapeType, BlendMode, LineCap, LineJoin, FillType, Units,
    
    # Color Models  
    RGBColor, RGBAColor, HSLColor, HexColor,
    
    # Gradients and Advanced Styling
    LinearGradient, RadialGradient, PatternFill,
    FillProperties, StrokeProperties, Effects,
    
    # Shape System
    Shape, Transform, StyleProperties,
    
    # Layer Management
    Layer, LayerGroup, LayerManager,
    
    # Document System
    CanvasSize, BackgroundProperties, DocumentMetadata, 
    ViewSettings, ExportSettings, DrawingDocument
)
```

## Usage Examples

### Basic Shape Creation
```python
from drawing_lib import Shape, ShapeType, RGBColor, FillProperties, StyleProperties

# Create styled shape
fill = FillProperties(color=RGBColor(r=255, g=128, b=64))
style = StyleProperties(fill=fill)
shape = Shape(
    type=ShapeType.RECTANGLE,
    geometry={'width': 100.0, 'height': 50.0, 'corner_radius': 5.0},
    style=style,
    name='Orange Rectangle'
)
```

### Document Creation
```python
from drawing_lib import DrawingDocument

# Create new document
doc = DrawingDocument.create_new(
    title='My Drawing',
    width=1920.0,
    height=1080.0,
    author='Artist Name'
)

# Or use preset
web_doc = DrawingDocument.create_preset('web', title='Web Design')
a4_doc = DrawingDocument.create_preset('print_a4', title='Print Design')
```

### Layer Management
```python
# Create layers
bg_layer = doc.create_layer('Background')
content_layer = doc.create_layer('Content')
ui_group = doc.create_layer_group('UI Elements')

# Add shapes to layers
bg_layer.add_shape(shape)
```

### JSON Serialization
```python
# Serialize to JSON
json_str = doc.model_dump_json()

# Deserialize from JSON
doc2 = DrawingDocument.model_validate_json(json_str)
```

## All Components Ready
Every component is fully implemented, tested, and ready for production use.