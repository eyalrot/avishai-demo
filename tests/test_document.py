"""
Tests for the drawing document system.
"""

import pytest
from datetime import datetime
from typing import Dict, Any

from drawing_lib.document import (
    CanvasSize, BackgroundProperties, DocumentMetadata, ViewSettings,
    ExportSettings, DrawingDocument
)
from drawing_lib.types import Units
from drawing_lib.styles import RGBColor
from drawing_lib.shapes import Shape
from drawing_lib.types import ShapeType


class TestCanvasSize:
    """Test CanvasSize model."""
    
    def test_canvas_size_creation(self) -> None:
        """Test basic canvas size creation."""
        canvas = CanvasSize(width=800.0, height=600.0, units=Units.PIXELS)
        assert canvas.width == 800.0
        assert canvas.height == 600.0
        assert canvas.units == Units.PIXELS
    
    def test_canvas_size_validation(self) -> None:
        """Test canvas size validation."""
        # Valid canvas
        canvas = CanvasSize(width=100.0, height=50.0)
        assert canvas.width == 100.0
        
        # Invalid dimensions should raise validation error
        with pytest.raises(ValueError):
            CanvasSize(width=0.0, height=100.0)
        
        with pytest.raises(ValueError):
            CanvasSize(width=100.0, height=-50.0)
    
    def test_to_pixels_conversion(self) -> None:
        """Test unit conversion to pixels."""
        # Pixels (no conversion)
        canvas_px = CanvasSize(width=800.0, height=600.0, units=Units.PIXELS)
        px_width, px_height = canvas_px.to_pixels()
        assert px_width == 800.0
        assert px_height == 600.0
        
        # Inches to pixels (96 DPI default)
        canvas_in = CanvasSize(width=8.5, height=11.0, units=Units.INCHES)
        px_width, px_height = canvas_in.to_pixels()
        assert px_width == 8.5 * 96.0  # 816.0
        assert px_height == 11.0 * 96.0  # 1056.0
        
        # Custom DPI
        px_width, px_height = canvas_in.to_pixels(dpi=300.0)
        assert px_width == 8.5 * 300.0  # 2550.0
        assert px_height == 11.0 * 300.0  # 3300.0
        
        # Millimeters to pixels
        canvas_mm = CanvasSize(width=210.0, height=297.0, units=Units.MILLIMETERS)  # A4
        px_width, px_height = canvas_mm.to_pixels()
        expected_width = (210.0 / 25.4) * 96.0  # ~793.7
        expected_height = (297.0 / 25.4) * 96.0  # ~1122.5
        assert abs(px_width - expected_width) < 0.1
        assert abs(px_height - expected_height) < 0.1
        
        # Points to pixels
        canvas_pt = CanvasSize(width=72.0, height=144.0, units=Units.POINTS)
        px_width, px_height = canvas_pt.to_pixels()
        assert px_width == 96.0  # 72 points = 1 inch = 96 pixels
        assert px_height == 192.0  # 144 points = 2 inches = 192 pixels
    
    def test_aspect_ratio(self) -> None:
        """Test aspect ratio calculation."""
        # 16:9 aspect ratio
        canvas = CanvasSize(width=1920.0, height=1080.0)
        assert abs(canvas.get_aspect_ratio() - 16/9) < 0.001
        
        # Square aspect ratio
        square_canvas = CanvasSize(width=500.0, height=500.0)
        assert square_canvas.get_aspect_ratio() == 1.0
        
        # Portrait aspect ratio
        portrait_canvas = CanvasSize(width=600.0, height=800.0)
        assert portrait_canvas.get_aspect_ratio() == 0.75


class TestBackgroundProperties:
    """Test BackgroundProperties model."""
    
    def test_background_defaults(self) -> None:
        """Test default background properties."""
        bg = BackgroundProperties()
        assert bg.color is None
        assert bg.transparent is True
        assert bg.image_url is None
        assert bg.image_opacity == 1.0
    
    def test_background_with_color(self) -> None:
        """Test background with color."""
        color = RGBColor(r=240, g=240, b=240)
        bg = BackgroundProperties(color=color, transparent=False)
        assert bg.color == color
        assert bg.transparent is False
    
    def test_background_validation(self) -> None:
        """Test background validation logic."""
        # Non-transparent background without color should get default white
        bg = BackgroundProperties(transparent=False)
        assert bg.color is not None
        assert bg.color.r == 255  # Default white
        assert bg.color.g == 255
        assert bg.color.b == 255
    
    def test_background_with_image(self) -> None:
        """Test background with image."""
        bg = BackgroundProperties(
            image_url="https://example.com/bg.jpg",
            image_opacity=0.7
        )
        assert bg.image_url == "https://example.com/bg.jpg"
        assert bg.image_opacity == 0.7


