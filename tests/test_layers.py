"""
Tests for the layer management system.
"""

import pytest
from typing import List

from drawing_lib.layers import Layer, LayerGroup, LayerManager
from drawing_lib.shapes import Shape
from drawing_lib.types import ShapeType, BlendMode


class TestLayer:
    """Test Layer model."""
    
    def test_layer_creation(self) -> None:
        """Test basic layer creation."""
        layer = Layer(name="Test Layer")
        assert layer.name == "Test Layer"
        assert layer.shapes == []
        assert layer.z_index == 0
        assert layer.visible is True
        assert layer.locked is False
        assert layer.opacity == 1.0
        assert layer.blend_mode == BlendMode.NORMAL
        assert layer.parent_id is None
        assert layer.id is not None
    
    def test_layer_with_properties(self) -> None:
        """Test layer with custom properties."""
        layer = Layer(
            name="Custom Layer",
            z_index=5,
            visible=False,
            locked=True,
            opacity=0.5,
            blend_mode=BlendMode.MULTIPLY
        )
        assert layer.z_index == 5
        assert layer.visible is False
        assert layer.locked is True
        assert layer.opacity == 0.5
        assert layer.blend_mode == BlendMode.MULTIPLY
    
    def test_layer_opacity_validation(self) -> None:
        """Test layer opacity validation."""
        # Valid opacity
        layer = Layer(name="Test", opacity=0.5)
        assert layer.opacity == 0.5
        
        # Invalid opacity should raise validation error
        with pytest.raises(ValueError):
            Layer(name="Test", opacity=1.5)
        
        with pytest.raises(ValueError):
            Layer(name="Test", opacity=-0.1)
    
    def test_add_shape(self) -> None:
        """Test adding shapes to layer."""
        layer = Layer(name="Test Layer")
        
        # Add shape object
        shape = Shape(type=ShapeType.RECTANGLE, geometry={"width": 100.0, "height": 50.0})
        layer.add_shape(shape)
        assert len(layer.shapes) == 1
        assert shape in layer.shapes
        
        # Add shape by ID
        shape_id = "test-shape-id"
        layer.add_shape(shape_id)
        assert len(layer.shapes) == 2
        assert shape_id in layer.shapes
        
        # Adding same shape should not duplicate
        layer.add_shape(shape)
        assert len(layer.shapes) == 2
    
    def test_remove_shape(self) -> None:
        """Test removing shapes from layer."""
        layer = Layer(name="Test Layer")
        shape = Shape(type=ShapeType.CIRCLE, geometry={"radius": 25.0})
        shape_id = "test-shape-id"
        
        layer.add_shape(shape)
        layer.add_shape(shape_id)
        assert len(layer.shapes) == 2
        
        # Remove shape object
        success = layer.remove_shape(shape)
        assert success is True
        assert len(layer.shapes) == 1
        assert shape not in layer.shapes
        
        # Remove shape by ID
        success = layer.remove_shape(shape_id)
        assert success is True
        assert len(layer.shapes) == 0
        
        # Remove non-existent shape
        success = layer.remove_shape("non-existent")
        assert success is False
    
    def test_move_shape(self) -> None:
        """Test moving shapes within layer."""
        layer = Layer(name="Test Layer")
        shapes = ["shape1", "shape2", "shape3", "shape4"]
        
        for shape in shapes:
            layer.add_shape(shape)
        
        # Move shape from position 0 to position 2
        success = layer.move_shape("shape1", 2)
        assert success is True
        assert layer.shapes == ["shape2", "shape3", "shape1", "shape4"]
        
        # Move shape to front (last position)
        success = layer.move_shape("shape2", 3)
        assert success is True
        assert layer.shapes == ["shape3", "shape1", "shape4", "shape2"]
        
        # Move non-existent shape
        success = layer.move_shape("non-existent", 0)
        assert success is False
        
        # Move to invalid index (should clamp)
        success = layer.move_shape("shape3", 10)
        assert success is True
        assert layer.shapes[-1] == "shape3"  # Should be at end
    
    def test_layer_utility_methods(self) -> None:
        """Test layer utility methods."""
        layer = Layer(name="Test Layer")
        
        # Empty layer
        assert layer.get_shape_count() == 0
        assert layer.is_empty() is True
        
        # Add shapes
        layer.add_shape("shape1")
        layer.add_shape("shape2")
        assert layer.get_shape_count() == 2
        assert layer.is_empty() is False
        
        # Clear shapes
        layer.clear_shapes()
        assert layer.get_shape_count() == 0
        assert layer.is_empty() is True
    
    def test_get_shape_ids(self) -> None:
        """Test getting shape IDs from layer."""
        layer = Layer(name="Test Layer")
        
        # Add mix of Shape objects and IDs
        shape = Shape(type=ShapeType.LINE, geometry={"x1": 0, "y1": 0, "x2": 100, "y2": 100})
        shape_id = "direct-id"
        
        layer.add_shape(shape)
        layer.add_shape(shape_id)
        
        ids = layer.get_shape_ids()
        assert len(ids) == 2
        assert shape.id in ids
        assert shape_id in ids


