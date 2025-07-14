#!/usr/bin/env python3
"""
Basic Shapes Example

Demonstrates creating basic shapes with styling and organizing them in layers.
Shows fundamental library usage for common drawing operations.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from drawing_lib import (
    DrawingDocument, Shape, ShapeType,
    RGBColor, FillProperties, StrokeProperties, StyleProperties,
    Transform, Units
)
from svg_export import export_document_to_svg


def create_basic_shapes_document():
    """Create a document with basic shapes demonstrating core functionality."""
    
    # Create a new document with web preset
    doc = DrawingDocument.create_preset(
        "web", 
        title="Basic Shapes Demo",
        author="Drawing Library Example"
    )
    
    # Create layers for organization
    background_layer = doc.create_layer("Background")
    shapes_layer = doc.create_layer("Basic Shapes")
    text_layer = doc.create_layer("Labels")
    
    # Define common colors
    red = RGBColor(r=255, g=50, b=50)
    blue = RGBColor(r=50, g=150, b=255)
    green = RGBColor(r=50, g=200, b=50)
    black = RGBColor(r=0, g=0, b=0)
    white = RGBColor(r=255, g=255, b=255)
    
    # 1. Rectangle with fill and stroke
    rect_fill = FillProperties(color=red, opacity=0.8)
    rect_stroke = StrokeProperties(color=black, width=3.0)
    rect_style = StyleProperties(fill=rect_fill, stroke=rect_stroke)
    rect_transform = Transform(x=100.0, y=100.0)
    
    rectangle = Shape(
        type=ShapeType.RECTANGLE,
        geometry={"width": 200.0, "height": 120.0, "corner_radius": 10.0},
        style=rect_style,
        transform=rect_transform,
        name="Red Rectangle"
    )
    
    # 2. Circle with gradient-like effect using opacity
    circle_fill = FillProperties(color=blue, opacity=0.7)
    circle_style = StyleProperties(fill=circle_fill)
    circle_transform = Transform(x=400.0, y=150.0)
    
    circle = Shape(
        type=ShapeType.CIRCLE,
        geometry={"radius": 80.0},
        style=circle_style,
        transform=circle_transform,
        name="Blue Circle"
    )
    
    # 3. Triangle using polygon
    triangle_fill = FillProperties(color=green)
    triangle_stroke = StrokeProperties(color=black, width=2.0)
    triangle_style = StyleProperties(fill=triangle_fill, stroke=triangle_stroke)
    triangle_transform = Transform(x=700.0, y=100.0)
    
    triangle = Shape(
        type=ShapeType.POLYGON,
        geometry={"points": [[0.0, 120.0], [100.0, 120.0], [50.0, 20.0]]},
        style=triangle_style,
        transform=triangle_transform,
        name="Green Triangle"
    )
    
    # 4. Line with thick stroke
    line_stroke = StrokeProperties(color=black, width=5.0)
    line_style = StyleProperties(stroke=line_stroke)
    line_transform = Transform(x=100.0, y=300.0)
    
    line = Shape(
        type=ShapeType.LINE,
        geometry={"x1": 0.0, "y1": 0.0, "x2": 600.0, "y2": 100.0},
        style=line_style,
        transform=line_transform,
        name="Diagonal Line"
    )
    
    # 5. Ellipse
    ellipse_fill = FillProperties(color=RGBColor(r=255, g=200, b=50))
    ellipse_stroke = StrokeProperties(color=black, width=2.0)
    ellipse_style = StyleProperties(fill=ellipse_fill, stroke=ellipse_stroke)
    ellipse_transform = Transform(x=150.0, y=450.0)
    
    ellipse = Shape(
        type=ShapeType.ELLIPSE,
        geometry={"rx": 120.0, "ry": 60.0},
        style=ellipse_style,
        transform=ellipse_transform,
        name="Yellow Ellipse"
    )
    
    # 6. Path for complex shape
    path_stroke = StrokeProperties(color=RGBColor(r=150, g=50, b=150), width=4.0)
    path_style = StyleProperties(stroke=path_stroke)
    path_transform = Transform(x=500.0, y=400.0)
    
    path = Shape(
        type=ShapeType.PATH,
        geometry={
            "path_data": "M 0,0 C 0,-50 50,-50 50,0 C 50,50 100,50 100,0 L 150,0"
        },
        style=path_style,
        transform=path_transform,
        name="Purple Wave"
    )
    
    # Add background
    bg_fill = FillProperties(color=RGBColor(r=248, g=249, b=250))
    bg_style = StyleProperties(fill=bg_fill)
    
    background = Shape(
        type=ShapeType.RECTANGLE,
        geometry={"width": doc.canvas.width, "height": doc.canvas.height},
        style=bg_style,
        name="Background"
    )
    
    # Add shapes to layers
    background_layer.add_shape(background)
    shapes_layer.add_shape(rectangle)
    shapes_layer.add_shape(circle)
    shapes_layer.add_shape(triangle)
    shapes_layer.add_shape(line)
    shapes_layer.add_shape(ellipse)
    shapes_layer.add_shape(path)
    
    return doc


def demonstrate_layer_operations(doc):
    """Demonstrate layer management operations."""
    print("=== Layer Operations Demo ===")
    
    # Show layer information
    print(f"Total layers: {doc.layer_manager.get_layer_count()}")
    print(f"Total shapes: {doc.get_total_shape_count()}")
    
    print("\nLayers in document:")
    for layer in doc.layer_manager.get_all_layers():
        print(f"  - {layer.name}: {layer.get_shape_count()} shapes, visible: {layer.visible}")
    
    # Demonstrate layer visibility
    shapes_layer = None
    for layer in doc.layer_manager.get_all_layers():
        if layer.name == "Basic Shapes":
            shapes_layer = layer
            break
    
    if shapes_layer:
        print(f"\nToggling visibility of '{shapes_layer.name}' layer")
        shapes_layer.visible = False
        print(f"Layer now visible: {shapes_layer.visible}")
        shapes_layer.visible = True
    
    # Demonstrate z-order
    print(f"\nLayers by z-order:")
    ordered_layers = doc.layer_manager.get_layers_by_z_order()
    for i, layer in enumerate(ordered_layers):
        print(f"  {i}: {layer.name} (z-index: {layer.z_index})")


def save_and_load_demo(doc):
    """Demonstrate document serialization and loading."""
    print("\n=== Save/Load Demo ===")
    
    # Save to JSON
    json_data = doc.model_dump_json(indent=2)
    print(f"Document serialized to JSON ({len(json_data)} characters)")
    
    # Save to file
    with open("basic_shapes_output.json", "w") as f:
        f.write(json_data)
    print("Saved to: basic_shapes_output.json")
    
    # Load back from JSON
    loaded_doc = DrawingDocument.model_validate_json(json_data)
    print(f"Loaded document: '{loaded_doc.metadata.title}'")
    print(f"Shapes preserved: {loaded_doc.get_total_shape_count()}")
    print(f"Layers preserved: {loaded_doc.layer_manager.get_layer_count()}")
    
    return loaded_doc


def export_to_svg_demo(doc):
    """Demonstrate SVG export functionality."""
    print("\n=== SVG Export Demo ===")
    
    # Export to SVG
    svg_content = export_document_to_svg(doc, "basic_shapes_output.svg")
    print(f"Exported to SVG: basic_shapes_output.svg")
    print(f"SVG file size: {len(svg_content)} characters")
    
    # Show a snippet of the SVG content
    lines = svg_content.split('\n')
    print(f"SVG preview (first 5 lines):")
    for i, line in enumerate(lines[:5]):
        print(f"  {line}")
    if len(lines) > 5:
        print(f"  ... ({len(lines) - 5} more lines)")
    
    return svg_content


def main():
    """Main example function."""
    print("Drawing Library - Basic Shapes Example")
    print("=" * 50)
    
    # Create the document
    doc = create_basic_shapes_document()
    
    # Show document information
    info = doc.get_document_info()
    print(f"Created document: {info['title']}")
    print(f"Canvas size: {info['canvas_size']}")
    print(f"Total shapes: {info['total_shapes']}")
    print(f"Total layers: {info['total_layers']}")
    
    # Demonstrate layer operations
    demonstrate_layer_operations(doc)
    
    # Demonstrate save/load
    loaded_doc = save_and_load_demo(doc)
    
    # Demonstrate SVG export
    svg_content = export_to_svg_demo(loaded_doc)
    
    # Validate document integrity
    validation = loaded_doc.validate_document()
    if not validation["errors"]:
        print("\n✅ Document validation passed!")
    else:
        print(f"\n❌ Document validation errors: {validation['errors']}")
    
    if validation["warnings"]:
        print(f"⚠️ Warnings: {validation['warnings']}")
    
    print("\n🎉 Basic shapes example completed successfully!")


if __name__ == "__main__":
    main()