# Suggested Development Commands

## Environment Setup
```bash
# Activate virtual environment (required for all commands)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Development Workflow

### Testing
```bash
# Run all tests
python -m pytest tests/

# Run tests with verbose output
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_styles.py -v

# Run with coverage (if coverage is installed)
python -m pytest tests/ --cov=drawing_lib
```

### Type Checking
```bash
# Run mypy type checking (strict mode)
python -m mypy drawing_lib/ --strict

# Check specific file
python -m mypy drawing_lib/styles.py --strict
```

### Benchmarking
```bash
# Run performance benchmarks (when available)
python -m pytest tests/ --benchmark-only

# Save benchmark results
python -m pytest tests/ --benchmark-json=benchmark_results.json
```

## System Commands (Linux)
- `ls` - List directory contents
- `find` - Search for files
- `grep` - Search file contents  
- `git` - Version control operations
- `cd` - Change directory

## Python Import Testing
```bash
# Test module imports
python -c "import drawing_lib; print('Module imported successfully')"

# Test specific components
python -c "from drawing_lib.types import ShapeType; print('Types imported')"
python -c "from drawing_lib.styles import RGBColor; print('Styles imported')"
```