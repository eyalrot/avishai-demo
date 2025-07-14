"""Test the styles module."""

import pytest
from drawing_lib.styles import (
    RGBColor, RGBAColor, HSLColor, HexColor, GradientStop,
    LinearGradient, RadialGradient, PatternFill, FillProperties,
    StrokeProperties, ShadowEffect, BlurEffect, Effects
)
from drawing_lib.types import (
    FillType, LineCap, LineJoin, BlendMode, InvalidStyleError
)


class TestColorModels:
    """Test color model classes."""
    
    def test_rgb_color(self) -> None:
        """Test RGB color model."""
        color = RGBColor(r=255, g=128, b=64)
        assert color.r == 255
        assert color.g == 128
        assert color.b == 64
        assert color.to_hex() == "#ff8040"
        assert color.to_tuple() == (255, 128, 64)
    
    def test_rgba_color(self) -> None:
        """Test RGBA color model."""
        color = RGBAColor(r=255, g=128, b=64, a=0.5)
        assert color.r == 255
        assert color.g == 128
        assert color.b == 64
        assert color.a == 0.5
        assert color.to_hex() == "#ff804080"
        assert color.to_tuple() == (255, 128, 64, 0.5)
    
    def test_hsl_color(self) -> None:
        """Test HSL color model."""
        color = HSLColor(h=180.0, s=50.0, l=75.0)
        assert color.h == 180.0
        assert color.s == 50.0
        assert color.l == 75.0
        assert color.to_css() == "hsl(180.0, 50.0%, 75.0%)"
    
    def test_hex_color_valid(self) -> None:
        """Test valid hex color inputs."""
        # Test 6-character hex
        color1 = HexColor(value="#FF8040")
        assert color1.value == "#FF8040"
        
        # Test without #
        color2 = HexColor(value="FF8040")
        assert color2.value == "#FF8040"
        
        # Test 8-character hex with alpha
        color3 = HexColor(value="#FF804080")
        assert color3.value == "#FF804080"
        
        # Test conversion to RGB
        rgb = color1.to_rgb()
        assert rgb.r == 255
        assert rgb.g == 128
        assert rgb.b == 64
        
        # Test conversion to RGBA
        rgba = color3.to_rgba()
        assert rgba.r == 255
        assert rgba.g == 128
        assert rgba.b == 64
        assert abs(rgba.a - 0.5019607843137255) < 0.01  # 128/255
    
    def test_hex_color_invalid(self) -> None:
        """Test invalid hex color inputs."""
        with pytest.raises(InvalidStyleError):
            HexColor(value="#FF80")  # Too short
        
        with pytest.raises(InvalidStyleError):
            HexColor(value="#FF80403G")  # Invalid character
        
        with pytest.raises(InvalidStyleError):
            HexColor(value="#FF8040ABC")  # Too long


class TestGradients:
    """Test gradient models."""
    
    def test_gradient_stop(self) -> None:
        """Test gradient stop."""
        stop = GradientStop(
            position=0.5,
            color=RGBColor(r=255, g=0, b=0)
        )
        assert stop.position == 0.5
        assert isinstance(stop.color, RGBColor)
    
    def test_linear_gradient(self) -> None:
        """Test linear gradient."""
        stops = [
            GradientStop(position=0.0, color=RGBColor(r=255, g=0, b=0)),
            GradientStop(position=1.0, color=RGBColor(r=0, g=0, b=255))
        ]
        gradient = LinearGradient(
            start_x=0.0, start_y=0.0,
            end_x=1.0, end_y=1.0,
            stops=stops
        )
        assert gradient.start_x == 0.0
        assert gradient.end_y == 1.0
        assert len(gradient.stops) == 2
        assert gradient.id  # Should have generated ID
    
    def test_radial_gradient(self) -> None:
        """Test radial gradient."""
        stops = [
            GradientStop(position=0.0, color=RGBColor(r=255, g=255, b=255)),
            GradientStop(position=1.0, color=RGBColor(r=0, g=0, b=0))
        ]
        gradient = RadialGradient(
            center_x=0.5, center_y=0.5,
            radius=0.5,
            stops=stops
        )
        assert gradient.center_x == 0.5
        assert gradient.radius == 0.5
        assert len(gradient.stops) == 2
    
    def test_gradient_validation(self) -> None:
        """Test gradient stop validation."""
        # Test insufficient stops - this will raise a Pydantic ValidationError
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            LinearGradient(
                stops=[GradientStop(position=0.0, color=RGBColor(r=255, g=0, b=0))]
            )
        
        # Test duplicate positions
        with pytest.raises(InvalidStyleError):
            LinearGradient(
                stops=[
                    GradientStop(position=0.0, color=RGBColor(r=255, g=0, b=0)),
                    GradientStop(position=0.0, color=RGBColor(r=0, g=0, b=255))
                ]
            )


