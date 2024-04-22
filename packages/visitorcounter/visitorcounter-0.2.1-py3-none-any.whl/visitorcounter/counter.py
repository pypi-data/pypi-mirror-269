class VisitorCounter:
    def __init__(self):
        self.visitors = {}

    def add_visit(self, ip_address):
        if ip_address in self.visitors:
            self.visitors[ip_address] += 1
        else:
            self.visitors[ip_address] = 1

    def get_visit_count(self, ip_address):
        return self.visitors.get(ip_address, 0)