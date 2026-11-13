from collections import namedtuple
import numpy as np

def distance_between_point_and_line(A, B, P):
    x1, y1 = A
    x2, y2 = B
    p1, p2 = P
    #A = namedtuple('A',['x1', 'y1'])
    #B = namedtuple('B',['x2', 'y2'])
    return np.dot(A,B)

print(distance_between_point_and_line((1,2),(2,4),(0,0)))