class TestFillProperties:
    """Test fill properties."""
    
    def test_solid_fill(self) -> None:
        """Test solid color fill."""
        fill = FillProperties(
            type=FillType.SOLID,
            color=RGBColor(r=255, g=128, b=64),
            opacity=0.8
        )
        assert fill.type == FillType.SOLID
        assert isinstance(fill.color, RGBColor)
        assert fill.opacity == 0.8
    
    def test_gradient_fill(self) -> None:
        """Test gradient fill."""
        stops = [
            GradientStop(position=0.0, color=RGBColor(r=255, g=0, b=0)),
            GradientStop(position=1.0, color=RGBColor(r=0, g=0, b=255))
        ]
        gradient = LinearGradient(stops=stops)
        
        fill = FillProperties(
            type=FillType.LINEAR_GRADIENT,
            linear_gradient=gradient
        )
        assert fill.type == FillType.LINEAR_GRADIENT
        assert fill.linear_gradient is not None
        assert fill.color is None  # Should be cleared
    
    def test_fill_validation(self) -> None:
        """Test fill properties validation."""
        # Test solid fill without color
        with pytest.raises(InvalidStyleError):
            FillProperties(type=FillType.SOLID)
        
        # Test gradient fill without gradient
        with pytest.raises(InvalidStyleError):
            FillProperties(type=FillType.LINEAR_GRADIENT)


class TestStrokeProperties:
    """Test stroke properties."""
    
    def test_basic_stroke(self) -> None:
        """Test basic stroke properties."""
        stroke = StrokeProperties(
            color=RGBColor(r=0, g=0, b=0),
            width=2.0,
            cap=LineCap.ROUND,
            join=LineJoin.ROUND
        )
        assert isinstance(stroke.color, RGBColor)
        assert stroke.width == 2.0
        assert stroke.cap == LineCap.ROUND
        assert stroke.join == LineJoin.ROUND
        assert stroke.opacity == 1.0
    
    def test_dashed_stroke(self) -> None:
        """Test dashed stroke."""
        stroke = StrokeProperties(
            color=RGBColor(r=0, g=0, b=0),
            width=1.0,
            dash_array=[5.0, 3.0, 2.0, 3.0],
            dash_offset=1.0
        )
        assert stroke.dash_array == [5.0, 3.0, 2.0, 3.0]
        assert stroke.dash_offset == 1.0
    
    def test_dash_validation(self) -> None:
        """Test dash array validation."""
        # Test negative dash values
        with pytest.raises(InvalidStyleError):
            StrokeProperties(
                color=RGBColor(r=0, g=0, b=0),
                dash_array=[5.0, -3.0]
            )
        
        # Test empty dash array (should be converted to None)
        stroke = StrokeProperties(
            color=RGBColor(r=0, g=0, b=0),
            dash_array=[]
        )
        assert stroke.dash_array is None


class TestEffects:
    """Test visual effects."""
    
    def test_shadow_effect(self) -> None:
        """Test shadow effect."""
        shadow = ShadowEffect(
            offset_x=2.0,
            offset_y=2.0,
            blur_radius=4.0,
            color=RGBAColor(r=0, g=0, b=0, a=0.5)
        )
        assert shadow.offset_x == 2.0
        assert shadow.offset_y == 2.0
        assert shadow.blur_radius == 4.0
        assert not shadow.inset
    
    def test_blur_effect(self) -> None:
        """Test blur effect."""
        blur = BlurEffect(radius=3.0)
        assert blur.radius == 3.0
    
    def test_effects_collection(self) -> None:
        """Test effects collection."""
        shadow1 = ShadowEffect(
            offset_x=1.0, offset_y=1.0,
            color=RGBAColor(r=0, g=0, b=0, a=0.3)
        )
        shadow2 = ShadowEffect(
            offset_x=3.0, offset_y=3.0,
            blur_radius=6.0,
            color=RGBAColor(r=0, g=0, b=0, a=0.1)
        )
        blur = BlurEffect(radius=2.0)
        
        effects = Effects(
            shadows=[shadow1, shadow2],
            blur=blur,
            opacity=0.9,
            blend_mode=BlendMode.MULTIPLY
        )
        
        assert len(effects.shadows) == 2
        assert effects.blur is not None
        assert effects.opacity == 0.9
        assert effects.blend_mode == BlendMode.MULTIPLY


class TestPatternFill:
    """Test pattern fill."""
    
    def test_pattern_fill(self) -> None:
        """Test pattern fill properties."""
        pattern = PatternFill(
            image_data="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
            width=10.0,
            height=10.0,
            repeat_x=True,
            repeat_y=False
        )
        assert pattern.width == 10.0
        assert pattern.height == 10.0
        assert pattern.repeat_x
        assert not pattern.repeat_y
        assert pattern.id  # Should have generated ID