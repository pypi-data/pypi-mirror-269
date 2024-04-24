"""
This module defines properties to extend Blender's internal data. The result of these functions is used to assign properties to classes registered with Blender and can't be used directly.

[NOTE]
All parameters to these functions must be passed as keywords.


--------------------

Custom properties can be added to any subclass of an ID,
Bone and PoseBone.

These properties can be animated, accessed by the user interface and python
like Blender's existing properties.

[WARNING]
Access to these properties might happen in threaded context, on a per-data-block level.
This has to be carefully considered when using accessors or update callbacks.
Typically, these callbacks should not affect any other data that the one owned by their data-block.
When accessing external non-Blender data, thread safety mechanisms should be considered.

```../examples/bpy.props.py```


--------------------

A common use of custom properties is for python based Operator
classes. Test this code by running it in the text editor, or by clicking the
button in the 3D Viewport's Tools panel. The latter will show the properties
in the Redo panel and allow you to change them.

```../examples/bpy.props.1.py```


--------------------

PropertyGroups can be used for collecting custom settings into one value
to avoid many individual settings mixed in together.

```../examples/bpy.props.2.py```


--------------------

Custom properties can be added to any subclass of an ID,
Bone and PoseBone.

```../examples/bpy.props.3.py```


--------------------

It can be useful to perform an action when a property is changed and can be
used to update other properties or synchronize with external data.

All properties define update functions except for CollectionProperty.

[WARNING]
Remember that these callbacks may be executed in threaded context.

[WARNING]
If the property belongs to an Operator, the update callback's first
parameter will be an OperatorProperties instance, rather than an instance
of the operator itself. This means you can't access other internal functions
of the operator, only its other properties.

```../examples/bpy.props.4.py```


--------------------

Getter/setter functions can be used for boolean, int, float, string and enum properties.
If these callbacks are defined the property will not be stored in the ID properties
automatically. Instead, the get and set functions will be called when the property
is respectively read or written from the API.

[WARNING]
Remember that these callbacks may be executed in threaded context.

```../examples/bpy.props.5.py```

[NOTE]
Typically this function doesn't need to be accessed directly.
Instead use del cls.attr



"""

import typing

GenericType = typing.TypeVar("GenericType")

def BoolProperty(
    name: typing.Optional[str] = "",
    description: typing.Optional[str] = "",
    translation_context: typing.Optional[str] = "*",
    default=False,
    options: typing.Optional[set] = {'"ANIMATABLE"'},
    override: typing.Optional[set] = None(),
    tags: typing.Optional[set] = None(),
    subtype: typing.Optional[str] = "NONE",
    update: typing.Optional[typing.Any] = None,
    get: typing.Optional[typing.Any] = None,
    set: typing.Optional[typing.Any] = None,
):
    """Returns a new boolean property definition.

        :param name: Name used in the user interface.
        :type name: typing.Optional[str]
        :param description: Text used for the tooltip and api documentation.
        :type description: typing.Optional[str]
        :param translation_context: Text used as context to disambiguate translations.
        :type translation_context: typing.Optional[str]
        :param options: Enumerator in `rna_enum_property_flag_items`.
        :type options: typing.Optional[set]
        :param override: Enumerator in `rna_enum_property_override_flag_items`.
        :type override: typing.Optional[set]
        :param tags: Enumerator of tags that are defined by parent class.
        :type tags: typing.Optional[set]
        :param subtype: Enumerator in `rna_enum_property_subtype_number_items`.
        :type subtype: typing.Optional[str]
        :param update: Function to be called when this value is modified,
    This function must take 2 values (self, context) and return None.
    Warning there are no safety checks to avoid infinite recursion.
        :type update: typing.Optional[typing.Any]
        :param get: Function to be called when this value is 'read',
    This function must take 1 value (self) and return the value of the property.
        :type get: typing.Optional[typing.Any]
        :param set: Function to be called when this value is 'written',
    This function must take 2 values (self, value) and return None.
        :type set: typing.Optional[typing.Any]
    """

    ...

