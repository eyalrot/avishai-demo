#!/usr/bin/env python3
"""
SVG Export Module

Provides functionality to export drawing library documents to SVG format.
This module operates outside the document class as a separate export utility.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from drawing_lib import DrawingDocument, Shape, ShapeType, RGBColor, Units
from typing import List, Dict, Any, Optional
import xml.etree.ElementTree as ET


class SVGExporter:
    """SVG export utility for drawing library documents."""
    
    def __init__(self, document: DrawingDocument):
        """Initialize SVG exporter with a document."""
        self.document = document
        self.svg_root = None
        self.defs = None
        
    def export_to_svg(self, filename: str, include_invisible: bool = False) -> str:
        """
        Export document to SVG file.
        
        Args:
            filename: Output SVG filename
            include_invisible: Whether to include invisible layers
            
        Returns:
            SVG content as string
        """
        svg_content = self.generate_svg_content(include_invisible)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(svg_content)
            
        return svg_content
    
    def generate_svg_content(self, include_invisible: bool = False) -> str:
        """Generate SVG content from the document."""
        
        # Create SVG root element
        canvas_width, canvas_height = self._get_canvas_dimensions()
        self.svg_root = ET.Element('svg', {
            'xmlns': 'http://www.w3.org/2000/svg',
            'xmlns:xlink': 'http://www.w3.org/1999/xlink',
            'width': f"{canvas_width}",
            'height': f"{canvas_height}",
            'viewBox': f"0 0 {canvas_width} {canvas_height}"
        })
        
        # Add document metadata as comment
        comment = ET.Comment(f" Generated from: {self.document.metadata.title} ")
        self.svg_root.insert(0, comment)
        
        # Create defs section for reusable elements
        self.defs = ET.SubElement(self.svg_root, 'defs')
        
        # Add background if not transparent
        self._add_background()
        
        # Process layers in z-order
        layers = self.document.layer_manager.get_layers_by_z_order()
        for layer in layers:
            if layer.visible or include_invisible:
                self._add_layer_to_svg(layer, include_invisible)
        
        # Convert to string with proper formatting
        self._indent_xml(self.svg_root)
        return ET.tostring(self.svg_root, encoding='unicode', method='xml')
    
    def _get_canvas_dimensions(self) -> tuple[float, float]:
        """Get canvas dimensions in pixels."""
        if self.document.canvas.units == Units.PIXELS:
            return self.document.canvas.width, self.document.canvas.height
        else:
            # Convert to pixels using document export settings DPI
            dpi = self.document.export_settings.dpi
            return self.document.canvas.to_pixels(dpi)
    
    def _add_background(self):
        """Add background rectangle if not transparent."""
        if not self.document.background.transparent and self.document.background.color:
            canvas_width, canvas_height = self._get_canvas_dimensions()
            
            bg_attrs = {
                'x': '0',
                'y': '0',
                'width': str(canvas_width),
                'height': str(canvas_height),
                'fill': self._color_to_svg(self.document.background.color)
            }
            
            if hasattr(self.document.background, 'image_opacity') and self.document.background.image_opacity < 1.0:
                bg_attrs['opacity'] = str(self.document.background.image_opacity)
            
            ET.SubElement(self.svg_root, 'rect', bg_attrs)
    
    def _add_layer_to_svg(self, layer, include_invisible: bool = False):
        """Add a layer to SVG as a group."""
        
        # Create layer group
        group_attrs = {'id': f"layer-{layer.id}"}
        if hasattr(layer, 'name'):
            group_attrs['data-name'] = layer.name
        
        if not layer.visible:
            group_attrs['opacity'] = '0'
        
        layer_group = ET.SubElement(self.svg_root, 'g', group_attrs)
        
        # Add shapes from the layer
        for shape in layer.shapes:
            if isinstance(shape, Shape):
                self._add_shape_to_svg(shape, layer_group)
    
    def _add_shape_to_svg(self, shape: Shape, parent_group: ET.Element):
        """Add a shape to SVG."""
        
        # Apply transform if present
        transform_attr = self._get_transform_string(shape.transform)
        
        if shape.type == ShapeType.RECTANGLE:
            self._add_rectangle(shape, parent_group, transform_attr)
        elif shape.type == ShapeType.CIRCLE:
            self._add_circle(shape, parent_group, transform_attr)
        elif shape.type == ShapeType.ELLIPSE:
            self._add_ellipse(shape, parent_group, transform_attr)
        elif shape.type == ShapeType.LINE:
            self._add_line(shape, parent_group, transform_attr)
        elif shape.type == ShapeType.POLYGON:
            self._add_polygon(shape, parent_group, transform_attr)
        elif shape.type == ShapeType.PATH:
            self._add_path(shape, parent_group, transform_attr)
        # Add other shape types as needed
    
    def _add_rectangle(self, shape: Shape, parent: ET.Element, transform: str):
        """Add rectangle to SVG."""
        geom = shape.geometry
        
        attrs = {
            'x': '0',
            'y': '0',
            'width': str(geom.get('width', 0)),
            'height': str(geom.get('height', 0))
        }
        
        # Add corner radius if specified
        if 'corner_radius' in geom and geom['corner_radius'] > 0:
            attrs['rx'] = str(geom['corner_radius'])
            attrs['ry'] = str(geom['corner_radius'])
        
        # Add styling
        self._add_style_attributes(attrs, shape.style)
        
        # Add transform
        if transform:
            attrs['transform'] = transform
        
        # Add name as id if present
        if shape.name:
            attrs['id'] = self._sanitize_id(shape.name)
        
        ET.SubElement(parent, 'rect', attrs)
    
    def _add_circle(self, shape: Shape, parent: ET.Element, transform: str):
        """Add circle to SVG."""
        geom = shape.geometry
        
        attrs = {
            'cx': '0',
            'cy': '0',
            'r': str(geom.get('radius', 0))
        }
        
        self._add_style_attributes(attrs, shape.style)
        
        if transform:
            attrs['transform'] = transform
        
        if shape.name:
            attrs['id'] = self._sanitize_id(shape.name)
        
        ET.SubElement(parent, 'circle', attrs)
    
    def _add_ellipse(self, shape: Shape, parent: ET.Element, transform: str):
        """Add ellipse to SVG."""
        geom = shape.geometry
        
        attrs = {
            'cx': '0',
            'cy': '0',
            'rx': str(geom.get('rx', 0)),
            'ry': str(geom.get('ry', 0))
        }
        
        self._add_style_attributes(attrs, shape.style)
        
        if transform:
            attrs['transform'] = transform
        
        if shape.name:
            attrs['id'] = self._sanitize_id(shape.name)
        
        ET.SubElement(parent, 'ellipse', attrs)
    
    def _add_line(self, shape: Shape, parent: ET.Element, transform: str):
        """Add line to SVG."""
        geom = shape.geometry
        
        attrs = {
            'x1': str(geom.get('x1', 0)),
            'y1': str(geom.get('y1', 0)),
            'x2': str(geom.get('x2', 0)),
            'y2': str(geom.get('y2', 0))
        }
        
        self._add_style_attributes(attrs, shape.style)
        
        if transform:
            attrs['transform'] = transform
        
        if shape.name:
            attrs['id'] = self._sanitize_id(shape.name)
        
        ET.SubElement(parent, 'line', attrs)
    
    def _add_polygon(self, shape: Shape, parent: ET.Element, transform: str):
        """Add polygon to SVG."""
        geom = shape.geometry
        points = geom.get('points', [])
        
        # Convert points to SVG format
        points_str = ' '.join([f"{p[0]},{p[1]}" for p in points])
        
        attrs = {
            'points': points_str
        }
        
        self._add_style_attributes(attrs, shape.style)
        
        if transform:
            attrs['transform'] = transform
        
        if shape.name:
            attrs['id'] = self._sanitize_id(shape.name)
        
        ET.SubElement(parent, 'polygon', attrs)
    
    def _add_path(self, shape: Shape, parent: ET.Element, transform: str):
        """Add path to SVG."""
        geom = shape.geometry
        path_data = geom.get('path_data', '')
        
        attrs = {
            'd': path_data
        }
        
        self._add_style_attributes(attrs, shape.style)
        
        if transform:
            attrs['transform'] = transform
        
        if shape.name:
            attrs['id'] = self._sanitize_id(shape.name)
        
        ET.SubElement(parent, 'path', attrs)
    
    def _add_style_attributes(self, attrs: Dict[str, str], style):
        """Add style attributes to SVG element."""
        if not style:
            return
        
        # Handle fill
        if hasattr(style, 'fill') and style.fill:
            fill_color = self._color_to_svg(style.fill.color)
            attrs['fill'] = fill_color
            
            if hasattr(style.fill, 'opacity') and style.fill.opacity < 1.0:
                attrs['fill-opacity'] = str(style.fill.opacity)
        else:
            attrs['fill'] = 'none'
        
        # Handle stroke
        if hasattr(style, 'stroke') and style.stroke:
            stroke_color = self._color_to_svg(style.stroke.color)
            attrs['stroke'] = stroke_color
            attrs['stroke-width'] = str(style.stroke.width)
            
            if hasattr(style.stroke, 'opacity') and style.stroke.opacity < 1.0:
                attrs['stroke-opacity'] = str(style.stroke.opacity)
        else:
            attrs['stroke'] = 'none'
    
    def _color_to_svg(self, color) -> str:
        """Convert color to SVG format."""
        if hasattr(color, 'r') and hasattr(color, 'g') and hasattr(color, 'b'):
            return f"rgb({color.r},{color.g},{color.b})"
        return 'black'  # fallback
    
    def _get_transform_string(self, transform) -> str:
        """Convert transform to SVG format."""
        if not transform:
            return ''
        
        transforms = []
        
        # Translation
        if hasattr(transform, 'x') and hasattr(transform, 'y'):
            if transform.x != 0 or transform.y != 0:
                transforms.append(f"translate({transform.x},{transform.y})")
        
        # Rotation
        if hasattr(transform, 'rotation') and transform.rotation != 0:
            transforms.append(f"rotate({transform.rotation})")
        
        # Scale
        if hasattr(transform, 'scale_x') and hasattr(transform, 'scale_y'):
            if transform.scale_x != 1.0 or transform.scale_y != 1.0:
                transforms.append(f"scale({transform.scale_x},{transform.scale_y})")
        
        return ' '.join(transforms)
    
    def _sanitize_id(self, name: str) -> str:
        """Sanitize name for use as SVG ID."""
        # Replace invalid characters with underscores
        import re
        return re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    
    def _indent_xml(self, elem: ET.Element, level: int = 0):
        """Add indentation to XML for pretty printing."""
        indent = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = indent + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = indent
            for child in elem:
                self._indent_xml(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = indent
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = indent


def export_document_to_svg(document: DrawingDocument, filename: str, include_invisible: bool = False) -> str:
    """
    Convenience function to export a document to SVG.
    
    Args:
        document: Drawing document to export
        filename: Output SVG filename
        include_invisible: Whether to include invisible layers
        
    Returns:
        SVG content as string
    """
    exporter = SVGExporter(document)
    return exporter.export_to_svg(filename, include_invisible)


if __name__ == "__main__":
    # Example usage
    print("SVG Export Module - Test")
    
    # This would typically be used with a real document
    # from basic_shapes import create_basic_shapes_document
    # doc = create_basic_shapes_document()
    # svg_content = export_document_to_svg(doc, "test_output.svg")
    # print(f"Exported SVG with {len(svg_content)} characters")