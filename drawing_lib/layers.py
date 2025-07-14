"""
Layer management system for organizing shapes with z-ordering and hierarchy.
"""

from typing import List, Optional, Union, Any, Dict
from pydantic import BaseModel, Field

from .types import ID, BlendMode, generate_id
from .shapes import Shape


class Layer(BaseModel):
    """
    Layer model for organizing shapes with z-ordering and visibility controls.
    
    Layers provide hierarchical organization of shapes with support for:
    - Shape collection and management
    - Z-ordering for layering control
    - Visibility and locking states
    - Opacity and blend mode effects
    - Layer naming and metadata
    """
    
    id: ID = Field(default_factory=generate_id, description="Unique layer identifier")
    name: str = Field(..., description="Layer name")
    shapes: List[Union[ID, Shape]] = Field(default_factory=list, description="Shapes in this layer")
    z_index: int = Field(0, description="Z-order position (higher = front)")
    visible: bool = Field(True, description="Layer visibility")
    locked: bool = Field(False, description="Layer editing lock")
    opacity: float = Field(1.0, ge=0.0, le=1.0, description="Layer opacity")
    blend_mode: BlendMode = Field(BlendMode.NORMAL, description="Layer blend mode")
    parent_id: Optional[ID] = Field(None, description="Parent layer group ID")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional layer metadata")
    
    def add_shape(self, shape: Union[Shape, ID]) -> None:
        """Add a shape to this layer."""
        if shape not in self.shapes:
            self.shapes.append(shape)
    
    def remove_shape(self, shape: Union[Shape, ID]) -> bool:
        """
        Remove a shape from this layer.
        
        Returns:
            True if shape was found and removed, False otherwise
        """
        try:
            self.shapes.remove(shape)
            return True
        except ValueError:
            return False
    
    def move_shape(self, shape: Union[Shape, ID], new_index: int) -> bool:
        """
        Move a shape to a new position within the layer.
        
        Args:
            shape: Shape or shape ID to move
            new_index: New index position (0 = bottom, len(shapes)-1 = top)
            
        Returns:
            True if shape was found and moved, False otherwise
        """
        try:
            current_index = self.shapes.index(shape)
            shape_obj = self.shapes.pop(current_index)
            
            # Clamp index to valid range
            new_index = max(0, min(new_index, len(self.shapes)))
            self.shapes.insert(new_index, shape_obj)
            return True
        except ValueError:
            return False
    
    def get_shape_count(self) -> int:
        """Get the number of shapes in this layer."""
        return len(self.shapes)
    
    def is_empty(self) -> bool:
        """Check if this layer has no shapes."""
        return len(self.shapes) == 0
    
    def clear_shapes(self) -> None:
        """Remove all shapes from this layer."""
        self.shapes.clear()
    
    def get_shape_ids(self) -> List[ID]:
        """
        Get list of shape IDs in this layer.
        
        Returns:
            List of shape IDs, extracting IDs from Shape objects when needed
        """
        ids = []
        for shape in self.shapes:
            if isinstance(shape, Shape):
                ids.append(shape.id)
            else:
                ids.append(shape)
        return ids