class TestDocumentMetadata:
    """Test DocumentMetadata model."""
    
    def test_metadata_defaults(self) -> None:
        """Test default metadata values."""
        metadata = DocumentMetadata()
        assert metadata.title == "Untitled Document"
        assert metadata.description is None
        assert metadata.author is None
        assert metadata.keywords == []
        assert metadata.version == "1.0"
        assert metadata.app_version == "0.1.0"
        assert isinstance(metadata.created_at, datetime)
        assert isinstance(metadata.modified_at, datetime)
        assert metadata.custom_properties == {}
    
    def test_metadata_with_values(self) -> None:
        """Test metadata with custom values."""
        metadata = DocumentMetadata(
            title="My Drawing",
            description="A test drawing",
            author="Test Author",
            keywords=["test", "drawing", "vector"],
            version="2.1"
        )
        assert metadata.title == "My Drawing"
        assert metadata.description == "A test drawing"
        assert metadata.author == "Test Author"
        assert metadata.keywords == ["test", "drawing", "vector"]
        assert metadata.version == "2.1"
    
    def test_update_modified_time(self) -> None:
        """Test updating modified time."""
        metadata = DocumentMetadata()
        original_time = metadata.modified_at
        
        # Small delay to ensure different timestamp
        import time
        time.sleep(0.01)
        
        metadata.update_modified_time()
        assert metadata.modified_at > original_time


class TestViewSettings:
    """Test ViewSettings model."""
    
    def test_view_defaults(self) -> None:
        """Test default view settings."""
        view = ViewSettings()
        assert view.zoom_level == 1.0
        assert view.pan_x == 0.0
        assert view.pan_y == 0.0
        assert view.show_grid is False
        assert view.show_rulers is True
        assert view.show_guides is True
        assert view.snap_to_grid is False
        assert view.snap_to_guides is True
        assert view.grid_size == 10.0
        assert view.grid_color is not None
    
    def test_view_custom_settings(self) -> None:
        """Test custom view settings."""
        view = ViewSettings(
            zoom_level=2.0,
            pan_x=100.0,
            pan_y=-50.0,
            show_grid=True,
            snap_to_grid=True,
            grid_size=20.0
        )
        assert view.zoom_level == 2.0
        assert view.pan_x == 100.0
        assert view.pan_y == -50.0
        assert view.show_grid is True
        assert view.snap_to_grid is True
        assert view.grid_size == 20.0


class TestExportSettings:
    """Test ExportSettings model."""
    
    def test_export_defaults(self) -> None:
        """Test default export settings."""
        export = ExportSettings()
        assert export.default_format == "svg"
        assert export.dpi == 96.0
        assert export.quality == 0.9
        assert export.include_metadata is True
        assert export.transparent_background is True
    
    def test_export_custom_settings(self) -> None:
        """Test custom export settings."""
        export = ExportSettings(
            default_format="png",
            dpi=300.0,
            quality=0.8,
            include_metadata=False,
            transparent_background=False
        )
        assert export.default_format == "png"
        assert export.dpi == 300.0
        assert export.quality == 0.8
        assert export.include_metadata is False
        assert export.transparent_background is False


