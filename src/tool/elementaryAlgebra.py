import math

class elementaryAlgebra():
    @staticmethod
    def dot(a, b):
        return ((a.x * b.x) + (a.y * b.y) + (a.z * b.z))
    @staticmethod
    def length(N):
        return math.sqrt(elementaryAlgebra.dot(N, N))