def BoolVectorProperty(
    name: typing.Optional[str] = "",
    description: typing.Optional[str] = "",
    translation_context: typing.Optional[str] = "*",
    default: typing.Optional[typing.Sequence] = (False, False, False),
    options: typing.Optional[set] = {'"ANIMATABLE"'},
    override: typing.Optional[set] = None(),
    tags: typing.Optional[set] = None(),
    subtype: typing.Optional[str] = "NONE",
    size: typing.Optional[typing.Union[int, typing.Sequence[int]]] = 3,
    update: typing.Optional[typing.Any] = None,
    get: typing.Optional[typing.Any] = None,
    set: typing.Optional[typing.Any] = None,
):
    """Returns a new vector boolean property definition.

        :param name: Name used in the user interface.
        :type name: typing.Optional[str]
        :param description: Text used for the tooltip and api documentation.
        :type description: typing.Optional[str]
        :param translation_context: Text used as context to disambiguate translations.
        :type translation_context: typing.Optional[str]
        :param default: sequence of booleans the length of size.
        :type default: typing.Optional[typing.Sequence]
        :param options: Enumerator in `rna_enum_property_flag_items`.
        :type options: typing.Optional[set]
        :param override: Enumerator in `rna_enum_property_override_flag_items`.
        :type override: typing.Optional[set]
        :param tags: Enumerator of tags that are defined by parent class.
        :type tags: typing.Optional[set]
        :param subtype: Enumerator in `rna_enum_property_subtype_number_array_items`.
        :type subtype: typing.Optional[str]
        :param size: Vector dimensions in [1, 32]. An int sequence can be used to define multi-dimension arrays.
        :type size: typing.Optional[typing.Union[int, typing.Sequence[int]]]
        :param update: Function to be called when this value is modified,
    This function must take 2 values (self, context) and return None.
    Warning there are no safety checks to avoid infinite recursion.
        :type update: typing.Optional[typing.Any]
        :param get: Function to be called when this value is 'read',
    This function must take 1 value (self) and return the value of the property.
        :type get: typing.Optional[typing.Any]
        :param set: Function to be called when this value is 'written',
    This function must take 2 values (self, value) and return None.
        :type set: typing.Optional[typing.Any]
    """

    ...

def CollectionProperty(
    type=None,
    name: typing.Optional[str] = "",
    description: typing.Optional[str] = "",
    translation_context: typing.Optional[str] = "*",
    options: typing.Optional[set] = {'"ANIMATABLE"'},
    override: typing.Optional[set] = None(),
    tags: typing.Optional[set] = None(),
):
    """Returns a new collection property definition.

    :param type: A subclass of `bpy.types.PropertyGroup`.
    :param name: Name used in the user interface.
    :type name: typing.Optional[str]
    :param description: Text used for the tooltip and api documentation.
    :type description: typing.Optional[str]
    :param translation_context: Text used as context to disambiguate translations.
    :type translation_context: typing.Optional[str]
    :param options: Enumerator in `rna_enum_property_flag_items`.
    :type options: typing.Optional[set]
    :param override: Enumerator in `rna_enum_property_override_flag_collection_items`.
    :type override: typing.Optional[set]
    :param tags: Enumerator of tags that are defined by parent class.
    :type tags: typing.Optional[set]
    """

    ...

