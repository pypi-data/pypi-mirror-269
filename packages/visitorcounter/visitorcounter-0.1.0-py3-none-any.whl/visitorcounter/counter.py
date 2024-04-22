class VisitorCounter:
    def __init__(self):
        self.count = 0

    def visit(self):
        self.count += 1
        return self.count

    def get_count(self):
        return self.count
