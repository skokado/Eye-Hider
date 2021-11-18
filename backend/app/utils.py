from typing import List
import math

import numpy as np

from app.types import Point, Rectangle


def eye_contour(points: List[Point]) -> Rectangle:
    """目のランドマーク座標を入力に与え、輪郭となる長方形を返す"""
    # 最も左の座標を取得する
    x_coordinates = [x for (x, _) in points]
    y_coordinates = [y for (_, y) in points]
    # pt1: 左上の点の座標
    pt1 = (min(x_coordinates), min(y_coordinates))
    # pt2: 右下の点の座標
    pt2 = (max(x_coordinates), max(y_coordinates))
    return Rectangle(pt1, pt2)


def get_theta(rect1: Rectangle, rect2: Rectangle) -> float:
    """二つの長方形のそれぞれの中心を結んだ線分が作る、水平線との角度をラジアンで返す
    """
    # rect1 の中心
    (p1_x, p1_y), (p2_x, p2_y) = rect1
    x1, y1 = ((p1_x + p2_x) / 2, (p1_y + p2_y) / 2)
    # rect2 の中心
    (p1_x, p1_y), (p2_x, p2_y) = rect2
    x2, y2 = ((p1_x + p2_x) / 2, (p1_y + p2_y) / 2)
    # 傾きを求める
    # 画像における水平方向の傾きのため、ユークリッド平面とは x, y が逆転する
    angle = math.atan2(x2 - x1, y2 - y1)
    if angle < 0:
        angle += math.pi / 2
    return angle


def scaled_rect(rect: Rectangle, rate: float = 2.5) -> Rectangle:
    """2点の座標として与えられた長方形を拡大し、拡大後の2点情報からなる長方形を返す"""
    if rate < 1.0:
        raise ValueError('rate must be > 1')
    (x1, y1), (x2, y2) = rect
    # 2点の中心座標
    mx, my = ((x1 + x2) / 2, (y1 + y2) / 2)
    # 左上の点は座標を減算する
    x1 = max(x1 - (mx - x1) * (rate - 1), 0)
    y1 = max(y1 - (my - y1) * (rate - 1), 0)
    # 右下の点は座標を加算する
    x2 = x2 + (x2 - mx) * (rate - 1)
    y2 = y2 + (y2 - my) * (rate - 1)

    # 各点の座標を整数に直して return
    x1 = round(x1)
    y1 = round(y1)
    x2 = round(x2)
    y2 = round(y2)

    return Rectangle((x1, y1), (x2, y2))


def rotated_rect(rect: Rectangle, t: float) -> np.ndarray:
    """長方形を、その長方形の中心を起点に t(rad) 回転させた4点の座標を返す
    """
    (x1, y1), (x3, y3) = rect
    p1, p3 = np.array([x1, y1]), np.array([x3, y3])
    p2 = np.array([x1, y3])
    p4 = np.array([x3, y1])

    middle = (p1 + p3) / 2
    
    # 回転の作用素となる行列
    R = np.array([[np.cos(-t), -np.sin(-t)],
                  [np.sin(-t), np.cos(-t)]])
    # 長方形の中心座標を中心に回転する
    # 数式の導出は参考サイトを参照: https://python.atelierkobato.com/rotation-matrix/
    # 「次は cy 平面上点 Q(x, y) を点 P(a, b) の周りに回転させることを考えます」
    x1, y1 = np.dot(R, p1 - middle) + middle
    x1, y1 = round(x1), round(y1)
    x2, y2 = np.dot(R, p2 - middle) + middle
    x2, y2 = round(x2), round(y2)
    x3, y3 = np.dot(R, p3 - middle) + middle
    x3, y3 = round(x3), round(y3)
    x4, y4 = np.dot(R, p4 - middle) + middle
    x4, y4 = round(x4), round(y4)
    return (
        (x1, y1),
        (x2, y2),
        (x3, y3),
        (x4, y4),
    )
