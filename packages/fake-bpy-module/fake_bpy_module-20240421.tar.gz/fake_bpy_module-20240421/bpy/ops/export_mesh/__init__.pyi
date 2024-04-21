import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def stl(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    filepath: typing.Union[str, typing.Any] = "",
    check_existing: typing.Union[bool, typing.Any] = True,
    filter_glob: typing.Union[str, typing.Any] = "*.stl",
    use_selection: typing.Union[bool, typing.Any] = False,
    global_scale: typing.Any = 1.0,
    use_scene_unit: typing.Union[bool, typing.Any] = False,
    ascii: typing.Union[bool, typing.Any] = False,
    use_mesh_modifiers: typing.Union[bool, typing.Any] = True,
    batch_mode: typing.Any = "OFF",
    global_space: typing.Any = (
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
    ),
    axis_forward: typing.Any = "Y",
    axis_up: typing.Any = "Z",
):
    """Save STL triangle mesh data

        :type override_context: typing.Union[dict, bpy.types.Context]
        :type execution_context: typing.Union[str, int]
        :type undo: bool
        :param filepath: File Path, Filepath used for exporting the file
        :type filepath: typing.Union[str, typing.Any]
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: typing.Union[bool, typing.Any]
        :param filter_glob: filter_glob
        :type filter_glob: typing.Union[str, typing.Any]
        :param use_selection: Selection Only, Export selected objects only
        :type use_selection: typing.Union[bool, typing.Any]
        :param global_scale: Scale
        :type global_scale: typing.Any
        :param use_scene_unit: Scene Unit, Apply current scene's unit (as defined by unit scale) to exported data
        :type use_scene_unit: typing.Union[bool, typing.Any]
        :param ascii: Ascii, Save the file in ASCII file format
        :type ascii: typing.Union[bool, typing.Any]
        :param use_mesh_modifiers: Apply Modifiers, Apply the modifiers before saving
        :type use_mesh_modifiers: typing.Union[bool, typing.Any]
        :param batch_mode: Batch Mode

    OFF
    Off -- All data in one file.

    OBJECT
    Object -- Each object as a file.
        :type batch_mode: typing.Any
        :param global_space: Global Space, Export in this reference space
        :type global_space: typing.Any
        :param axis_forward: Forward
        :type axis_forward: typing.Any
        :param axis_up: Up
        :type axis_up: typing.Any
    """

    ...
