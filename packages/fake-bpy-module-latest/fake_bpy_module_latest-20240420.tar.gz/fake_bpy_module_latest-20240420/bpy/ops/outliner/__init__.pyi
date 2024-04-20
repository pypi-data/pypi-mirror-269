import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def action_set(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    action: typing.Union[str, int, typing.Any] = "",
):
    """Change the active action used

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param action: Action
    :type action: typing.Union[str, int, typing.Any]
    """

    ...

def animdata_operation(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    type: typing.Any = "CLEAR_ANIMDATA",
):
    """Undocumented, consider contributing.

        :type override_context: typing.Union[dict, bpy.types.Context]
        :type execution_context: typing.Union[str, int]
        :type undo: bool
        :param type: Animation Operation

    CLEAR_ANIMDATA
    Clear Animation Data -- Remove this animation data container.

    SET_ACT
    Set Action.

    CLEAR_ACT
    Unlink Action.

    REFRESH_DRIVERS
    Refresh Drivers.

    CLEAR_DRIVERS
    Clear Drivers.
        :type type: typing.Any
    """

    ...

def collection_color_tag_set(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    color: typing.Union[str, int] = "NONE",
):
    """Set a color tag for the selected collections

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param color: Color Tag
    :type color: typing.Union[str, int]
    """

    ...

