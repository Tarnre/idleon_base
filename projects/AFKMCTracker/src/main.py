##MADE BY AI##

from __future__ import annotations

import csv
import re
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
import pytesseract
from mss import mss
from PIL import Image

# If on Windows and Tesseract isn't on PATH, set this:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
WINDOW_TITLE_SUBSTR = "IdleOn"


# ---- Settings ----
INTERVAL_S = 0.5  # custom interval (seconds)
WRITE_CSV = True
CSV_PATH = Path("value_changes.csv")

# ---- OCR helpers ----
_NUMBER_RE = re.compile(r"[-+]?\d+(?:[.,]\d+)?")

def preprocess(img_bgr: np.ndarray) -> np.ndarray:
    """Preprocess for white digits on gray background with shadow."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # Upscale to help OCR with small HUD fonts
    gray = cv2.resize(gray, None, fx=3.0, fy=3.0, interpolation=cv2.INTER_CUBIC)

    # Boost contrast
    gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)

    # If text is light-on-dark-ish, invert so OCR sees dark text on light bg
    # (Tesseract tends to like dark text on white)
    inv = cv2.bitwise_not(gray)

    # Adaptive threshold handles gray backgrounds + subtle shadow better than Otsu
    th = cv2.adaptiveThreshold(
        inv,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,   # block size (odd)
        7,    # constant
    )

    # Light cleanup to thicken strokes a bit
    kernel = np.ones((2, 2), np.uint8)
    th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel, iterations=1)

    return th


def ocr_digits(pil_img: Image.Image) -> str:
    """OCR tuned to digits."""
    config = "--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789.,+-"

    return pytesseract.image_to_string(pil_img, config=config).strip()

def parse_number(text: str) -> float | None:
    """Parse the first number found in OCR text."""
    m = _NUMBER_RE.search(text)
    if not m:
        return None
    s = m.group(0).replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None

# ---- Data model ----
@dataclass(frozen=True)
class Reading:
    ts: datetime
    raw_text: str
    value: float | None

# ---- Capture + calibration ----
def capture_region(sct: mss, region: dict[str, int]) -> np.ndarray:
    """Capture a region of the screen and return BGR image."""
    grab = sct.grab(region)  # BGRA
    img = np.array(grab)[:, :, :3]
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

def calibrate_region(sct: mss) -> dict[str, int]:
    """Show a full-screen capture; user drags a ROI to define region."""
    monitor = sct.monitors[1]  # primary monitor
    full = np.array(sct.grab(monitor))[:, :, :3]
    full = cv2.cvtColor(full, cv2.COLOR_RGB2BGR)

    r = cv2.selectROI(
        "Select number region (Enter to confirm, Esc to cancel)",
        full,
        showCrosshair=True,
    )
    cv2.destroyAllWindows()

    left, top, width, height = map(int, r)
    if width == 0 or height == 0:
        raise RuntimeError("No region selected (cancelled).")

    region = {"left": left, "top": top, "width": width, "height": height}
    print(f"Calibrated REGION = {region}")
    return region

# ---- Tracking loop ----
def track_loop(interval_s: float) -> None:
    region: dict[str, int] | None = None
    tracking = False
    prev: Reading | None = None

    csv_file = None
    csv_writer = None

    if WRITE_CSV:
        is_new = not CSV_PATH.exists()
        csv_file = CSV_PATH.open("a", newline="", encoding="utf-8")
        csv_writer = csv.writer(csv_file)
        if is_new:
            csv_writer.writerow(["timestamp", "previous_value", "value", "ocr_text"])

    print("Controls:")
    print("  c = calibrate region (drag box)")
    print("  t = toggle tracking on/off")
    print("  q = quit")
    print("")
    print("Tip: Calibrate first, then press 't'.")
    preview = False
    last_raw = None
    last_proc = None

    with mss() as sct:
        while True:
            # We keep a tiny OpenCV window just to capture keypresses reliably.
            # (It doesn't need to show anything meaningful.)
            key_img = np.zeros((40, 420, 3), dtype=np.uint8)
            cv2.putText(
                key_img,
                f"c=calibrate  t=track({tracking})  q=quit",
                (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )
            cv2.imshow("Tracker Controls (focus this window)", key_img)

            k = cv2.waitKey(1) & 0xFF
            if k == ord("v"):
                preview = not preview
                print(f"Preview = {preview}")

            if k == ord("s"):
                if last_raw is not None and last_proc is not None:
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    cv2.imwrite(f"debug_raw_{ts}.png", last_raw)
                    cv2.imwrite(f"debug_proc_{ts}.png", last_proc)
                    print(f"Saved debug_raw_{ts}.png and debug_proc_{ts}.png")
                else:
                    print("No frames captured yet to save.")
            if k == ord("q"):
                break
            if k == ord("c"):
                try:
                    region = calibrate_region(sct)
                    prev = None  # reset change detection after recalibration
                except RuntimeError as e:
                    print(f"Calibration cancelled: {e}")
            if k == ord("t"):
                if region is None:
                    print("Calibrate first (press 'c').")
                else:
                    tracking = not tracking
                    print(f"Tracking = {tracking}")

            if tracking and region is not None:
                img_bgr = capture_region(sct, region)
                proc = preprocess(img_bgr)

                last_raw = img_bgr
                last_proc = proc

                if preview:
                    cv2.imshow("ROI raw", img_bgr)
                    cv2.imshow("ROI processed", proc)

                ts = datetime.now()
                img_bgr = capture_region(sct, region)
                proc = preprocess(img_bgr)

                txt = ocr_digits(Image.fromarray(proc))
                val = parse_number(txt)

                reading = Reading(ts=ts, raw_text=txt, value=val)

                changed = prev is None or reading.value != prev.value
                if changed:
                    before = prev.value if prev else None
                    print(
                        f"{reading.ts.isoformat(timespec='seconds')}  "
                        f"{before} -> {reading.value}   (ocr='{reading.raw_text}')"
                    )
                    if csv_writer is not None:
                        csv_writer.writerow(
                            [
                                reading.ts.isoformat(timespec="seconds"),
                                before,
                                reading.value,
                                reading.raw_text,
                            ]
                        )
                        csv_file.flush()
                    prev = reading

                time.sleep(interval_s)

    cv2.destroyAllWindows()
    if csv_file is not None:
        csv_file.close()

if __name__ == "__main__":
    track_loop(INTERVAL_S)
