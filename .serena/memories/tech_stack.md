# Technology Stack

## Core Dependencies
- **Python 3.12** - Primary language, strict version requirement
- **Pydantic ≥2.0.0** - Data validation and serialization
- **pytest ≥7.0.0** - Testing framework
- **pytest-benchmark ≥4.0.0** - Performance benchmarking
- **mypy ≥1.0.0** - Static type checking

## Development Environment
- **Virtual environment**: Using `venv` module (required)
- **Type checking**: mypy in strict mode
- **Testing**: pytest with comprehensive configuration
- **Package structure**: Standard Python package with drawing_lib/ and tests/

## Project Structure
```
drawing_lib/          # Main package
├── __init__.py      # Package initialization with version
├── types.py         # Core enums and type definitions
└── styles.py        # Styling system (colors, gradients, effects)

tests/               # Test suite
├── test_setup.py    # Basic setup tests
├── test_types.py    # Type system tests
└── test_styles.py   # Styling system tests
```