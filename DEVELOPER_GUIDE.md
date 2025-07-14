# Developer Guide

## Overview

This guide provides detailed information for developers working with or contributing to the Drawing Library. It covers architecture decisions, development practices, and implementation details.

## Development Environment Setup

### Prerequisites

- Python 3.12+
- pip or poetry for dependency management
- Git for version control

### Setup Steps

```bash
# Clone repository
git clone <repository-url>
cd drawing-library

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov mypy black isort flake8

# Verify installation
python -c "import drawing_lib; print('Installation successful')"
```

### IDE Configuration

#### VS Code

Recommended extensions:
- Python
- Pylance
- Python Docstring Generator
- Pydantic

Settings (`.vscode/settings.json`):
```json
{
    "python.linting.enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "python.analysis.typeCheckingMode": "strict"
}
```

#### PyCharm

Configuration:
- Enable mypy in Settings → Tools → Python Integrated Tools
- Set Black as code formatter
- Configure isort for import sorting

## Architecture Overview

### Design Principles

1. **Type Safety**: All code is fully typed with mypy compatibility
2. **Validation**: Runtime validation using Pydantic
3. **Immutability**: Prefer immutable operations where possible
4. **Separation of Concerns**: Clear module boundaries
5. **Performance**: Optimized for common operations
6. **Extensibility**: Easy to add new shape types and features

### Module Architecture

```
drawing_lib/
├── __init__.py          # Public API exports
├── types.py             # Core types, enums, exceptions
├── styles.py            # Color and styling system
├── shapes.py            # Shape definitions and geometry
├── layers.py            # Layer hierarchy management  
├── document.py          # Document model and operations
└── utils.py             # Utility functions (if needed)
```

### Dependency Graph

```
document.py
    ├── layers.py
    │   └── shapes.py
    │       ├── styles.py
    │       └── types.py
    └── types.py
```

### Core Concepts

#### Pydantic Integration

All models inherit from `BaseModel`:

```python
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    field: str = Field(..., description="Required field")
    optional: Optional[int] = None
    
    def custom_method(self) -> str:
        return f"Value: {self.field}"
```

#### ID Management

Uses string-based UUIDs for performance:

```python
from typing import TypeAlias
from uuid import uuid4

ID: TypeAlias = str

def generate_id() -> ID:
    return str(uuid4())
```

#### Geometry Validation

Shape-specific validation in the `Shape` model:

```python
@model_validator(mode='after')
def validate_geometry(self) -> 'Shape':
    if self.type == ShapeType.RECTANGLE:
        self._validate_rectangle_geometry(self.geometry)
    # ... other shape types
    return self
```

## Code Organization

### File Structure Best Practices

#### Module Level (`__init__.py`)

Export only public API:

```python
# Good
from .document import DrawingDocument
from .shapes import Shape, ShapeType
from .styles import RGBColor, StyleProperties

# Avoid
from .internal_utils import _private_function
```

#### Class Organization

Standard order within classes:

```python
class ExampleClass(BaseModel):
    # 1. Class variables
    DEFAULT_VALUE: ClassVar[str] = "default"
    
    # 2. Fields (Pydantic)
    id: ID = Field(default_factory=generate_id)
    name: str
    
    # 3. Validators
    @model_validator(mode='after')
    def validate_data(self) -> 'ExampleClass':
        return self
    
    # 4. Properties
    @property
    def computed_value(self) -> str:
        return f"computed_{self.name}"
    
    # 5. Public methods
    def public_method(self) -> None:
        pass
    
    # 6. Private methods
    def _private_method(self) -> None:
        pass
    
    # 7. Class methods
    @classmethod
    def create_default(cls) -> 'ExampleClass':
        return cls(name="default")
```

### Naming Conventions

#### Variables and Functions
- `snake_case` for variables, functions, and methods
- `UPPER_CASE` for constants
- `_private` prefix for internal methods

#### Classes and Types
- `PascalCase` for classes
- `PascalCase` for type aliases
- Descriptive names over abbreviations