def collection_disable(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Disable viewport display in the view layers

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_disable_render(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Do not render this collection

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_drop(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Drag to move to collection in Outliner

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_duplicate(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Recursively duplicate the collection, all its children, objects and object data

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_duplicate_linked(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Recursively duplicate the collection, all its children and objects, with linked object data

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_enable(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Enable viewport display in the view layers

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_enable_render(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Render the collection

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_exclude_clear(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Include collection in the active view layer

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_exclude_set(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Exclude collection from the active view layer

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_hide(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Hide the collection in this view layer

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_hide_inside(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Hide all the objects and collections inside the collection

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_hierarchy_delete(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Delete selected collection hierarchies

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_holdout_clear(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Clear masking of collection in the active view layer

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_holdout_set(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Mask collection in the active view layer

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_indirect_only_clear(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Clear collection contributing only indirectly in the view layer

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_indirect_only_set(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Set collection to only contribute indirectly (through shadows and reflections) in the view layer

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_instance(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Instance selected collections to active scene

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_isolate(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    extend: typing.Union[bool, typing.Any] = False,
):
    """Hide all but this collection and its parents

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param extend: Extend, Extend current visible collections
    :type extend: typing.Union[bool, typing.Any]
    """

    ...

def collection_link(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Link selected collections to active scene

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_new(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    nested: typing.Union[bool, typing.Any] = True,
):
    """Add a new collection inside selected collection

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param nested: Nested, Add as child of selected collection
    :type nested: typing.Union[bool, typing.Any]
    """

    ...

def collection_objects_deselect(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Deselect objects in collection

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_objects_select(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Select objects in collection

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_show(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Show the collection in this view layer

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_show_inside(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Show all the objects and collections inside the collection

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def constraint_operation(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    type: typing.Any = "ENABLE",
):
    """Undocumented, consider contributing.

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param type: Constraint Operation
    :type type: typing.Any
    """

    ...

def data_operation(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    type: typing.Union[str, int, typing.Any] = "DEFAULT",
):
    """Undocumented, consider contributing.

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param type: Data Operation
    :type type: typing.Union[str, int, typing.Any]
    """

    ...

def datastack_drop(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Copy or reorder modifiers, constraints, and effects

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def delete(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    hierarchy: typing.Union[bool, typing.Any] = False,
):
    """Delete selected objects and collections

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param hierarchy: Hierarchy, Delete child objects and collections
    :type hierarchy: typing.Union[bool, typing.Any]
    """

    ...

def drivers_add_selected(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Add drivers to selected items

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def drivers_delete_selected(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Delete drivers assigned to selected items

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def expanded_toggle(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Expand/Collapse all items

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def hide(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Hide selected objects and collections

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def highlight_update(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Update the item highlight based on the current mouse position

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def id_copy(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Copy the selected data-blocks to the internal clipboard

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def id_delete(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Delete the ID under cursor

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def id_operation(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    type: typing.Any = "UNLINK",
):
    """General data-block management operations

        :type override_context: typing.Union[dict, bpy.types.Context]
        :type execution_context: typing.Union[str, int]
        :type undo: bool
        :param type: ID Data Operation

    UNLINK
    Unlink.

    LOCAL
    Make Local.

    SINGLE
    Make Single User.

    DELETE
    Delete.

    REMAP
    Remap Users -- Make all users of selected data-blocks to use instead current (clicked) one.

    COPY
    Copy.

    PASTE
    Paste.

    ADD_FAKE
    Add Fake User -- Ensure data-block gets saved even if it isn't in use (e.g. for motion and material libraries).

    CLEAR_FAKE
    Clear Fake User.

    RENAME
    Rename.

    SELECT_LINKED
    Select Linked.
        :type type: typing.Any
    """

    ...

def id_paste(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Paste data-blocks from the internal clipboard

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def id_remap(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    id_type: typing.Union[str, int] = "OBJECT",
    old_id: typing.Union[str, int, typing.Any] = "",
    new_id: typing.Union[str, int, typing.Any] = "",
):
    """Undocumented, consider contributing.

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param id_type: ID Type
    :type id_type: typing.Union[str, int]
    :param old_id: Old ID, Old ID to replace
    :type old_id: typing.Union[str, int, typing.Any]
    :param new_id: New ID, New ID to remap all selected IDs' users to
    :type new_id: typing.Union[str, int, typing.Any]
    """

    ...

def item_activate(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    extend: typing.Union[bool, typing.Any] = False,
    extend_range: typing.Union[bool, typing.Any] = False,
    deselect_all: typing.Union[bool, typing.Any] = False,
    recurse: typing.Union[bool, typing.Any] = False,
):
    """Handle mouse clicks to select and activate items

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param extend: Extend, Extend selection for activation
    :type extend: typing.Union[bool, typing.Any]
    :param extend_range: Extend Range, Select a range from active element
    :type extend_range: typing.Union[bool, typing.Any]
    :param deselect_all: Deselect On Nothing, Deselect all when nothing under the cursor
    :type deselect_all: typing.Union[bool, typing.Any]
    :param recurse: Recurse, Select objects recursively from active element
    :type recurse: typing.Union[bool, typing.Any]
    """

    ...

def item_drag_drop(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Drag and drop element to another place

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def item_openclose(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    all: typing.Union[bool, typing.Any] = False,
):
    """Toggle whether item under cursor is enabled or closed

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param all: All, Close or open all items
    :type all: typing.Union[bool, typing.Any]
    """

    ...

def item_rename(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    use_active: typing.Union[bool, typing.Any] = False,
):
    """Rename the active element

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param use_active: Use Active, Rename the active item, rather than the one the mouse is over
    :type use_active: typing.Union[bool, typing.Any]
    """

    ...

def keyingset_add_selected(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Add selected items (blue-gray rows) to active Keying Set

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def keyingset_remove_selected(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Remove selected items (blue-gray rows) from active Keying Set

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def lib_operation(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    type: typing.Any = "DELETE",
):
    """Undocumented, consider contributing.

        :type override_context: typing.Union[dict, bpy.types.Context]
        :type execution_context: typing.Union[str, int]
        :type undo: bool
        :param type: Library Operation

    DELETE
    Delete -- Delete this library and all its items.
    Warning: No undo.

    RELOCATE
    Relocate -- Select a new path for this library, and reload all its data.

    RELOAD
    Reload -- Reload all data from this library.
        :type type: typing.Any
    """

    ...

def lib_relocate(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Relocate the library under cursor

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def liboverride_operation(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    type: typing.Any = "OVERRIDE_LIBRARY_CREATE_HIERARCHY",
    selection_set: typing.Any = "SELECTED",
):
    """Create, reset or clear library override hierarchies

        :type override_context: typing.Union[dict, bpy.types.Context]
        :type execution_context: typing.Union[str, int]
        :type undo: bool
        :param type: Library Override Operation

    OVERRIDE_LIBRARY_CREATE_HIERARCHY
    Make -- Create a local override of the selected linked data-blocks, and their hierarchy of dependencies.

    OVERRIDE_LIBRARY_RESET
    Reset -- Reset the selected local overrides to their linked references values.

    OVERRIDE_LIBRARY_CLEAR_SINGLE
    Clear -- Delete the selected local overrides and relink their usages to the linked data-blocks if possible, else reset them and mark them as non editable.
        :type type: typing.Any
        :param selection_set: Selection Set, Over which part of the tree items to apply the operation

    SELECTED
    Selected -- Apply the operation over selected data-blocks only.

    CONTENT
    Content -- Apply the operation over content of the selected items only (the data-blocks in their sub-tree).

    SELECTED_AND_CONTENT
    Selected & Content -- Apply the operation over selected data-blocks and all their dependencies.
        :type selection_set: typing.Any
    """

    ...

def liboverride_troubleshoot_operation(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    type: typing.Any = "OVERRIDE_LIBRARY_RESYNC_HIERARCHY",
    selection_set: typing.Any = "SELECTED",
):
    """Advanced operations over library override to help fix broken hierarchies

        :type override_context: typing.Union[dict, bpy.types.Context]
        :type execution_context: typing.Union[str, int]
        :type undo: bool
        :param type: Library Override Troubleshoot Operation

    OVERRIDE_LIBRARY_RESYNC_HIERARCHY
    Resync -- Rebuild the selected local overrides from their linked references, as well as their hierarchies of dependencies.

    OVERRIDE_LIBRARY_RESYNC_HIERARCHY_ENFORCE
    Resync Enforce -- Rebuild the selected local overrides from their linked references, as well as their hierarchies of dependencies, enforcing these hierarchies to match the linked data (i.e. ignoring existing overrides on data-blocks pointer properties).

    OVERRIDE_LIBRARY_DELETE_HIERARCHY
    Delete -- Delete the selected local overrides (including their hierarchies of override dependencies) and relink their usages to the linked data-blocks.
        :type type: typing.Any
        :param selection_set: Selection Set, Over which part of the tree items to apply the operation

    SELECTED
    Selected -- Apply the operation over selected data-blocks only.

    CONTENT
    Content -- Apply the operation over content of the selected items only (the data-blocks in their sub-tree).

    SELECTED_AND_CONTENT
    Selected & Content -- Apply the operation over selected data-blocks and all their dependencies.
        :type selection_set: typing.Any
    """

    ...

def material_drop(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Drag material to object in Outliner

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def modifier_operation(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    type: typing.Any = "APPLY",
):
    """Undocumented, consider contributing.

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param type: Modifier Operation
    :type type: typing.Any
    """

    ...

def object_operation(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    type: typing.Any = "SELECT",
):
    """Undocumented, consider contributing.

        :type override_context: typing.Union[dict, bpy.types.Context]
        :type execution_context: typing.Union[str, int]
        :type undo: bool
        :param type: Object Operation

    SELECT
    Select.

    DESELECT
    Deselect.

    SELECT_HIERARCHY
    Select Hierarchy.

    REMAP
    Remap Users -- Make all users of selected data-blocks to use instead a new chosen one.

    RENAME
    Rename.
        :type type: typing.Any
    """

    ...

def operation(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Context menu for item operations

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def orphans_manage(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Open a window to manage unused data

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def orphans_purge(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    do_local_ids: typing.Union[bool, typing.Any] = True,
    do_linked_ids: typing.Union[bool, typing.Any] = True,
    do_recursive: typing.Union[bool, typing.Any] = True,
):
    """Clear all orphaned data-blocks without any users from the file

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param do_local_ids: Local Data-blocks, Include unused local data-blocks into deletion
    :type do_local_ids: typing.Union[bool, typing.Any]
    :param do_linked_ids: Linked Data-blocks, Include unused linked data-blocks into deletion
    :type do_linked_ids: typing.Union[bool, typing.Any]
    :param do_recursive: Recursive Delete, Recursively check for indirectly unused data-blocks, ensuring that no orphaned data-blocks remain after execution
    :type do_recursive: typing.Union[bool, typing.Any]
    """

    ...

def parent_clear(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Drag to clear parent in Outliner

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def parent_drop(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Drag to parent in Outliner

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def scene_drop(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Drag object to scene in Outliner

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def scene_operation(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    type: typing.Union[str, int, typing.Any] = "DELETE",
):
    """Context menu for scene operations

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param type: Scene Operation
    :type type: typing.Union[str, int, typing.Any]
    """

    ...

def scroll_page(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    up: typing.Union[bool, typing.Any] = False,
):
    """Scroll page up or down

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param up: Up, Scroll up one page
    :type up: typing.Union[bool, typing.Any]
    """

    ...

def select_all(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    action: typing.Any = "TOGGLE",
):
    """Toggle the Outliner selection of items

        :type override_context: typing.Union[dict, bpy.types.Context]
        :type execution_context: typing.Union[str, int]
        :type undo: bool
        :param action: Action, Selection action to execute

    TOGGLE
    Toggle -- Toggle selection for all elements.

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.

    INVERT
    Invert -- Invert selection of all elements.
        :type action: typing.Any
    """

    ...

def select_box(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    tweak: typing.Union[bool, typing.Any] = False,
    xmin: typing.Any = 0,
    xmax: typing.Any = 0,
    ymin: typing.Any = 0,
    ymax: typing.Any = 0,
    wait_for_input: typing.Union[bool, typing.Any] = True,
    mode: typing.Any = "SET",
):
    """Use box selection to select tree elements

        :type override_context: typing.Union[dict, bpy.types.Context]
        :type execution_context: typing.Union[str, int]
        :type undo: bool
        :param tweak: Tweak, Tweak gesture from empty space for box selection
        :type tweak: typing.Union[bool, typing.Any]
        :param xmin: X Min
        :type xmin: typing.Any
        :param xmax: X Max
        :type xmax: typing.Any
        :param ymin: Y Min
        :type ymin: typing.Any
        :param ymax: Y Max
        :type ymax: typing.Any
        :param wait_for_input: Wait for Input
        :type wait_for_input: typing.Union[bool, typing.Any]
        :param mode: Mode

    SET
    Set -- Set a new selection.

    ADD
    Extend -- Extend existing selection.

    SUB
    Subtract -- Subtract existing selection.
        :type mode: typing.Any
    """

    ...

def select_walk(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    direction: typing.Any = "UP",
    extend: typing.Union[bool, typing.Any] = False,
    toggle_all: typing.Union[bool, typing.Any] = False,
):
    """Use walk navigation to select tree elements

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param direction: Walk Direction, Select/Deselect element in this direction
    :type direction: typing.Any
    :param extend: Extend, Extend selection on walk
    :type extend: typing.Union[bool, typing.Any]
    :param toggle_all: Toggle All, Toggle open/close hierarchy
    :type toggle_all: typing.Union[bool, typing.Any]
    """

    ...

def show_active(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Open up the tree and adjust the view so that the active object is shown centered

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def show_hierarchy(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Open all object entries and close all others

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def show_one_level(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    open: typing.Union[bool, typing.Any] = True,
):
    """Expand/collapse all entries by one level

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param open: Open, Expand all entries one level deep
    :type open: typing.Union[bool, typing.Any]
    """

    ...

def unhide_all(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Unhide all objects and collections

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...
