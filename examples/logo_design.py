#!/usr/bin/env python3
"""
Logo Design Example

Demonstrates creating a complex logo design with multiple layers, groups,
advanced styling, and precise positioning. Shows how to build professional
graphic designs using the drawing library.
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


def create_logo_document():
    """Create a logo design document with corporate branding elements."""
    
    # Create document with print preset for high-quality output
    doc = DrawingDocument.create_preset(
        "print_letter",
        title="Corporate Logo Design",
        author="Design Team"
    )
    
    # Convert to pixels for easier working (300 DPI)
    doc.set_canvas_size(2550.0, 3300.0, Units.PIXELS)  # 8.5x11 at 300 DPI
    
    # Create layer structure
    background_layer = doc.create_layer("Background")
    logo_group = doc.create_layer_group("Logo Elements")
    icon_layer = doc.create_layer("Icon", parent_group=logo_group)
    text_layer = doc.create_layer("Company Text", parent_group=logo_group)
    tagline_layer = doc.create_layer("Tagline", parent_group=logo_group)
    
    # Define brand colors
    primary_blue = RGBColor(r=25, g=118, b=210)
    secondary_blue = RGBColor(r=66, g=165, b=245)
    accent_orange = RGBColor(r=255, g=152, b=0)
    dark_gray = RGBColor(r=66, g=66, b=66)
    light_gray = RGBColor(r=245, g=245, b=245)
    white = RGBColor(r=255, g=255, b=255)
    
    return doc, {
        'background_layer': background_layer,
        'icon_layer': icon_layer,
        'text_layer': text_layer,
        'tagline_layer': tagline_layer,
        'colors': {
            'primary_blue': primary_blue,
            'secondary_blue': secondary_blue,
            'accent_orange': accent_orange,
            'dark_gray': dark_gray,
            'light_gray': light_gray,
            'white': white
        }
    }


def create_logo_icon(icon_layer, colors, center_x=1275.0, center_y=1000.0):
    """Create a modern geometric logo icon."""
    
    # Main circle background
    main_circle_fill = FillProperties(color=colors['primary_blue'])
    main_circle_style = StyleProperties(fill=main_circle_fill)
    main_circle_transform = Transform(x=center_x, y=center_y)
    
    main_circle = Shape(
        type=ShapeType.CIRCLE,
        geometry={"radius": 150.0},
        style=main_circle_style,
        transform=main_circle_transform,
        name="Main Circle"
    )
    
    # Inner accent circle
    accent_circle_fill = FillProperties(color=colors['accent_orange'])
    accent_circle_style = StyleProperties(fill=accent_circle_fill)
    accent_circle_transform = Transform(x=center_x - 40.0, y=center_y - 40.0)
    
    accent_circle = Shape(
        type=ShapeType.CIRCLE,
        geometry={"radius": 60.0},
        style=accent_circle_style,
        transform=accent_circle_transform,
        name="Accent Circle"
    )
    
    # Geometric triangles for modern look
    triangle1_fill = FillProperties(color=colors['white'], opacity=0.9)
    triangle1_style = StyleProperties(fill=triangle1_fill)
    triangle1_transform = Transform(x=center_x + 30.0, y=center_y + 20.0)
    
    triangle1 = Shape(
        type=ShapeType.POLYGON,
        geometry={"points": [[0.0, 0.0], [60.0, 0.0], [30.0, -52.0]]},
        style=triangle1_style,
        transform=triangle1_transform,
        name="Triangle 1"
    )
    
    triangle2_fill = FillProperties(color=colors['secondary_blue'], opacity=0.8)
    triangle2_style = StyleProperties(fill=triangle2_fill)
    triangle2_transform = Transform(x=center_x + 30.0, y=center_y + 80.0)
    
    triangle2 = Shape(
        type=ShapeType.POLYGON,
        geometry={"points": [[0.0, 0.0], [60.0, 0.0], [30.0, 52.0]]},
        style=triangle2_style,
        transform=triangle2_transform,
        name="Triangle 2"
    )
    
    # Add shapes to icon layer
    icon_layer.add_shape(main_circle)
    icon_layer.add_shape(accent_circle)
    icon_layer.add_shape(triangle1)
    icon_layer.add_shape(triangle2)
    
    return center_x, center_y + 200.0  # Return position for next elements


def create_company_text(text_layer, colors, start_x, start_y):
    """Create company name using geometric shapes (since we don't have text yet)."""
    
    # Simulate "TECHCORP" using rectangles and lines
    letter_width = 60.0
    letter_height = 80.0
    letter_spacing = 80.0
    stroke_width = 8.0
    
    text_stroke = StrokeProperties(color=colors['dark_gray'], width=stroke_width)
    text_style = StyleProperties(stroke=text_stroke)
    
    # T
    t_horizontal = Shape(
        type=ShapeType.RECTANGLE,
        geometry={"width": letter_width, "height": stroke_width},
        style=text_style,
        transform=Transform(x=start_x, y=start_y),
        name="T Horizontal"
    )
    
    t_vertical = Shape(
        type=ShapeType.RECTANGLE,
        geometry={"width": stroke_width, "height": letter_height},
        style=text_style,
        transform=Transform(x=start_x + letter_width/2 - stroke_width/2, y=start_y),
        name="T Vertical"
    )
    
    # E (simplified as rectangles)
    e_vertical = Shape(
        type=ShapeType.RECTANGLE,
        geometry={"width": stroke_width, "height": letter_height},
        style=text_style,
        transform=Transform(x=start_x + letter_spacing, y=start_y),
        name="E Vertical"
    )
    
    e_top = Shape(
        type=ShapeType.RECTANGLE,
        geometry={"width": letter_width - stroke_width, "height": stroke_width},
        style=text_style,
        transform=Transform(x=start_x + letter_spacing + stroke_width, y=start_y),
        name="E Top"
    )
    
    e_middle = Shape(
        type=ShapeType.RECTANGLE,
        geometry={"width": letter_width - stroke_width - 15, "height": stroke_width},
        style=text_style,
        transform=Transform(x=start_x + letter_spacing + stroke_width, y=start_y + letter_height/2),
        name="E Middle"
    )
    
    e_bottom = Shape(
        type=ShapeType.RECTANGLE,
        geometry={"width": letter_width - stroke_width, "height": stroke_width},
        style=text_style,
        transform=Transform(x=start_x + letter_spacing + stroke_width, y=start_y + letter_height - stroke_width),
        name="E Bottom"
    )
    
    # Add decorative elements
    accent_line_fill = FillProperties(color=colors['accent_orange'])
    accent_line_style = StyleProperties(fill=accent_line_fill)
    
    accent_line = Shape(
        type=ShapeType.RECTANGLE,
        geometry={"width": 200.0, "height": 4.0},
        style=accent_line_style,
        transform=Transform(x=start_x, y=start_y + letter_height + 20.0),
        name="Accent Line"
    )
    
    # Add all text elements
    text_shapes = [t_horizontal, t_vertical, e_vertical, e_top, e_middle, e_bottom, accent_line]
    for shape in text_shapes:
        text_layer.add_shape(shape)
    
    return start_y + letter_height + 60.0  # Return position for tagline


def create_tagline(tagline_layer, colors, start_x, start_y):
    """Create tagline using simple geometric representation."""
    
    # Tagline "Innovation Through Technology" represented as lines
    line_stroke = StrokeProperties(color=colors['secondary_blue'], width=3.0)
    line_style = StyleProperties(stroke=line_stroke)
    
    # Create series of lines to represent text
    for i in range(3):  # 3 words
        for j in range(8):  # 8 characters per word average
            line = Shape(
                type=ShapeType.LINE,
                geometry={"x1": 0.0, "y1": 0.0, "x2": 12.0, "y2": 0.0},
                style=line_style,
                transform=Transform(
                    x=start_x + i * 120.0 + j * 15.0,
                    y=start_y + (i % 2) * 5.0  # Slight wave effect
                ),
                name=f"Tagline Word {i+1} Char {j+1}"
            )
            tagline_layer.add_shape(line)


def create_background_elements(background_layer, colors, doc):
    """Create subtle background elements."""
    
    # Subtle gradient effect using overlapping shapes
    bg_fill = FillProperties(color=colors['light_gray'])
    bg_style = StyleProperties(fill=bg_fill)
    
    background = Shape(
        type=ShapeType.RECTANGLE,
        geometry={"width": doc.canvas.width, "height": doc.canvas.height},
        style=bg_style,
        name="Background"
    )
    
    # Decorative corner elements
    corner_fill = FillProperties(color=colors['primary_blue'], opacity=0.1)
    corner_style = StyleProperties(fill=corner_fill)
    
    # Top-left corner decoration
    corner_tl = Shape(
        type=ShapeType.CIRCLE,
        geometry={"radius": 300.0},
        style=corner_style,
        transform=Transform(x=-150.0, y=-150.0),
        name="Corner TL"
    )
    
    # Bottom-right corner decoration
    corner_br = Shape(
        type=ShapeType.CIRCLE,
        geometry={"radius": 400.0},
        style=corner_style,
        transform=Transform(x=doc.canvas.width - 200.0, y=doc.canvas.height - 200.0),
        name="Corner BR"
    )
    
    background_layer.add_shape(background)
    background_layer.add_shape(corner_tl)
    background_layer.add_shape(corner_br)


def main():
    """Main logo design example."""
    print("Drawing Library - Logo Design Example")
    print("=" * 50)
    
    # Create the document and layers
    doc, elements = create_logo_document()
    
    # Create background
    create_background_elements(elements['background_layer'], elements['colors'], doc)
    
    # Create logo elements
    center_x = doc.canvas.width / 2
    _, text_y = create_logo_icon(elements['icon_layer'], elements['colors'], center_x, 800.0)
    
    tagline_y = create_company_text(elements['text_layer'], elements['colors'], center_x - 100.0, text_y)
    
    create_tagline(elements['tagline_layer'], elements['colors'], center_x - 150.0, tagline_y)
    
    # Show document information
    info = doc.get_document_info()
    print(f"Created logo design: {info['title']}")
    print(f"Canvas size: {info['canvas_size']}")
    print(f"Total shapes: {info['total_shapes']}")
    print(f"Total layers: {info['total_layers']}")
    
    # Demonstrate layer group operations
    print(f"\nLayer structure:")
    for layer in doc.layer_manager.get_all_layers():
        indent = "  " if hasattr(layer, 'parent_group') and layer.parent_group else ""
        print(f"{indent}- {layer.name}: {layer.get_shape_count()} shapes")
    
    # Save the design
    json_data = doc.model_dump_json(indent=2)
    with open("logo_design_output.json", "w") as f:
        f.write(json_data)
    print(f"\nSaved logo design to: logo_design_output.json")
    print(f"JSON file size: {len(json_data)} characters")
    
    # Export to SVG
    svg_content = export_document_to_svg(doc, "logo_design_output.svg")
    print(f"Exported to SVG: logo_design_output.svg")
    print(f"SVG file size: {len(svg_content)} characters")
    
    # Validate design
    validation = doc.validate_document()
    if not validation["errors"]:
        print("\n✅ Logo design validation passed!")
    else:
        print(f"\n❌ Validation errors: {validation['errors']}")
    
    print("\n🎨 Logo design example completed successfully!")
    
    return doc


if __name__ == "__main__":
    main()