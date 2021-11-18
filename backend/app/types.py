from typing import NamedTuple

# dlib face lanmark indexes
_right_eye_from_id = 36
_right_eye_to_id = 41
RIGHT_EYE = range(_right_eye_from_id, _right_eye_to_id + 1)

_left_eye_from_id = 42
_left_eye_to_id = 47
LEFT_EYE = range(_left_eye_from_id, _left_eye_to_id + 1)


class Point(NamedTuple):
    x: int
    y: int


class Rectangle(NamedTuple):
    p1: Point
    p2: Point
