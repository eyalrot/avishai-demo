"""Styling system models for colors, fills, strokes, and effects."""

from typing import List, Optional, Union, Tuple, Any
from pydantic import BaseModel, Field, field_validator, model_validator
import re

from .types import (
    BlendMode, LineCap, LineJoin, FillType, Coordinate, 
    InvalidStyleError, generate_id
)


class RGBColor(BaseModel):
    """RGB color model with values from 0-255."""
    
    r: int = Field(..., ge=0, le=255, description="Red component (0-255)")
    g: int = Field(..., ge=0, le=255, description="Green component (0-255)")
    b: int = Field(..., ge=0, le=255, description="Blue component (0-255)")
    
    def to_hex(self) -> str:
        """Convert to hex string format."""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
    
    def to_tuple(self) -> Tuple[int, int, int]:
        """Convert to RGB tuple."""
        return (self.r, self.g, self.b)


class RGBAColor(BaseModel):
    """RGBA color model with values from 0-255 and alpha 0.0-1.0."""
    
    r: int = Field(..., ge=0, le=255, description="Red component (0-255)")
    g: int = Field(..., ge=0, le=255, description="Green component (0-255)")
    b: int = Field(..., ge=0, le=255, description="Blue component (0-255)")
    a: float = Field(..., ge=0.0, le=1.0, description="Alpha component (0.0-1.0)")
    
    def to_hex(self) -> str:
        """Convert to hex string format with alpha."""
        alpha_hex = format(round(self.a * 255), '02x')
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}{alpha_hex}"
    
    def to_tuple(self) -> Tuple[int, int, int, float]:
        """Convert to RGBA tuple."""
        return (self.r, self.g, self.b, self.a)


class HSLColor(BaseModel):
    """HSL color model with hue (0-360), saturation and lightness (0-100)."""
    
    h: float = Field(..., ge=0.0, le=360.0, description="Hue (0-360)")
    s: float = Field(..., ge=0.0, le=100.0, description="Saturation (0-100)")
    l: float = Field(..., ge=0.0, le=100.0, description="Lightness (0-100)")
    
    def to_css(self) -> str:
        """Convert to CSS HSL format."""
        return f"hsl({self.h}, {self.s}%, {self.l}%)"


class HexColor(BaseModel):
    """Hex color model with validation."""
    
    value: str = Field(..., description="Hex color value (e.g., '#FF0000' or '#FF0000FF')")
    
    @field_validator('value')
    @classmethod
    def validate_hex_color(cls, v: str) -> str:
        """Validate hex color format."""
        if not isinstance(v, str):
            raise InvalidStyleError("Hex color must be a string")
        
        # Remove # if present
        if v.startswith('#'):
            v = v[1:]
        
        # Check length (6 for RGB, 8 for RGBA)
        if len(v) not in [6, 8]:
            raise InvalidStyleError("Hex color must be 6 or 8 characters long")
        
        # Check if all characters are valid hex
        if not re.match(r'^[0-9A-Fa-f]+$', v):
            raise InvalidStyleError("Hex color contains invalid characters")
        
        return f"#{v.upper()}"
    
    def to_rgb(self) -> RGBColor:
        """Convert to RGB color."""
        hex_value = self.value[1:]  # Remove #
        r = int(hex_value[0:2], 16)
        g = int(hex_value[2:4], 16)
        b = int(hex_value[4:6], 16)
        return RGBColor(r=r, g=g, b=b)
    
    def to_rgba(self) -> RGBAColor:
        """Convert to RGBA color."""
        hex_value = self.value[1:]  # Remove #
        r = int(hex_value[0:2], 16)
        g = int(hex_value[2:4], 16)
        b = int(hex_value[4:6], 16)
        a = 1.0
        if len(hex_value) == 8:
            a = int(hex_value[6:8], 16) / 255.0
        return RGBAColor(r=r, g=g, b=b, a=a)


# Union type for all color models
Color = Union[RGBColor, RGBAColor, HSLColor, HexColor]


class GradientStop(BaseModel):
    """A color stop in a gradient."""
    
    position: float = Field(..., ge=0.0, le=1.0, description="Position along gradient (0.0-1.0)")
    color: Color = Field(..., description="Color at this position")


class LinearGradient(BaseModel):
    """Linear gradient definition."""
    
    id: str = Field(default_factory=generate_id, description="Unique gradient ID")
    start_x: Coordinate = Field(0.0, description="Starting X coordinate")
    start_y: Coordinate = Field(0.0, description="Starting Y coordinate") 
    end_x: Coordinate = Field(1.0, description="Ending X coordinate")
    end_y: Coordinate = Field(1.0, description="Ending Y coordinate")
    stops: List[GradientStop] = Field(..., min_length=2, description="Color stops")
    
    @field_validator('stops')
    @classmethod
    def validate_stops(cls, v: List[GradientStop]) -> List[GradientStop]:
        """Validate gradient stops are properly ordered."""
        if len(v) < 2:
            raise InvalidStyleError("Gradient must have at least 2 color stops")
        
        # Sort by position
        sorted_stops = sorted(v, key=lambda stop: stop.position)
        
        # Check for duplicate positions
        positions = [stop.position for stop in sorted_stops]
        if len(set(positions)) != len(positions):
            raise InvalidStyleError("Gradient stops cannot have duplicate positions")
        
        return sorted_stops


