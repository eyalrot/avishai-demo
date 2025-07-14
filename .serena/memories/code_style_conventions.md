# Code Style and Conventions

## Type Hints
- **Full type hints required** - All functions and methods must have type annotations
- **Python 3.12 features** - Leveraging modern Union syntax (X | Y) and generic syntax
- **Strict mypy compliance** - All code must pass mypy strict mode

## Documentation
- **Comprehensive docstrings** - All classes and public methods have detailed docstrings
- **Google-style docstrings** - Clear, consistent documentation format
- **Type annotations in docstrings** - Parameters and return types documented

## Pydantic Patterns
- **Field constraints** - Using `Field(..., ge=0, le=255)` for validation
- **Descriptive field names** - Clear, self-documenting field descriptions
- **Custom validators** - Using `@root_validator` for complex validation logic
- **Model methods** - Helper methods like `to_hex()`, `to_tuple()` for conversions

## Testing Patterns
- **Class-based test organization** - Tests grouped by functionality (TestColorModels, TestGradients)
- **Descriptive test names** - Clear test method names describing what's being tested
- **Type hints in tests** - All test methods have `-> None` return type annotation
- **Comprehensive validation testing** - Both valid and invalid inputs tested

## Error Handling
- **Custom exceptions** - Domain-specific exception hierarchy
- **Validation errors** - Meaningful error messages for invalid data
- **Type safety** - Preventing runtime type errors through static checking