#### Files and Modules
- `snake_case` for file names
- Singular nouns for modules (e.g., `shape.py` not `shapes.py` unless it's a collection)

## Development Workflow

### Testing Strategy

#### Test Organization

```
tests/
├── __init__.py
├── test_types.py          # Core types and utilities
├── test_styles.py         # Color and styling system
├── test_shapes.py         # Shape creation and validation
├── test_layers.py         # Layer management
├── test_document.py       # Document operations
├── test_benchmarks.py     # Performance tests
└── test_integration.py    # End-to-end tests
```

#### Test Categories

1. **Unit Tests**: Individual component testing
2. **Integration Tests**: Component interaction testing
3. **Performance Tests**: Benchmark critical operations
4. **Validation Tests**: Error handling and edge cases

#### Writing Tests

```python
import pytest
from drawing_lib import Shape, ShapeType

class TestShapeCreation:
    """Test shape creation and validation."""
    
    def test_valid_rectangle_creation(self):
        """Test creating a valid rectangle."""
        shape = Shape(
            type=ShapeType.RECTANGLE,
            geometry={"width": 100.0, "height": 50.0}
        )
        assert shape.type == ShapeType.RECTANGLE
        assert shape.geometry["width"] == 100.0
    
    def test_invalid_rectangle_geometry(self):
        """Test validation of invalid rectangle geometry."""
        with pytest.raises(ValueError):
            Shape(
                type=ShapeType.RECTANGLE,
                geometry={"width": -10.0, "height": 50.0}
            )
    
    @pytest.mark.parametrize("width,height", [
        (100.0, 50.0),
        (1.0, 1.0),
        (1000.0, 2000.0)
    ])
    def test_rectangle_dimensions(self, width: float, height: float):
        """Test various rectangle dimensions."""
        shape = Shape(
            type=ShapeType.RECTANGLE,
            geometry={"width": width, "height": height}
        )
        assert shape.geometry["width"] == width
        assert shape.geometry["height"] == height
```

### Code Quality Tools

#### Type Checking with mypy

Configuration in `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

Run type checking:
```bash
mypy drawing_lib/
```

#### Code Formatting with Black

Configuration in `pyproject.toml`:

```toml
[tool.black]
line-length = 88
target-version = ['py312']
include = '\.pyi?$'
```

Format code:
```bash
black drawing_lib/ tests/
```

#### Import Sorting with isort

Configuration in `pyproject.toml`:

```toml
[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
```

Sort imports:
```bash
isort drawing_lib/ tests/
```

#### Linting with flake8

Configuration in `.flake8`:

```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = venv, __pycache__
```

Run linter:
```bash
flake8 drawing_lib/ tests/
```

### Git Workflow

#### Commit Message Format

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

Examples:
```
feat(shapes): add ellipse shape support
fix(layers): resolve z-index sorting issue
docs(api): update Shape class documentation
```

#### Branch Strategy

- `main`: Production-ready code
- `develop`: Integration branch
- `feature/feature-name`: Feature development
- `fix/issue-description`: Bug fixes
- `docs/documentation-update`: Documentation changes

## Performance Considerations

### Profiling

Use cProfile for performance analysis:

```python
import cProfile
import pstats

def profile_shape_creation():
    # Your code here
    pass

if __name__ == "__main__":
    cProfile.run('profile_shape_creation()', 'profile_stats')
    stats = pstats.Stats('profile_stats')
    stats.sort_stats('cumulative')
    stats.print_stats(10)
```

### Memory Management

#### Efficient Data Structures

- Use `__slots__` for performance-critical classes
- Prefer generators over lists for large datasets
- Use weak references to avoid circular dependencies

#### Example Optimization

```python
from __future__ import annotations
from typing import Optional

class OptimizedShape:
    __slots__ = ('_id', '_type', '_geometry', '_transform')
    
    def __init__(self, shape_type: ShapeType, geometry: dict):
        self._id = generate_id()
        self._type = shape_type
        self._geometry = geometry
        self._transform: Optional[Transform] = None
```

### Benchmark Guidelines

Write benchmarks for:
- Shape creation and modification
- Layer operations
- Document serialization
- Large dataset operations

Example benchmark:

```python
import pytest

class TestPerformance:
    @pytest.mark.benchmark(group="creation")
    def test_shape_creation_performance(self, benchmark):
        def create_shapes():
            return [
                Shape(type=ShapeType.RECTANGLE, 
                      geometry={"width": 100, "height": 50})
                for _ in range(1000)
            ]
        
        shapes = benchmark(create_shapes)
        assert len(shapes) == 1000
```

## Extension Guidelines

### Adding New Shape Types

1. **Update ShapeType enum** in `types.py`:
```python
class ShapeType(str, Enum):
    # Existing types...
    NEW_SHAPE = "new_shape"
```

2. **Add geometry validation** in `shapes.py`:
```python
def _validate_new_shape_geometry(self, geometry: Dict[str, Any]) -> None:
    required_fields = ["required_param"]
    for field in required_fields:
        if field not in geometry:
            raise InvalidGeometryError(f"New shape requires {field}")
    
    # Validate parameter values
    if geometry["required_param"] <= 0:
        raise InvalidGeometryError("Required param must be positive")
```

3. **Update shape validator**:
```python
@model_validator(mode='after')
def validate_geometry(self) -> 'Shape':
    # Existing validations...
    elif self.type == ShapeType.NEW_SHAPE:
        self._validate_new_shape_geometry(self.geometry)
    return self
```

4. **Add tests**:
```python
def test_new_shape_creation(self):
    shape = Shape(
        type=ShapeType.NEW_SHAPE,
        geometry={"required_param": 10.0}
    )
    assert shape.type == ShapeType.NEW_SHAPE
```

5. **Update documentation** in API reference and examples.

### Adding New Color Types

Follow similar pattern in `styles.py`:

```python
class NewColorType(BaseModel):
    # Color-specific fields
    
    def to_rgb(self) -> RGBColor:
        """Convert to RGB representation."""
        # Implementation
        pass

# Update Color union type
Color = Union[RGBColor, HSLColor, NewColorType]
```

## Common Patterns

### Error Handling

```python
from drawing_lib.types import InvalidGeometryError

try:
    shape = Shape(type=ShapeType.RECTANGLE, geometry=invalid_geometry)
except InvalidGeometryError as e:
    logger.error(f"Shape creation failed: {e}")
    # Handle error appropriately
```

### Optional Parameters

```python
def create_styled_shape(
    shape_type: ShapeType,
    geometry: Dict[str, Any],
    fill_color: Optional[RGBColor] = None,
    stroke_width: float = 1.0
) -> Shape:
    style = None
    if fill_color:
        fill = FillProperties(color=fill_color)
        style = StyleProperties(fill=fill)
    
    return Shape(type=shape_type, geometry=geometry, style=style)
```

### Factory Methods

```python
class Shape(BaseModel):
    @classmethod
    def create_rectangle(
        cls, 
        width: float, 
        height: float, 
        x: float = 0, 
        y: float = 0
    ) -> 'Shape':
        return cls(
            type=ShapeType.RECTANGLE,
            geometry={"width": width, "height": height},
            transform=Transform(x=x, y=y)
        )
```

## Debugging

### Common Issues

1. **Validation Errors**: Check field types and constraints
2. **Import Errors**: Verify module structure and circular imports
3. **Performance Issues**: Profile and benchmark critical paths
4. **Type Errors**: Run mypy and fix type annotations

### Debugging Tools

```python
# Enable Pydantic debugging
import os
os.environ['PYDANTIC_DEBUG'] = '1'

# Add debug prints in validators
@model_validator(mode='after')
def debug_validator(self) -> 'Shape':
    print(f"Validating shape: {self.type}, geometry: {self.geometry}")
    return self
```

### Testing Edge Cases

Always test:
- Boundary values (0, negative numbers, very large numbers)
- Empty collections and None values
- Invalid enum values
- Circular references
- Memory-intensive operations

## Contributing Guidelines

### Pull Request Process

1. **Fork and branch** from `develop`
2. **Write tests** for new functionality
3. **Update documentation** for API changes
4. **Run full test suite** and ensure all pass
5. **Check code quality** with mypy, black, isort, flake8
6. **Submit PR** with clear description and test evidence

### Code Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests cover new functionality
- [ ] Documentation is updated
- [ ] Performance impact is acceptable
- [ ] No breaking changes (or properly documented)
- [ ] Error handling is appropriate
- [ ] Type annotations are complete

## Resources

### Documentation
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [pytest Documentation](https://docs.pytest.org/)

### Tools
- [mypy](http://mypy-lang.org/)
- [Black](https://black.readthedocs.io/)
- [isort](https://isort.readthedocs.io/)
- [flake8](https://flake8.pycqa.org/)

### Best Practices
- [Python Code Style Guide (PEP 8)](https://peps.python.org/pep-0008/)
- [Type Hints (PEP 484)](https://peps.python.org/pep-0484/)
- [Pydantic Best Practices](https://docs.pydantic.dev/latest/concepts/performance/)

---

This developer guide is a living document. Update it as the project evolves and new patterns emerge.