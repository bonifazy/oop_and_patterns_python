class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""


class Event:
    def __init__(self, var=None):
        self.var = var or None


class EventGet(Event):
    pass


class EventSet(Event):
    pass


class NullHandler:
    def __init__(self, successor=None):
        # передаём следующее звено
        self.__successor = successor

    def handle(self, new_obj, action):  # обработчик
        if self.__successor is not None:  # даём следующему
            # print(self.__successor)
            self.__successor.handle(new_obj, action)


class IntHandler(NullHandler):
    def handle(self, new_obj, action):
        if action.var == int:
            print(new_obj.integer_field)
            return new_obj.integer_field
        elif type(action.var) == int:
            new_obj.integer_field = action.var
            print(new_obj.integer_field)
        else:
            super().handle(new_obj, action)


class FloatHandler(NullHandler):
    def handle(self, new_obj, action):
        if action.var == float:
            print(new_obj.float_field)
            return new_obj.float_field
        elif type(action.var) == float:
            new_obj.float_field = action.var
            print(new_obj.float_field)
        else:
            super().handle(new_obj, action)


class StrHandler(NullHandler):
    def handle(self, new_obj, action):
        if action.var == str:
            print(new_obj.string_field)
            return new_obj.string_field
        elif type(action.var) == str:
            new_obj.string_field = action.var
            print(new_obj.string_field)
        else:
            super().handle(new_obj, action)


if __name__ == "__main__":
    chain = IntHandler(FloatHandler(StrHandler(NullHandler())))
    obj = SomeObject()
    print(chain.handle(obj, EventGet(int)))  # вернуть значение obj.integer_field
    chain.handle(obj, EventGet(float))  # вернуть значение obj.float_field
    chain.handle(obj, EventGet(str))  # вернуть значение obj.string_field
    chain.handle(obj, EventGet(float))  # вернуть значение obj.float_field
    print(chain.handle(obj, EventSet(1)))  # установить значение obj.integer_field =1
    print(obj.integer_field)
    chain.handle(obj, EventSet(1.1))  # установить значение obj.float_field = 1.1
    chain.handle(obj, EventSet("str"))  # установить значение obj.string_field = "str"
    print(obj.float_field, obj.string_field)
