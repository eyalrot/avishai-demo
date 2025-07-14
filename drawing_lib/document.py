"""
Drawing document model with canvas properties, metadata, and version management.
"""

from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
from pydantic import BaseModel, Field, model_validator

from .types import ID, Units, generate_id
from .styles import Color, RGBColor
from .layers import LayerManager


class CanvasSize(BaseModel):
    """Canvas size with units."""
    
    width: float = Field(..., gt=0.0, description="Canvas width")
    height: float = Field(..., gt=0.0, description="Canvas height")
    units: Units = Field(Units.PIXELS, description="Measurement units")
    
    def to_pixels(self, dpi: float = 96.0) -> Tuple[float, float]:
        """
        Convert canvas size to pixels.
        
        Args:
            dpi: Dots per inch for conversion
            
        Returns:
            Tuple of (width_px, height_px)
        """
        if self.units == Units.PIXELS:
            return (self.width, self.height)
        elif self.units == Units.INCHES:
            return (self.width * dpi, self.height * dpi)
        elif self.units == Units.MILLIMETERS:
            # 1 inch = 25.4 mm
            inches_width = self.width / 25.4
            inches_height = self.height / 25.4
            return (inches_width * dpi, inches_height * dpi)
        elif self.units == Units.CENTIMETERS:
            # 1 inch = 2.54 cm
            inches_width = self.width / 2.54
            inches_height = self.height / 2.54
            return (inches_width * dpi, inches_height * dpi)
        elif self.units == Units.POINTS:
            # 1 inch = 72 points
            inches_width = self.width / 72.0
            inches_height = self.height / 72.0
            return (inches_width * dpi, inches_height * dpi)
        else:
            # Default to pixels if unknown unit
            return (self.width, self.height)
    
    def get_aspect_ratio(self) -> float:
        """Get the aspect ratio (width/height)."""
        return self.width / self.height


class BackgroundProperties(BaseModel):
    """Background properties for the canvas."""
    
    color: Optional[Color] = Field(None, description="Background color")
    transparent: bool = Field(True, description="Whether background is transparent")
    image_url: Optional[str] = Field(None, description="Background image URL")
    image_opacity: float = Field(1.0, ge=0.0, le=1.0, description="Background image opacity")
    
    @model_validator(mode='after')
    def validate_background(self) -> 'BackgroundProperties':
        """Validate background properties consistency."""
        if not self.transparent and self.color is None:
            # Default to white background if not transparent and no color specified
            self.color = RGBColor(r=255, g=255, b=255)
        
        return self


class DocumentMetadata(BaseModel):
    """Document metadata and version information."""
    
    title: str = Field("Untitled Document", description="Document title")
    description: Optional[str] = Field(None, description="Document description")
    author: Optional[str] = Field(None, description="Document author")
    keywords: List[str] = Field(default_factory=list, description="Document keywords/tags")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    modified_at: datetime = Field(default_factory=datetime.now, description="Last modification timestamp")
    version: str = Field("1.0", description="Document version")
    app_version: str = Field("0.1.0", description="Application version that created/modified this document")
    custom_properties: Dict[str, Any] = Field(default_factory=dict, description="Custom metadata properties")
    
    def update_modified_time(self) -> None:
        """Update the modified timestamp to now."""
        self.modified_at = datetime.now()


class ViewSettings(BaseModel):
    """View settings for the document canvas."""
    
    zoom_level: float = Field(1.0, gt=0.0, description="Zoom level (1.0 = 100%)")
    pan_x: float = Field(0.0, description="Horizontal pan offset")
    pan_y: float = Field(0.0, description="Vertical pan offset")
    show_grid: bool = Field(False, description="Whether to show grid")
    show_rulers: bool = Field(True, description="Whether to show rulers")
    show_guides: bool = Field(True, description="Whether to show guides")
    snap_to_grid: bool = Field(False, description="Whether to snap to grid")
    snap_to_guides: bool = Field(True, description="Whether to snap to guides")
    grid_size: float = Field(10.0, gt=0.0, description="Grid size in canvas units")
    grid_color: Color = Field(default_factory=lambda: RGBColor(r=200, g=200, b=200), description="Grid color")


class ExportSettings(BaseModel):
    """Export settings for the document."""
    
    default_format: str = Field("svg", description="Default export format")
    dpi: float = Field(96.0, gt=0.0, description="Default DPI for raster exports")
    quality: float = Field(0.9, ge=0.0, le=1.0, description="Export quality for lossy formats")
    include_metadata: bool = Field(True, description="Whether to include metadata in exports")
    transparent_background: bool = Field(True, description="Whether to export with transparent background")


