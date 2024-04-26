from typing import Tuple, Union
import numpy as np
import cv2
from funcnodes import Shelf, NodeDecorator, io
import colorsys
from ..utils import cv2_image_preview_generator, convert_to_uint8_img


def rgbstring_to_rgb_array(
    rgb_string
) -> Union[Tuple[int, int, int], Tuple[int, int, int, int]]:
    """
    Converts a RGB string to an RGB array.
    Args:
    - rgb_string (str): A string representing a color in RGB format. Can be in the
                        format '#RGB', '#RRGGBB', or '#RRGGBBAA'.
    Returns:
    - list: A list of integers representing the color in RGB format. Alpha is included
            if provided in the input.
    """

    # Remove the '#' character
    hex_color = rgb_string.lstrip("#").lower()
    # Short format '#RGB' or '#RGBA', need to double each character
    if len(hex_color) == 3 or len(hex_color) == 4:
        hex_color = "".join([c * 2 for c in hex_color])

    # Convert the hex color to an integer, then to a list of RGB(A) values
    rgb_array = [int(hex_color[i : i + 2], 16) for i in range(0, len(hex_color), 2)]
    return np.array(rgb_array, dtype=np.uint8)


def rgb_to_hsv(rgb: Union[Tuple[int, int, int], Tuple[int, int, int, int], str]):
    """
    Converts an RGB or RGBA color to HSV.
    Args:
    - rgb (Tuple[int, int, int] | Tuple[int, int, int, int] | str): RGB or RGBA color.

    Returns:
    - Tuple[float, float, float]: HSV representation of the color.
    """

    # If the input is a string, first convert it to an RGB or RGBA tuple

    if isinstance(rgb, str):
        rgb = rgbstring_to_rgb_array(rgb)

    rgb = rgb[:3]

    # Normalize RGB values to [0, 1] range
    r, g, b = [x / 255.0 for x in rgb]
    # Convert to HSV using colorsys, values will be in the range [0, 1]
    hsv = colorsys.rgb_to_hsv(r, g, b)
    hsv = np.array([hsv[0] * 180, hsv[1] * 255, hsv[2] * 255], dtype=np.uint8)
    return hsv


def hsv_mask(
    min_th: Union[Tuple[int, int, int], str],
    max_th: Union[Tuple[int, int, int], str],
    frame: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    if isinstance(min_th, str):
        min_th = rgb_to_hsv(rgbstring_to_rgb_array(min_th))
    else:
        min_th = [min_th[0] / 360 * 255, min_th[1] / 100 * 255, min_th[2] / 100 * 255]
    if isinstance(max_th, str):
        max_th = rgb_to_hsv(rgbstring_to_rgb_array(max_th))
    else:
        max_th = [max_th[0] / 360 * 255, max_th[1] / 100 * 255, max_th[2] / 100 * 255]

    min_th = np.array(min_th, dtype=np.uint8)
    max_th = np.array(max_th, dtype=np.uint8)
    frame = convert_to_uint8_img(frame, assert_3_channels=True)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, np.array(min_th), np.array(max_th))
    mask = mask.astype(bool)
    # make frame greyscale only the mask is colored
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grey_frame = cv2.cvtColor(grey_frame, cv2.COLOR_GRAY2BGR)

    grey_frame[mask] = frame[mask]

    return grey_frame, mask


def largest_contour(mask: np.ndarray) -> np.ndarray:
    mask = convert_to_uint8_img(mask, assert_3_channels=False)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return np.array([])
    return max(contours, key=cv2.contourArea)


@NodeDecorator(
    "largest_contour",
    default_render_options={},
)
def largest_contour_node(mask: np.ndarray) -> np.ndarray:
    return largest_contour(mask)


@NodeDecorator(
    "plot_contour",
    default_render_options={
        "data": {
            "src": "out",
            "type": "image",
            "preview_type": "image",
        }
    },
    default_io_options={
        "out": io.NodeOutputOptions(
            valuepreview_generator=cv2_image_preview_generator,
            valuepreview_type="image",
        ),
    },
)
def plot_contour(img: np.ndarray, contour: np.ndarray) -> np.ndarray:
    img = convert_to_uint8_img(img, assert_3_channels=True)
    if len(contour) == 0:
        return img

    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    img = cv2.drawContours(img, [contour], -1, (0, 255, 0), 2)

    return img


@NodeDecorator(
    "contour_bounds",
    outputs=[
        {"name": "left", "type": "int"},
        {"name": "top", "type": "int"},
        {"name": "width/right", "type": "int"},
        {"name": "height/bottom", "type": "int"},
    ],
)
def contour_bounds(
    contour: np.ndarray, as_tlrb: bool = True, img: np.ndarray = None
) -> Tuple[int, int, int, int]:
    if len(contour) == 0:
        return io.NoValue
    x, y, w, h = cv2.boundingRect(contour)
    if as_tlrb and img is not None:
        return (x, y, img.shape[1] - x - w, img.shape[0] - y - h)

    return (x, y, w, h)


@NodeDecorator(
    "image_shape",
    outputs=[
        {"name": "height", "type": "int"},
        {"name": "width", "type": "int"},
    ],
)
def image_shape(img: np.ndarray) -> Tuple[int, int]:
    return (
        img.shape[0],
        img.shape[1],
    )


def get_brighness(frame: np.ndarray) -> np.ndarray:
    """gets the brightness of a frame"""
    # convert to hsl
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # calculate the brightness
    return hsv[..., 2]


FILTER_SHELVE = Shelf(
    nodes=[
        NodeDecorator(
            "hsv_mask",
            default_value_options={
                "min_th": {"colorspace": "hsv"},
                "max_th": {"colorspace": "hsv"},
            },
            default_render_options={
                "io": {"min_th": {"type": "color"}, "max_th": {"type": "color"}},
                "data": {
                    "src": "grey_frame",
                    "type": "plot",
                    "plottype": "imshow",
                    "colorscale": "bgr",
                },
            },
            outputs=[
                {
                    "name": "grey_frame",
                },
                {"name": "mask"},
            ],
            default_io_options={
                "grey_frame": io.NodeOutputOptions(
                    valuepreview_generator=cv2_image_preview_generator,
                    valuepreview_type="image",
                ),
                "mask": io.NodeOutputOptions(
                    valuepreview_generator=cv2_image_preview_generator,
                    valuepreview_type="image",
                ),
                "min_th": io.NodeInputOptions(
                    value_options={"colorspace": "hsv"},
                ),
                "max_th": io.NodeInputOptions(
                    value_options={"colorspace": "hsv"},
                ),
            },
        )(hsv_mask),
        largest_contour_node,
        plot_contour,
        contour_bounds,
        image_shape,
        NodeDecorator(
            "get_brighness",
            outputs=[
                {"name": "brightness"},
            ],
        )(get_brighness),
    ],
    name="filter",
    subshelves=[],
    description="webcam stream filter",
)
