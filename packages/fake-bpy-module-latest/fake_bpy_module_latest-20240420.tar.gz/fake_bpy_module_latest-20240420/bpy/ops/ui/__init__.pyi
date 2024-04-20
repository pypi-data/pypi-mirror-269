import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def assign_default_button(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Set this property's current value as the new default

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def button_execute(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    skip_depressed: typing.Union[bool, typing.Any] = False,
):
    """Presses active button

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param skip_depressed: Skip Depressed
    :type skip_depressed: typing.Union[bool, typing.Any]
    """

    ...

def button_string_clear(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Unsets the text of the active button

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def copy_as_driver_button(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Create a new driver with this property as input, and copy it to the internal clipboard. Use Paste Driver to add it to the target property, or Paste Driver Variables to extend an existing driver

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def copy_data_path_button(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    full_path: typing.Union[bool, typing.Any] = False,
):
    """Copy the RNA data path for this property to the clipboard

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param full_path: full_path, Copy full data path
    :type full_path: typing.Union[bool, typing.Any]
    """

    ...

def copy_python_command_button(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Copy the Python command matching this button

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def copy_to_selected_button(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    all: typing.Union[bool, typing.Any] = True,
):
    """Copy the property's value from the active item to the same property of all selected items if the same property exists

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param all: All, Copy to selected all elements of the array
    :type all: typing.Union[bool, typing.Any]
    """

    ...

def drop_color(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    color: typing.Any = (0.0, 0.0, 0.0),
    gamma: typing.Union[bool, typing.Any] = False,
):
    """Drop colors to buttons

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param color: Color, Source color
    :type color: typing.Any
    :param gamma: Gamma Corrected, The source color is gamma corrected
    :type gamma: typing.Union[bool, typing.Any]
    """

    ...

def drop_material(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    session_uid: typing.Any = 0,
):
    """Drag material to Material slots in Properties

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param session_uid: Session UID, Session UID of the data-block to use by the operator
    :type session_uid: typing.Any
    """

    ...

def drop_name(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    string: typing.Union[str, typing.Any] = "",
):
    """Drop name to button

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param string: String, The string value to drop into the button
    :type string: typing.Union[str, typing.Any]
    """

    ...

def editsource(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Edit UI source code of the active button

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def edittranslation_init(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Edit i18n in current language for the active button

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def eyedropper_color(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Sample a color from the Blender window to store in a property

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def eyedropper_colorramp(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Sample a color band

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def eyedropper_colorramp_point(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Point-sample a color band

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def eyedropper_depth(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Sample depth from the 3D view

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def eyedropper_driver(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    mapping_type: typing.Any = "SINGLE_MANY",
):
    """Pick a property to use as a driver target

        :type override_context: typing.Union[dict, bpy.types.Context]
        :type execution_context: typing.Union[str, int]
        :type undo: bool
        :param mapping_type: Mapping Type, Method used to match target and driven properties

    SINGLE_MANY
    All from Target -- Drive all components of this property using the target picked.

    DIRECT
    Single from Target -- Drive this component of this property using the target picked.

    MATCH
    Match Indices -- Create drivers for each pair of corresponding elements.

    NONE_ALL
    Manually Create Later -- Create drivers for all properties without assigning any targets yet.

    NONE_SINGLE
    Manually Create Later (Single) -- Create driver for this property only and without assigning any targets yet.
        :type mapping_type: typing.Any
    """

    ...

def eyedropper_gpencil_color(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    mode: typing.Any = "MATERIAL",
):
    """Sample a color from the Blender Window and create Grease Pencil material

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param mode: Mode
    :type mode: typing.Any
    """

    ...

def eyedropper_id(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Sample a data-block from the 3D View to store in a property

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def jump_to_target_button(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Switch to the target object or bone

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def list_start_filter(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Start entering filter text for the list in focus

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def override_idtemplate_clear(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Delete the selected local override and relink its usages to the linked data-block if possible, else reset it and mark it as non editable

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def override_idtemplate_make(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Create a local override of the selected linked data-block, and its hierarchy of dependencies

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def override_idtemplate_reset(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Reset the selected local override to its linked reference values

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def override_remove_button(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    all: typing.Union[bool, typing.Any] = True,
):
    """Remove an override operation

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param all: All, Reset to default values all elements of the array
    :type all: typing.Union[bool, typing.Any]
    """

    ...

def override_type_set_button(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    all: typing.Union[bool, typing.Any] = True,
    type: typing.Any = "REPLACE",
):
    """Create an override operation, or set the type of an existing one

        :type override_context: typing.Union[dict, bpy.types.Context]
        :type execution_context: typing.Union[str, int]
        :type undo: bool
        :param all: All, Reset to default values all elements of the array
        :type all: typing.Union[bool, typing.Any]
        :param type: Type, Type of override operation

    NOOP
    NoOp -- 'No-Operation', place holder preventing automatic override to ever affect the property.

    REPLACE
    Replace -- Completely replace value from linked data by local one.

    DIFFERENCE
    Difference -- Store difference to linked data value.

    FACTOR
    Factor -- Store factor to linked data value (useful e.g. for scale).
        :type type: typing.Any
    """

    ...

def reloadtranslation(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Force a full reload of UI translation

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def reset_default_button(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    all: typing.Union[bool, typing.Any] = True,
):
    """Reset this property's value to its default value

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param all: All, Reset to default values all elements of the array
    :type all: typing.Union[bool, typing.Any]
    """

    ...

def unset_property_button(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Clear the property and use default or generated value in operators

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def view_drop(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Drag and drop onto a data-set or item within the data-set

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def view_item_rename(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Rename the active item in the data-set view

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def view_start_filter(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Start entering filter text for the data-set in focus

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...
