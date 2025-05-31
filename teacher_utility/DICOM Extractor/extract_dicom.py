#!/usr/bin/env python3
"""
extract_dicom_simple.py

Traverse a root DICOM directory (regardless of filename extension),
apply window/level for proper grayscale display, save as PNGs,
and emit a metadata.csv—with no text overlays on the images.
"""

import os
import csv

import numpy as np
import pydicom
from pydicom.pixel_data_handlers.util import apply_modality_lut, apply_voi_lut
from PIL import Image

# === USER CONFIGURATION ===
INPUT_DIR  = r"C:/MS Course Mat/Comfort Data/CD3/DICOM"
OUTPUT_DIR = r"C:/MS Course Mat/Comfort Data/CD3/DICOM/output"

# Which tags to emit into metadata.csv
METADATA_TAGS = [
    ("PatientID",         "PatientID"),
    ("PatientSex",        "PatientSex"),
    ("PatientAge",        "PatientAge"),
    ("StudyDate",         "StudyDate"),
    ("StudyTime",         "StudyTime"),
    ("Modality",          "Modality"),
    ("SeriesDescription", "SeriesDescription"),
    ("SeriesNumber",      "SeriesNumber"),
    ("InstanceNumber",    "InstanceNumber"),
    ("SliceLocation",     "SliceLocation"),
    ("SliceThickness",    "SliceThickness"),
    ("PixelSpacing",      "PixelSpacing"),
    ("WindowCenter",      "WindowCenter"),
    ("WindowWidth",       "WindowWidth"),
]

def is_dicom_file(path: str) -> bool:
    """Return True if the file has 'DICM' at byte offset 128."""
    try:
        with open(path, "rb") as f:
            f.seek(128)
            return f.read(4) == b"DICM"
    except:
        return False

def get_display_array(ds: pydicom.Dataset) -> np.ndarray:
    """
    1) apply modality LUT (rescale slope/intercept)
    2) apply VOI LUT or window/level
    3) invert if MONOCHROME1
    4) normalize to uint8 [0..255]
    """
    arr = ds.pixel_array
    arr = apply_modality_lut(arr, ds)
    arr = apply_voi_lut(arr, ds, index=0)
    if getattr(ds, "PhotometricInterpretation", "") == "MONOCHROME1":
        arr = np.max(arr) - arr
    arr = arr.astype(np.float32)
    mn, mx = arr.min(), arr.max()
    if mx > mn:
        arr = (arr - mn) / (mx - mn) * 255.0
    else:
        arr = np.zeros_like(arr)
    return arr.astype(np.uint8)

def extract(root_in: str, root_out: str):
    img_root = os.path.join(root_out, "images")
    os.makedirs(img_root, exist_ok=True)
    csv_path = os.path.join(root_out, "metadata.csv")

    # Open CSV and write header
    with open(csv_path, "w", newline="", encoding="utf-8") as cf:
        writer = csv.writer(cf)
        writer.writerow(["relative_path"] + [lbl for (lbl, _) in METADATA_TAGS])

        # Walk input tree
        for dirpath, _, files in os.walk(root_in):
            for fname in files:
                full = os.path.join(dirpath, fname)
                rel  = os.path.relpath(full, root_in)

                if not is_dicom_file(full):
                    continue

                # Read DICOM
                try:
                    ds = pydicom.dcmread(full, force=True)
                except Exception as e:
                    print(f"⚠️  Skipping {rel}: {e}")
                    continue

                # Extract & save image
                if "PixelData" in ds:
                    try:
                        arr = get_display_array(ds)
                        img = Image.fromarray(arr)  # 8-bit grayscale
                        out_img = os.path.join(img_root, rel + ".png")
                        os.makedirs(os.path.dirname(out_img), exist_ok=True)
                        img.save(out_img)
                    except Exception as e:
                        print(f"⚠️  Failed to process pixels for {rel}: {e}")

                # Write metadata row
                row = [rel]
                for label, tag in METADATA_TAGS:
                    val = getattr(ds, tag, "")
                    if isinstance(val, (list, tuple)):
                        val = "\\".join(str(v) for v in val)
                    row.append(val)
                writer.writerow(row)

    print(f"✅ Done!\n - Images → {img_root}\n - Metadata → {csv_path}")

if __name__ == "__main__":
    extract(INPUT_DIR, OUTPUT_DIR)