class LayerGroup(BaseModel):
    """
    Layer group for hierarchical organization of layers.
    
    LayerGroups provide folder-like organization with:
    - Nested layer and group structure
    - Collective visibility and locking
    - Group-level transformations and effects
    - Expanded/collapsed display states
    """
    
    id: ID = Field(default_factory=generate_id, description="Unique group identifier")
    name: str = Field(..., description="Group name")
    children: List[Union['LayerGroup', Layer]] = Field(default_factory=list, description="Child layers and groups")
    z_index: int = Field(0, description="Z-order position among siblings")
    visible: bool = Field(True, description="Group visibility (affects all children)")
    locked: bool = Field(False, description="Group editing lock (affects all children)")
    expanded: bool = Field(True, description="UI expansion state")
    opacity: float = Field(1.0, ge=0.0, le=1.0, description="Group opacity")
    blend_mode: BlendMode = Field(BlendMode.NORMAL, description="Group blend mode")
    parent_id: Optional[ID] = Field(None, description="Parent group ID")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional group metadata")
    
    def add_child(self, child: Union['LayerGroup', Layer]) -> None:
        """Add a child layer or group."""
        child.parent_id = self.id
        self.children.append(child)
    
    def remove_child(self, child: Union['LayerGroup', Layer, ID]) -> bool:
        """
        Remove a child layer or group.
        
        Args:
            child: Child object or ID to remove
            
        Returns:
            True if child was found and removed, False otherwise
        """
        if isinstance(child, str):  # ID string
            for i, existing_child in enumerate(self.children):
                if existing_child.id == child:
                    removed_child = self.children.pop(i)
                    removed_child.parent_id = None
                    return True
            return False
        else:
            try:
                self.children.remove(child)
                child.parent_id = None
                return True
            except ValueError:
                return False
    
    def move_child(self, child: Union['LayerGroup', Layer, ID], new_index: int) -> bool:
        """
        Move a child to a new position within the group.
        
        Args:
            child: Child object or ID to move
            new_index: New index position
            
        Returns:
            True if child was found and moved, False otherwise
        """
        if isinstance(child, str):  # ID string
            for i, existing_child in enumerate(self.children):
                if existing_child.id == child:
                    child_obj = self.children.pop(i)
                    new_index = max(0, min(new_index, len(self.children)))
                    self.children.insert(new_index, child_obj)
                    return True
            return False
        else:
            try:
                current_index = self.children.index(child)
                child_obj = self.children.pop(current_index)
                new_index = max(0, min(new_index, len(self.children)))
                self.children.insert(new_index, child_obj)
                return True
            except ValueError:
                return False
    
    def get_all_layers(self, recursive: bool = True) -> List[Layer]:
        """
        Get all layers in this group.
        
        Args:
            recursive: If True, include layers from nested groups
            
        Returns:
            List of all Layer objects
        """
        layers = []
        for child in self.children:
            if isinstance(child, Layer):
                layers.append(child)
            elif isinstance(child, LayerGroup) and recursive:
                layers.extend(child.get_all_layers(recursive=True))
        return layers
    
    def get_all_shapes(self, recursive: bool = True) -> List[Union[Shape, ID]]:
        """
        Get all shapes from all layers in this group.
        
        Args:
            recursive: If True, include shapes from nested groups
            
        Returns:
            List of all shapes
        """
        shapes = []
        for layer in self.get_all_layers(recursive=recursive):
            shapes.extend(layer.shapes)
        return shapes
    
    def get_child_count(self) -> int:
        """Get the number of direct children in this group."""
        return len(self.children)
    
    def is_empty(self) -> bool:
        """Check if this group has no children."""
        return len(self.children) == 0
    
    def find_layer_by_id(self, layer_id: ID, recursive: bool = True) -> Optional[Layer]:
        """
        Find a layer by ID within this group.
        
        Args:
            layer_id: ID of the layer to find
            recursive: If True, search nested groups
            
        Returns:
            Layer object if found, None otherwise
        """
        for child in self.children:
            if isinstance(child, Layer) and child.id == layer_id:
                return child
            elif isinstance(child, LayerGroup) and recursive:
                found = child.find_layer_by_id(layer_id, recursive=True)
                if found:
                    return found
        return None
    
    def find_group_by_id(self, group_id: ID, recursive: bool = True) -> Optional['LayerGroup']:
        """
        Find a group by ID within this group.
        
        Args:
            group_id: ID of the group to find
            recursive: If True, search nested groups
            
        Returns:
            LayerGroup object if found, None otherwise
        """
        if self.id == group_id:
            return self
        
        for child in self.children:
            if isinstance(child, LayerGroup):
                if child.id == group_id:
                    return child
                elif recursive:
                    found = child.find_group_by_id(group_id, recursive=True)
                    if found:
                        return found
        return None


# Enable forward references for LayerGroup
LayerGroup.model_rebuild()


