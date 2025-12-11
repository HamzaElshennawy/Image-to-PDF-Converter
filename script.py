"""
Image to PDF Context Menu Converter
This script converts selected images to a single PDF file.
"""

import sys
import os
from pathlib import Path
from PIL import Image
import traceback
from datetime import datetime


def convert_images_to_pdf(image_paths, output_path=None):
    """Convert multiple images to a single PDF file."""

    # Expand directories and filter valid image files
    valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"}
    expanded = []
    for p in image_paths:
        p = str(p)
        path = Path(p)
        if path.is_dir():
            for f in sorted(path.iterdir()):
                if f.suffix.lower() in valid_extensions and f.is_file():
                    expanded.append(str(f))
        else:
            expanded.append(p)

    valid_images = [p for p in expanded if Path(p).suffix.lower() in valid_extensions]

    if not valid_images:
        print("No valid image files found.")
        return False

    # Sort images by name
    valid_images.sort()

    # Generate output filename if not provided
    if output_path is None:
        first_image_dir = Path(valid_images[0]).parent
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = first_image_dir / f"converted_{timestamp}.pdf"
    else:
        output_path = Path(output_path)

    # Prepare a log file next to the output so users can find errors when run from Explorer
    try:
        log_dir = (
            first_image_dir if "first_image_dir" in locals() else Path(__file__).parent
        )
    except Exception:
        log_dir = Path(__file__).parent
    log_path = log_dir / f"convert_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    # We'll write diagnostic output to a log so it's available even when Explorer runs the script
    try:
        images = []
        with open(log_path, "w", encoding="utf-8") as log_file:
            log_file.write(f"Starting conversion: {datetime.now().isoformat()}\n")
            log_file.write(f"Found {len(valid_images)} image(s):\n")
            for v in valid_images:
                log_file.write(f"  {v}\n")

            # Open images safely using context managers to avoid file handle issues
            for img_path in valid_images:
                try:
                    with Image.open(img_path) as im:
                        if im.mode != "RGB":
                            converted = im.convert("RGB")
                        else:
                            converted = im.copy()
                        images.append(converted)
                except Exception as ie:
                    log_file.write(f"Failed to open/convert image {img_path}: {ie}\n")

            if not images:
                log_file.write("No images could be opened/converted. Aborting.\n")
                print("No valid image files could be opened.")
                return False

            # Save as PDF
            out_str = str(output_path)
            try:
                if len(images) == 1:
                    images[0].save(out_str, "PDF", resolution=100.0)
                else:
                    images[0].save(
                        out_str,
                        "PDF",
                        resolution=100.0,
                        save_all=True,
                        append_images=images[1:],
                    )
                log_file.write(f"PDF created successfully: {out_str}\n")
                log_file.write(f"Converted {len(images)} image(s)\n")
                print(f"PDF created successfully: {output_path}")
                print(f"Converted {len(images)} image(s)")
                return True
            except Exception as se:
                log_file.write("Error creating PDF:\n")
                log_file.write(traceback.format_exc())
                print(f"Error creating PDF: {se}")
                return False

    except Exception as e:
        # Write unexpected errors to log
        try:
            with open(log_path, "a", encoding="utf-8") as log_file:
                log_file.write("Unexpected error during conversion:\n")
                log_file.write(traceback.format_exc())
        except Exception:
            pass
        print(f"Unexpected error: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <image1|dir1> [image2|dir2] ...")
        sys.exit(1)

    # Get all image paths or directories from command line arguments
    image_paths = sys.argv[1:]

    # Convert to PDF
    success = convert_images_to_pdf(image_paths)

    # If running interactively, keep console open to show result
    try:
        if sys.stdin and sys.stdin.isatty():
            input("\nPress Enter to close...")
    except Exception:
        pass

    sys.exit(0 if success else 1)
