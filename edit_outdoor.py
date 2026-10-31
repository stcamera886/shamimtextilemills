"""Presentable mill exterior — arched facade crop (no cars/plates), grade."""
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).parent
SRC = ROOT / "images" / "Factory_outdoor_image.jpeg"
OUT = ROOT / "images" / "factory-exterior.jpg"
OUT_WEB = ROOT / "images" / "hero-exterior.jpg"


def main():
    bgr = cv2.imread(str(SRC))
    if bgr is None:
        raise SystemExit(f"Could not read {SRC}")
    h, w = bgr.shape[:2]

    # Mild straighten
    src = np.float32([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]])
    inset = w * 0.025
    dst = np.float32([
        [-inset * 0.3, 0],
        [w - 1 + inset * 0.3, 0],
        [w - 1 - inset, h - 1],
        [inset, h - 1],
    ])
    M = cv2.getPerspectiveTransform(src, dst)
    bgr = cv2.warpPerspective(
        bgr, M, (w, h), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE
    )

    # Arched wing only — skip unfinished tower, trucks, cars, bay clutter
    x0, x1 = int(w * 0.16), int(w * 0.55)
    y0, y1 = int(h * 0.14), int(h * 0.54)
    crop = bgr[y0:y1, x0:x1].copy()

    soft = cv2.bilateralFilter(crop, 5, 20, 20)
    crop = cv2.addWeighted(crop, 0.82, soft, 0.18, 0)

    rgb = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
    arr = np.array(rgb).astype(np.float32)
    arr[..., 0] = np.clip(arr[..., 0] * 0.94, 0, 255)
    arr[..., 2] = np.clip(arr[..., 2] * 1.07, 0, 255)
    rgb = Image.fromarray(arr.astype(np.uint8))
    rgb = ImageEnhance.Contrast(rgb).enhance(1.14)
    rgb = ImageEnhance.Color(rgb).enhance(1.08)
    rgb = ImageEnhance.Brightness(rgb).enhance(1.05)
    rgb = ImageEnhance.Sharpness(rgb).enhance(1.18)
    rgb = ImageOps.autocontrast(rgb, cutoff=0.35)
    out = cv2.cvtColor(np.array(rgb), cv2.COLOR_RGB2BGR)

    cv2.imwrite(str(OUT), out, [int(cv2.IMWRITE_JPEG_QUALITY), 93])
    hh, ww = out.shape[:2]
    web = (
        cv2.resize(out, (1920, int(1920 * hh / ww)), interpolation=cv2.INTER_AREA)
        if ww > 1920
        else out
    )
    cv2.imwrite(str(OUT_WEB), web, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    print("wrote", OUT.name, ww, hh)


if __name__ == "__main__":
    main()
