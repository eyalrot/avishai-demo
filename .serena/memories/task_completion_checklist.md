# Task Completion Checklist

When completing any development task, always run these commands in order:

## 1. Type Checking
```bash
source venv/bin/activate
python -m mypy drawing_lib/ --strict
```
**Expected result**: "Success: no issues found in X source files"

## 2. Run Test Suite
```bash
python -m pytest tests/ -v
```
**Expected result**: All tests should pass (currently 28 tests)

## 3. Import Validation
```bash
python -c "import drawing_lib; print('Module imported successfully')"
```
**Expected result**: No import errors

## 4. Code Quality Checks
- Ensure all new code has proper type hints
- Verify docstrings are present for public APIs
- Check that Pydantic Field constraints are appropriate
- Validate error handling with custom exceptions

## 5. Test Coverage
- Add tests for any new functionality
- Test both valid and invalid inputs
- Follow existing test patterns (class-based organization)
- Use descriptive test method names

## Performance Considerations
- For large changes, consider running benchmarks
- Ensure string IDs are used for better JSON performance
- Validate that the code can handle 10k+ shapes efficiently

## Git Workflow
- Only commit after all checks pass
- Use descriptive commit messages
- Consider the component-based design impact on changes