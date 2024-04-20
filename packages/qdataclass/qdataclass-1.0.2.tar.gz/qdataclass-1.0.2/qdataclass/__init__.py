from PySide6.QtQml import qmlRegisterType
from .qdataclass import qDataClass



def registerQmlType(uri, versionMajor: int = 1, versionMinor: int = 0):
    def wrap(cls):
        qmlRegisterType(cls, uri, versionMajor, versionMinor, cls.__name__)
        return cls
    return wrap