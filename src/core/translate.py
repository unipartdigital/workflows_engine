from weakref import WeakKeyDictionary


class Translatable:
    """ Helper Class to allow for translate component attributes to be translated to the users
        language

        By default no translation occurs, to setup translations replace the `_translator` class
        method with your own translation mechanism.

        e.g
        ```python
        Translatable._translator = staticmethod(magic_translation_function)
        ```
    """

    _translator = staticmethod(lambda x: x)

    def __init__(self):
        self._refs = WeakKeyDictionary()

    def __get__(self, inst, cls):
        if inst is None:
            return self

        value = self._refs.get(inst)
        if isinstance(value, str):
            return self._translator(value)
        else:
            return value

    def __set__(self, inst, value):
        self._refs[inst] = value
