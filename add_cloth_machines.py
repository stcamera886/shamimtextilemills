"""Composite cream woven cloth onto empty thermosol & continuous bleaching photos."""
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

ROOT = Path(__file__).parent
THERMO_SRC = ROOT / "images" / "Thermosol.jpg"
BLEACH_SRC = ROOT / "images" / "continous_bleaching.jpg"
THERMO_OUT = ROOT / "images" / "gallery-thermosol.jpg"
BLEACH_OUT = ROOT / "images" / "gallery-bleaching.jpg"
TMP = ROOT / "images" / "_tmp"
TMP.mkdir(exist_ok=True)


def make_cream_cloth(tw: int = 640, th: int = 900) -> np.ndarray:
    """Procedural cream woven fabric — matches mill greige/processed cloth look."""
    # BGR cream / off-white
    base = np.zeros((th, tw, 3), np.float32)
    base[..., 0] = 214  # B
    base[..., 1] = 224  # G
    base[..., 2] = 232  # R
    yy, xx = np.mgrid[0:th, 0:tw]
    # warp threads
    weave_v = (np.sin(yy / 2.8) * 4.5).astype(np.float32)
    weave_h = (np.sin(xx / 3.2) * 3.5).astype(np.float32)
    base += (weave_v + weave_h)[..., None]
    # soft mottling
    noise = np.random.normal(0, 5.5, (th, tw, 3)).astype(np.float32)
    soft = cv2.GaussianBlur(noise, (0, 0), 1.4)
    base += soft
    # faint fold shade bands
    fold = (np.sin(xx / 55.0) * 6.0).astype(np.float32)
    base += fold[..., None]
    return np.clip(base, 0, 255).astype(np.uint8)


def paste_quad(
    canvas: np.ndarray,
    cloth: np.ndarray,
    dst_quad: np.ndarray,
    opacity: float = 0.92,
) -> None:
    h, w = canvas.shape[:2]
    src_h, src_w = cloth.shape[:2]
    src_quad = np.float32([[0, 0], [src_w - 1, 0], [src_w - 1, src_h - 1], [0, src_h - 1]])
    dst = dst_quad.astype(np.float32)
    mat = cv2.getPerspectiveTransform(src_quad, dst)
    warped = cv2.warpPerspective(cloth, mat, (w, h), flags=cv2.INTER_LINEAR)

    mask = np.zeros((h, w), np.uint8)
    cv2.fillConvexPoly(mask, np.round(dst).astype(np.int32), 255)
    mask = cv2.GaussianBlur(mask, (0, 0), 1.8)

    # contact shadow under cloth edge
    shadow = cv2.GaussianBlur(mask, (0, 0), 4.0)
    sh = (shadow.astype(np.float32) / 255.0) * 0.18
    canvas[:] = (canvas.astype(np.float32) * (1.0 - sh[..., None])).astype(np.uint8)

    xs = dst[:, 0]
    x0, x1 = float(xs.min()), float(xs.max())
    shade = np.ones((h, w), np.float32)
    if x1 > x0:
        gx = np.linspace(0, 1, w, dtype=np.float32)
        # only meaningful inside bbox but cheap full-width curve is fine
        roll = 0.90 + 0.12 * (1.0 - np.abs(gx - ((x0 + x1) * 0.5 / max(w, 1))) * 2.0)
        # simpler: center highlight relative to quad center
        cx = (x0 + x1) * 0.5
        for x in range(max(0, int(x0) - 2), min(w, int(x1) + 3)):
            t = abs((x - cx) / max(1.0, (x1 - x0) * 0.5))
            shade[:, x] = 0.88 + 0.14 * max(0.0, 1.0 - t)

    alpha = (mask.astype(np.float32) / 255.0) * opacity
    a3 = alpha[..., None]
    shaded = warped.astype(np.float32) * shade[..., None]
    # slight warm lift so cloth reads in dim mill light
    shaded = shaded * np.array([0.98, 1.0, 1.03], dtype=np.float32)
    canvas[:] = np.clip(shaded * a3 + canvas.astype(np.float32) * (1 - a3), 0, 255).astype(np.uint8)


def nq(w: int, h: int, pts: list[tuple[float, float]]) -> np.ndarray:
    return np.float32([[p[0] * w, p[1] * h] for p in pts])


