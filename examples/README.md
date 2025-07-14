# Drawing Library Examples

This directory contains comprehensive examples demonstrating the capabilities of the drawing library. Each example showcases different aspects of the library and can serve as both learning materials and starting points for your own projects.

## Examples Overview

### 1. Basic Shapes (`basic_shapes.py`)

**Purpose**: Introduction to fundamental drawing operations
**Demonstrates**:
- Creating basic geometric shapes (rectangles, circles, triangles, lines, ellipses, paths)
- Applying fills, strokes, and styling
- Working with layers and transforms
- Document serialization and loading
- Layer visibility and management

**Key Features**:
- Mixed shape types with different styling
- Layer organization and z-ordering
- Transform positioning
- JSON serialization round-trip
- Document validation

**Run the example**:
```bash
cd examples
python basic_shapes.py
```

### 2. Logo Design (`logo_design.py`)

**Purpose**: Professional graphic design workflow
**Demonstrates**:
- Complex multi-layer compositions
- Layer groups and hierarchical organization
- Brand color management
- Geometric logo construction
- High-resolution output preparation

**Key Features**:
- Corporate branding elements
- Layer groups for organization
- Print-quality resolution (300 DPI)
- Professional color schemes
- Geometric shape combinations

**Run the example**:
```bash
cd examples
python logo_design.py
```

### 3. Data Visualization (`data_visualization.py`)

**Purpose**: Charts and data presentation
**Demonstrates**:
- Bar charts with dynamic scaling
- Line charts with data points
- Pie charts with percentage distribution
- Grid systems and backgrounds
- Dashboard layouts

**Key Features**:
- Multiple chart types in one document
- Data-driven shape generation
- Grid backgrounds and axes
- Color-coded data series
- Responsive scaling

**Run the example**:
```bash
cd examples
python data_visualization.py
```

## SVG Export Module (`svg_export.py`)

**Purpose**: External SVG export functionality
**Features**:
- Converts drawing library documents to standard SVG format
- Preserves layers, transforms, and styling
- Supports all shape types (rectangles, circles, ellipses, lines, polygons, paths)
- Maintains proper coordinate systems and viewports
- Generates clean, readable SVG code

**Key Features**:
- **Layer Support**: Each layer becomes an SVG group with proper naming
- **Transform Preservation**: All shape transforms (translation, rotation, scale) are maintained
- **Style Conversion**: Fill and stroke properties are converted to SVG attributes
- **Viewport Management**: Automatic canvas size and viewBox setup
- **Clean Output**: Properly formatted XML with indentation

**Usage**:
```python
from svg_export import export_document_to_svg

# Export document to SVG file
svg_content = export_document_to_svg(document, "output.svg")

# Or use the class directly for more control
from svg_export import SVGExporter
exporter = SVGExporter(document)
svg_content = exporter.generate_svg_content(include_invisible=False)
```

## Common Patterns Demonstrated

### Document Creation

All examples show different approaches to document creation:

```python
# Basic document
doc = DrawingDocument.create_new(title="My Document")

# Preset-based document
doc = DrawingDocument.create_preset("web", title="Web Graphics")

# Custom dimensions
doc.set_canvas_size(1920.0, 1080.0, Units.PIXELS)
```

### Layer Management

Examples demonstrate hierarchical layer organization:

```python
# Create layers
background_layer = doc.create_layer("Background")
content_layer = doc.create_layer("Content")

# Create layer groups
group = doc.create_layer_group("UI Elements")
ui_layer = doc.create_layer("Buttons", parent_group=group)
```

### Shape Creation and Styling

Consistent patterns for shape creation:

```python
# Define styling
fill = FillProperties(color=RGBColor(r=255, g=100, b=50))
stroke = StrokeProperties(color=RGBColor(r=0, g=0, b=0), width=2.0)
style = StyleProperties(fill=fill, stroke=stroke)

# Create shape with transform
shape = Shape(
    type=ShapeType.RECTANGLE,
    geometry={"width": 100.0, "height": 60.0},
    style=style,
    transform=Transform(x=50.0, y=50.0),
    name="My Rectangle"
)

# Add to layer
layer.add_shape(shape)
```

### Serialization and Export Workflow

All examples demonstrate save/load operations and SVG export:

```python
# Serialize to JSON
json_data = doc.model_dump_json(indent=2)

# Save to file
with open("output.json", "w") as f:
    f.write(json_data)

# Load from JSON
loaded_doc = DrawingDocument.model_validate_json(json_data)

# Export to SVG
from svg_export import export_document_to_svg
svg_content = export_document_to_svg(doc, "output.svg")
```

## Generated Output Files

Each example generates both JSON and SVG output files:

**JSON Files** (complete document structure):
- `basic_shapes_output.json` - Simple shapes demonstration
- `logo_design_output.json` - Corporate logo with layers
- `data_visualization_output.json` - Multi-chart dashboard

**SVG Files** (vector graphics):
- `basic_shapes_output.svg` - Rendered basic shapes
- `logo_design_output.svg` - High-resolution logo design
- `data_visualization_output.svg` - Interactive charts

The JSON files contain the complete document structure and can be loaded back into the library for further editing. The SVG files are standard vector graphics that can be opened in web browsers, graphic design software, or embedded in web applications.

## Performance Insights

The examples are designed to showcase different performance characteristics:

- **Basic Shapes**: ~20-30 shapes, demonstrating efficient small-scale operations
- **Logo Design**: ~50-70 shapes, showing complex hierarchical structures
- **Data Visualization**: ~100+ shapes, demonstrating data-driven generation

## Customization

Each example can be easily modified:

1. **Change Colors**: Modify the color definitions at the beginning of each example
2. **Adjust Data**: Update the sample datasets in data visualization
3. **Modify Layout**: Change positioning and sizing parameters
4. **Add Shapes**: Extend examples with additional geometric elements

## Best Practices Demonstrated

1. **Layer Organization**: Logical grouping of related elements
2. **Color Management**: Consistent color schemes and brand guidelines
3. **Naming Conventions**: Descriptive names for shapes and layers
4. **Transform Usage**: Proper positioning with transform objects
5. **Validation**: Document integrity checking before output
6. **Performance**: Efficient shape creation and memory usage

## Integration Examples

These examples can serve as starting points for:

- **Web Applications**: Using the JSON output in web-based editors
- **Design Tools**: Building drawing application interfaces
- **Data Dashboards**: Creating dynamic visualization systems
- **Print Workflows**: Generating high-resolution graphics
- **Automation**: Batch processing of design templates

## Next Steps

After exploring these examples, consider:

1. Combining techniques from multiple examples
2. Building interactive editing applications
3. Creating custom shape types and behaviors
4. Implementing export to other formats (SVG, PNG, etc.)
5. Building template systems for repeated designs

Each example is self-contained and includes comprehensive error handling and validation, making them suitable for both learning and production use.