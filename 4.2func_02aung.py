import math
def FindScaleneTriangleArea(a, b, c):
    s = (a + b + c) / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    print("Area of This Triangle is %.2f m²" % area)

Length1 = int(input("Input length of the first side(m): "))
Length2 = int(input("Input length of the second side(m): "))
Length3 = int(input("Input length of the third side(m): "))
FindScaleneTriangleArea(Length1, Length2, Length3)