def grade(bgr: np.ndarray) -> np.ndarray:
    rgb = Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
    rgb = ImageEnhance.Contrast(rgb).enhance(1.05)
    rgb = ImageEnhance.Color(rgb).enhance(1.03)
    rgb = ImageEnhance.Brightness(rgb).enhance(1.02)
    return cv2.cvtColor(np.array(rgb), cv2.COLOR_RGB2BGR)


def roller_cloth(
    out: np.ndarray,
    cloth: np.ndarray,
    x0: float,
    x1: float,
    y: float,
    thick: float = 0.022,
    opacity: float = 0.93,
) -> None:
    """Thin horizontal fabric strip draped on a roller."""
    h, w = out.shape[:2]
    paste_quad(
        out,
        cloth,
        nq(
            w,
            h,
            [
                (x0, y),
                (x1, y - thick * 0.15),
                (x1 + 0.004, y + thick),
                (x0 - 0.002, y + thick * 1.05),
            ],
        ),
        opacity,
    )


def hang_cloth(
    out: np.ndarray,
    cloth: np.ndarray,
    x0: float,
    x1: float,
    y0: float,
    y1: float,
    opacity: float = 0.82,
) -> None:
    """Vertical hanging fabric panel between rollers."""
    h, w = out.shape[:2]
    paste_quad(
        out,
        cloth,
        nq(w, h, [(x0, y0), (x1, y0 - 0.004), (x1 + 0.01, y1), (x0 - 0.008, y1 + 0.006)]),
        opacity,
    )


def process_thermosol(bgr: np.ndarray, cloth: np.ndarray) -> np.ndarray:
    out = bgr.copy()
    # Cloth on successive rollers — thin bands, not poster boards
    roller_cloth(out, cloth, 0.30, 0.50, 0.258, 0.020, 0.94)
    roller_cloth(out, cloth, 0.302, 0.498, 0.312, 0.018, 0.93)
    roller_cloth(out, cloth, 0.310, 0.490, 0.382, 0.016, 0.92)
    roller_cloth(out, cloth, 0.312, 0.488, 0.442, 0.016, 0.92)
    roller_cloth(out, cloth, 0.315, 0.485, 0.500, 0.016, 0.91)
    roller_cloth(out, cloth, 0.318, 0.482, 0.556, 0.016, 0.91)
    # Thread connecting rollers (narrower so machine stays visible)
    hang_cloth(out, cloth, 0.372, 0.430, 0.330, 0.575, 0.72)
    hang_cloth(out, cloth, 0.440, 0.505, 0.570, 0.760, 0.78)
    return grade(out)


def process_bleaching(bgr: np.ndarray, cloth: np.ndarray) -> np.ndarray:
    out = bgr.copy()
    roller_cloth(out, cloth, 0.390, 0.580, 0.160, 0.022, 0.94)
    roller_cloth(out, cloth, 0.395, 0.575, 0.218, 0.020, 0.93)
    hang_cloth(out, cloth, 0.445, 0.520, 0.240, 0.430, 0.75)
    # Cloth across front of large drum — curved-feeling quad, not a billboard
    h, w = out.shape[:2]
    paste_quad(
        out,
        cloth,
        nq(
            w,
            h,
            [
                (0.375, 0.445),
                (0.620, 0.438),
                (0.615, 0.520),
                (0.380, 0.528),
            ],
        ),
        0.88,
    )
    roller_cloth(out, cloth, 0.410, 0.570, 0.590, 0.018, 0.91)
    hang_cloth(out, cloth, 0.445, 0.525, 0.610, 0.745, 0.80)
    return grade(out)


def main():
    cloth = make_cream_cloth()
    thermo = cv2.imread(str(THERMO_SRC))
    bleach = cv2.imread(str(BLEACH_SRC))
    if thermo is None or bleach is None:
        raise SystemExit("Missing source images")

    thermo_web = process_thermosol(thermo, cloth)
    bleach_web = process_bleaching(bleach, cloth)

    # keep native 720 width — portrait gallery
    cv2.imwrite(str(THERMO_OUT), thermo_web, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    cv2.imwrite(str(BLEACH_OUT), bleach_web, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    print("wrote", THERMO_OUT, thermo_web.shape)
    print("wrote", BLEACH_OUT, bleach_web.shape)
    cv2.imwrite(str(TMP / "qa_thermo.jpg"), thermo_web)
    cv2.imwrite(str(TMP / "qa_bleach.jpg"), bleach_web)


if __name__ == "__main__":
    main()
