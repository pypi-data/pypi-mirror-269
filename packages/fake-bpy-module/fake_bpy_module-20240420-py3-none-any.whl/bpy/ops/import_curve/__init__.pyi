import typing
import bpy.types

GenericType = typing.TypeVar("GenericType")

def svg(
    override_context: typing.Union[dict, bpy.types.Context] = None,
    execution_context: typing.Union[str, int] = None,
    undo: bool = None,
    filepath: typing.Union[str, typing.Any] = "",
    filter_glob: typing.Union[str, typing.Any] = "*.svg",
):
    """Load a SVG file

    :type override_context: typing.Union[dict, bpy.types.Context]
    :type execution_context: typing.Union[str, int]
    :type undo: bool
    :param filepath: File Path, Filepath used for importing the file
    :type filepath: typing.Union[str, typing.Any]
    :param filter_glob: filter_glob
    :type filter_glob: typing.Union[str, typing.Any]
    """

    ...
