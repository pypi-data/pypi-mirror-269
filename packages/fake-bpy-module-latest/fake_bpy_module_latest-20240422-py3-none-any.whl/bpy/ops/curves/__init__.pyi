import typing
import bpy.ops.transform
import bpy.types

GenericType = typing.TypeVar("GenericType")

def add_bezier(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    radius: typing.Optional[typing.Any] = 1.0,
    enter_editmode: typing.Optional[typing.Union[bool, typing.Any]] = False,
    align: typing.Optional[typing.Any] = "WORLD",
    location: typing.Optional[typing.Any] = (0.0, 0.0, 0.0),
    rotation: typing.Optional[typing.Any] = (0.0, 0.0, 0.0),
    scale: typing.Optional[typing.Any] = (0.0, 0.0, 0.0),
):
    """Add new bezier curve

        :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param radius: Radius
        :type radius: typing.Optional[typing.Any]
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object
        :type enter_editmode: typing.Optional[typing.Union[bool, typing.Any]]
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: typing.Optional[typing.Any]
        :param location: Location, Location for the newly added object
        :type location: typing.Optional[typing.Any]
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: typing.Optional[typing.Any]
        :param scale: Scale, Scale for the newly added object
        :type scale: typing.Optional[typing.Any]
    """

    ...

def add_circle(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    radius: typing.Optional[typing.Any] = 1.0,
    enter_editmode: typing.Optional[typing.Union[bool, typing.Any]] = False,
    align: typing.Optional[typing.Any] = "WORLD",
    location: typing.Optional[typing.Any] = (0.0, 0.0, 0.0),
    rotation: typing.Optional[typing.Any] = (0.0, 0.0, 0.0),
    scale: typing.Optional[typing.Any] = (0.0, 0.0, 0.0),
):
    """Add new circle curve

        :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param radius: Radius
        :type radius: typing.Optional[typing.Any]
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object
        :type enter_editmode: typing.Optional[typing.Union[bool, typing.Any]]
        :param align: Align, The alignment of the new object

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: typing.Optional[typing.Any]
        :param location: Location, Location for the newly added object
        :type location: typing.Optional[typing.Any]
        :param rotation: Rotation, Rotation for the newly added object
        :type rotation: typing.Optional[typing.Any]
        :param scale: Scale, Scale for the newly added object
        :type scale: typing.Optional[typing.Any]
    """

    ...