def EnumProperty(
    items: typing.Optional[
        typing.Union[typing.Iterable[typing.Iterable[str]], typing.Callable]
    ],
    name: typing.Optional[str] = "",
    description: typing.Optional[str] = "",
    translation_context: typing.Optional[str] = "*",
    default: typing.Optional[typing.Union[str, set]] = None,
    options: typing.Optional[set] = {'"ANIMATABLE"'},
    override: typing.Optional[set] = None(),
    tags: typing.Optional[set] = None(),
    update: typing.Optional[typing.Any] = None,
    get: typing.Optional[typing.Any] = None,
    set: typing.Optional[typing.Any] = None,
):
    """Returns a new enumerator property definition.

        :param items: sequence of enum items formatted:
    [(identifier, name, description, icon, number), ...].

    The first three elements of the tuples are mandatory.

    identifier

    The identifier is used for Python access.

    name

    Name for the interface.

    description

    Used for documentation and tooltips.

    icon

    An icon string identifier or integer icon value
    (e.g. returned by `bpy.types.UILayout.icon`)

    number

    Unique value used as the identifier for this item (stored in file data).
    Use when the identifier may need to change. If the ENUM_FLAG option is used,
    the values are bit-masks and should be powers of two.

    When an item only contains 4 items they define (identifier, name, description, number).

    Separators may be added using None instead of a tuple.
    For dynamic values a callback can be passed which returns a list in
    the same format as the static list.
    This function must take 2 arguments (self, context), context may be None.

    There is a known bug with using a callback,
    Python must keep a reference to the strings returned by the callback or Blender
    will misbehave or even crash.
        :type items: typing.Optional[typing.Union[typing.Iterable[typing.Iterable[str]], typing.Callable]]
        :param name: Name used in the user interface.
        :type name: typing.Optional[str]
        :param description: Text used for the tooltip and api documentation.
        :type description: typing.Optional[str]
        :param translation_context: Text used as context to disambiguate translations.
        :type translation_context: typing.Optional[str]
        :param default: The default value for this enum, a string from the identifiers used in items, or integer matching an item number.
    If the ENUM_FLAG option is used this must be a set of such string identifiers instead.
    WARNING: Strings cannot be specified for dynamic enums
    (i.e. if a callback function is given as items parameter).
        :type default: typing.Optional[typing.Union[str, set]]
        :param options: Enumerator in `rna_enum_property_flag_enum_items`.
        :type options: typing.Optional[set]
        :param override: Enumerator in `rna_enum_property_override_flag_items`.
        :type override: typing.Optional[set]
        :param tags: Enumerator of tags that are defined by parent class.
        :type tags: typing.Optional[set]
        :param update: Function to be called when this value is modified,
    This function must take 2 values (self, context) and return None.
    Warning there are no safety checks to avoid infinite recursion.
        :type update: typing.Optional[typing.Any]
        :param get: Function to be called when this value is 'read',
    This function must take 1 value (self) and return the value of the property.
        :type get: typing.Optional[typing.Any]
        :param set: Function to be called when this value is 'written',
    This function must take 2 values (self, value) and return None.
        :type set: typing.Optional[typing.Any]
    """

    ...

