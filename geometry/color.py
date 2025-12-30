class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        
    def clamp(self):
        self.r = min(255, max(0, self.r))
        self.g = min(255, max(0, self.g))
        self.b = min(255, max(0, self.b))
        return self
    
    def round(self):
        self.r = int(self.r)
        self.g = int(self.g)
        self.b = int(self.b)
        return self

    def mul(self, n):
        return Color(self.r * n, self.g * n, self.b * n)

    def add(self, other):
        return Color(self.r + other.r, self.g + other.g, self.b + other.b)