class RadialGradient(BaseModel):
    """Radial gradient definition."""
    
    id: str = Field(default_factory=generate_id, description="Unique gradient ID")
    center_x: Coordinate = Field(0.5, description="Center X coordinate")
    center_y: Coordinate = Field(0.5, description="Center Y coordinate")
    radius: Coordinate = Field(0.5, ge=0.0, description="Gradient radius")
    stops: List[GradientStop] = Field(..., min_length=2, description="Color stops")
    
    @field_validator('stops')
    @classmethod
    def validate_stops(cls, v: List[GradientStop]) -> List[GradientStop]:
        """Validate gradient stops are properly ordered."""
        if len(v) < 2:
            raise InvalidStyleError("Gradient must have at least 2 color stops")
        
        # Sort by position
        sorted_stops = sorted(v, key=lambda stop: stop.position)
        
        # Check for duplicate positions
        positions = [stop.position for stop in sorted_stops]
        if len(set(positions)) != len(positions):
            raise InvalidStyleError("Gradient stops cannot have duplicate positions")
        
        return sorted_stops


class PatternFill(BaseModel):
    """Pattern fill definition."""
    
    id: str = Field(default_factory=generate_id, description="Unique pattern ID")
    image_data: str = Field(..., description="Base64 encoded image data or URL")
    width: Coordinate = Field(..., gt=0, description="Pattern width")
    height: Coordinate = Field(..., gt=0, description="Pattern height")
    repeat_x: bool = Field(True, description="Repeat pattern horizontally")
    repeat_y: bool = Field(True, description="Repeat pattern vertically")


class FillProperties(BaseModel):
    """Fill properties for shapes."""
    
    type: FillType = Field(FillType.SOLID, description="Type of fill")
    color: Optional[Color] = Field(None, description="Solid color fill")
    linear_gradient: Optional[LinearGradient] = Field(None, description="Linear gradient fill")
    radial_gradient: Optional[RadialGradient] = Field(None, description="Radial gradient fill")
    pattern: Optional[PatternFill] = Field(None, description="Pattern fill")
    opacity: float = Field(1.0, ge=0.0, le=1.0, description="Fill opacity")
    
    @model_validator(mode='after')
    def validate_fill_consistency(self) -> 'FillProperties':
        """Validate that fill type matches the provided fill data."""
        if self.type == FillType.SOLID and not self.color:
            raise InvalidStyleError("Solid fill requires a color")
        elif self.type == FillType.LINEAR_GRADIENT and not self.linear_gradient:
            raise InvalidStyleError("Linear gradient fill requires linear_gradient data")
        elif self.type == FillType.RADIAL_GRADIENT and not self.radial_gradient:
            raise InvalidStyleError("Radial gradient fill requires radial_gradient data")
        elif self.type == FillType.PATTERN and not self.pattern:
            raise InvalidStyleError("Pattern fill requires pattern data")
        
        # Clear unused fill data
        if self.type != FillType.SOLID:
            self.color = None
        if self.type != FillType.LINEAR_GRADIENT:
            self.linear_gradient = None
        if self.type != FillType.RADIAL_GRADIENT:
            self.radial_gradient = None
        if self.type != FillType.PATTERN:
            self.pattern = None
        
        return self


class StrokeProperties(BaseModel):
    """Stroke properties for shapes."""
    
    color: Color = Field(..., description="Stroke color")
    width: Coordinate = Field(1.0, gt=0.0, description="Stroke width")
    cap: LineCap = Field(LineCap.BUTT, description="Line cap style")
    join: LineJoin = Field(LineJoin.MITER, description="Line join style")
    miter_limit: float = Field(4.0, gt=0.0, description="Miter limit for miter joins")
    dash_array: Optional[List[float]] = Field(None, description="Dash pattern array")
    dash_offset: float = Field(0.0, description="Dash pattern offset")
    opacity: float = Field(1.0, ge=0.0, le=1.0, description="Stroke opacity")
    
    @field_validator('dash_array')
    @classmethod
    def validate_dash_array(cls, v: Optional[List[float]]) -> Optional[List[float]]:
        """Validate dash array values."""
        if v is not None:
            if len(v) == 0:
                return None
            if any(val < 0 for val in v):
                raise InvalidStyleError("Dash array values cannot be negative")
        return v


class ShadowEffect(BaseModel):
    """Drop shadow effect."""
    
    offset_x: Coordinate = Field(0.0, description="Horizontal shadow offset")
    offset_y: Coordinate = Field(0.0, description="Vertical shadow offset")
    blur_radius: Coordinate = Field(0.0, ge=0.0, description="Shadow blur radius")
    spread_radius: Coordinate = Field(0.0, description="Shadow spread radius")
    color: Color = Field(..., description="Shadow color")
    inset: bool = Field(False, description="Inner shadow")


class BlurEffect(BaseModel):
    """Blur effect."""
    
    radius: Coordinate = Field(0.0, ge=0.0, description="Blur radius")


class Effects(BaseModel):
    """Collection of visual effects."""
    
    shadows: List[ShadowEffect] = Field(default_factory=list, description="Drop shadows")
    blur: Optional[BlurEffect] = Field(None, description="Blur effect")
    opacity: float = Field(1.0, ge=0.0, le=1.0, description="Overall opacity")
    blend_mode: BlendMode = Field(BlendMode.NORMAL, description="Blend mode")