import numpy as np
import cv2
from funcnodes import Shelf, NodeDecorator, io


def rotate_cw(img: np.ndarray):
    return np.rot90(img, 1)


def rotate_ccw(img: np.ndarray):
    return np.rot90(img, 3)


def rotate_180(img: np.ndarray):
    return np.rot90(img, 2)


def flip_horizontal(img: np.ndarray):
    return np.flip(img, axis=1)


def flip_vertical(img: np.ndarray):
    return np.flip(img, axis=0)


def crop(
    img: np.ndarray, top: int = 0, left: int = 0, bottom: int = 0, right: int = 0
) -> np.ndarray:
    print(top, left, bottom, right)
    if bottom > 0:
        bottom = -bottom
    else:
        bottom = None
    if right > 0:
        right = -right
    else:
        right = None

    if top < 0:
        top = 0
    if left < 0:
        left = 0

    return img[top:bottom, left:right].copy()


MANIPULATION_SHELVE = Shelf(
    nodes=[
        NodeDecorator(
            "crop_image",
        )(crop),
    ],
    name="manipulation",
    subshelves=[],
    description="webcam stream manipulations",
    default_io_options={
        "out": io.NodeOutputOptions(emit_value_set=False),
        "img": io.NodeInputOptions(emit_value_set=False),
    },
)
