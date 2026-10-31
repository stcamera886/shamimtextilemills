"""Restore clean thermosol machine photo (no wrong mill-09 substitute)."""
from pathlib import Path
import cv2

ROOT = Path(__file__).parent
SRC = ROOT / "images" / "_tmp" / "thermosol_clean_src.jpg"
OUT = ROOT / "images" / "gallery-thermosol.jpg"
OUT_MILL = ROOT / "images" / "mill" / "thermosol.jpg"


def main():
    im = cv2.imread(str(SRC))
    if im is None:
        raise SystemExit(f"missing {SRC}")
    cv2.imwrite(str(OUT), im, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
    cv2.imwrite(str(OUT_MILL), im, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
    print("restored", OUT, im.shape[1], im.shape[0])


if __name__ == "__main__":
    main()
