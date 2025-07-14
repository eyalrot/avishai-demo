"""
Performance benchmarks for the drawing library using pytest-benchmark.

Tests performance of core operations with practical dataset sizes for faster testing:
- Insert (add to layer): 1,000 / 2,000 shapes
- Save (to JSON): 1,000 / 2,000 shapes  
- Load (from JSON): 1,000 / 2,000 shapes

Uses mixed shape types (rectangles, circles, polygons) and measures both time and memory usage.
"""

import pytest
import json
from typing import List

from drawing_lib import (
    DrawingDocument, Shape, ShapeType, Layer,
    RGBColor, FillProperties, StrokeProperties, StyleProperties
)


class TestPerformanceBenchmarks:
    """Performance benchmarks for drawing library operations."""
    
    @pytest.fixture
    def sample_shapes(self) -> List[Shape]:
        """Create a variety of sample shapes for testing."""
        shapes = []
        
        # Rectangle with styling
        rect_fill = FillProperties(color=RGBColor(r=255, g=100, b=50))
        rect_stroke = StrokeProperties(color=RGBColor(r=0, g=0, b=0), width=2.0)
        rect_style = StyleProperties(fill=rect_fill, stroke=rect_stroke)
        
        rectangle = Shape(
            type=ShapeType.RECTANGLE,
            geometry={"width": 100.0, "height": 60.0, "corner_radius": 5.0},
            style=rect_style,
            name="Styled Rectangle"
        )
        shapes.append(rectangle)
        
        # Circle with different styling  
        circle_fill = FillProperties(color=RGBColor(r=50, g=150, b=255))
        circle_style = StyleProperties(fill=circle_fill)
        
        circle = Shape(
            type=ShapeType.CIRCLE,
            geometry={"radius": 30.0},
            style=circle_style,
            name="Blue Circle"
        )
        shapes.append(circle)
        
        # Polygon (triangle)
        triangle = Shape(
            type=ShapeType.POLYGON,
            geometry={"points": [[0.0, 0.0], [50.0, 0.0], [25.0, 43.3]]},
            name="Triangle"
        )
        shapes.append(triangle)
        
        # Line
        line = Shape(
            type=ShapeType.LINE,
            geometry={"x1": 0.0, "y1": 0.0, "x2": 100.0, "y2": 50.0},
            name="Diagonal Line"
        )
        shapes.append(line)
        
        # Ellipse
        ellipse = Shape(
            type=ShapeType.ELLIPSE,
            geometry={"rx": 40.0, "ry": 20.0},
            name="Ellipse"
        )
        shapes.append(ellipse)
        
        return shapes
    
    def create_test_document_with_shapes(self, num_shapes: int, sample_shapes: List[Shape]) -> DrawingDocument:
        """Create a test document with specified number of shapes."""
        doc = DrawingDocument.create_new(
            title=f"Benchmark Document ({num_shapes} shapes)",
            width=2000.0,
            height=2000.0
        )
        
        # Create layers
        main_layer = doc.create_layer("Main Layer")
        
        # Add shapes in cycles through the sample shapes
        for i in range(num_shapes):
            base_shape = sample_shapes[i % len(sample_shapes)]
            
            # Create a copy with slight variations to avoid identical shapes
            shape_data = base_shape.model_dump()
            shape_data.pop('id', None)  # Remove ID to generate new one
            shape_data['name'] = f"{base_shape.name} {i}"
            
            # Vary position slightly
            if 'transform' in shape_data:
                shape_data['transform']['x'] = (i % 100) * 2.0
                shape_data['transform']['y'] = (i // 100) * 2.0
            
            new_shape = Shape.model_validate(shape_data)
            main_layer.add_shape(new_shape)
        
        return doc
    
    # INSERT BENCHMARKS
    
    @pytest.mark.benchmark(group="insert")
    def test_insert_1000_shapes(self, benchmark, sample_shapes):
        """Benchmark inserting 1,000 shapes to layer."""
        def insert_shapes():
            doc = DrawingDocument.create_new(title="Insert Test 1K")
            layer = doc.create_layer("Test Layer")
            
            for i in range(1000):
                base_shape = sample_shapes[i % len(sample_shapes)]
                shape_data = base_shape.model_dump()
                shape_data.pop('id', None)  # Remove ID to generate new one
                shape_data['name'] = f"Shape {i}"
                
                new_shape = Shape.model_validate(shape_data)
                layer.add_shape(new_shape)
            
            return doc
        
        result = benchmark(insert_shapes)
        assert result.get_total_shape_count() == 1000
    
    @pytest.mark.benchmark(group="insert")
    def test_insert_2000_shapes(self, benchmark, sample_shapes):
        """Benchmark inserting 2,000 shapes to layer."""
        def insert_shapes():
            doc = DrawingDocument.create_new(title="Insert Test 2K")
            layer = doc.create_layer("Test Layer")
            
            for i in range(2000):
                base_shape = sample_shapes[i % len(sample_shapes)]
                shape_data = base_shape.model_dump()
                shape_data.pop('id', None)  # Remove ID to generate new one
                shape_data['name'] = f"Shape {i}"
                
                new_shape = Shape.model_validate(shape_data)
                layer.add_shape(new_shape)
            
            return doc
        
        result = benchmark(insert_shapes)
        assert result.get_total_shape_count() == 2000
    

    
    # SAVE (JSON SERIALIZATION) BENCHMARKS
    
    @pytest.mark.benchmark(group="save")
    def test_save_1000_shapes(self, benchmark, sample_shapes):
        """Benchmark JSON serialization of 1,000 shapes."""
        doc = self.create_test_document_with_shapes(1000, sample_shapes)
        
        def save_to_json():
            return doc.model_dump_json()
        
        json_data = benchmark(save_to_json)
        assert len(json_data) > 1000  # Should have substantial JSON data
        assert '"shapes"' in json_data  # Should contain shapes data
    
    @pytest.mark.benchmark(group="save")
    def test_save_2000_shapes(self, benchmark, sample_shapes):
        """Benchmark JSON serialization of 2,000 shapes."""
        doc = self.create_test_document_with_shapes(2000, sample_shapes)
        
        def save_to_json():
            return doc.model_dump_json()
        
        json_data = benchmark(save_to_json)
        assert len(json_data) > 2000
        assert '"shapes"' in json_data
    

    
    # LOAD (JSON DESERIALIZATION) BENCHMARKS
    
    @pytest.mark.benchmark(group="load")
    def test_load_1000_shapes(self, benchmark, sample_shapes):
        """Benchmark JSON deserialization of 1,000 shapes."""
        doc = self.create_test_document_with_shapes(1000, sample_shapes)
        json_data = doc.model_dump_json()
        
        def load_from_json():
            return DrawingDocument.model_validate_json(json_data)
        
        loaded_doc = benchmark(load_from_json)
        assert loaded_doc.get_total_shape_count() == 1000
        assert loaded_doc.metadata.title.startswith("Benchmark Document")
    
    @pytest.mark.benchmark(group="load") 
    def test_load_2000_shapes(self, benchmark, sample_shapes):
        """Benchmark JSON deserialization of 2,000 shapes."""
        doc = self.create_test_document_with_shapes(2000, sample_shapes)
        json_data = doc.model_dump_json()
        
        def load_from_json():
            return DrawingDocument.model_validate_json(json_data)
        
        loaded_doc = benchmark(load_from_json)
        assert loaded_doc.get_total_shape_count() == 2000
        assert loaded_doc.metadata.title.startswith("Benchmark Document")
    

    
    # MIXED OPERATIONS BENCHMARKS
    
    @pytest.mark.benchmark(group="mixed")
    def test_mixed_operations_1000(self, benchmark, sample_shapes):
        """Benchmark mixed operations with 1,000 shapes."""
        def mixed_operations():
            # Create document
            doc = DrawingDocument.create_new(title="Mixed Test")
            layer1 = doc.create_layer("Layer 1") 
            layer2 = doc.create_layer("Layer 2")
            
            # Add shapes to different layers
            for i in range(500):
                base_shape = sample_shapes[i % len(sample_shapes)]
                shape_data = base_shape.model_dump()
                shape_data.pop('id', None)  # Remove ID to generate new one
                shape_data['name'] = f"L1 Shape {i}"
                
                new_shape = Shape.model_validate(shape_data)
                layer1.add_shape(new_shape)
            
            for i in range(500):
                base_shape = sample_shapes[i % len(sample_shapes)]
                shape_data = base_shape.model_dump()
                shape_data.pop('id', None)  # Remove ID to generate new one
                shape_data['name'] = f"L2 Shape {i}"
                
                new_shape = Shape.model_validate(shape_data)
                layer2.add_shape(new_shape)
            
            # Serialize and deserialize
            json_data = doc.model_dump_json()
            loaded_doc = DrawingDocument.model_validate_json(json_data)
            
            # Validate round-trip
            assert loaded_doc.get_total_shape_count() == 1000
            return loaded_doc
        
        result = benchmark(mixed_operations)
        assert result.layer_manager.get_layer_count() == 3  # Default + 2 created
    
    @pytest.mark.benchmark(group="mixed")
    def test_mixed_operations_2000(self, benchmark, sample_shapes):
        """Benchmark mixed operations with 2,000 shapes."""
        def mixed_operations():
            doc = DrawingDocument.create_new(title="Mixed Test 2K")
            layers = [doc.create_layer(f"Layer {i}") for i in range(4)]
            
            # Distribute shapes across layers
            shapes_per_layer = 500
            for layer_idx, layer in enumerate(layers):
                for i in range(shapes_per_layer):
                    base_shape = sample_shapes[i % len(sample_shapes)]
                    shape_data = base_shape.model_dump()
                    shape_data.pop('id', None)  # Remove ID to generate new one
                    shape_data['name'] = f"L{layer_idx} Shape {i}"
                    
                    new_shape = Shape.model_validate(shape_data)
                    layer.add_shape(new_shape)
            
            # Serialize and deserialize
            json_data = doc.model_dump_json()
            loaded_doc = DrawingDocument.model_validate_json(json_data)
            
            return loaded_doc
        
        result = benchmark(mixed_operations)
        assert result.get_total_shape_count() == 2000
    
    # LAYER OPERATIONS BENCHMARKS
    
    @pytest.mark.benchmark(group="layers")
    def test_layer_operations_1000(self, benchmark, sample_shapes):
        """Benchmark layer operations with 1,000 shapes."""
        def layer_operations():
            doc = DrawingDocument.create_new(title="Layer Ops Test")
            
            # Create many layers
            layers = [doc.create_layer(f"Layer {i}") for i in range(10)]
            
            # Add shapes distributed across layers
            for i in range(1000):
                layer = layers[i % len(layers)]
                base_shape = sample_shapes[i % len(sample_shapes)]
                shape_data = base_shape.model_dump()
                shape_data.pop('id', None)  # Remove ID to generate new one
                shape_data['name'] = f"Shape {i}"
                
                new_shape = Shape.model_validate(shape_data)
                layer.add_shape(new_shape)
            
            # Perform layer operations
            visible_layers = doc.layer_manager.get_visible_layers()
            all_shapes = doc.layer_manager.get_all_layers()
            z_ordered = doc.layer_manager.get_layers_by_z_order()
            
            # Layer manipulation
            if len(layers) > 1:
                doc.layer_manager.set_active_layer(layers[1].id)
                active = doc.layer_manager.get_active_layer()
            
            return doc
        
        result = benchmark(layer_operations)
        assert result.get_total_shape_count() == 1000
        assert result.layer_manager.get_layer_count() == 11  # Default + 10 created