import types
from PySide6.QtCore import QObject, Signal, Property
import sys


def qDataClass(cls=None):
    def wrap(cls):
        return _process_cls(cls)

    if cls is None:
        return wrap
    return wrap(cls)


def _getter_setter(prop_name, default=None):
    def getter(self):
        return getattr(self, "_"+prop_name) if hasattr(self, "_"+prop_name) else default

    def setter(self, value):
        setattr(self, "_"+prop_name, value)
        if hasattr(self, prop_name+"Changed"):
            getattr(self, prop_name+"Changed").emit(value)

    return getter, setter


def _process_cls(cls: type):
    if "staticMetaObject" not in cls.__dict__:
        raise Exception("Class must be a QObject")
    ann = cls.__annotations__
    for prop_name, prop_type in ann.items():
        if hasattr(cls, prop_name):
            continue
        if prop_type in {Property, Signal}:
            continue
        getter, setter = _getter_setter(prop_name)
        signal = Signal(prop_type)
        setattr(cls, prop_name+"Changed", signal)
        setattr(cls, prop_name, Property(
            prop_type, getter, setter, notify=signal))
    new_class = types.new_class(
        cls.__name__, cls.__bases__, exec_body=lambda ns: ns.update(cls.__dict__))
    sys.modules[cls.__module__].__dict__[cls.__name__] = new_class
    del cls
    return new_class