class TestLayerGroup:
    """Test LayerGroup model."""
    
    def test_group_creation(self) -> None:
        """Test basic group creation."""
        group = LayerGroup(name="Test Group")
        assert group.name == "Test Group"
        assert group.children == []
        assert group.z_index == 0
        assert group.visible is True
        assert group.locked is False
        assert group.expanded is True
        assert group.opacity == 1.0
        assert group.blend_mode == BlendMode.NORMAL
        assert group.parent_id is None
        assert group.id is not None
    
    def test_add_child_layer(self) -> None:
        """Test adding child layers to group."""
        group = LayerGroup(name="Parent Group")
        layer = Layer(name="Child Layer")
        
        group.add_child(layer)
        assert len(group.children) == 1
        assert layer in group.children
        assert layer.parent_id == group.id
    
    def test_add_child_group(self) -> None:
        """Test adding child groups to group."""
        parent = LayerGroup(name="Parent Group")
        child = LayerGroup(name="Child Group")
        
        parent.add_child(child)
        assert len(parent.children) == 1
        assert child in parent.children
        assert child.parent_id == parent.id
    
    def test_remove_child(self) -> None:
        """Test removing children from group."""
        group = LayerGroup(name="Parent Group")
        layer = Layer(name="Child Layer")
        child_group = LayerGroup(name="Child Group")
        
        group.add_child(layer)
        group.add_child(child_group)
        assert len(group.children) == 2
        
        # Remove by object
        success = group.remove_child(layer)
        assert success is True
        assert len(group.children) == 1
        assert layer.parent_id is None
        
        # Remove by ID
        success = group.remove_child(child_group.id)
        assert success is True
        assert len(group.children) == 0
        assert child_group.parent_id is None
        
        # Remove non-existent child
        success = group.remove_child("non-existent")
        assert success is False
    
    def test_move_child(self) -> None:
        """Test moving children within group."""
        group = LayerGroup(name="Parent Group")
        layers = [Layer(name=f"Layer {i}") for i in range(4)]
        
        for layer in layers:
            group.add_child(layer)
        
        # Move by object
        success = group.move_child(layers[0], 2)
        assert success is True
        assert group.children[2] == layers[0]
        
        # Move by ID
        success = group.move_child(layers[1].id, 3)
        assert success is True
        assert group.children[3] == layers[1]
        
        # Move non-existent child
        success = group.move_child("non-existent", 0)
        assert success is False
    
    def test_get_all_layers(self) -> None:
        """Test getting all layers from group."""
        root = LayerGroup(name="Root")
        group1 = LayerGroup(name="Group 1")
        group2 = LayerGroup(name="Group 2")
        
        layer1 = Layer(name="Layer 1")
        layer2 = Layer(name="Layer 2")
        layer3 = Layer(name="Layer 3")
        
        # Build hierarchy: root -> group1 -> layer1, layer2
        #                        -> group2 -> layer3
        root.add_child(group1)
        root.add_child(group2)
        group1.add_child(layer1)
        group1.add_child(layer2)
        group2.add_child(layer3)
        
        # Get all layers recursively
        all_layers = root.get_all_layers(recursive=True)
        assert len(all_layers) == 3
        assert layer1 in all_layers
        assert layer2 in all_layers
        assert layer3 in all_layers
        
        # Get layers non-recursively
        direct_layers = root.get_all_layers(recursive=False)
        assert len(direct_layers) == 0  # No direct layer children
        
        # Get layers from group1
        group1_layers = group1.get_all_layers(recursive=True)
        assert len(group1_layers) == 2
        assert layer1 in group1_layers
        assert layer2 in group1_layers
    
    def test_get_all_shapes(self) -> None:
        """Test getting all shapes from group."""
        group = LayerGroup(name="Test Group")
        layer1 = Layer(name="Layer 1")
        layer2 = Layer(name="Layer 2")
        
        # Add shapes to layers
        layer1.add_shape("shape1")
        layer1.add_shape("shape2")
        layer2.add_shape("shape3")
        
        group.add_child(layer1)
        group.add_child(layer2)
        
        all_shapes = group.get_all_shapes()
        assert len(all_shapes) == 3
        assert "shape1" in all_shapes
        assert "shape2" in all_shapes
        assert "shape3" in all_shapes
    
    def test_find_layer_by_id(self) -> None:
        """Test finding layers by ID."""
        root = LayerGroup(name="Root")
        group1 = LayerGroup(name="Group 1")
        layer1 = Layer(name="Layer 1")
        layer2 = Layer(name="Layer 2")
        
        root.add_child(group1)
        group1.add_child(layer1)
        root.add_child(layer2)
        
        # Find existing layers
        found = root.find_layer_by_id(layer1.id)
        assert found == layer1
        
        found = root.find_layer_by_id(layer2.id)
        assert found == layer2
        
        # Find non-existent layer
        found = root.find_layer_by_id("non-existent")
        assert found is None
    
    def test_find_group_by_id(self) -> None:
        """Test finding groups by ID."""
        root = LayerGroup(name="Root")
        group1 = LayerGroup(name="Group 1")
        group2 = LayerGroup(name="Group 2")
        
        root.add_child(group1)
        group1.add_child(group2)
        
        # Find existing groups
        found = root.find_group_by_id(root.id)
        assert found == root
        
        found = root.find_group_by_id(group1.id)
        assert found == group1
        
        found = root.find_group_by_id(group2.id)
        assert found == group2
        
        # Find non-existent group
        found = root.find_group_by_id("non-existent")
        assert found is None
    
    def test_group_utility_methods(self) -> None:
        """Test group utility methods."""
        group = LayerGroup(name="Test Group")
        
        # Empty group
        assert group.get_child_count() == 0
        assert group.is_empty() is True
        
        # Add children
        group.add_child(Layer(name="Layer 1"))
        group.add_child(LayerGroup(name="Group 1"))
        assert group.get_child_count() == 2
        assert group.is_empty() is False


