import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def align(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Align selected bones to the active bone (or to their parent)

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def assign_to_collection(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    collection_index: typing.Any = -1,
    new_collection_name: typing.Union[str, typing.Any] = "",
):
    """Assign all selected bones to a collection, or unassign them, depending on whether the active bone is already assigned or not

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param collection_index: Collection Index, Index of the collection to assign selected bones to. When the operator should create a new bone collection, use new_collection_name to define the collection name, and set this parameter to the parent index of the new bone collection
    :type collection_index: typing.Any
    :param new_collection_name: Name, Name of a to-be-added bone collection. Only pass this if you want to create a new bone collection and assign the selected bones to it. To assign to an existing collection, do not include this parameter and use collection_index
    :type new_collection_name: typing.Union[str, typing.Any]
    """

    ...

def autoside_names(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    type: typing.Any = "XAXIS",
):
    """Automatically renames the selected bones according to which side of the target axis they fall on

        :type override_context: typing.Union[dict, bpy.types.Context]
        :type execution_context: typing.Union[str, int]
        :type undo: bool
        :param type: Axis, Axis to tag names with

    XAXIS
    X-Axis -- Left/Right.

    YAXIS
    Y-Axis -- Front/Back.

    ZAXIS
    Z-Axis -- Top/Bottom.
        :type type: typing.Any
    """

    ...

def bone_primitive_add(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    name: typing.Union[str, typing.Any] = "",
):
    """Add a new bone located at the 3D cursor

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param name: Name, Name of the newly created bone
    :type name: typing.Union[str, typing.Any]
    """

    ...

def calculate_roll(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    type: typing.Any = "POS_X",
    axis_flip: typing.Union[bool, typing.Any] = False,
    axis_only: typing.Union[bool, typing.Any] = False,
):
    """Automatically fix alignment of select bones' axes

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param type: Type
    :type type: typing.Any
    :param axis_flip: Flip Axis, Negate the alignment axis
    :type axis_flip: typing.Union[bool, typing.Any]
    :param axis_only: Shortest Rotation, Ignore the axis direction, use the shortest rotation to align
    :type axis_only: typing.Union[bool, typing.Any]
    """

    ...

def click_extrude(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Create a new bone going from the last selected joint to the mouse position

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_add(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Add a new bone collection

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_assign(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    name: typing.Union[str, typing.Any] = "",
):
    """Add selected bones to the chosen bone collection

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param name: Bone Collection, Name of the bone collection to assign this bone to; empty to assign to the active bone collection
    :type name: typing.Union[str, typing.Any]
    """

    ...

def collection_create_and_assign(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    name: typing.Union[str, typing.Any] = "",
):
    """Create a new bone collection and assign all selected bones

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param name: Bone Collection, Name of the bone collection to create
    :type name: typing.Union[str, typing.Any]
    """

    ...

def collection_deselect(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Deselect bones of active Bone Collection

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_move(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    direction: typing.Any = "UP",
):
    """Change position of active Bone Collection in list of Bone collections

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param direction: Direction, Direction to move the active Bone Collection towards
    :type direction: typing.Any
    """

    ...

def collection_remove(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Remove the active bone collection

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_remove_unused(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Remove all bone collections that have neither bones nor children. This is done recursively, so bone collections that only have unused children are also removed

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_select(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Select bones in active Bone Collection

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_show_all(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Show all bone collections

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def collection_unassign(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    name: typing.Union[str, typing.Any] = "",
):
    """Remove selected bones from the active bone collection

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param name: Bone Collection, Name of the bone collection to unassign this bone from; empty to unassign from the active bone collection
    :type name: typing.Union[str, typing.Any]
    """

    ...

def collection_unassign_named(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    name: typing.Union[str, typing.Any] = "",
    bone_name: typing.Union[str, typing.Any] = "",
):
    """Unassign the named bone from this bone collection

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param name: Bone Collection, Name of the bone collection to unassign this bone from; empty to unassign from the active bone collection
    :type name: typing.Union[str, typing.Any]
    :param bone_name: Bone Name, Name of the bone to unassign from the collection; empty to use the active bone
    :type bone_name: typing.Union[str, typing.Any]
    """

    ...

def collection_unsolo_all(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Clear the 'solo' setting on all bone collections

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def copy_bone_color_to_selected(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    bone_type: typing.Any = "EDIT",
):
    """Copy the bone color of the active bone to all selected bones

        :type override_context: typing.Union[dict, bpy.types.Context]
        :type execution_context: typing.Union[str, int]
        :type undo: bool
        :param bone_type: Type

    EDIT
    Bone -- Copy Bone colors from the active bone to all selected bones.

    POSE
    Pose Bone -- Copy Pose Bone colors from the active pose bone to all selected pose bones.
        :type bone_type: typing.Any
    """

    ...

def delete(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    confirm: typing.Union[bool, typing.Any] = True,
):
    """Remove selected bones from the armature

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param confirm: Confirm, Prompt for confirmation
    :type confirm: typing.Union[bool, typing.Any]
    """

    ...

def dissolve(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Dissolve selected bones from the armature

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def duplicate(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    do_flip_names: typing.Union[bool, typing.Any] = False,
):
    """Make copies of the selected bones within the same armature

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param do_flip_names: Flip Names, Try to flip names of the bones, if possible, instead of adding a number extension
    :type do_flip_names: typing.Union[bool, typing.Any]
    """

    ...

def duplicate_move(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    ARMATURE_OT_duplicate: typing.Any = None,
    TRANSFORM_OT_translate: typing.Any = None,
):
    """Make copies of the selected bones within the same armature and move them

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param ARMATURE_OT_duplicate: Duplicate Selected Bone(s), Make copies of the selected bones within the same armature
    :type ARMATURE_OT_duplicate: typing.Any
    :param TRANSFORM_OT_translate: Move, Move selected items
    :type TRANSFORM_OT_translate: typing.Any
    """

    ...

def extrude(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    forked: typing.Union[bool, typing.Any] = False,
):
    """Create new bones from the selected joints

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param forked: Forked
    :type forked: typing.Union[bool, typing.Any]
    """

    ...

def extrude_forked(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    ARMATURE_OT_extrude: typing.Any = None,
    TRANSFORM_OT_translate: typing.Any = None,
):
    """Create new bones from the selected joints and move them

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param ARMATURE_OT_extrude: Extrude, Create new bones from the selected joints
    :type ARMATURE_OT_extrude: typing.Any
    :param TRANSFORM_OT_translate: Move, Move selected items
    :type TRANSFORM_OT_translate: typing.Any
    """

    ...

def extrude_move(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    ARMATURE_OT_extrude: typing.Any = None,
    TRANSFORM_OT_translate: typing.Any = None,
):
    """Create new bones from the selected joints and move them

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param ARMATURE_OT_extrude: Extrude, Create new bones from the selected joints
    :type ARMATURE_OT_extrude: typing.Any
    :param TRANSFORM_OT_translate: Move, Move selected items
    :type TRANSFORM_OT_translate: typing.Any
    """

    ...

def fill(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Add bone between selected joint(s) and/or 3D cursor

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def flip_names(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    do_strip_numbers: typing.Union[bool, typing.Any] = False,
):
    """Flips (and corrects) the axis suffixes of the names of selected bones

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param do_strip_numbers: Strip Numbers, Try to remove right-most dot-number from flipped names.Warning: May result in incoherent naming in some cases
    :type do_strip_numbers: typing.Union[bool, typing.Any]
    """

    ...

def hide(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    unselected: typing.Union[bool, typing.Any] = False,
):
    """Tag selected bones to not be visible in Edit Mode

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param unselected: Unselected, Hide unselected rather than selected
    :type unselected: typing.Union[bool, typing.Any]
    """

    ...

def move_to_collection(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    collection_index: typing.Any = -1,
    new_collection_name: typing.Union[str, typing.Any] = "",
):
    """Move bones to a collection

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param collection_index: Collection Index, Index of the collection to move selected bones to. When the operator should create a new bone collection, do not include this parameter and pass new_collection_name
    :type collection_index: typing.Any
    :param new_collection_name: Name, Name of a to-be-added bone collection. Only pass this if you want to create a new bone collection and move the selected bones to it. To move to an existing collection, do not include this parameter and use collection_index
    :type new_collection_name: typing.Union[str, typing.Any]
    """

    ...

def parent_clear(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    type: typing.Any = "CLEAR",
):
    """Remove the parent-child relationship between selected bones and their parents

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param type: Clear Type, What way to clear parenting
    :type type: typing.Any
    """

    ...

def parent_set(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    type: typing.Any = "CONNECTED",
):
    """Set the active bone as the parent of the selected bones

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param type: Parent Type, Type of parenting
    :type type: typing.Any
    """

    ...

def reveal(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    select: typing.Union[bool, typing.Any] = True,
):
    """Reveal all bones hidden in Edit Mode

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param select: Select
    :type select: typing.Union[bool, typing.Any]
    """

    ...

def roll_clear(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    roll: typing.Any = 0.0,
):
    """Clear roll for selected bones

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param roll: Roll
    :type roll: typing.Any
    """

    ...

def select_all(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    action: typing.Any = "TOGGLE",
):
    """Toggle selection status of all bones

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

def select_hierarchy(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    direction: typing.Any = "PARENT",
    extend: typing.Union[bool, typing.Any] = False,
):
    """Select immediate parent/children of selected bones

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param direction: Direction
    :type direction: typing.Any
    :param extend: Extend, Extend the selection
    :type extend: typing.Union[bool, typing.Any]
    """

    ...

def select_less(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Deselect those bones at the boundary of each selection region

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def select_linked(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    all_forks: typing.Union[bool, typing.Any] = False,
):
    """Select all bones linked by parent/child connections to the current selection

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param all_forks: All Forks, Follow forks in the parents chain
    :type all_forks: typing.Union[bool, typing.Any]
    """

    ...

def select_linked_pick(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    deselect: typing.Union[bool, typing.Any] = False,
    all_forks: typing.Union[bool, typing.Any] = False,
):
    """(De)select bones linked by parent/child connections under the mouse cursor

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param deselect: Deselect
    :type deselect: typing.Union[bool, typing.Any]
    :param all_forks: All Forks, Follow forks in the parents chain
    :type all_forks: typing.Union[bool, typing.Any]
    """

    ...

def select_mirror(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    only_active: typing.Union[bool, typing.Any] = False,
    extend: typing.Union[bool, typing.Any] = False,
):
    """Mirror the bone selection

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param only_active: Active Only, Only operate on the active bone
    :type only_active: typing.Union[bool, typing.Any]
    :param extend: Extend, Extend the selection
    :type extend: typing.Union[bool, typing.Any]
    """

    ...

def select_more(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Select those bones connected to the initial selection

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def select_similar(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    type: typing.Any = "LENGTH",
    threshold: typing.Any = 0.1,
):
    """Select similar bones by property types

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param type: Type
    :type type: typing.Any
    :param threshold: Threshold
    :type threshold: typing.Any
    """

    ...

def separate(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Isolate selected bones into a separate armature

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def shortest_path_pick(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Select shortest path between two bones

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def split(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Split off selected bones from connected unselected bones

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def subdivide(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    number_cuts: typing.Any = 1,
):
    """Break selected bones into chains of smaller bones

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param number_cuts: Number of Cuts
    :type number_cuts: typing.Any
    """

    ...

def switch_direction(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Change the direction that a chain of bones points in (head and tail swap)

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def symmetrize(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    direction: typing.Any = "NEGATIVE_X",
):
    """Enforce symmetry, make copies of the selection or use existing

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param direction: Direction, Which sides to copy from and to (when both are selected)
    :type direction: typing.Any
    """

    ...
