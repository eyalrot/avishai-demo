#!/usr/bin/env python3
"""
Data Visualization Example

Demonstrates creating charts and data visualizations using the drawing library.
Shows how to build bar charts, line graphs, and pie charts with proper scaling,
labels, and styling for data presentation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import math

from drawing_lib import (
    DrawingDocument, Shape, ShapeType,
    RGBColor, FillProperties, StrokeProperties, StyleProperties,
    Transform, Units
)
from svg_export import export_document_to_svg


def create_chart_document():
    """Create a document for data visualizations."""
    
    doc = DrawingDocument.create_preset(
        "web",
        title="Data Visualization Dashboard",
        author="Analytics Team"
    )
    
    # Create layers for different chart types
    background_layer = doc.create_layer("Background")
    bar_chart_layer = doc.create_layer("Bar Chart")
    line_chart_layer = doc.create_layer("Line Chart")
    pie_chart_layer = doc.create_layer("Pie Chart")
    labels_layer = doc.create_layer("Labels & Axes")
    
    # Define visualization colors
    colors = {
        'background': RGBColor(r=248, g=249, b=250),
        'primary': RGBColor(r=59, g=130, b=246),
        'secondary': RGBColor(r=16, g=185, b=129),
        'accent': RGBColor(r=245, g=158, b=11),
        'danger': RGBColor(r=239, g=68, b=68),
        'text': RGBColor(r=55, g=65, b=81),
        'grid': RGBColor(r=229, g=231, b=235),
        'white': RGBColor(r=255, g=255, b=255)
    }
    
    return doc, {
        'background_layer': background_layer,
        'bar_chart_layer': bar_chart_layer,
        'line_chart_layer': line_chart_layer,
        'pie_chart_layer': pie_chart_layer,
        'labels_layer': labels_layer,
        'colors': colors
    }


def create_background_grid(background_layer, labels_layer, colors, chart_area):
    """Create background and grid for charts."""
    
    x, y, width, height = chart_area
    
    # Main background
    bg_fill = FillProperties(color=colors['background'])
    bg_style = StyleProperties(fill=bg_fill)
    
    background = Shape(
        type=ShapeType.RECTANGLE,
        geometry={"width": 1920.0, "height": 1080.0},
        style=bg_style,
        name="Background"
    )
    background_layer.add_shape(background)
    
    # Chart area background
    chart_bg_fill = FillProperties(color=colors['white'])
    chart_bg_stroke = StrokeProperties(color=colors['grid'], width=1.0)
    chart_bg_style = StyleProperties(fill=chart_bg_fill, stroke=chart_bg_stroke)
    
    chart_background = Shape(
        type=ShapeType.RECTANGLE,
        geometry={"width": width, "height": height},
        style=chart_bg_style,
        transform=Transform(x=x, y=y),
        name="Chart Background"
    )
    background_layer.add_shape(chart_background)
    
    # Grid lines
    grid_stroke = StrokeProperties(color=colors['grid'], width=0.5)
    grid_style = StyleProperties(stroke=grid_stroke)
    
    # Horizontal grid lines
    for i in range(6):  # 5 divisions
        grid_y = y + (height / 5) * i
        grid_line = Shape(
            type=ShapeType.LINE,
            geometry={"x1": 0.0, "y1": 0.0, "x2": width, "y2": 0.0},
            style=grid_style,
            transform=Transform(x=x, y=grid_y),
            name=f"Grid H {i}"
        )
        labels_layer.add_shape(grid_line)
    
    # Vertical grid lines
    for i in range(8):  # 7 divisions
        grid_x = x + (width / 7) * i
        grid_line = Shape(
            type=ShapeType.LINE,
            geometry={"x1": 0.0, "y1": 0.0, "x2": 0.0, "y2": height},
            style=grid_style,
            transform=Transform(x=grid_x, y=y),
            name=f"Grid V {i}"
        )
        labels_layer.add_shape(grid_line)


def create_bar_chart(bar_chart_layer, colors, chart_area, data):
    """Create a bar chart from data."""
    
    x, y, width, height = chart_area
    
    # Sample data: monthly sales
    values = data.get('values', [45, 67, 23, 89, 56, 78, 34])
    max_value = max(values)
    bar_width = width / len(values) * 0.8  # 80% width for bars
    bar_spacing = width / len(values) * 0.2  # 20% for spacing
    
    colors_cycle = [colors['primary'], colors['secondary'], colors['accent'], colors['danger']]
    
    for i, value in enumerate(values):
        # Calculate bar dimensions
        bar_height = (value / max_value) * height * 0.9  # 90% of chart height
        bar_x = x + i * (width / len(values)) + bar_spacing / 2
        bar_y = y + height - bar_height
        
        # Create bar
        bar_color = colors_cycle[i % len(colors_cycle)]
        bar_fill = FillProperties(color=bar_color, opacity=0.8)
        bar_stroke = StrokeProperties(color=bar_color, width=1.0)
        bar_style = StyleProperties(fill=bar_fill, stroke=bar_stroke)
        
        bar = Shape(
            type=ShapeType.RECTANGLE,
            geometry={"width": bar_width, "height": bar_height, "corner_radius": 4.0},
            style=bar_style,
            transform=Transform(x=bar_x, y=bar_y),
            name=f"Bar {i+1} ({value})"
        )
        bar_chart_layer.add_shape(bar)
        
        # Create value label on top of bar
        # Simulated as small rectangle (since we don't have text rendering)
        label_fill = FillProperties(color=colors['text'])
        label_style = StyleProperties(fill=label_fill)
        
        label = Shape(
            type=ShapeType.RECTANGLE,
            geometry={"width": 20.0, "height": 3.0},
            style=label_style,
            transform=Transform(x=bar_x + bar_width/2 - 10.0, y=bar_y - 10.0),
            name=f"Label {value}"
        )
        bar_chart_layer.add_shape(label)


def create_line_chart(line_chart_layer, colors, chart_area, data):
    """Create a line chart from data."""
    
    x, y, width, height = chart_area
    
    # Sample data: performance over time
    values = data.get('line_values', [30, 45, 35, 60, 55, 70, 85])
    max_value = max(values)
    min_value = min(values)
    value_range = max_value - min_value if max_value != min_value else 1
    
    # Create line path
    line_stroke = StrokeProperties(color=colors['secondary'], width=3.0)
    line_style = StyleProperties(stroke=line_stroke)
    
    # Calculate points
    points = []
    for i, value in enumerate(values):
        point_x = (i / (len(values) - 1)) * width
        point_y = height - ((value - min_value) / value_range) * height * 0.9
        points.append([point_x, point_y])
    
    # Create line using path
    path_data = f"M {points[0][0]},{points[0][1]}"
    for point in points[1:]:
        path_data += f" L {point[0]},{point[1]}"
    
    line_path = Shape(
        type=ShapeType.PATH,
        geometry={"path_data": path_data},
        style=line_style,
        transform=Transform(x=x, y=y),
        name="Performance Line"
    )
    line_chart_layer.add_shape(line_path)
    
    # Add data points as circles
    point_fill = FillProperties(color=colors['secondary'])
    point_stroke = StrokeProperties(color=colors['white'], width=2.0)
    point_style = StyleProperties(fill=point_fill, stroke=point_stroke)
    
    for i, (point_x, point_y) in enumerate(points):
        point = Shape(
            type=ShapeType.CIRCLE,
            geometry={"radius": 5.0},
            style=point_style,
            transform=Transform(x=x + point_x, y=y + point_y),
            name=f"Point {i+1} ({values[i]})"
        )
        line_chart_layer.add_shape(point)


def create_pie_chart(pie_chart_layer, colors, center, radius, data):
    """Create a pie chart from data."""
    
    center_x, center_y = center
    
    # Sample data: market share
    values = data.get('pie_values', [35, 25, 20, 15, 5])
    labels = data.get('pie_labels', ['Product A', 'Product B', 'Product C', 'Product D', 'Others'])
    total = sum(values)
    
    colors_cycle = [colors['primary'], colors['secondary'], colors['accent'], colors['danger'], colors['text']]
    
    current_angle = 0
    
    for i, value in enumerate(values):
        # Calculate slice angle
        slice_angle = (value / total) * 360
        
        # Create pie slice using path (approximated with polygon for simplicity)
        slice_color = colors_cycle[i % len(colors_cycle)]
        slice_fill = FillProperties(color=slice_color, opacity=0.8)
        slice_stroke = StrokeProperties(color=colors['white'], width=2.0)
        slice_style = StyleProperties(fill=slice_fill, stroke=slice_stroke)
        
        # Calculate points for pie slice (simplified as triangle from center)
        start_angle_rad = math.radians(current_angle)
        end_angle_rad = math.radians(current_angle + slice_angle)
        
        # Create points for the slice
        start_x = radius * math.cos(start_angle_rad)
        start_y = radius * math.sin(start_angle_rad)
        end_x = radius * math.cos(end_angle_rad)
        end_y = radius * math.sin(end_angle_rad)
        
        # Simplified pie slice as triangle
        slice_points = [[0.0, 0.0], [start_x, start_y], [end_x, end_y]]
        
        slice_shape = Shape(
            type=ShapeType.POLYGON,
            geometry={"points": slice_points},
            style=slice_style,
            transform=Transform(x=center_x, y=center_y),
            name=f"Slice {labels[i]} ({value}%)"
        )
        pie_chart_layer.add_shape(slice_shape)
        
        # Add label indicator (small circle)
        mid_angle_rad = math.radians(current_angle + slice_angle / 2)
        label_x = center_x + (radius + 30) * math.cos(mid_angle_rad)
        label_y = center_y + (radius + 30) * math.sin(mid_angle_rad)
        
        label_fill = FillProperties(color=slice_color)
        label_style = StyleProperties(fill=label_fill)
        
        label_indicator = Shape(
            type=ShapeType.CIRCLE,
            geometry={"radius": 8.0},
            style=label_style,
            transform=Transform(x=label_x, y=label_y),
            name=f"Label {labels[i]}"
        )
        pie_chart_layer.add_shape(label_indicator)
        
        current_angle += slice_angle


def create_chart_titles(labels_layer, colors):
    """Create titles and labels for charts."""
    
    # Chart titles (represented as rectangles since we don't have text)
    title_fill = FillProperties(color=colors['text'])
    title_style = StyleProperties(fill=title_fill)
    
    # Main title
    main_title = Shape(
        type=ShapeType.RECTANGLE,
        geometry={"width": 300.0, "height": 8.0},
        style=title_style,
        transform=Transform(x=810.0, y=50.0),
        name="Main Title: Analytics Dashboard"
    )
    labels_layer.add_shape(main_title)
    
    # Chart subtitles
    subtitle_fill = FillProperties(color=colors['text'], opacity=0.7)
    subtitle_style = StyleProperties(fill=subtitle_fill)
    
    bar_title = Shape(
        type=ShapeType.RECTANGLE,
        geometry={"width": 120.0, "height": 4.0},
        style=subtitle_style,
        transform=Transform(x=100.0, y=120.0),
        name="Bar Chart: Monthly Sales"
    )
    
    line_title = Shape(
        type=ShapeType.RECTANGLE,
        geometry={"width": 140.0, "height": 4.0},
        style=subtitle_style,
        transform=Transform(x=600.0, y=120.0),
        name="Line Chart: Performance"
    )
    
    pie_title = Shape(
        type=ShapeType.RECTANGLE,
        geometry={"width": 110.0, "height": 4.0},
        style=subtitle_style,
        transform=Transform(x=1200.0, y=120.0),
        name="Pie Chart: Market Share"
    )
    
    labels_layer.add_shape(bar_title)
    labels_layer.add_shape(line_title)
    labels_layer.add_shape(pie_title)


def main():
    """Main data visualization example."""
    print("Drawing Library - Data Visualization Example")
    print("=" * 50)
    
    # Create document and layers
    doc, elements = create_chart_document()
    
    # Sample datasets
    datasets = {
        'values': [45, 67, 23, 89, 56, 78, 34],  # Bar chart data
        'line_values': [30, 45, 35, 60, 55, 70, 85],  # Line chart data
        'pie_values': [35, 25, 20, 15, 5],  # Pie chart data
        'pie_labels': ['Product A', 'Product B', 'Product C', 'Product D', 'Others']
    }
    
    # Define chart areas
    bar_chart_area = (80, 150, 400, 300)  # x, y, width, height
    line_chart_area = (580, 150, 400, 300)
    pie_chart_center = (1300, 300)
    pie_chart_radius = 120
    
    # Create visualizations
    create_background_grid(elements['background_layer'], elements['labels_layer'], 
                          elements['colors'], bar_chart_area)
    
    create_background_grid(elements['background_layer'], elements['labels_layer'], 
                          elements['colors'], line_chart_area)
    
    create_bar_chart(elements['bar_chart_layer'], elements['colors'], 
                    bar_chart_area, datasets)
    
    create_line_chart(elements['line_chart_layer'], elements['colors'], 
                     line_chart_area, datasets)
    
    create_pie_chart(elements['pie_chart_layer'], elements['colors'], 
                    pie_chart_center, pie_chart_radius, datasets)
    
    create_chart_titles(elements['labels_layer'], elements['colors'])
    
    # Show document information
    info = doc.get_document_info()
    print(f"Created visualization: {info['title']}")
    print(f"Canvas size: {info['canvas_size']}")
    print(f"Total shapes: {info['total_shapes']}")
    print(f"Total layers: {info['total_layers']}")
    
    # Show data insights
    print(f"\nData Insights:")
    print(f"- Bar chart shows {len(datasets['values'])} data points")
    print(f"- Line chart tracks {len(datasets['line_values'])} time periods")
    print(f"- Pie chart represents {len(datasets['pie_values'])} categories")
    print(f"- Total data points visualized: {sum(len(v) if isinstance(v, list) else 0 for v in datasets.values())}")
    
    # Save the visualization
    json_data = doc.model_dump_json(indent=2)
    with open("data_visualization_output.json", "w") as f:
        f.write(json_data)
    print(f"\nSaved visualization to: data_visualization_output.json")
    print(f"JSON file size: {len(json_data)} characters")
    
    # Export to SVG
    svg_content = export_document_to_svg(doc, "data_visualization_output.svg")
    print(f"Exported to SVG: data_visualization_output.svg")
    print(f"SVG file size: {len(svg_content)} characters")
    
    # Performance analysis
    print(f"\nPerformance Analysis:")
    print(f"- Document creation: Efficient multi-layer structure")
    print(f"- Shape count: {info['total_shapes']} shapes for complex dashboard")
    print(f"- Memory usage: ~{len(json_data)} bytes serialized")
    
    # Validate visualization
    validation = doc.validate_document()
    if not validation["errors"]:
        print("\n✅ Data visualization validation passed!")
    else:
        print(f"\n❌ Validation errors: {validation['errors']}")
    
    print("\n📊 Data visualization example completed successfully!")
    
    return doc


if __name__ == "__main__":
    main()