class TestLayerManager:
    """Test LayerManager system."""
    
    def test_manager_creation(self) -> None:
        """Test layer manager creation."""
        manager = LayerManager()
        assert manager.root_group.name == "Root"
        assert manager.active_layer_id is None
        assert len(manager.get_all_layers()) == 0
    
    def test_create_layer(self) -> None:
        """Test creating layers through manager."""
        manager = LayerManager()
        
        # Create first layer (should become active)
        layer1 = manager.create_layer("Layer 1")
        assert layer1.name == "Layer 1"
        assert manager.active_layer_id == layer1.id
        assert len(manager.get_all_layers()) == 1
        
        # Create second layer (should not change active)
        layer2 = manager.create_layer("Layer 2")
        assert manager.active_layer_id == layer1.id  # Still first layer
        assert len(manager.get_all_layers()) == 2
    
    def test_create_group(self) -> None:
        """Test creating groups through manager."""
        manager = LayerManager()
        
        group = manager.create_group("Test Group")
        assert group.name == "Test Group"
        assert group.parent_id == manager.root_group.id
        
        # Create layer in group
        layer = manager.create_layer("Layer in Group", parent_group=group)
        assert layer.parent_id == group.id
        assert len(group.get_all_layers()) == 1
    
    def test_delete_layer(self) -> None:
        """Test deleting layers through manager."""
        manager = LayerManager()
        
        layer1 = manager.create_layer("Layer 1")
        layer2 = manager.create_layer("Layer 2")
        assert len(manager.get_all_layers()) == 2
        
        # Delete layer
        success = manager.delete_layer(layer1.id)
        assert success is True
        assert len(manager.get_all_layers()) == 1
        assert manager.find_layer_by_id(layer1.id) is None
        
        # Active layer should be cleared if deleted
        if manager.active_layer_id == layer1.id:
            assert manager.active_layer_id is None
        
        # Delete non-existent layer
        success = manager.delete_layer("non-existent")
        assert success is False
    
    def test_delete_group(self) -> None:
        """Test deleting groups through manager."""
        manager = LayerManager()
        
        group = manager.create_group("Test Group")
        layer = manager.create_layer("Layer in Group", parent_group=group)
        
        # Delete group (should delete contained layers too)
        success = manager.delete_group(group.id)
        assert success is True
        assert manager.find_group_by_id(group.id) is None
        assert len(manager.get_all_layers()) == 0
        
        # Cannot delete root group
        success = manager.delete_group(manager.root_group.id)
        assert success is False
    
    def test_active_layer_management(self) -> None:
        """Test active layer management."""
        manager = LayerManager()
        
        layer1 = manager.create_layer("Layer 1")
        layer2 = manager.create_layer("Layer 2")
        
        # Set active layer
        success = manager.set_active_layer(layer2.id)
        assert success is True
        assert manager.active_layer_id == layer2.id
        
        # Get active layer
        active = manager.get_active_layer()
        assert active == layer2
        
        # Set non-existent layer as active
        success = manager.set_active_layer("non-existent")
        assert success is False
        assert manager.active_layer_id == layer2.id  # Should not change
    
    def test_layer_z_ordering(self) -> None:
        """Test layer z-ordering functionality."""
        manager = LayerManager()
        
        # Create layers with different z-indices
        layer1 = manager.create_layer("Layer 1")
        layer2 = manager.create_layer("Layer 2")
        layer3 = manager.create_layer("Layer 3")
        
        layer1.z_index = 2
        layer2.z_index = 1
        layer3.z_index = 3
        
        # Get layers by z-order
        ordered_layers = manager.get_layers_by_z_order()
        assert len(ordered_layers) == 3
        assert ordered_layers[0] == layer2  # z_index = 1
        assert ordered_layers[1] == layer1  # z_index = 2
        assert ordered_layers[2] == layer3  # z_index = 3
        
        # Reorder layers by z-index
        manager.reorder_layers_by_z_index()
        # This should sort children within groups by z_index
    
    def test_layer_filtering(self) -> None:
        """Test layer filtering methods."""
        manager = LayerManager()
        
        layer1 = manager.create_layer("Layer 1")
        layer2 = manager.create_layer("Layer 2")
        layer3 = manager.create_layer("Layer 3")
        
        # Set properties
        layer1.visible = True
        layer1.locked = False
        layer2.visible = False
        layer2.locked = True
        layer3.visible = True
        layer3.locked = True
        
        # Test visible layers
        visible = manager.get_visible_layers()
        assert len(visible) == 2
        assert layer1 in visible
        assert layer3 in visible
        
        # Test unlocked layers
        unlocked = manager.get_unlocked_layers()
        assert len(unlocked) == 1
        assert layer1 in unlocked
    
    def test_layer_count(self) -> None:
        """Test layer counting."""
        manager = LayerManager()
        
        assert manager.get_layer_count() == 0
        
        manager.create_layer("Layer 1")
        assert manager.get_layer_count() == 1
        
        group = manager.create_group("Group 1")
        manager.create_layer("Layer 2", parent_group=group)
        assert manager.get_layer_count() == 2
        
        manager.delete_layer(manager.get_all_layers()[0].id)
        assert manager.get_layer_count() == 1


