import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def brush_edit(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    stroke: bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement] = None,
):
    """Apply a stroke of brush to the particles

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param stroke: Stroke
    :type stroke: bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement]
    """

    ...

def connect_hair(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    all: typing.Union[bool, typing.Any] = False,
):
    """Connect hair to the emitter mesh

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param all: All Hair, Connect all hair systems to the emitter mesh
    :type all: typing.Union[bool, typing.Any]
    """

    ...

def copy_particle_systems(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    space: typing.Any = "OBJECT",
    remove_target_particles: typing.Union[bool, typing.Any] = True,
    use_active: typing.Union[bool, typing.Any] = False,
):
    """Copy particle systems from the active object to selected objects

        :type override_context: typing.Union[dict, bpy.types.Context]
        :type execution_context: typing.Union[str, int]
        :type undo: bool
        :param space: Space, Space transform for copying from one object to another

    OBJECT
    Object -- Copy inside each object's local space.

    WORLD
    World -- Copy in world space.
        :type space: typing.Any
        :param remove_target_particles: Remove Target Particles, Remove particle systems on the target objects
        :type remove_target_particles: typing.Union[bool, typing.Any]
        :param use_active: Use Active, Use the active particle system from the context
        :type use_active: typing.Union[bool, typing.Any]
    """

    ...

def delete(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    type: typing.Any = "PARTICLE",
):
    """Delete selected particles or keys

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param type: Type, Delete a full particle or only keys
    :type type: typing.Any
    """

    ...

def disconnect_hair(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    all: typing.Union[bool, typing.Any] = False,
):
    """Disconnect hair from the emitter mesh

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param all: All Hair, Disconnect all hair systems from the emitter mesh
    :type all: typing.Union[bool, typing.Any]
    """

    ...

def duplicate_particle_system(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    use_duplicate_settings: typing.Union[bool, typing.Any] = False,
):
    """Duplicate particle system within the active object

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param use_duplicate_settings: Duplicate Settings, Duplicate settings as well, so the new particle system uses its own settings
    :type use_duplicate_settings: typing.Union[bool, typing.Any]
    """

    ...

def dupliob_copy(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Duplicate the current instance object

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def dupliob_move_down(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Move instance object down in the list

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def dupliob_move_up(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Move instance object up in the list

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def dupliob_refresh(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Refresh list of instance objects and their weights

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def dupliob_remove(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Remove the selected instance object

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def edited_clear(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Undo all edition performed on the particle system

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def hair_dynamics_preset_add(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    name: typing.Union[str, typing.Any] = "",
    remove_name: typing.Union[bool, typing.Any] = False,
    remove_active: typing.Union[bool, typing.Any] = False,
):
    """Add or remove a Hair Dynamics Preset

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param name: Name, Name of the preset, used to make the path name
    :type name: typing.Union[str, typing.Any]
    :param remove_name: remove_name
    :type remove_name: typing.Union[bool, typing.Any]
    :param remove_active: remove_active
    :type remove_active: typing.Union[bool, typing.Any]
    """

    ...

def hide(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    unselected: typing.Union[bool, typing.Any] = False,
):
    """Hide selected particles

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param unselected: Unselected, Hide unselected rather than selected
    :type unselected: typing.Union[bool, typing.Any]
    """

    ...

def mirror(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Duplicate and mirror the selected particles along the local X axis

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def new(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Add new particle settings

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def new_target(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Add a new particle target

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def particle_edit_toggle(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Toggle particle edit mode

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def rekey(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    keys_number: typing.Any = 2,
):
    """Change the number of keys of selected particles (root and tip keys included)

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param keys_number: Number of Keys
    :type keys_number: typing.Any
    """

    ...

def remove_doubles(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    threshold: typing.Any = 0.0002,
):
    """Remove selected particles close enough of others

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param threshold: Merge Distance, Threshold distance within which particles are removed
    :type threshold: typing.Any
    """

    ...

def reveal(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    select: typing.Union[bool, typing.Any] = True,
):
    """Show hidden particles

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param select: Select
    :type select: typing.Union[bool, typing.Any]
    """

    ...

def select_all(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    action: typing.Any = "TOGGLE",
):
    """(De)select all particles' keys

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

def select_less(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Deselect boundary selected keys of each particle

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def select_linked(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Select all keys linked to already selected ones

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def select_linked_pick(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    deselect: typing.Union[bool, typing.Any] = False,
    location: typing.Any = (0, 0),
):
    """Select nearest particle from mouse pointer

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param deselect: Deselect, Deselect linked keys rather than selecting them
    :type deselect: typing.Union[bool, typing.Any]
    :param location: Location
    :type location: typing.Any
    """

    ...

def select_more(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Select keys linked to boundary selected keys of each particle

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def select_random(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    ratio: typing.Any = 0.5,
    seed: typing.Any = 0,
    action: typing.Any = "SELECT",
    type: typing.Any = "HAIR",
):
    """Select a randomly distributed set of hair or points

        :type override_context: typing.Union[dict, bpy.types.Context]
        :type execution_context: typing.Union[str, int]
        :type undo: bool
        :param ratio: Ratio, Portion of items to select randomly
        :type ratio: typing.Any
        :param seed: Random Seed, Seed for the random number generator
        :type seed: typing.Any
        :param action: Action, Selection action to execute

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.
        :type action: typing.Any
        :param type: Type, Select either hair or points
        :type type: typing.Any
    """

    ...

def select_roots(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    action: typing.Any = "SELECT",
):
    """Select roots of all visible particles

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

def select_tips(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    action: typing.Any = "SELECT",
):
    """Select tips of all visible particles

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

def shape_cut(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Cut hair to conform to the set shape object

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def subdivide(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Subdivide selected particles segments (adds keys)

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def target_move_down(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Move particle target down in the list

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def target_move_up(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Move particle target up in the list

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def target_remove(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Remove the selected particle target

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def unify_length(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Make selected hair the same length

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def weight_set(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    factor: typing.Any = 1.0,
):
    """Set the weight of selected keys

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param factor: Factor, Interpolation factor between current brush weight, and keys' weights
    :type factor: typing.Any
    """

    ...
