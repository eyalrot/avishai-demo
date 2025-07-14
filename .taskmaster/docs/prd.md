# Drawing Application Data Model - Product Requirements Document

## Overview
Design a Python module using Pydantic for a drawing application's data model that supports basic shapes and layers with a focus on flexibility and extensibility.

## Core Requirements

### 1. Data Model Architecture
- Use **component-based design** (Approach 2) for maximum flexibility
- All models must use Pydantic for validation and serialization
- Support JSON serialization/deserialization out of the box

### 2. Shapes Support
Must support at minimum:
- Rectangle, Circle, Ellipse
- Line, Polyline, Polygon
- Path (for complex curves)
- Group (for shape collections)

**Implementation Hints for Component-Based Approach**:
- Single `Shape` model with `type: ShapeType` enum field
- `geometry: Dict[str, Any]` for flexible shape-specific data storage
- Validate geometry data based on shape type using `@root_validator`
- Example: Rectangle needs `{width, height}`, Circle needs `{radius}`

### 3. Styling System
- Fill properties (solid color, gradients, patterns)
- Stroke properties (color, width, dash patterns, line caps/joins)
- Opacity and blend modes
- Shadow and blur effects

### 4. Layer Management
- Multiple layers with z-ordering
- Layer visibility and locking
- Layer opacity and blend modes
- Layer groups/folders support

### 5. Transform System
- Position (x, y)
- Rotation
- Scale (uniform and non-uniform)
- Skew transformations

### 6. Drawing Document
- Canvas size and units
- Background properties
- Metadata (creation date, modification date, author)
- Version information for backwards compatibility

## Technical Requirements

### Development Environment
- **Python Version**: 3.12 only
- **Virtual Environment**: Required (use `venv` module)
- Setup instructions must include:
  ```bash
  python3.12 -m venv .venv
  source .venv/bin/activate  # or .venv\Scripts\activate on Windows
  pip install -r requirements.txt
  ```

### Testing Requirements
- Unit tests using `pytest`
- Minimum 80% code coverage
- Test categories:
  - Model validation tests
  - Serialization/deserialization tests
  - Edge cases and error handling
  - Performance tests for large datasets

### Performance Benchmarks
Generate performance benchmark reports using `pytest-benchmark` for the following scenarios:

| Operation | Object Counts to Test |
|-----------|----------------------|
| Insert (add to layer) | 1,000 / 10,000 / 100,000 |
| Save (to JSON) | 1,000 / 10,000 / 100,000 |
| Load (from JSON) | 1,000 / 10,000 / 100,000 |

**Benchmark Implementation Requirements**:
- Use `pytest-benchmark` for consistent measurements
- Test with mixed shape types (rectangles, circles, polygons)
- Measure both time and memory usage
- Generate detailed performance reports with statistics
- Export benchmark results in JSON/HTML format for tracking

### Component-Based Design Guidelines
```python
# Example structure hint:
class Shape(BaseModel):
    id: str
    type: ShapeType
    geometry: Dict[str, Any]  # Validated based on type
    style: StyleProperties
    transform: Transform
    
    @root_validator
    def validate_geometry(cls, values):
        # Validate geometry data matches shape type requirements
        pass
```

## Additional Considerations

### Performance
- Design for documents with 10k+ shapes
- Consider using string IDs over UUID objects for better JSON performance

### Validation
- Use Pydantic's `Field` constraints effectively
- Custom validators for complex geometric constraints
- Ensure data consistency across references

### Project Structure
```
drawing_lib/
├── __init__.py
├── models/
│   ├── shapes.py
│   ├── styles.py
│   ├── layers.py
│   └── drawing.py
├── validators/
├── tests/
│   ├── test_shapes.py
│   ├── test_layers.py
│   └── test_drawing.py
└── requirements.txt
```

## Success Criteria
- Clean, intuitive API
- Full type hints leveraging Python 3.12 features
- Comprehensive test suite with pytest
- No runtime type errors when used with mypy strict mode