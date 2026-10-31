"""Subtle fabric drape on upper rollers — empty machines look better than zigzag fakes."""
from pathlib import Path
import cv2
import numpy as np

ROOT = Path(__file__).parent
THERM_SRC = ROOT / "images" / "Thermosol.jpg"
BLEACH_SRC = ROOT / "images" / "continous_bleaching.jpg"
THERM_OUT = ROOT / "images" / "gallery-thermosol.jpg"
BLEACH_OUT = ROOT / "images" / "gallery-bleaching.jpg"


def cream_cloth(h=400, w=280) -> np.ndarray:
    img = np.full((h, w, 3), (210, 214, 218), np.uint8)
    noise = np.random.normal(0, 5.5, (h, w)).astype(np.float32)
    for y in range(0, h, 2):
        noise[y] += 2.5
    for x in range(0, w, 3):
        noise[:, x] += 2.0
    for c in range(3):
        ch = img[..., c].astype(np.float32) + noise
        if c == 2:
            ch += 5
        img[..., c] = np.clip(ch, 0, 255).astype(np.uint8)
    # Soft vertical folds
    x = np.linspace(0, 4 * np.pi, w)
    fold = (np.sin(x) * 6).astype(np.float32)
    img = img.astype(np.float32)
    img += fold[None, :, None]
    img = np.clip(img, 0, 255).astype(np.uint8)
    return cv2.GaussianBlur(img, (3, 3), 0)


def drape_quad(canvas, cloth, dst_quad, opacity=0.88):
    """Perspective-place a cloth rectangle; soft-edge composite."""
    h, w = canvas.shape[:2]
    ch, cw = cloth.shape[:2]
    src = np.float32([[0, 0], [cw - 1, 0], [cw - 1, ch - 1], [0, ch - 1]])
    dst = np.float32(dst_quad)
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(cloth, M, (w, h))
    mask = np.zeros((h, w), np.uint8)
    cv2.fillConvexPoly(mask, dst.astype(np.int32), 255)
    # Erode then blur for soft textile edge
    mask = cv2.erode(mask, np.ones((3, 3), np.uint8), iterations=1)
    alpha = cv2.GaussianBlur(mask.astype(np.float32) / 255.0, (11, 11), 0) * opacity
    # Contact shadow
    sh = cv2.GaussianBlur((alpha * 255).astype(np.uint8), (21, 21), 0).astype(np.float32) / 255.0
    canvas[:] = (canvas.astype(np.float32) * (1.0 - sh[..., None] * 0.15)).astype(np.uint8)
    a3 = alpha[..., None]
    canvas[:] = (warped.astype(np.float32) * a3 + canvas.astype(np.float32) * (1 - a3)).astype(
        np.uint8
    )


def thermosol(cloth: np.ndarray) -> np.ndarray:
    bgr = cv2.imread(str(THERM_SRC))
    h, w = bgr.shape[:2]
    out = bgr.copy()
    # Flat open-width sheet over upper roller bank (not a zig-zag snake)
    # Quad: TL TR BR BL in image coords
    drape_quad(
        out,
        cloth,
        [
            [w * 0.30, h * 0.09],
            [w * 0.58, h * 0.08],
            [w * 0.57, h * 0.28],
            [w * 0.31, h * 0.29],
        ],
        opacity=0.84,
    )
    # Short hanging drop from front roller
    drape_quad(
        out,
        cloth,
        [
            [w * 0.34, h * 0.26],
            [w * 0.54, h * 0.25],
            [w * 0.53, h * 0.48],
            [w * 0.35, h * 0.49],
        ],
        opacity=0.80,
    )
    return cv2.convertScaleAbs(out, alpha=1.03, beta=3)


def bleaching(cloth: np.ndarray) -> np.ndarray:
    bgr = cv2.imread(str(BLEACH_SRC))
    h, w = bgr.shape[:2]
    out = bgr.copy()
    # Sheet across top rollers
    drape_quad(
        out,
        cloth,
        [
            [w * 0.36, h * 0.08],
            [w * 0.64, h * 0.07],
            [w * 0.63, h * 0.24],
            [w * 0.37, h * 0.25],
        ],
        opacity=0.85,
    )
    # Cloth sitting on / wrapping upper face of drum (trapezoid)
    drape_quad(
        out,
        cloth,
        [
            [w * 0.34, h * 0.40],
            [w * 0.66, h * 0.39],
            [w * 0.62, h * 0.55],
            [w * 0.38, h * 0.56],
        ],
        opacity=0.78,
    )
    return cv2.convertScaleAbs(out, alpha=1.03, beta=3)


def main():
    cloth = cream_cloth()
    therm = thermosol(cloth)
    bleach = bleaching(cloth)
    cv2.imwrite(str(THERM_OUT), therm, [int(cv2.IMWRITE_JPEG_QUALITY), 91])
    cv2.imwrite(str(BLEACH_OUT), bleach, [int(cv2.IMWRITE_JPEG_QUALITY), 91])
    print("wrote", THERM_OUT.name, BLEACH_OUT.name)


if __name__ == "__main__":
    main()