def FloatProperty(
    name: typing.Optional[str] = "",
    description: typing.Optional[str] = "",
    translation_context: typing.Optional[str] = "*",
    default=0.0,
    min: typing.Optional[float] = -3.402823e38,
    max: typing.Optional[float] = 3.402823e38,
    soft_min: typing.Optional[float] = -3.402823e38,
    soft_max: typing.Optional[float] = 3.402823e38,
    step: typing.Optional[int] = 3,
    precision: typing.Optional[int] = 2,
    options: typing.Optional[set] = {'"ANIMATABLE"'},
    override: typing.Optional[set] = None(),
    tags: typing.Optional[set] = None(),
    subtype: typing.Optional[str] = "NONE",
    unit: typing.Optional[str] = "NONE",
    update: typing.Optional[typing.Any] = None,
    get: typing.Optional[typing.Any] = None,
    set: typing.Optional[typing.Any] = None,
):
    """Returns a new float (single precision) property definition.

        :param name: Name used in the user interface.
        :type name: typing.Optional[str]
        :param description: Text used for the tooltip and api documentation.
        :type description: typing.Optional[str]
        :param translation_context: Text used as context to disambiguate translations.
        :type translation_context: typing.Optional[str]
        :param min: Hard minimum, trying to assign a value below will silently assign this minimum instead.
        :type min: typing.Optional[float]
        :param max: Hard maximum, trying to assign a value above will silently assign this maximum instead.
        :type max: typing.Optional[float]
        :param soft_min: Soft minimum (>= min), user won't be able to drag the widget below this value in the UI.
        :type soft_min: typing.Optional[float]
        :param soft_max: Soft maximum (<= max), user won't be able to drag the widget above this value in the UI.
        :type soft_max: typing.Optional[float]
        :param step: Step of increment/decrement in UI, in [1, 100], defaults to 3 (WARNING: actual value is /100).
        :type step: typing.Optional[int]
        :param precision: Maximum number of decimal digits to display, in [0, 6]. Fraction is automatically hidden for exact integer values of fields with unit 'NONE' or 'TIME' (frame count) and step divisible by 100.
        :type precision: typing.Optional[int]
        :param options: Enumerator in `rna_enum_property_flag_items`.
        :type options: typing.Optional[set]
        :param override: Enumerator in `rna_enum_property_override_flag_items`.
        :type override: typing.Optional[set]
        :param tags: Enumerator of tags that are defined by parent class.
        :type tags: typing.Optional[set]
        :param subtype: Enumerator in `rna_enum_property_subtype_number_items`.
        :type subtype: typing.Optional[str]
        :param unit: Enumerator in `rna_enum_property_unit_items`.
        :type unit: typing.Optional[str]
        :param update: Function to be called when this value is modified,
    This function must take 2 values (self, context) and return None.
    Warning there are no safety checks to avoid infinite recursion.
        :type update: typing.Optional[typing.Any]
        :param get: Function to be called when this value is 'read',
    This function must take 1 value (self) and return the value of the property.
        :type get: typing.Optional[typing.Any]
        :param set: Function to be called when this value is 'written',
    This function must take 2 values (self, value) and return None.
        :type set: typing.Optional[typing.Any]
    """

    ...

def FloatVectorProperty(
    name: typing.Optional[str] = "",
    description: typing.Optional[str] = "",
    translation_context: typing.Optional[str] = "*",
    default: typing.Optional[typing.Sequence] = (0.0, 0.0, 0.0),
    min: typing.Optional[float] = None,
    max: typing.Optional[float] = None,
    soft_min: typing.Optional[float] = None,
    soft_max: typing.Optional[float] = None,
    step: typing.Optional[int] = 3,
    precision: typing.Optional[int] = 2,
    options: typing.Optional[set] = {'"ANIMATABLE"'},
    override: typing.Optional[set] = None(),
    tags: typing.Optional[set] = None(),
    subtype: typing.Optional[str] = "NONE",
    unit: typing.Optional[str] = "NONE",
    size: typing.Optional[typing.Union[int, typing.Sequence[int]]] = 3,
    update: typing.Optional[typing.Any] = None,
    get: typing.Optional[typing.Any] = None,
    set: typing.Optional[typing.Any] = None,
):
    """Returns a new vector float property definition.

        :param name: Name used in the user interface.
        :type name: typing.Optional[str]
        :param description: Text used for the tooltip and api documentation.
        :type description: typing.Optional[str]
        :param translation_context: Text used as context to disambiguate translations.
        :type translation_context: typing.Optional[str]
        :param default: sequence of floats the length of size.
        :type default: typing.Optional[typing.Sequence]
        :param min: Hard minimum, trying to assign a value below will silently assign this minimum instead.
        :type min: typing.Optional[float]
        :param max: Hard maximum, trying to assign a value above will silently assign this maximum instead.
        :type max: typing.Optional[float]
        :param soft_min: Soft minimum (>= min), user won't be able to drag the widget below this value in the UI.
        :type soft_min: typing.Optional[float]
        :param soft_max: Soft maximum (<= max), user won't be able to drag the widget above this value in the UI.
        :type soft_max: typing.Optional[float]
        :param step: Step of increment/decrement in UI, in [1, 100], defaults to 3 (WARNING: actual value is /100).
        :type step: typing.Optional[int]
        :param precision: Maximum number of decimal digits to display, in [0, 6]. Fraction is automatically hidden for exact integer values of fields with unit 'NONE' or 'TIME' (frame count) and step divisible by 100.
        :type precision: typing.Optional[int]
        :param options: Enumerator in `rna_enum_property_flag_items`.
        :type options: typing.Optional[set]
        :param override: Enumerator in `rna_enum_property_override_flag_items`.
        :type override: typing.Optional[set]
        :param tags: Enumerator of tags that are defined by parent class.
        :type tags: typing.Optional[set]
        :param subtype: Enumerator in `rna_enum_property_subtype_number_array_items`.
        :type subtype: typing.Optional[str]
        :param unit: Enumerator in `rna_enum_property_unit_items`.
        :type unit: typing.Optional[str]
        :param size: Vector dimensions in [1, 32]. An int sequence can be used to define multi-dimension arrays.
        :type size: typing.Optional[typing.Union[int, typing.Sequence[int]]]
        :param update: Function to be called when this value is modified,
    This function must take 2 values (self, context) and return None.
    Warning there are no safety checks to avoid infinite recursion.
        :type update: typing.Optional[typing.Any]
        :param get: Function to be called when this value is 'read',
    This function must take 1 value (self) and return the value of the property.
        :type get: typing.Optional[typing.Any]
        :param set: Function to be called when this value is 'written',
    This function must take 2 values (self, value) and return None.
        :type set: typing.Optional[typing.Any]
    """

    ...

