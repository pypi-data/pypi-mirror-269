import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def add_render_slot(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Add a new render slot

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def change_frame(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    frame: typing.Any = 0,
):
    """Interactively change the current frame number

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param frame: Frame
    :type frame: typing.Any
    """

    ...

def clear_render_border(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Clear the boundaries of the render region and disable render region

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def clear_render_slot(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Clear the currently selected render slot

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def clipboard_copy(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Copy the image to the clipboard

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def clipboard_paste(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Paste new image from the clipboard

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def curves_point_set(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    point: typing.Any = "BLACK_POINT",
    size: typing.Any = 1,
):
    """Set black point or white point for curves

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param point: Point, Set black point or white point for curves
    :type point: typing.Any
    :param size: Sample Size
    :type size: typing.Any
    """

    ...

def cycle_render_slot(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    reverse: typing.Union[bool, typing.Any] = False,
):
    """Cycle through all non-void render slots

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param reverse: Cycle in Reverse
    :type reverse: typing.Union[bool, typing.Any]
    """

    ...

def external_edit(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    filepath: typing.Union[str, typing.Any] = "",
):
    """Edit image in an external application

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param filepath: filepath
    :type filepath: typing.Union[str, typing.Any]
    """

    ...

def file_browse(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    filepath: typing.Union[str, typing.Any] = "",
    hide_props_region: typing.Union[bool, typing.Any] = True,
    check_existing: typing.Union[bool, typing.Any] = False,
    filter_blender: typing.Union[bool, typing.Any] = False,
    filter_backup: typing.Union[bool, typing.Any] = False,
    filter_image: typing.Union[bool, typing.Any] = True,
    filter_movie: typing.Union[bool, typing.Any] = True,
    filter_python: typing.Union[bool, typing.Any] = False,
    filter_font: typing.Union[bool, typing.Any] = False,
    filter_sound: typing.Union[bool, typing.Any] = False,
    filter_text: typing.Union[bool, typing.Any] = False,
    filter_archive: typing.Union[bool, typing.Any] = False,
    filter_btx: typing.Union[bool, typing.Any] = False,
    filter_collada: typing.Union[bool, typing.Any] = False,
    filter_alembic: typing.Union[bool, typing.Any] = False,
    filter_usd: typing.Union[bool, typing.Any] = False,
    filter_obj: typing.Union[bool, typing.Any] = False,
    filter_volume: typing.Union[bool, typing.Any] = False,
    filter_folder: typing.Union[bool, typing.Any] = True,
    filter_blenlib: typing.Union[bool, typing.Any] = False,
    filemode: typing.Any = 9,
    relative_path: typing.Union[bool, typing.Any] = True,
    show_multiview: typing.Union[bool, typing.Any] = False,
    use_multiview: typing.Union[bool, typing.Any] = False,
    display_type: typing.Any = "DEFAULT",
    sort_method: typing.Union[str, int, typing.Any] = "",
):
    """Open an image file browser, hold Shift to open the file, Alt to browse containing directory

        :type override_context: typing.Union[dict, bpy.types.Context]
        :type execution_context: typing.Union[str, int]
        :type undo: bool
        :param filepath: File Path, Path to file
        :type filepath: typing.Union[str, typing.Any]
        :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings
        :type hide_props_region: typing.Union[bool, typing.Any]
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: typing.Union[bool, typing.Any]
        :param filter_blender: Filter .blend files
        :type filter_blender: typing.Union[bool, typing.Any]
        :param filter_backup: Filter .blend files
        :type filter_backup: typing.Union[bool, typing.Any]
        :param filter_image: Filter image files
        :type filter_image: typing.Union[bool, typing.Any]
        :param filter_movie: Filter movie files
        :type filter_movie: typing.Union[bool, typing.Any]
        :param filter_python: Filter Python files
        :type filter_python: typing.Union[bool, typing.Any]
        :param filter_font: Filter font files
        :type filter_font: typing.Union[bool, typing.Any]
        :param filter_sound: Filter sound files
        :type filter_sound: typing.Union[bool, typing.Any]
        :param filter_text: Filter text files
        :type filter_text: typing.Union[bool, typing.Any]
        :param filter_archive: Filter archive files
        :type filter_archive: typing.Union[bool, typing.Any]
        :param filter_btx: Filter btx files
        :type filter_btx: typing.Union[bool, typing.Any]
        :param filter_collada: Filter COLLADA files
        :type filter_collada: typing.Union[bool, typing.Any]
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: typing.Union[bool, typing.Any]
        :param filter_usd: Filter USD files
        :type filter_usd: typing.Union[bool, typing.Any]
        :param filter_obj: Filter OBJ files
        :type filter_obj: typing.Union[bool, typing.Any]
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: typing.Union[bool, typing.Any]
        :param filter_folder: Filter folders
        :type filter_folder: typing.Union[bool, typing.Any]
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: typing.Union[bool, typing.Any]
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: typing.Any
        :param relative_path: Relative Path, Select the file relative to the blend file
        :type relative_path: typing.Union[bool, typing.Any]
        :param show_multiview: Enable Multi-View
        :type show_multiview: typing.Union[bool, typing.Any]
        :param use_multiview: Use Multi-View
        :type use_multiview: typing.Union[bool, typing.Any]
        :param display_type: Display Type

    DEFAULT
    Default -- Automatically determine display type for files.

    LIST_VERTICAL
    Short List -- Display files as short list.

    LIST_HORIZONTAL
    Long List -- Display files as a detailed list.

    THUMBNAIL
    Thumbnails -- Display files as thumbnails.
        :type display_type: typing.Any
        :param sort_method: File sorting mode
        :type sort_method: typing.Union[str, int, typing.Any]
    """

    ...

def flip(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    use_flip_x: typing.Union[bool, typing.Any] = False,
    use_flip_y: typing.Union[bool, typing.Any] = False,
):
    """Flip the image

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param use_flip_x: Horizontal, Flip the image horizontally
    :type use_flip_x: typing.Union[bool, typing.Any]
    :param use_flip_y: Vertical, Flip the image vertically
    :type use_flip_y: typing.Union[bool, typing.Any]
    """

    ...

def invert(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    invert_r: typing.Union[bool, typing.Any] = False,
    invert_g: typing.Union[bool, typing.Any] = False,
    invert_b: typing.Union[bool, typing.Any] = False,
    invert_a: typing.Union[bool, typing.Any] = False,
):
    """Invert image's channels

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param invert_r: Red, Invert red channel
    :type invert_r: typing.Union[bool, typing.Any]
    :param invert_g: Green, Invert green channel
    :type invert_g: typing.Union[bool, typing.Any]
    :param invert_b: Blue, Invert blue channel
    :type invert_b: typing.Union[bool, typing.Any]
    :param invert_a: Alpha, Invert alpha channel
    :type invert_a: typing.Union[bool, typing.Any]
    """

    ...

def match_movie_length(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Set image's user's length to the one of this video

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def new(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    name: typing.Union[str, typing.Any] = "Untitled",
    width: typing.Any = 1024,
    height: typing.Any = 1024,
    color: typing.Any = (0.0, 0.0, 0.0, 1.0),
    alpha: typing.Union[bool, typing.Any] = True,
    generated_type: typing.Union[str, int] = "BLANK",
    float: typing.Union[bool, typing.Any] = False,
    use_stereo_3d: typing.Union[bool, typing.Any] = False,
    tiled: typing.Union[bool, typing.Any] = False,
):
    """Create a new image

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param name: Name, Image data-block name
    :type name: typing.Union[str, typing.Any]
    :param width: Width, Image width
    :type width: typing.Any
    :param height: Height, Image height
    :type height: typing.Any
    :param color: Color, Default fill color
    :type color: typing.Any
    :param alpha: Alpha, Create an image with an alpha channel
    :type alpha: typing.Union[bool, typing.Any]
    :param generated_type: Generated Type, Fill the image with a grid for UV map testing
    :type generated_type: typing.Union[str, int]
    :param float: 32-bit Float, Create image with 32-bit floating-point bit depth
    :type float: typing.Union[bool, typing.Any]
    :param use_stereo_3d: Stereo 3D, Create an image with left and right views
    :type use_stereo_3d: typing.Union[bool, typing.Any]
    :param tiled: Tiled, Create a tiled image
    :type tiled: typing.Union[bool, typing.Any]
    """

    ...

def open(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    allow_path_tokens: typing.Union[bool, typing.Any] = True,
    filepath: typing.Union[str, typing.Any] = "",
    directory: typing.Union[str, typing.Any] = "",
    files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement] = None,
    hide_props_region: typing.Union[bool, typing.Any] = True,
    check_existing: typing.Union[bool, typing.Any] = False,
    filter_blender: typing.Union[bool, typing.Any] = False,
    filter_backup: typing.Union[bool, typing.Any] = False,
    filter_image: typing.Union[bool, typing.Any] = True,
    filter_movie: typing.Union[bool, typing.Any] = True,
    filter_python: typing.Union[bool, typing.Any] = False,
    filter_font: typing.Union[bool, typing.Any] = False,
    filter_sound: typing.Union[bool, typing.Any] = False,
    filter_text: typing.Union[bool, typing.Any] = False,
    filter_archive: typing.Union[bool, typing.Any] = False,
    filter_btx: typing.Union[bool, typing.Any] = False,
    filter_collada: typing.Union[bool, typing.Any] = False,
    filter_alembic: typing.Union[bool, typing.Any] = False,
    filter_usd: typing.Union[bool, typing.Any] = False,
    filter_obj: typing.Union[bool, typing.Any] = False,
    filter_volume: typing.Union[bool, typing.Any] = False,
    filter_folder: typing.Union[bool, typing.Any] = True,
    filter_blenlib: typing.Union[bool, typing.Any] = False,
    filemode: typing.Any = 9,
    relative_path: typing.Union[bool, typing.Any] = True,
    show_multiview: typing.Union[bool, typing.Any] = False,
    use_multiview: typing.Union[bool, typing.Any] = False,
    display_type: typing.Any = "DEFAULT",
    sort_method: typing.Any = "",
    use_sequence_detection: typing.Union[bool, typing.Any] = True,
    use_udim_detecting: typing.Union[bool, typing.Any] = True,
):
    """Open image

        :type override_context: typing.Union[dict, bpy.types.Context]
        :type execution_context: typing.Union[str, int]
        :type undo: bool
        :param allow_path_tokens: Allow the path to contain substitution tokens
        :type allow_path_tokens: typing.Union[bool, typing.Any]
        :param filepath: File Path, Path to file
        :type filepath: typing.Union[str, typing.Any]
        :param directory: Directory, Directory of the file
        :type directory: typing.Union[str, typing.Any]
        :param files: Files
        :type files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]
        :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings
        :type hide_props_region: typing.Union[bool, typing.Any]
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: typing.Union[bool, typing.Any]
        :param filter_blender: Filter .blend files
        :type filter_blender: typing.Union[bool, typing.Any]
        :param filter_backup: Filter .blend files
        :type filter_backup: typing.Union[bool, typing.Any]
        :param filter_image: Filter image files
        :type filter_image: typing.Union[bool, typing.Any]
        :param filter_movie: Filter movie files
        :type filter_movie: typing.Union[bool, typing.Any]
        :param filter_python: Filter Python files
        :type filter_python: typing.Union[bool, typing.Any]
        :param filter_font: Filter font files
        :type filter_font: typing.Union[bool, typing.Any]
        :param filter_sound: Filter sound files
        :type filter_sound: typing.Union[bool, typing.Any]
        :param filter_text: Filter text files
        :type filter_text: typing.Union[bool, typing.Any]
        :param filter_archive: Filter archive files
        :type filter_archive: typing.Union[bool, typing.Any]
        :param filter_btx: Filter btx files
        :type filter_btx: typing.Union[bool, typing.Any]
        :param filter_collada: Filter COLLADA files
        :type filter_collada: typing.Union[bool, typing.Any]
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: typing.Union[bool, typing.Any]
        :param filter_usd: Filter USD files
        :type filter_usd: typing.Union[bool, typing.Any]
        :param filter_obj: Filter OBJ files
        :type filter_obj: typing.Union[bool, typing.Any]
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: typing.Union[bool, typing.Any]
        :param filter_folder: Filter folders
        :type filter_folder: typing.Union[bool, typing.Any]
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: typing.Union[bool, typing.Any]
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: typing.Any
        :param relative_path: Relative Path, Select the file relative to the blend file
        :type relative_path: typing.Union[bool, typing.Any]
        :param show_multiview: Enable Multi-View
        :type show_multiview: typing.Union[bool, typing.Any]
        :param use_multiview: Use Multi-View
        :type use_multiview: typing.Union[bool, typing.Any]
        :param display_type: Display Type

    DEFAULT
    Default -- Automatically determine display type for files.

    LIST_VERTICAL
    Short List -- Display files as short list.

    LIST_HORIZONTAL
    Long List -- Display files as a detailed list.

    THUMBNAIL
    Thumbnails -- Display files as thumbnails.
        :type display_type: typing.Any
        :param sort_method: File sorting mode

    DEFAULT
    Default -- Automatically determine sort method for files.

    FILE_SORT_ALPHA
    Name -- Sort the file list alphabetically.

    FILE_SORT_EXTENSION
    Extension -- Sort the file list by extension/type.

    FILE_SORT_TIME
    Modified Date -- Sort files by modification time.

    FILE_SORT_SIZE
    Size -- Sort files by size.
        :type sort_method: typing.Any
        :param use_sequence_detection: Detect Sequences, Automatically detect animated sequences in selected images (based on file names)
        :type use_sequence_detection: typing.Union[bool, typing.Any]
        :param use_udim_detecting: Detect UDIMs, Detect selected UDIM files and load all matching tiles
        :type use_udim_detecting: typing.Union[bool, typing.Any]
    """

    ...

def pack(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Pack an image as embedded data into the .blend file

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def project_apply(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Project edited image back onto the object

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def project_edit(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Edit a snapshot of the 3D Viewport in an external image editor

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def read_viewlayers(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Read all the current scene's view layers from cache, as needed

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def reload(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Reload current image from disk

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def remove_render_slot(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Remove the current render slot

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def render_border(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    xmin: typing.Any = 0,
    xmax: typing.Any = 0,
    ymin: typing.Any = 0,
    ymax: typing.Any = 0,
    wait_for_input: typing.Union[bool, typing.Any] = True,
):
    """Set the boundaries of the render region and enable render region

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
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
    """

    ...

def replace(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    filepath: typing.Union[str, typing.Any] = "",
    hide_props_region: typing.Union[bool, typing.Any] = True,
    check_existing: typing.Union[bool, typing.Any] = False,
    filter_blender: typing.Union[bool, typing.Any] = False,
    filter_backup: typing.Union[bool, typing.Any] = False,
    filter_image: typing.Union[bool, typing.Any] = True,
    filter_movie: typing.Union[bool, typing.Any] = True,
    filter_python: typing.Union[bool, typing.Any] = False,
    filter_font: typing.Union[bool, typing.Any] = False,
    filter_sound: typing.Union[bool, typing.Any] = False,
    filter_text: typing.Union[bool, typing.Any] = False,
    filter_archive: typing.Union[bool, typing.Any] = False,
    filter_btx: typing.Union[bool, typing.Any] = False,
    filter_collada: typing.Union[bool, typing.Any] = False,
    filter_alembic: typing.Union[bool, typing.Any] = False,
    filter_usd: typing.Union[bool, typing.Any] = False,
    filter_obj: typing.Union[bool, typing.Any] = False,
    filter_volume: typing.Union[bool, typing.Any] = False,
    filter_folder: typing.Union[bool, typing.Any] = True,
    filter_blenlib: typing.Union[bool, typing.Any] = False,
    filemode: typing.Any = 9,
    relative_path: typing.Union[bool, typing.Any] = True,
    show_multiview: typing.Union[bool, typing.Any] = False,
    use_multiview: typing.Union[bool, typing.Any] = False,
    display_type: typing.Any = "DEFAULT",
    sort_method: typing.Union[str, int, typing.Any] = "",
):
    """Replace current image by another one from disk

        :type override_context: typing.Union[dict, bpy.types.Context]
        :type execution_context: typing.Union[str, int]
        :type undo: bool
        :param filepath: File Path, Path to file
        :type filepath: typing.Union[str, typing.Any]
        :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings
        :type hide_props_region: typing.Union[bool, typing.Any]
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: typing.Union[bool, typing.Any]
        :param filter_blender: Filter .blend files
        :type filter_blender: typing.Union[bool, typing.Any]
        :param filter_backup: Filter .blend files
        :type filter_backup: typing.Union[bool, typing.Any]
        :param filter_image: Filter image files
        :type filter_image: typing.Union[bool, typing.Any]
        :param filter_movie: Filter movie files
        :type filter_movie: typing.Union[bool, typing.Any]
        :param filter_python: Filter Python files
        :type filter_python: typing.Union[bool, typing.Any]
        :param filter_font: Filter font files
        :type filter_font: typing.Union[bool, typing.Any]
        :param filter_sound: Filter sound files
        :type filter_sound: typing.Union[bool, typing.Any]
        :param filter_text: Filter text files
        :type filter_text: typing.Union[bool, typing.Any]
        :param filter_archive: Filter archive files
        :type filter_archive: typing.Union[bool, typing.Any]
        :param filter_btx: Filter btx files
        :type filter_btx: typing.Union[bool, typing.Any]
        :param filter_collada: Filter COLLADA files
        :type filter_collada: typing.Union[bool, typing.Any]
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: typing.Union[bool, typing.Any]
        :param filter_usd: Filter USD files
        :type filter_usd: typing.Union[bool, typing.Any]
        :param filter_obj: Filter OBJ files
        :type filter_obj: typing.Union[bool, typing.Any]
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: typing.Union[bool, typing.Any]
        :param filter_folder: Filter folders
        :type filter_folder: typing.Union[bool, typing.Any]
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: typing.Union[bool, typing.Any]
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: typing.Any
        :param relative_path: Relative Path, Select the file relative to the blend file
        :type relative_path: typing.Union[bool, typing.Any]
        :param show_multiview: Enable Multi-View
        :type show_multiview: typing.Union[bool, typing.Any]
        :param use_multiview: Use Multi-View
        :type use_multiview: typing.Union[bool, typing.Any]
        :param display_type: Display Type

    DEFAULT
    Default -- Automatically determine display type for files.

    LIST_VERTICAL
    Short List -- Display files as short list.

    LIST_HORIZONTAL
    Long List -- Display files as a detailed list.

    THUMBNAIL
    Thumbnails -- Display files as thumbnails.
        :type display_type: typing.Any
        :param sort_method: File sorting mode
        :type sort_method: typing.Union[str, int, typing.Any]
    """

    ...

def resize(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    size: typing.Any = (0, 0),
):
    """Resize the image

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param size: Size
    :type size: typing.Any
    """

    ...

def rotate_orthogonal(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    degrees: typing.Any = "90",
):
    """Rotate the image

        :type override_context: typing.Union[dict, bpy.types.Context]
        :type execution_context: typing.Union[str, int]
        :type undo: bool
        :param degrees: Degrees, Amount of rotation in degrees (90, 180, 270)

    90
    90 Degrees -- Rotate 90 degrees clockwise.

    180
    180 Degrees -- Rotate 180 degrees clockwise.

    270
    270 Degrees -- Rotate 270 degrees clockwise.
        :type degrees: typing.Any
    """

    ...

def sample(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    size: typing.Any = 1,
):
    """Use mouse to sample a color in current image

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param size: Sample Size
    :type size: typing.Any
    """

    ...

def sample_line(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    xstart: typing.Any = 0,
    xend: typing.Any = 0,
    ystart: typing.Any = 0,
    yend: typing.Any = 0,
    flip: typing.Union[bool, typing.Any] = False,
    cursor: typing.Any = 5,
):
    """Sample a line and show it in Scope panels

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param xstart: X Start
    :type xstart: typing.Any
    :param xend: X End
    :type xend: typing.Any
    :param ystart: Y Start
    :type ystart: typing.Any
    :param yend: Y End
    :type yend: typing.Any
    :param flip: Flip
    :type flip: typing.Union[bool, typing.Any]
    :param cursor: Cursor, Mouse cursor style to use during the modal operator
    :type cursor: typing.Any
    """

    ...

def save(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Save the image with current name and settings

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def save_all_modified(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Save all modified images

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def save_as(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    save_as_render: typing.Union[bool, typing.Any] = False,
    copy: typing.Union[bool, typing.Any] = False,
    allow_path_tokens: typing.Union[bool, typing.Any] = True,
    filepath: typing.Union[str, typing.Any] = "",
    check_existing: typing.Union[bool, typing.Any] = True,
    filter_blender: typing.Union[bool, typing.Any] = False,
    filter_backup: typing.Union[bool, typing.Any] = False,
    filter_image: typing.Union[bool, typing.Any] = True,
    filter_movie: typing.Union[bool, typing.Any] = True,
    filter_python: typing.Union[bool, typing.Any] = False,
    filter_font: typing.Union[bool, typing.Any] = False,
    filter_sound: typing.Union[bool, typing.Any] = False,
    filter_text: typing.Union[bool, typing.Any] = False,
    filter_archive: typing.Union[bool, typing.Any] = False,
    filter_btx: typing.Union[bool, typing.Any] = False,
    filter_collada: typing.Union[bool, typing.Any] = False,
    filter_alembic: typing.Union[bool, typing.Any] = False,
    filter_usd: typing.Union[bool, typing.Any] = False,
    filter_obj: typing.Union[bool, typing.Any] = False,
    filter_volume: typing.Union[bool, typing.Any] = False,
    filter_folder: typing.Union[bool, typing.Any] = True,
    filter_blenlib: typing.Union[bool, typing.Any] = False,
    filemode: typing.Any = 9,
    relative_path: typing.Union[bool, typing.Any] = True,
    show_multiview: typing.Union[bool, typing.Any] = False,
    use_multiview: typing.Union[bool, typing.Any] = False,
    display_type: typing.Any = "DEFAULT",
    sort_method: typing.Union[str, int, typing.Any] = "",
):
    """Save the image with another name and/or settings

        :type override_context: typing.Union[dict, bpy.types.Context]
        :type execution_context: typing.Union[str, int]
        :type undo: bool
        :param save_as_render: Save As Render, Save image with render color management.For display image formats like PNG, apply view and display transform.For intermediate image formats like OpenEXR, use the default render output color space
        :type save_as_render: typing.Union[bool, typing.Any]
        :param copy: Copy, Create a new image file without modifying the current image in Blender
        :type copy: typing.Union[bool, typing.Any]
        :param allow_path_tokens: Allow the path to contain substitution tokens
        :type allow_path_tokens: typing.Union[bool, typing.Any]
        :param filepath: File Path, Path to file
        :type filepath: typing.Union[str, typing.Any]
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: typing.Union[bool, typing.Any]
        :param filter_blender: Filter .blend files
        :type filter_blender: typing.Union[bool, typing.Any]
        :param filter_backup: Filter .blend files
        :type filter_backup: typing.Union[bool, typing.Any]
        :param filter_image: Filter image files
        :type filter_image: typing.Union[bool, typing.Any]
        :param filter_movie: Filter movie files
        :type filter_movie: typing.Union[bool, typing.Any]
        :param filter_python: Filter Python files
        :type filter_python: typing.Union[bool, typing.Any]
        :param filter_font: Filter font files
        :type filter_font: typing.Union[bool, typing.Any]
        :param filter_sound: Filter sound files
        :type filter_sound: typing.Union[bool, typing.Any]
        :param filter_text: Filter text files
        :type filter_text: typing.Union[bool, typing.Any]
        :param filter_archive: Filter archive files
        :type filter_archive: typing.Union[bool, typing.Any]
        :param filter_btx: Filter btx files
        :type filter_btx: typing.Union[bool, typing.Any]
        :param filter_collada: Filter COLLADA files
        :type filter_collada: typing.Union[bool, typing.Any]
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: typing.Union[bool, typing.Any]
        :param filter_usd: Filter USD files
        :type filter_usd: typing.Union[bool, typing.Any]
        :param filter_obj: Filter OBJ files
        :type filter_obj: typing.Union[bool, typing.Any]
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: typing.Union[bool, typing.Any]
        :param filter_folder: Filter folders
        :type filter_folder: typing.Union[bool, typing.Any]
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: typing.Union[bool, typing.Any]
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: typing.Any
        :param relative_path: Relative Path, Select the file relative to the blend file
        :type relative_path: typing.Union[bool, typing.Any]
        :param show_multiview: Enable Multi-View
        :type show_multiview: typing.Union[bool, typing.Any]
        :param use_multiview: Use Multi-View
        :type use_multiview: typing.Union[bool, typing.Any]
        :param display_type: Display Type

    DEFAULT
    Default -- Automatically determine display type for files.

    LIST_VERTICAL
    Short List -- Display files as short list.

    LIST_HORIZONTAL
    Long List -- Display files as a detailed list.

    THUMBNAIL
    Thumbnails -- Display files as thumbnails.
        :type display_type: typing.Any
        :param sort_method: File sorting mode
        :type sort_method: typing.Union[str, int, typing.Any]
    """

    ...

def save_sequence(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Save a sequence of images

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def tile_add(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    number: typing.Any = 1002,
    count: typing.Any = 1,
    label: typing.Union[str, typing.Any] = "",
    fill: typing.Union[bool, typing.Any] = True,
    color: typing.Any = (0.0, 0.0, 0.0, 1.0),
    generated_type: typing.Union[str, int] = "BLANK",
    width: typing.Any = 1024,
    height: typing.Any = 1024,
    float: typing.Union[bool, typing.Any] = False,
    alpha: typing.Union[bool, typing.Any] = True,
):
    """Adds a tile to the image

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param number: Number, UDIM number of the tile
    :type number: typing.Any
    :param count: Count, How many tiles to add
    :type count: typing.Any
    :param label: Label, Optional tile label
    :type label: typing.Union[str, typing.Any]
    :param fill: Fill, Fill new tile with a generated image
    :type fill: typing.Union[bool, typing.Any]
    :param color: Color, Default fill color
    :type color: typing.Any
    :param generated_type: Generated Type, Fill the image with a grid for UV map testing
    :type generated_type: typing.Union[str, int]
    :param width: Width, Image width
    :type width: typing.Any
    :param height: Height, Image height
    :type height: typing.Any
    :param float: 32-bit Float, Create image with 32-bit floating-point bit depth
    :type float: typing.Union[bool, typing.Any]
    :param alpha: Alpha, Create an image with an alpha channel
    :type alpha: typing.Union[bool, typing.Any]
    """

    ...

def tile_fill(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    color: typing.Any = (0.0, 0.0, 0.0, 1.0),
    generated_type: typing.Union[str, int] = "BLANK",
    width: typing.Any = 1024,
    height: typing.Any = 1024,
    float: typing.Union[bool, typing.Any] = False,
    alpha: typing.Union[bool, typing.Any] = True,
):
    """Fill the current tile with a generated image

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param color: Color, Default fill color
    :type color: typing.Any
    :param generated_type: Generated Type, Fill the image with a grid for UV map testing
    :type generated_type: typing.Union[str, int]
    :param width: Width, Image width
    :type width: typing.Any
    :param height: Height, Image height
    :type height: typing.Any
    :param float: 32-bit Float, Create image with 32-bit floating-point bit depth
    :type float: typing.Union[bool, typing.Any]
    :param alpha: Alpha, Create an image with an alpha channel
    :type alpha: typing.Union[bool, typing.Any]
    """

    ...

def tile_remove(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Removes a tile from the image

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def unpack(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    method: typing.Union[str, int] = "USE_LOCAL",
    id: typing.Union[str, typing.Any] = "",
):
    """Save an image packed in the .blend file to disk

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param method: Method, How to unpack
    :type method: typing.Union[str, int]
    :param id: Image Name, Image data-block name to unpack
    :type id: typing.Union[str, typing.Any]
    """

    ...

def view_all(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    fit_view: typing.Union[bool, typing.Any] = False,
):
    """View the entire image

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param fit_view: Fit View, Fit frame to the viewport
    :type fit_view: typing.Union[bool, typing.Any]
    """

    ...

def view_center_cursor(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Center the view so that the cursor is in the middle of the view

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def view_cursor_center(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    fit_view: typing.Union[bool, typing.Any] = False,
):
    """Set 2D Cursor To Center View location

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param fit_view: Fit View, Fit frame to the viewport
    :type fit_view: typing.Union[bool, typing.Any]
    """

    ...

def view_ndof(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """Use a 3D mouse device to pan/zoom the view

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def view_pan(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    offset: typing.Any = (0.0, 0.0),
):
    """Pan the view

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param offset: Offset, Offset in floating-point units, 1.0 is the width and height of the image
    :type offset: typing.Any
    """

    ...

def view_selected(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
):
    """View all selected UVs

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    """

    ...

def view_zoom(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    factor: typing.Any = 0.0,
    use_cursor_init: typing.Union[bool, typing.Any] = True,
):
    """Zoom in/out the image

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param factor: Factor, Zoom factor, values higher than 1.0 zoom in, lower values zoom out
    :type factor: typing.Any
    :param use_cursor_init: Use Mouse Position, Allow the initial mouse position to be used
    :type use_cursor_init: typing.Union[bool, typing.Any]
    """

    ...

def view_zoom_border(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    xmin: typing.Any = 0,
    xmax: typing.Any = 0,
    ymin: typing.Any = 0,
    ymax: typing.Any = 0,
    wait_for_input: typing.Union[bool, typing.Any] = True,
    zoom_out: typing.Union[bool, typing.Any] = False,
):
    """Zoom in the view to the nearest item contained in the border

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
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
    :param zoom_out: Zoom Out
    :type zoom_out: typing.Union[bool, typing.Any]
    """

    ...

def view_zoom_in(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    location: typing.Any = (0.0, 0.0),
):
    """Zoom in the image (centered around 2D cursor)

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param location: Location, Cursor location in screen coordinates
    :type location: typing.Any
    """

    ...

def view_zoom_out(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    location: typing.Any = (0.0, 0.0),
):
    """Zoom out the image (centered around 2D cursor)

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param location: Location, Cursor location in screen coordinates
    :type location: typing.Any
    """

    ...

def view_zoom_ratio(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    ratio: typing.Any = 0.0,
):
    """Set zoom ratio of the view

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param ratio: Ratio, Zoom ratio, 1.0 is 1:1, higher is zoomed in, lower is zoomed out
    :type ratio: typing.Any
    """

    ...
