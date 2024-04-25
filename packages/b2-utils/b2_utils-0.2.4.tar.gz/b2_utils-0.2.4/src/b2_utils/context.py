from collections.abc import Callable as _Callable
from contextlib import contextmanager as _contextmanager
from typing import Any as _Any

from django.apps import apps as _apps
from django.db.models.signals import ModelSignal as _ModelSignal

from b2_utils.helpers import get_component as _get_component

__all__ = [
    "signal_muffler",
]


@_contextmanager
def signal_muffler(
    signal: _ModelSignal,
    receiver: str | _Callable,
    sender: _Any | str | tuple[str, str] | None = None,
    dispatch_uid: str | None = None,
):
    """
    Temporarily disconnect a signal handler to mute its effects within a context.

    This context manager allows you to temporarily mute the effects of a signal handler by disconnecting it during
    the execution of the enclosed block of code. After the block is executed, the signal handler is reconnected.

    Args:
        signal (ModelSignal): The signal to be muted.
        receiver (str | Callable): The receiver of the signal, either as a callable function or as a string path
            to a function.
        sender (Any | str | tuple[str, str] | None, optional): The sender of the signal, which can be specified as
            a model class, a string path to a model, or a tuple containing two strings (app label and model name).
            Defaults to None.
        dispatch_uid (str | None, optional): An optional unique identifier for the signal. Defaults to None.

    Yields:
        None: A context is yielded to the enclosed block of code.

    Examples:
        # Mute a signal within a context using a function receiver
        with signal_muffler(post_save, my_signal_handler):
            my_model_instance.save()  # The signal handler is temporarily disconnected.

        # Mute a signal within a context using a string receiver and specifying the sender
        with signal_muffler(pre_delete, "myapp.signals.my_signal_handler", sender="myapp.MyModel"):
            MyModel.objects.get(pk=1).delete()  # The signal handler is temporarily disconnected.

    """
    if isinstance(receiver, str):
        receiver = _get_component(receiver)

    if isinstance(sender, str):
        sender = _apps.get_model(sender)
    elif isinstance(sender, tuple):
        sender = _apps.get_model(*sender)

    signal.disconnect(receiver, sender, dispatch_uid=dispatch_uid)
    try:
        yield

    finally:
        signal.connect(receiver, sender, dispatch_uid=dispatch_uid)
