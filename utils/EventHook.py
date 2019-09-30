class EventHook(object):
    def __init__(self):
        self.__handlers = []

    def __iadd__(self, handler):
        self.__handlers.append(handler)
        return self

    def __isub__(self, handler):
        self.__handlers.remove(handler)
        return self

    def fire(self, *args, **keywargs):
        print(f'Event fired with args {args} and kwargs {keywargs}')
        for handler in self.__handlers:
            print(f'Handler {handler.__name__} responding')
            handler(*args, **keywargs)