class TestLayerSerialization:
    """Test layer JSON serialization and deserialization."""
    
    def test_layer_serialization(self) -> None:
        """Test layer serialization round-trip."""
        layer = Layer(
            name="Test Layer",
            z_index=5,
            visible=False,
            opacity=0.7,
            blend_mode=BlendMode.MULTIPLY
        )
        layer.add_shape("shape1")
        layer.add_shape("shape2")
        
        # Serialize to JSON
        json_data = layer.model_dump()
        
        # Deserialize back
        layer2 = Layer.model_validate(json_data)
        
        assert layer2.name == "Test Layer"
        assert layer2.z_index == 5
        assert layer2.visible is False
        assert layer2.opacity == 0.7
        assert layer2.blend_mode == BlendMode.MULTIPLY
        assert len(layer2.shapes) == 2
        assert "shape1" in layer2.shapes
        assert "shape2" in layer2.shapes
    
    def test_layer_group_serialization(self) -> None:
        """Test layer group serialization round-trip."""
        group = LayerGroup(name="Test Group", expanded=False)
        layer = Layer(name="Child Layer")
        group.add_child(layer)
        
        # Serialize to JSON
        json_data = group.model_dump()
        
        # Deserialize back
        group2 = LayerGroup.model_validate(json_data)
        
        assert group2.name == "Test Group"
        assert group2.expanded is False
        assert len(group2.children) == 1
        assert group2.children[0].name == "Child Layer"
    
    def test_layer_manager_serialization(self) -> None:
        """Test layer manager serialization round-trip."""
        manager = LayerManager()
        layer1 = manager.create_layer("Layer 1")
        group = manager.create_group("Group 1")
        layer2 = manager.create_layer("Layer 2", parent_group=group)
        
        # Serialize to JSON
        json_data = manager.model_dump()
        
        # Deserialize back
        manager2 = LayerManager.model_validate(json_data)
        
        assert len(manager2.get_all_layers()) == 2
        assert manager2.active_layer_id == layer1.id
        found_group = manager2.find_group_by_id(group.id)
        assert found_group is not None
        assert len(found_group.children) == 1