class PrettyFormatter:
    def __init__(self):
        pass

    def __call__(self, obj, depth: int = 0):
        return str(obj)

    def format(self, obj, depth: int = 0) -> str:
        return self(obj, depth)
