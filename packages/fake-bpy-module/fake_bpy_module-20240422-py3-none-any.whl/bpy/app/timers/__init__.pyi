"""

--------------------

```../examples/bpy.app.timers.1.py```


--------------------

```../examples/bpy.app.timers.2.py```


--------------------

```../examples/bpy.app.timers.3.py```


--------------------

```../examples/bpy.app.timers.4.py```


--------------------

You should never modify Blender data at arbitrary points in time in separate threads.
However you can use a queue to collect all the actions that should be executed when Blender is in the right state again.
Pythons queue.Queue can be used here, because it implements the required locking semantics.

```../examples/bpy.app.timers.5.py```

"""

import typing

GenericType = typing.TypeVar("GenericType")

def is_registered(function: typing.Optional[int]) -> bool:
    """Check if this function is registered as a timer.

    :param function: Function to check.
    :type function: typing.Optional[int]
    :return: True when this function is registered, otherwise False.
    :rtype: bool
    """

    ...

def register(
    function: typing.Optional[typing.Callable],
    first_interval: typing.Optional[float] = 0,
    persistent: typing.Optional[bool] = False,
):
    """Add a new function that will be called after the specified amount of seconds.
    The function gets no arguments and is expected to return either None or a float.
    If None is returned, the timer will be unregistered.
    A returned number specifies the delay until the function is called again.
    functools.partial can be used to assign some parameters.

        :param function: The function that should called.
        :type function: typing.Optional[typing.Callable]
        :param first_interval: Seconds until the callback should be called the first time.
        :type first_interval: typing.Optional[float]
        :param persistent: Don't remove timer when a new file is loaded.
        :type persistent: typing.Optional[bool]
    """

    ...

def unregister(function: typing.Optional[typing.Any]):
    """Unregister timer.

    :param function: Function to unregister.
    :type function: typing.Optional[typing.Any]
    """

    ...
