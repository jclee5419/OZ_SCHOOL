# mymath.py

import math

def triangle_area(base, height):
    return base * height / 2

def circle_area(radius):
    return math.pi * radius ** 2

def cuboid_area(length, width, height):
    return 2 * (length * width + length * height + width * height)