def IntProperty(
    name: typing.Optional[str] = "",
    description: typing.Optional[str] = "",
    translation_context: typing.Optional[str] = "*",
    default=0,
    min: typing.Optional[int] = None,
    max: typing.Optional[int] = None,
    soft_min: typing.Optional[int] = None,
    soft_max: typing.Optional[int] = None,
    step: typing.Optional[int] = 1,
    options: typing.Optional[set] = {'"ANIMATABLE"'},
    override: typing.Optional[set] = None(),
    tags: typing.Optional[set] = None(),
    subtype: typing.Optional[str] = "NONE",
    update: typing.Optional[typing.Any] = None,
    get: typing.Optional[typing.Any] = None,
    set: typing.Optional[typing.Any] = None,
):
    """Returns a new int property definition.

        :param name: Name used in the user interface.
        :type name: typing.Optional[str]
        :param description: Text used for the tooltip and api documentation.
        :type description: typing.Optional[str]
        :param translation_context: Text used as context to disambiguate translations.
        :type translation_context: typing.Optional[str]
        :param min: Hard minimum, trying to assign a value below will silently assign this minimum instead.
        :type min: typing.Optional[int]
        :param max: Hard maximum, trying to assign a value above will silently assign this maximum instead.
        :type max: typing.Optional[int]
        :param soft_min: Soft minimum (>= min), user won't be able to drag the widget below this value in the UI.
        :type soft_min: typing.Optional[int]
        :param soft_max: Soft maximum (<= max), user won't be able to drag the widget above this value in the UI.
        :type soft_max: typing.Optional[int]
        :param step: Step of increment/decrement in UI, in [1, 100], defaults to 1 (WARNING: unused currently!).
        :type step: typing.Optional[int]
        :param options: Enumerator in `rna_enum_property_flag_items`.
        :type options: typing.Optional[set]
        :param override: Enumerator in `rna_enum_property_override_flag_items`.
        :type override: typing.Optional[set]
        :param tags: Enumerator of tags that are defined by parent class.
        :type tags: typing.Optional[set]
        :param subtype: Enumerator in `rna_enum_property_subtype_number_items`.
        :type subtype: typing.Optional[str]
        :param update: Function to be called when this value is modified,
    This function must take 2 values (self, context) and return None.
    Warning there are no safety checks to avoid infinite recursion.
        :type update: typing.Optional[typing.Any]
        :param get: Function to be called when this value is 'read',
    This function must take 1 value (self) and return the value of the property.
        :type get: typing.Optional[typing.Any]
        :param set: Function to be called when this value is 'written',
    This function must take 2 values (self, value) and return None.
        :type set: typing.Optional[typing.Any]
    """

    ...