class TestDrawingDocument:
    """Test DrawingDocument model."""
    
    def test_document_creation(self) -> None:
        """Test basic document creation."""
        canvas = CanvasSize(width=800.0, height=600.0)
        doc = DrawingDocument(canvas=canvas)
        
        assert doc.canvas.width == 800.0
        assert doc.canvas.height == 600.0
        assert doc.id is not None
        assert doc.background is not None
        assert doc.layer_manager is not None
        assert doc.metadata is not None
        assert doc.view_settings is not None
        assert doc.export_settings is not None
    
    def test_document_shape_count(self) -> None:
        """Test shape counting in document."""
        canvas = CanvasSize(width=800.0, height=600.0)
        doc = DrawingDocument(canvas=canvas)
        
        # Empty document
        assert doc.get_total_shape_count() == 0
        
        # Add shapes to layers
        layer1 = doc.create_layer("Layer 1")
        layer2 = doc.create_layer("Layer 2")
        
        shape1 = Shape(type=ShapeType.RECTANGLE, geometry={"width": 100.0, "height": 50.0})
        shape2 = Shape(type=ShapeType.CIRCLE, geometry={"radius": 25.0})
        shape3 = Shape(type=ShapeType.LINE, geometry={"x1": 0, "y1": 0, "x2": 100, "y2": 100})
        
        layer1.add_shape(shape1)
        layer1.add_shape(shape2)
        layer2.add_shape(shape3)
        
        assert doc.get_total_shape_count() == 3
    
    def test_canvas_bounds_and_center(self) -> None:
        """Test canvas bounds and center calculations."""
        canvas = CanvasSize(width=800.0, height=600.0)
        doc = DrawingDocument(canvas=canvas)
        
        bounds = doc.get_canvas_bounds()
        assert bounds == (0.0, 0.0, 800.0, 600.0)
        
        center = doc.get_canvas_center()
        assert center == (400.0, 300.0)
    
    def test_update_metadata(self) -> None:
        """Test metadata updates."""
        canvas = CanvasSize(width=800.0, height=600.0)
        doc = DrawingDocument(canvas=canvas)
        
        original_time = doc.metadata.modified_at
        
        # Small delay to ensure different timestamp
        import time
        time.sleep(0.01)
        
        doc.update_metadata(title="Updated Title", author="New Author")
        
        assert doc.metadata.title == "Updated Title"
        assert doc.metadata.author == "New Author"
        assert doc.metadata.modified_at > original_time
    
    def test_set_canvas_size(self) -> None:
        """Test canvas size updates."""
        canvas = CanvasSize(width=800.0, height=600.0)
        doc = DrawingDocument(canvas=canvas)
        
        doc.set_canvas_size(1920.0, 1080.0, Units.PIXELS)
        
        assert doc.canvas.width == 1920.0
        assert doc.canvas.height == 1080.0
        assert doc.canvas.units == Units.PIXELS
    
    def test_create_new_document(self) -> None:
        """Test creating new document with factory method."""
        doc = DrawingDocument.create_new(
            title="Test Document",
            width=1200.0,
            height=800.0,
            units=Units.PIXELS,
            author="Test Author"
        )
        
        assert doc.metadata.title == "Test Document"
        assert doc.metadata.author == "Test Author"
        assert doc.canvas.width == 1200.0
        assert doc.canvas.height == 800.0
        assert doc.canvas.units == Units.PIXELS
        
        # Should have default layer
        assert doc.layer_manager.get_layer_count() == 1
        layers = doc.layer_manager.get_all_layers()
        assert layers[0].name == "Layer 1"
    
    def test_create_preset_documents(self) -> None:
        """Test creating documents with presets."""
        # Web preset
        web_doc = DrawingDocument.create_preset("web", title="Web Document")
        assert web_doc.canvas.width == 1920.0
        assert web_doc.canvas.height == 1080.0
        assert web_doc.canvas.units == Units.PIXELS
        assert web_doc.metadata.title == "Web Document"
        
        # Print A4 preset
        a4_doc = DrawingDocument.create_preset("print_a4", title="A4 Document")
        assert a4_doc.canvas.width == 210.0
        assert a4_doc.canvas.height == 297.0
        assert a4_doc.canvas.units == Units.MILLIMETERS
        
        # Mobile preset
        mobile_doc = DrawingDocument.create_preset("mobile")
        assert mobile_doc.canvas.width == 375.0
        assert mobile_doc.canvas.height == 667.0
        assert mobile_doc.canvas.units == Units.PIXELS
        
        # Invalid preset
        with pytest.raises(ValueError, match="Unknown preset"):
            DrawingDocument.create_preset("invalid_preset")
    
    def test_document_info(self) -> None:
        """Test document info generation."""
        doc = DrawingDocument.create_new(title="Info Test")
        layer = doc.create_layer("Test Layer")
        shape = Shape(type=ShapeType.RECTANGLE, geometry={"width": 100.0, "height": 50.0})
        layer.add_shape(shape)
        
        info = doc.get_document_info()
        
        assert info["title"] == "Info Test"
        assert info["canvas_size"] == "800.0x600.0 px"
        assert info["total_layers"] == 2  # Default layer + Test Layer
        assert info["total_shapes"] == 1
        assert info["visible_layers"] == 2
        assert info["background_transparent"] is True
        assert "created_at" in info
        assert "modified_at" in info
        assert info["version"] == "1.0"
        assert info["app_version"] == "0.1.0"
    
    def test_document_validation(self) -> None:
        """Test document validation."""
        # Valid document
        doc = DrawingDocument.create_new()
        layer = doc.create_layer("Test Layer")
        shape = Shape(type=ShapeType.CIRCLE, geometry={"radius": 25.0})
        layer.add_shape(shape)
        
        validation = doc.validate_document()
        assert len(validation["errors"]) == 0
        # May have warnings about empty default layer
        
        # Document with very large canvas
        large_doc = DrawingDocument.create_new(width=50000.0, height=50000.0)
        validation = large_doc.validate_document()
        assert any("performance" in warning.lower() for warning in validation["warnings"])
        
        # Document with no shapes
        empty_doc = DrawingDocument.create_new()
        validation = empty_doc.validate_document()
        assert any("no shapes" in warning.lower() for warning in validation["warnings"])
    
    def test_cleanup_empty_layers(self) -> None:
        """Test cleaning up empty layers."""
        doc = DrawingDocument.create_new()
        
        # Create some layers
        layer1 = doc.create_layer("Layer 1")  # Will have shape
        layer2 = doc.create_layer("Layer 2")  # Will be empty
        layer3 = doc.create_layer("Layer 3")  # Will be empty
        
        # Add shape to layer1
        shape = Shape(type=ShapeType.RECTANGLE, geometry={"width": 100.0, "height": 50.0})
        layer1.add_shape(shape)
        
        initial_count = doc.layer_manager.get_layer_count()
        removed_count = doc.cleanup_empty_layers()
        
        # Should remove empty layers (at least layer2, layer3, possibly default layer)
        assert removed_count >= 2
        assert doc.layer_manager.get_layer_count() < initial_count
        
        # layer1 should still exist (has shape)
        assert doc.layer_manager.find_layer_by_id(layer1.id) is not None
    
    def test_document_duplication(self) -> None:
        """Test document duplication."""
        # Create original document with content
        original = DrawingDocument.create_new(title="Original Document", author="Original Author")
        layer = original.create_layer("Test Layer")
        shape = Shape(type=ShapeType.CIRCLE, geometry={"radius": 25.0})
        layer.add_shape(shape)
        
        # Duplicate document
        duplicate = original.duplicate("Duplicated Document")
        
        # Should have different ID
        assert duplicate.id != original.id
        
        # Should have updated metadata
        assert duplicate.metadata.title == "Duplicated Document"
        assert duplicate.metadata.author == "Original Author"  # Preserved
        assert duplicate.metadata.created_at >= original.metadata.created_at
        
        # Should have same content structure
        assert duplicate.canvas.width == original.canvas.width
        assert duplicate.canvas.height == original.canvas.height
        assert duplicate.get_total_shape_count() == original.get_total_shape_count()
        assert duplicate.layer_manager.get_layer_count() == original.layer_manager.get_layer_count()
        
        # Duplicate without new title
        duplicate2 = original.duplicate()
        assert duplicate2.metadata.title == "Original Document (Copy)"


