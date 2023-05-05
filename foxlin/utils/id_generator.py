class genid:
    def __init__(self, base: int):
        self.x = base

    def __call__(self):
        x = self.x
        y = self.x = x + 1
        return y

