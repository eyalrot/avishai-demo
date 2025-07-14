# Drawing Library

A comprehensive Python library for creating, manipulating, and exporting vector graphics with full type safety and robust validation.

## Features

🎨 **Complete Shape System**
- Rectangles, circles, ellipses, lines, polygons, and paths
- Advanced styling with fills, strokes, and effects
- Transform support (translation, rotation, scaling)

📐 **Layer Management** 
- Hierarchical layer organization with groups
- Z-ordering and visibility controls
- Blend modes and opacity

🎯 **Type Safety**
- Built on Pydantic for runtime validation
- Full mypy compatibility
- Comprehensive error handling

📊 **Multiple Export Formats**
- JSON serialization for document persistence
- SVG export for web and print
- High-performance benchmarking

📚 **Rich Documentation**
- Complete API reference
- Practical examples
- Performance guidelines

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd drawing-library

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest
```

### Basic Usage

```python
from drawing_lib import (
    DrawingDocument, Shape, ShapeType,
    RGBColor, FillProperties, StyleProperties,
    Transform
)

# Create a document
doc = DrawingDocument.create_preset("web", title="My Drawing")

# Create a styled shape
fill = FillProperties(color=RGBColor(r=255, g=100, b=50))
style = StyleProperties(fill=fill)

rectangle = Shape(
    type=ShapeType.RECTANGLE,
    geometry={"width": 200.0, "height": 120.0},
    style=style,
    transform=Transform(x=100.0, y=100.0)
)

# Add to document
layer = doc.create_layer("Main Layer")
layer.add_shape(rectangle)

# Save as JSON
with open("my_drawing.json", "w") as f:
    f.write(doc.model_dump_json(indent=2))

# Export as SVG
from examples.svg_export import export_document_to_svg
export_document_to_svg(doc, "my_drawing.svg")
```

## Examples

The `examples/` directory contains comprehensive demonstrations:

- **`basic_shapes.py`** - Fundamental shape creation and styling
- **`logo_design.py`** - Professional logo design workflow  
- **`data_visualization.py`** - Charts and data presentation
- **`svg_export.py`** - SVG export functionality

Run any example:
```bash
cd examples
python basic_shapes.py
```

## Documentation

- **[API Reference](API_REFERENCE.md)** - Complete class and method documentation
- **[Examples Guide](examples/README.md)** - Detailed example walkthrough
- **[Performance Report](performance.md)** - Benchmarks and optimization guide

## Architecture

### Core Modules

```
drawing_lib/
├── types.py          # Core types, enums, and utilities
├── styles.py         # Color and styling system
├── shapes.py         # Shape definitions and validation
├── layers.py         # Layer management and hierarchy
└── document.py       # Document model and operations
```

### Key Components

- **Shape System**: Unified shape model with type-specific geometry validation
- **Layer Management**: Hierarchical organization with groups and z-ordering
- **Styling**: Comprehensive fill, stroke, and effect properties
- **Transform System**: 2D transformations with matrix operations
- **Document Model**: Complete drawing document with metadata and settings

## Performance

The library is optimized for production use:

- **Insertion**: 1,000 shapes in ~1 second
- **Serialization**: 2,000 shapes to JSON in ~25ms
- **Memory**: ~1KB per complex shape
- **Validation**: Runtime type checking with Pydantic

See [performance.md](performance.md) for detailed benchmarks.

## Development

### Project Structure

```
├── drawing_lib/           # Main library code
├── tests/                 # Comprehensive test suite
├── examples/              # Example applications
├── performance.md         # Performance benchmarks
├── API_REFERENCE.md       # Complete API documentation
└── requirements.txt       # Dependencies
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=drawing_lib

# Run benchmarks
pytest tests/test_benchmarks.py --benchmark-only

# Type checking
mypy drawing_lib/
```

### Code Quality

The project maintains high code quality standards:

- **Type Safety**: Full mypy compatibility
- **Validation**: Pydantic runtime validation
- **Testing**: 100+ tests with comprehensive coverage
- **Documentation**: Complete API reference and examples
- **Performance**: Benchmarked and optimized

## Use Cases

### Design Applications
- Vector graphics editors
- Logo and brand design tools
- Technical illustration software

### Data Visualization
- Chart and graph generation
- Dashboard creation
- Scientific plotting

### Web Development
- SVG asset generation
- Dynamic graphics creation
- Template-based design systems

### Print and Publishing
- High-resolution graphics
- Multi-format export
- Professional typography

## Roadmap

Future enhancements planned:

- **Advanced Shape Operations**: Union, intersection, difference
- **Additional Export Formats**: PDF, PNG, EPS
- **Animation Support**: Keyframes and transitions
- **Text Rendering**: Advanced typography and layout
- **Performance Optimization**: Batch operations and lazy loading

## Contributing

Contributions are welcome! Please see our contributing guidelines for:

- Code style and standards
- Testing requirements
- Documentation expectations
- Pull request process

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

- **Documentation**: Complete API reference and examples
- **Issues**: GitHub Issues for bug reports and feature requests
- **Examples**: Practical demonstrations in `examples/` directory

---

Built with ❤️ using Python, Pydantic, and modern development practices.