def IntVectorProperty(
    name: typing.Optional[str] = "",
    description: typing.Optional[str] = "",
    translation_context: typing.Optional[str] = "*",
    default: typing.Optional[typing.Sequence] = (0, 0, 0),
    min: typing.Optional[int] = None,
    max: typing.Optional[int] = None,
    soft_min: typing.Optional[int] = None,
    soft_max: typing.Optional[int] = None,
    step: typing.Optional[int] = 1,
    options: typing.Optional[set] = {'"ANIMATABLE"'},
    override: typing.Optional[set] = None(),
    tags: typing.Optional[set] = None(),
    subtype: typing.Optional[str] = "NONE",
    size: typing.Optional[typing.Union[int, typing.Sequence[int]]] = 3,
    update: typing.Optional[typing.Any] = None,
    get: typing.Optional[typing.Any] = None,
    set: typing.Optional[typing.Any] = None,
):
    """Returns a new vector int property definition.

        :param name: Name used in the user interface.
        :type name: typing.Optional[str]
        :param description: Text used for the tooltip and api documentation.
        :type description: typing.Optional[str]
        :param translation_context: Text used as context to disambiguate translations.
        :type translation_context: typing.Optional[str]
        :param default: sequence of ints the length of size.
        :type default: typing.Optional[typing.Sequence]
        :param min: Hard minimum, trying to assign a value below will silently assign this minimum instead.
        :type min: typing.Optional[int]
        :param max: Hard maximum, trying to assign a value above will silently assign this maximum instead.
        :type max: typing.Optional[int]
        :param soft_min: Soft minimum (>= min), user won't be able to drag the widget below this value in the UI.
        :type soft_min: typing.Optional[int]
        :param soft_max: Soft maximum (<= max), user won't be able to drag the widget above this value in the UI.
        :type soft_max: typing.Optional[int]
        :param step: Step of increment/decrement in UI, in [1, 100], defaults to 1 (WARNING: unused currently!).
        :type step: typing.Optional[int]
        :param options: Enumerator in `rna_enum_property_flag_items`.
        :type options: typing.Optional[set]
        :param override: Enumerator in `rna_enum_property_override_flag_items`.
        :type override: typing.Optional[set]
        :param tags: Enumerator of tags that are defined by parent class.
        :type tags: typing.Optional[set]
        :param subtype: Enumerator in `rna_enum_property_subtype_number_array_items`.
        :type subtype: typing.Optional[str]
        :param size: Vector dimensions in [1, 32]. An int sequence can be used to define multi-dimension arrays.
        :type size: typing.Optional[typing.Union[int, typing.Sequence[int]]]
        :param update: Function to be called when this value is modified,
    This function must take 2 values (self, context) and return None.
    Warning there are no safety checks to avoid infinite recursion.
        :type update: typing.Optional[typing.Any]
        :param get: Function to be called when this value is 'read',
    This function must take 1 value (self) and return the value of the property.
        :type get: typing.Optional[typing.Any]
        :param set: Function to be called when this value is 'written',
    This function must take 2 values (self, value) and return None.
        :type set: typing.Optional[typing.Any]
    """

    ...

