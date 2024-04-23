from typing import Optional, Any


class ClassPropertyDescriptor(object):
    def __init__(self, fget: Any, fset: Optional[Any] = None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj: Any, klass: Any = None) -> Any:
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj: Any, value: Any) -> Any:
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func: Any) -> Any:
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self


def classproperty(func: Any) -> Any:
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)
    return ClassPropertyDescriptor(func)
