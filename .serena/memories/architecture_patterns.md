# Architecture and Design Patterns

## Component-Based Design
The project follows a **component-based architecture** as specified in the PRD:

### Core Pattern
- Single `Shape` model with `type: ShapeType` enum field
- `geometry: Dict[str, Any]` for flexible shape-specific data storage
- Validation of geometry data based on shape type using `@root_validator`
- Example: Rectangle needs `{width, height}`, Circle needs `{radius}`

### Current Implementation Status
- ✅ **Type System** (`drawing_lib/types.py`) - Enums for ShapeType, BlendMode, LineCap, LineJoin, FillType, Units
- ✅ **Styling System** (`drawing_lib/styles.py`) - Color models, gradients, fills, strokes, effects
- 🚧 **Shape Models** - Not yet implemented
- 🚧 **Layer System** - Not yet implemented  
- 🚧 **Transform System** - Not yet implemented
- 🚧 **Drawing Document** - Not yet implemented

## Validation Strategy
- **Pydantic Field constraints** for basic validation (ranges, types)
- **Custom validators** using `@root_validator` for complex logic
- **Type safety** through comprehensive type hints and mypy strict mode
- **Error hierarchy** with custom exception classes

## Performance Design
- **String IDs** preferred over UUID objects for better JSON performance
- **Dict-based geometry** for flexible shape data without excessive inheritance
- **Efficient serialization** through Pydantic's built-in JSON support
- **Target**: Handle 10k+ shapes efficiently

## Key Principles
1. **Flexibility**: Component-based approach allows adding new shape types easily
2. **Type Safety**: Full type coverage prevents runtime errors
3. **Validation**: Comprehensive data validation at model boundaries
4. **Performance**: Designed for large-scale drawing applications
5. **Extensibility**: Clear patterns for adding new features