def PointerProperty(
    type=None,
    name: typing.Optional[str] = "",
    description: typing.Optional[str] = "",
    translation_context: typing.Optional[str] = "*",
    options: typing.Optional[set] = {'"ANIMATABLE"'},
    override: typing.Optional[set] = None(),
    tags: typing.Optional[set] = None(),
    poll: typing.Optional[typing.Any] = None,
    update: typing.Optional[typing.Any] = None,
):
    """Returns a new pointer property definition.

        :param type: A subclass of `bpy.types.PropertyGroup` or `bpy.types.ID`.
        :param name: Name used in the user interface.
        :type name: typing.Optional[str]
        :param description: Text used for the tooltip and api documentation.
        :type description: typing.Optional[str]
        :param translation_context: Text used as context to disambiguate translations.
        :type translation_context: typing.Optional[str]
        :param options: Enumerator in `rna_enum_property_flag_items`.
        :type options: typing.Optional[set]
        :param override: Enumerator in `rna_enum_property_override_flag_items`.
        :type override: typing.Optional[set]
        :param tags: Enumerator of tags that are defined by parent class.
        :type tags: typing.Optional[set]
        :param poll: function to be called to determine whether an item is valid for this property.
    The function must take 2 values (self, object) and return Bool.
        :type poll: typing.Optional[typing.Any]
        :param update: Function to be called when this value is modified,
    This function must take 2 values (self, context) and return None.
    Warning there are no safety checks to avoid infinite recursion.
        :type update: typing.Optional[typing.Any]
    """

    ...

def RemoveProperty(cls: typing.Optional[typing.Any], attr: typing.Optional[str]):
    """Removes a dynamically defined property.

    :param cls: The class containing the property (must be a positional argument).
    :type cls: typing.Optional[typing.Any]
    :param attr: Property name (must be passed as a keyword).
    :type attr: typing.Optional[str]
    """

    ...

def StringProperty(
    name: typing.Optional[str] = "",
    description: typing.Optional[str] = "",
    translation_context: typing.Optional[str] = "*",
    default: typing.Optional[str] = "",
    maxlen: typing.Optional[int] = 0,
    options: typing.Optional[set] = {'"ANIMATABLE"'},
    override: typing.Optional[set] = None(),
    tags: typing.Optional[set] = None(),
    subtype: typing.Optional[str] = "NONE",
    update: typing.Optional[typing.Any] = None,
    get: typing.Optional[typing.Any] = None,
    set: typing.Optional[typing.Any] = None,
    search: typing.Optional[typing.Any] = None,
    search_options: typing.Optional[set] = {'"SUGGESTION"'},
):
    """Returns a new string property definition.

        :param name: Name used in the user interface.
        :type name: typing.Optional[str]
        :param description: Text used for the tooltip and api documentation.
        :type description: typing.Optional[str]
        :param translation_context: Text used as context to disambiguate translations.
        :type translation_context: typing.Optional[str]
        :param default: initializer string.
        :type default: typing.Optional[str]
        :param maxlen: maximum length of the string.
        :type maxlen: typing.Optional[int]
        :param options: Enumerator in `rna_enum_property_flag_items`.
        :type options: typing.Optional[set]
        :param override: Enumerator in `rna_enum_property_override_flag_items`.
        :type override: typing.Optional[set]
        :param tags: Enumerator of tags that are defined by parent class.
        :type tags: typing.Optional[set]
        :param subtype: Enumerator in `rna_enum_property_subtype_string_items`.
        :type subtype: typing.Optional[str]
        :param update: Function to be called when this value is modified,
    This function must take 2 values (self, context) and return None.
    Warning there are no safety checks to avoid infinite recursion.
        :type update: typing.Optional[typing.Any]
        :param get: Function to be called when this value is 'read',
    This function must take 1 value (self) and return the value of the property.
        :type get: typing.Optional[typing.Any]
        :param set: Function to be called when this value is 'written',
    This function must take 2 values (self, value) and return None.
        :type set: typing.Optional[typing.Any]
        :param search: Function to be called to show candidates for this string (shown in the UI).
    This function must take 3 values (self, context, edit_text)
    and return a sequence, iterator or generator where each item must be:

    A single string (representing a candidate to display).

    A tuple-pair of strings, where the first is a candidate and the second
    is additional information about the candidate.
        :type search: typing.Optional[typing.Any]
        :param search_options: Set of strings in:

    'SORT' sorts the resulting items.

    'SUGGESTION' lets the user enter values not found in search candidates.
    WARNING disabling this flag causes the search callback to run on redraw,
    so only disable this flag if it's not likely to cause performance issues.
        :type search_options: typing.Optional[set]
    """

    ...