class DrawingDocument(BaseModel):
    """
    Top-level drawing document model.
    
    Contains all elements of a drawing document:
    - Canvas properties and background
    - Layer hierarchy with shapes
    - Document metadata and version info
    - View and export settings
    - Full serialization support
    """
    
    id: ID = Field(default_factory=generate_id, description="Unique document identifier")
    canvas: CanvasSize = Field(..., description="Canvas size and units")
    background: BackgroundProperties = Field(default_factory=BackgroundProperties, description="Background properties")  # type: ignore
    layer_manager: LayerManager = Field(default_factory=LayerManager, description="Layer management system")  # type: ignore
    metadata: DocumentMetadata = Field(default_factory=DocumentMetadata, description="Document metadata")  # type: ignore
    view_settings: ViewSettings = Field(default_factory=ViewSettings, description="View settings")  # type: ignore
    export_settings: ExportSettings = Field(default_factory=ExportSettings, description="Export settings")  # type: ignore
    
    def get_total_shape_count(self) -> int:
        """Get total number of shapes in the document."""
        total = 0
        for layer in self.layer_manager.get_all_layers():
            total += layer.get_shape_count()
        return total
    
    def get_canvas_bounds(self) -> Tuple[float, float, float, float]:
        """
        Get canvas bounds in canvas units.
        
        Returns:
            Tuple of (min_x, min_y, max_x, max_y)
        """
        return (0.0, 0.0, self.canvas.width, self.canvas.height)
    
    def get_canvas_center(self) -> Tuple[float, float]:
        """
        Get canvas center point.
        
        Returns:
            Tuple of (center_x, center_y)
        """
        return (self.canvas.width / 2.0, self.canvas.height / 2.0)
    
    def update_metadata(self, **kwargs: Any) -> None:
        """
        Update document metadata and refresh modified time.
        
        Args:
            **kwargs: Metadata fields to update
        """
        for key, value in kwargs.items():
            if hasattr(self.metadata, key):
                setattr(self.metadata, key, value)
        
        self.metadata.update_modified_time()
    
    def set_canvas_size(self, width: float, height: float, units: Units = Units.PIXELS) -> None:
        """
        Set canvas size and update metadata.
        
        Args:
            width: Canvas width
            height: Canvas height
            units: Measurement units
        """
        self.canvas = CanvasSize(width=width, height=height, units=units)
        self.metadata.update_modified_time()
    
    def create_layer(self, name: str, **kwargs: Any) -> Any:
        """
        Create a new layer and update metadata.
        
        Args:
            name: Layer name
            **kwargs: Additional layer properties
            
        Returns:
            The created Layer object
        """
        layer = self.layer_manager.create_layer(name, **kwargs)
        self.metadata.update_modified_time()
        return layer
    
    def create_layer_group(self, name: str, **kwargs: Any) -> Any:
        """
        Create a new layer group and update metadata.
        
        Args:
            name: Group name
            **kwargs: Additional group properties
            
        Returns:
            The created LayerGroup object
        """
        group = self.layer_manager.create_group(name, **kwargs)
        self.metadata.update_modified_time()
        return group
    
    def get_document_info(self) -> Dict[str, Any]:
        """
        Get summary information about the document.
        
        Returns:
            Dictionary with document statistics and info
        """
        return {
            "id": self.id,
            "title": self.metadata.title,
            "canvas_size": f"{self.canvas.width}x{self.canvas.height} {self.canvas.units.value}",
            "canvas_aspect_ratio": round(self.canvas.get_aspect_ratio(), 2),
            "total_layers": self.layer_manager.get_layer_count(),
            "total_shapes": self.get_total_shape_count(),
            "visible_layers": len(self.layer_manager.get_visible_layers()),
            "background_transparent": self.background.transparent,
            "created_at": self.metadata.created_at.isoformat(),
            "modified_at": self.metadata.modified_at.isoformat(),
            "version": self.metadata.version,
            "app_version": self.metadata.app_version
        }
    
    def validate_document(self) -> Dict[str, List[str]]:
        """
        Validate document integrity and return any issues found.
        
        Returns:
            Dictionary with validation results, empty if no issues
        """
        issues: Dict[str, List[str]] = {
            "errors": [],
            "warnings": []
        }
        
        # Check canvas size
        if self.canvas.width <= 0 or self.canvas.height <= 0:
            issues["errors"].append("Canvas size must be positive")
        
        # Check for very large canvas (potential performance issue)
        canvas_px = self.canvas.to_pixels()
        total_pixels = canvas_px[0] * canvas_px[1]
        if total_pixels > 100_000_000:  # 100 megapixels
            issues["warnings"].append("Very large canvas may impact performance")
        
        # Check for empty document
        if self.get_total_shape_count() == 0:
            issues["warnings"].append("Document contains no shapes")
        
        # Check for layers without shapes
        empty_layers = [layer.name for layer in self.layer_manager.get_all_layers() if layer.is_empty()]
        if empty_layers:
            issues["warnings"].append(f"Empty layers found: {', '.join(empty_layers)}")
        
        return issues
    
    def cleanup_empty_layers(self) -> int:
        """
        Remove empty layers from the document.
        
        Returns:
            Number of layers removed
        """
        empty_layers = [layer for layer in self.layer_manager.get_all_layers() if layer.is_empty()]
        removed_count = 0
        
        for layer in empty_layers:
            if self.layer_manager.delete_layer(layer.id):
                removed_count += 1
        
        if removed_count > 0:
            self.metadata.update_modified_time()
        
        return removed_count
    
    @classmethod
    def create_new(
        cls,
        title: str = "New Document",
        width: float = 800.0,
        height: float = 600.0,
        units: Units = Units.PIXELS,
        author: Optional[str] = None
    ) -> 'DrawingDocument':
        """
        Create a new document with default settings.
        
        Args:
            title: Document title
            width: Canvas width
            height: Canvas height
            units: Canvas units
            author: Document author
            
        Returns:
            New DrawingDocument instance
        """
        canvas = CanvasSize(width=width, height=height, units=units)
        metadata = DocumentMetadata(title=title, author=author)  # type: ignore
        
        doc = cls(canvas=canvas, metadata=metadata)
        
        # Create a default layer
        doc.create_layer("Layer 1")
        
        return doc
    
    @classmethod
    def create_preset(cls, preset: str, **kwargs: Any) -> 'DrawingDocument':
        """
        Create a document with preset dimensions.
        
        Args:
            preset: Preset name (e.g., "web", "print", "mobile", "4k")
            **kwargs: Additional arguments passed to create_new
            
        Returns:
            New DrawingDocument instance
        """
        presets = {
            "web": {"width": 1920.0, "height": 1080.0, "units": Units.PIXELS},
            "web_hd": {"width": 1920.0, "height": 1080.0, "units": Units.PIXELS},
            "web_4k": {"width": 3840.0, "height": 2160.0, "units": Units.PIXELS},
            "mobile": {"width": 375.0, "height": 667.0, "units": Units.PIXELS},
            "tablet": {"width": 768.0, "height": 1024.0, "units": Units.PIXELS},
            "print_letter": {"width": 8.5, "height": 11.0, "units": Units.INCHES},
            "print_a4": {"width": 210.0, "height": 297.0, "units": Units.MILLIMETERS},
            "print_a3": {"width": 297.0, "height": 420.0, "units": Units.MILLIMETERS},
            "social_instagram": {"width": 1080.0, "height": 1080.0, "units": Units.PIXELS},
            "social_facebook": {"width": 1200.0, "height": 630.0, "units": Units.PIXELS},
            "social_twitter": {"width": 1024.0, "height": 512.0, "units": Units.PIXELS},
        }
        
        if preset not in presets:
            raise ValueError(f"Unknown preset: {preset}. Available: {list(presets.keys())}")
        
        preset_config = presets[preset]
        merged_config = {**preset_config, **kwargs}
        
        return cls.create_new(**merged_config)
    
    def duplicate(self, new_title: Optional[str] = None) -> 'DrawingDocument':
        """
        Create a duplicate of this document.
        
        Args:
            new_title: Title for the duplicated document
            
        Returns:
            New DrawingDocument instance
        """
        # Serialize and deserialize to create a deep copy
        doc_data = self.model_dump()
        
        # Create new document with fresh ID and metadata
        new_doc = DrawingDocument.model_validate(doc_data)
        new_doc.id = generate_id()
        
        if new_title:
            new_doc.metadata.title = new_title
        else:
            new_doc.metadata.title = f"{self.metadata.title} (Copy)"
        
        # Reset timestamps
        now = datetime.now()
        new_doc.metadata.created_at = now
        new_doc.metadata.modified_at = now
        
        return new_doc