class TestDocumentSerialization:
    """Test document JSON serialization and deserialization."""
    
    def test_document_serialization(self) -> None:
        """Test complete document serialization round-trip."""
        # Create complex document
        doc = DrawingDocument.create_new(
            title="Serialization Test",
            width=1920.0,
            height=1080.0,
            author="Test Author"
        )
        
        # Add content
        layer1 = doc.create_layer("Background")
        layer2 = doc.create_layer("Content")
        group = doc.create_layer_group("UI Group")
        layer3 = doc.create_layer("UI", parent_group=group)
        
        # Add shapes
        rect = Shape(type=ShapeType.RECTANGLE, geometry={"width": 100.0, "height": 50.0})
        circle = Shape(type=ShapeType.CIRCLE, geometry={"radius": 25.0})
        layer1.add_shape(rect)
        layer2.add_shape(circle)
        
        # Update settings
        doc.view_settings.zoom_level = 1.5
        doc.view_settings.show_grid = True
        doc.export_settings.dpi = 300.0
        
        # Serialize to JSON
        json_data = doc.model_dump()
        
        # Deserialize back
        doc2 = DrawingDocument.model_validate(json_data)
        
        # Verify structure
        assert doc2.metadata.title == "Serialization Test"
        assert doc2.metadata.author == "Test Author"
        assert doc2.canvas.width == 1920.0
        assert doc2.canvas.height == 1080.0
        assert doc2.view_settings.zoom_level == 1.5
        assert doc2.view_settings.show_grid is True
        assert doc2.export_settings.dpi == 300.0
        
        # Verify layer structure
        assert doc2.layer_manager.get_layer_count() == 4  # Default + 3 created
        found_group = doc2.layer_manager.find_group_by_id(group.id)
        assert found_group is not None
        assert len(found_group.get_all_layers()) == 1
        
        # Verify shapes
        assert doc2.get_total_shape_count() == 2
    
    def test_preset_document_serialization(self) -> None:
        """Test serialization of preset documents."""
        presets_to_test = ["web", "print_a4", "mobile", "social_instagram"]
        
        for preset in presets_to_test:
            doc = DrawingDocument.create_preset(preset, title=f"Test {preset}")
            
            # Add some content
            layer = doc.create_layer(f"{preset} layer")
            shape = Shape(type=ShapeType.RECTANGLE, geometry={"width": 50.0, "height": 30.0})
            layer.add_shape(shape)
            
            # Serialize and deserialize
            json_data = doc.model_dump()
            doc2 = DrawingDocument.model_validate(json_data)
            
            # Verify basic structure preserved
            assert doc2.metadata.title == f"Test {preset}"
            assert doc2.canvas.width == doc.canvas.width
            assert doc2.canvas.height == doc.canvas.height
            assert doc2.canvas.units == doc.canvas.units
            assert doc2.get_total_shape_count() == 1