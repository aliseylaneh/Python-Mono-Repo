class ContextManagerExample:
    def __init__(self):
        self.name = "I'm a context manager"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_trace) -> bool:
        return False


with ContextManagerExample() as obj:
    print(type(obj))
    print("We are in context manager: ", obj.name)