class LayerManager(BaseModel):
    """
    Layer management system for organizing and manipulating layers.
    
    Provides high-level operations for:
    - Layer creation, deletion, and organization
    - Z-order management and sorting
    - Batch operations on multiple layers
    - Layer hierarchy navigation
    """
    
    root_group: LayerGroup = Field(default_factory=lambda: LayerGroup(name="Root"), description="Root layer group")  # type: ignore
    active_layer_id: Optional[ID] = Field(None, description="Currently active layer ID")
    
    def create_layer(self, name: str, parent_group: Optional[LayerGroup] = None) -> Layer:
        """
        Create a new layer.
        
        Args:
            name: Name for the new layer
            parent_group: Parent group (defaults to root)
            
        Returns:
            The created Layer object
        """
        layer = Layer(name=name)  # type: ignore
        target_group = parent_group or self.root_group
        target_group.add_child(layer)
        
        # Set as active if no active layer
        if self.active_layer_id is None:
            self.active_layer_id = layer.id
        
        return layer
    
    def create_group(self, name: str, parent_group: Optional[LayerGroup] = None) -> LayerGroup:
        """
        Create a new layer group.
        
        Args:
            name: Name for the new group
            parent_group: Parent group (defaults to root)
            
        Returns:
            The created LayerGroup object
        """
        group = LayerGroup(name=name)  # type: ignore
        target_group = parent_group or self.root_group
        target_group.add_child(group)
        return group
    
    def delete_layer(self, layer_id: ID) -> bool:
        """
        Delete a layer by ID.
        
        Args:
            layer_id: ID of the layer to delete
            
        Returns:
            True if layer was found and deleted, False otherwise
        """
        layer = self.find_layer_by_id(layer_id)
        if not layer:
            return False
        
        # Find parent group and remove layer
        parent = self._find_parent_group(layer_id)
        if parent:
            success = parent.remove_child(layer_id)
            
            # Clear active layer if it was deleted
            if self.active_layer_id == layer_id:
                self.active_layer_id = None
                
            return success
        
        return False
    
    def delete_group(self, group_id: ID) -> bool:
        """
        Delete a group by ID.
        
        Args:
            group_id: ID of the group to delete
            
        Returns:
            True if group was found and deleted, False otherwise
        """
        if group_id == self.root_group.id:
            return False  # Cannot delete root group
        
        group = self.find_group_by_id(group_id)
        if not group:
            return False
        
        # Find parent group and remove
        parent = self._find_parent_group(group_id)
        if parent:
            return parent.remove_child(group_id)
        
        return False
    
    def get_all_layers(self) -> List[Layer]:
        """Get all layers in the document."""
        return self.root_group.get_all_layers(recursive=True)
    
    def get_layers_by_z_order(self) -> List[Layer]:
        """Get all layers sorted by z-index (back to front)."""
        layers = self.get_all_layers()
        return sorted(layers, key=lambda layer: layer.z_index)
    
    def find_layer_by_id(self, layer_id: ID) -> Optional[Layer]:
        """Find a layer by ID."""
        return self.root_group.find_layer_by_id(layer_id, recursive=True)
    
    def find_group_by_id(self, group_id: ID) -> Optional[LayerGroup]:
        """Find a group by ID."""
        return self.root_group.find_group_by_id(group_id, recursive=True)
    
    def set_active_layer(self, layer_id: ID) -> bool:
        """
        Set the active layer.
        
        Args:
            layer_id: ID of the layer to make active
            
        Returns:
            True if layer exists and was set active, False otherwise
        """
        if self.find_layer_by_id(layer_id):
            self.active_layer_id = layer_id
            return True
        return False
    
    def get_active_layer(self) -> Optional[Layer]:
        """Get the currently active layer."""
        if self.active_layer_id:
            return self.find_layer_by_id(self.active_layer_id)
        return None
    
    def reorder_layers_by_z_index(self) -> None:
        """Reorder all layers within their groups based on z_index."""
        def sort_group(group: LayerGroup) -> None:
            # Sort children by z_index
            group.children.sort(key=lambda child: child.z_index)
            
            # Recursively sort nested groups
            for child in group.children:
                if isinstance(child, LayerGroup):
                    sort_group(child)
        
        sort_group(self.root_group)
    
    def _find_parent_group(self, child_id: ID) -> Optional[LayerGroup]:
        """Find the parent group of a layer or group by child ID."""
        def search_group(group: LayerGroup) -> Optional[LayerGroup]:
            for child in group.children:
                if child.id == child_id:
                    return group
                elif isinstance(child, LayerGroup):
                    found = search_group(child)
                    if found:
                        return found
            return None
        
        return search_group(self.root_group)
    
    def get_layer_count(self) -> int:
        """Get total number of layers."""
        return len(self.get_all_layers())
    
    def get_visible_layers(self) -> List[Layer]:
        """Get all visible layers."""
        return [layer for layer in self.get_all_layers() if layer.visible]
    
    def get_unlocked_layers(self) -> List[Layer]:
        """Get all unlocked layers."""
        return [layer for layer in self.get_all_layers() if not layer.locked]