import os
from pathlib import Path

import cv2
import dlib
from imutils import face_utils
import numpy as np

from app import colors
from app.types import (
    LEFT_EYE,
    RIGHT_EYE
)
from app.utils import *

BASE_DIR = Path(__file__).resolve().parent
IMAGES_BASE_DIR = BASE_DIR / 'tests/images'
MODELS_BASE_DIR = BASE_DIR / 'models'

face_detector = dlib.get_frontal_face_detector()

# 顔のランドマーク検出器
# http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
face_predictor = dlib.shape_predictor(str(MODELS_BASE_DIR / 'shape_predictor_68_face_landmarks.dat'))


def main_handle(input: bytes) -> bytes:
    from tempfile import NamedTemporaryFile
    with NamedTemporaryFile() as tf:
        tf.write(input)
        tf.seek(0)
        img = cv2.imread(tf.name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def _handle_face(img, face):
        # 検出した顔のランドマーク
        landmarks = face_predictor(gray, face)
        # ランドマークを ndarray に変換
        landmarks = face_utils.shape_to_np(landmarks)

        left_eye_points = [
            (x, y)
            for i, (x, y) in enumerate(landmarks)
            if i in LEFT_EYE
        ]
        right_eye_points = [
            (x, y)
            for i, (x, y) in enumerate(landmarks)
            if i in RIGHT_EYE
        ]
        # 左目の輪郭の長方形
        left_eye_rect = eye_contour(left_eye_points)
        # 右目の輪郭の長方形
        right_eye_rect = eye_contour(right_eye_points)


        # 目を囲う長方形を拡大して描画
        (x1, y1), (x2, y2) = scaled_rect(left_eye_rect)
        # cv2.rectangle(img, (x1, y1), (x2, y2), RED, 3)
        (x1, y1), (x2, y2) = scaled_rect(right_eye_rect)
        # cv2.rectangle(img, (x1, y1), (x2, y2), BLUE, 3)

        # 左右の目の回転傾き
        theta = get_theta(left_eye_rect, right_eye_rect)

        # 右目の処理
        scaled_right_eye_rect = scaled_rect(right_eye_rect)
        p1, p2, _, _ = rotated_rect(scaled_right_eye_rect, theta)

        # 左目の処理
        scaled_left_eye_rect = scaled_rect(left_eye_rect)
        rotated_rectangle = rotated_rect(scaled_left_eye_rect, theta)
        _, _, p3, p4 = rotated_rectangle

        # 4つの点を多角形として描画
        points = np.array([p1, p2, p3, p4])
        cv2.fillConvexPoly(img, points, colors.BLACK)
        return img
        
    # 顔検出
    faces = face_detector(gray, 1)
    assert len(faces) >= 1

    for face in faces:
        img = _handle_face(img, face)

    success, img = cv2.imencode('.jpg', img)
    return img.tostring()

if __name__ == '__main__':
    import glob
    for path in glob.glob(str(IMAGES_BASE_DIR / 'input/*.jpeg')):
        filename = os.path.basename(path)
        output_path = IMAGES_BASE_DIR / 'output' / filename
        try:
            print(path)
            with open(path, 'rb') as f:
                masked_img = main_handle(f.read())
            with open(output_path, 'wb') as f:
                f.write(masked_img)
        except AssertionError:
            print('No frontal face detected.')
    for path in glob.glob(str(IMAGES_BASE_DIR / 'input/*.png')):
        filename = os.path.basename(path)
        output_path = IMAGES_BASE_DIR / 'output' / filename
        try:
            print(path)
            with open(path, 'rb') as f:
                masked_img = main_handle(f.read())
            with open(output_path, 'wb') as f:
                f.write(masked_img)
        except AssertionError:
            print('No frontal face detected.')