def attribute_set(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    value_float: typing.Optional[typing.Any] = 0.0,
    value_float_vector_2d: typing.Optional[typing.Any] = (0.0, 0.0),
    value_float_vector_3d: typing.Optional[typing.Any] = (0.0, 0.0, 0.0),
    value_int: typing.Optional[typing.Any] = 0,
    value_int_vector_2d: typing.Optional[typing.Any] = (0, 0),
    value_color: typing.Optional[typing.Any] = (1.0, 1.0, 1.0, 1.0),
    value_bool: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Set values of the active attribute for selected elements

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param value_float: Value
    :type value_float: typing.Optional[typing.Any]
    :param value_float_vector_2d: Value
    :type value_float_vector_2d: typing.Optional[typing.Any]
    :param value_float_vector_3d: Value
    :type value_float_vector_3d: typing.Optional[typing.Any]
    :param value_int: Value
    :type value_int: typing.Optional[typing.Any]
    :param value_int_vector_2d: Value
    :type value_int_vector_2d: typing.Optional[typing.Any]
    :param value_color: Value
    :type value_color: typing.Optional[typing.Any]
    :param value_bool: Value
    :type value_bool: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def convert_from_particle_system(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Add a new curves object based on the current state of the particle system

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def convert_to_particle_system(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Add a new or update an existing hair particle system on the surface object

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def curve_type_set(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    type: typing.Optional[typing.Union[str, int]] = "POLY",
):
    """Set type of selected curves

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param type: Type, Curve type
    :type type: typing.Optional[typing.Union[str, int]]
    """

    ...

def cyclic_toggle(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Make active curve closed/opened loop

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def delete(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Remove selected control points or curves

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def draw(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    error_threshold: typing.Optional[typing.Any] = 0.0,
    fit_method: typing.Optional[typing.Union[str, int]] = "REFIT",
    corner_angle: typing.Optional[typing.Any] = 1.22173,
    use_cyclic: typing.Optional[typing.Union[bool, typing.Any]] = True,
    stroke: typing.Optional[
        bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement]
    ] = None,
    wait_for_input: typing.Optional[typing.Union[bool, typing.Any]] = True,
    is_curve_2d: typing.Optional[typing.Union[bool, typing.Any]] = False,
    bezier_as_nurbs: typing.Optional[typing.Union[bool, typing.Any]] = False,
):
    """Draw a freehand curve

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param error_threshold: Error, Error distance threshold (in object units)
    :type error_threshold: typing.Optional[typing.Any]
    :param fit_method: Fit Method
    :type fit_method: typing.Optional[typing.Union[str, int]]
    :param corner_angle: Corner Angle
    :type corner_angle: typing.Optional[typing.Any]
    :param use_cyclic: Cyclic
    :type use_cyclic: typing.Optional[typing.Union[bool, typing.Any]]
    :param stroke: Stroke
    :type stroke: typing.Optional[bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement]]
    :param wait_for_input: Wait for Input
    :type wait_for_input: typing.Optional[typing.Union[bool, typing.Any]]
    :param is_curve_2d: Curve 2D
    :type is_curve_2d: typing.Optional[typing.Union[bool, typing.Any]]
    :param bezier_as_nurbs: As NURBS
    :type bezier_as_nurbs: typing.Optional[typing.Union[bool, typing.Any]]
    """

    ...

def duplicate(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Copy selected points or curves

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def duplicate_move(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    CURVES_OT_duplicate: typing.Optional[duplicate] = None,
    TRANSFORM_OT_translate: typing.Optional[bpy.ops.transform.translate] = None,
):
    """Make copies of selected elements and move them

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param CURVES_OT_duplicate: Duplicate, Copy selected points or curves
    :type CURVES_OT_duplicate: typing.Optional[duplicate]
    :param TRANSFORM_OT_translate: Move, Move selected items
    :type TRANSFORM_OT_translate: typing.Optional[bpy.ops.transform.translate]
    """

    ...

def extrude(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Extrude selected control point(s)

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def extrude_move(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    CURVES_OT_extrude: typing.Optional[extrude] = None,
    TRANSFORM_OT_translate: typing.Optional[bpy.ops.transform.translate] = None,
):
    """Extrude curve and move result

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param CURVES_OT_extrude: Extrude, Extrude selected control point(s)
    :type CURVES_OT_extrude: typing.Optional[extrude]
    :param TRANSFORM_OT_translate: Move, Move selected items
    :type TRANSFORM_OT_translate: typing.Optional[bpy.ops.transform.translate]
    """

    ...

def handle_type_set(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    type: typing.Optional[typing.Union[str, int]] = "AUTO",
):
    """Set the handle type for bezier curves

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param type: Type
    :type type: typing.Optional[typing.Union[str, int]]
    """

    ...

def sculptmode_toggle(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Enter/Exit sculpt mode for curves

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def select_all(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    action: typing.Optional[typing.Any] = "TOGGLE",
):
    """(De)select all control points

        :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param action: Action, Selection action to execute

    TOGGLE
    Toggle -- Toggle selection for all elements.

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.

    INVERT
    Invert -- Invert selection of all elements.
        :type action: typing.Optional[typing.Any]
    """

    ...

def select_ends(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    amount_start: typing.Optional[typing.Any] = 0,
    amount_end: typing.Optional[typing.Any] = 1,
):
    """Select end points of curves

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param amount_start: Amount Front, Number of points to select from the front
    :type amount_start: typing.Optional[typing.Any]
    :param amount_end: Amount Back, Number of points to select from the back
    :type amount_end: typing.Optional[typing.Any]
    """

    ...

def select_less(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Shrink the selection by one point

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def select_linked(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Select all points in curves with any point selection

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def select_more(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Grow the selection by one point

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def select_random(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    seed: typing.Optional[typing.Any] = 0,
    probability: typing.Optional[typing.Any] = 0.5,
):
    """Randomizes existing selection or create new random selection

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param seed: Seed, Source of randomness
    :type seed: typing.Optional[typing.Any]
    :param probability: Probability, Chance of every point or curve being included in the selection
    :type probability: typing.Optional[typing.Any]
    """

    ...

def set_selection_domain(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    domain: typing.Optional[typing.Union[str, int]] = "POINT",
):
    """Change the mode used for selection masking in curves sculpt mode

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param domain: Domain
    :type domain: typing.Optional[typing.Union[str, int]]
    """

    ...

def snap_curves_to_surface(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    attach_mode: typing.Optional[typing.Any] = "NEAREST",
):
    """Move curves so that the first point is exactly on the surface mesh

        :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
        :type execution_context: typing.Optional[typing.Union[str, int]]
        :type undo: typing.Optional[bool]
        :param attach_mode: Attach Mode, How to find the point on the surface to attach to

    NEAREST
    Nearest -- Find the closest point on the surface for the root point of every curve and move the root there.

    DEFORM
    Deform -- Re-attach curves to a deformed surface using the existing attachment information. This only works when the topology of the surface mesh has not changed.
        :type attach_mode: typing.Optional[typing.Any]
    """

    ...

def subdivide(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
    number_cuts: typing.Optional[typing.Any] = 1,
):
    """Subdivide selected curve segments

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    :param number_cuts: Number of Cuts
    :type number_cuts: typing.Optional[typing.Any]
    """

    ...

def surface_set(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Use the active object as surface for selected curves objects and set it as the parent

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def switch_direction(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Reverse the direction of the selected curves

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...

def tilt_clear(
    override_context: typing.Optional[typing.Union[dict, bpy.types.Context]] = None,
    execution_context: typing.Optional[typing.Union[str, int]] = None,
    undo: typing.Optional[bool] = None,
):
    """Clear the tilt of selected control points

    :type override_context: typing.Optional[typing.Union[dict, bpy.types.Context]]
    :type execution_context: typing.Optional[typing.Union[str, int]]
    :type undo: typing.Optional[bool]
    """

    ...
