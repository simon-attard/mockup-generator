#!/usr/bin/env python3
"""
Mockup Generator
Composites a master artwork onto frame templates to generate ecommerce product variants.

Usage:
    python mockup_generator.py artwork.jpg
    python mockup_generator.py artwork.jpg --config config.yaml --output ./out
"""

import argparse
import sys
import yaml
from pathlib import Path
from PIL import Image


def fit_artwork(artwork: Image.Image, width: int, height: int, mode: str) -> Image.Image:
    """Resize artwork to the placement area dimensions.

    Modes:
        stretch - fill exactly, ignoring aspect ratio (default)
        fit     - maintain aspect ratio, letterbox with white
        fill    - maintain aspect ratio, crop to fill
    """
    if mode == "stretch":
        return artwork.resize((width, height), Image.LANCZOS)

    elif mode == "fit":
        artwork = artwork.copy()
        artwork.thumbnail((width, height), Image.LANCZOS)
        canvas = Image.new("RGBA", (width, height), (255, 255, 255, 255))
        x = (width - artwork.width) // 2
        y = (height - artwork.height) // 2
        mask = artwork if artwork.mode == "RGBA" else None
        canvas.paste(artwork, (x, y), mask)
        return canvas

    elif mode == "fill":
        ratio = max(width / artwork.width, height / artwork.height)
        new_w = int(artwork.width * ratio)
        new_h = int(artwork.height * ratio)
        artwork = artwork.resize((new_w, new_h), Image.LANCZOS)
        x = (new_w - width) // 2
        y = (new_h - height) // 2
        return artwork.crop((x, y, x + width, y + height))

    else:
        raise ValueError(f"Unknown fit_mode '{mode}'. Use: stretch, fit, or fill")


def has_transparency(image: Image.Image) -> bool:
    """Return True if the image contains any transparent/semi-transparent pixels."""
    if image.mode != "RGBA":
        return False
    alpha_band = image.split()[3]
    return alpha_band.getextrema()[0] < 255


def generate_variant(master: Image.Image, variant: dict, output_path: Path) -> bool:
    template_path = Path(variant["template"])
    if not template_path.exists():
        print(f"  ✗  {output_path.name}  [template not found: {template_path}]")
        return False

    template = Image.open(template_path).convert("RGBA")

    p = variant["placement"]
    x, y, w, h = p["x"], p["y"], p["width"], p["height"]
    fit_mode = variant.get("fit_mode", "stretch")

    artwork = fit_artwork(master.copy().convert("RGBA"), w, h, fit_mode)

    if has_transparency(template):
        # Template has a transparent artwork cutout — place artwork behind the frame
        canvas = Image.new("RGBA", template.size, (255, 255, 255, 255))
        canvas.paste(artwork, (x, y))
        result = Image.alpha_composite(canvas, template)
    else:
        # Solid template — paste artwork directly at the placement coordinates
        result = template.copy()
        result.paste(artwork, (x, y))

    result.convert("RGB").save(output_path, "JPEG", quality=95, optimize=True)
    print(f"  ✓  {output_path.name}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate product variant images from a master artwork"
    )
    parser.add_argument("master", help="Path to the master artwork image")
    parser.add_argument(
        "--config", default="config.yaml", help="Path to config file (default: config.yaml)"
    )
    parser.add_argument(
        "--output", help="Output directory (overrides output_dir in config)"
    )
    args = parser.parse_args()

    master_path = Path(args.master)
    if not master_path.exists():
        print(f"Error: master image not found: {master_path}")
        sys.exit(1)

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Error: config file not found: {config_path}")
        sys.exit(1)

    with open(config_path) as f:
        config = yaml.safe_load(f)

    out_dir = Path(args.output or config.get("output_dir", "output"))
    out_dir.mkdir(parents=True, exist_ok=True)

    master = Image.open(master_path).convert("RGBA")

    print(f"Master:  {master_path.name}  ({master.width} x {master.height}px)")
    print(f"Output:  {out_dir}/\n")

    variants = config.get("variants", [])
    if not variants:
        print("No variants defined in config.")
        sys.exit(0)

    success = 0
    for variant in variants:
        output_filename = f"{master_path.stem}_{variant['name']}.jpg"
        if generate_variant(master, variant, out_dir / output_filename):
            success += 1

    print(f"\nDone — {success}/{len(variants)} variants generated.")


if __name__ == "__main__":
    main()
