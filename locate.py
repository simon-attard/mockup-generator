#!/usr/bin/env python3
"""
Locate - Helper to find artwork placement coordinates for config.yaml

Click the four corners of the artwork area in order:
  1. Top-left
  2. Top-right
  3. Bottom-right
  4. Bottom-left

The script will print the x, y, width, height values to paste into config.yaml.

Usage:
    python locate.py templates/white_frame.png
"""

import sys
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
except ImportError:
    print("matplotlib is required for this helper:")
    print("  pip install matplotlib")
    sys.exit(1)

LABELS = ["Top-left", "Top-right", "Bottom-right", "Bottom-left"]
NEXT_PROMPT = [
    "Click the TOP-LEFT corner of the artwork area",
    "Click the TOP-RIGHT corner",
    "Click the BOTTOM-RIGHT corner",
    "Click the BOTTOM-LEFT corner",
]


def locate(template_path: str):
    img = mpimg.imread(template_path)
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(img)
    ax.set_title(NEXT_PROMPT[0], fontsize=12, pad=12)
    plt.tight_layout()

    clicks = []

    def on_click(event):
        if event.inaxes != ax or event.button != 1:
            return
        if len(clicks) >= 4:
            return

        x, y = int(round(event.xdata)), int(round(event.ydata))
        clicks.append((x, y))

        ax.plot(x, y, "rx", markersize=14, markeredgewidth=2)
        ax.annotate(
            f"{LABELS[len(clicks)-1]}\n({x}, {y})",
            (x, y),
            textcoords="offset points",
            xytext=(10, 10),
            color="red",
            fontsize=9,
            fontweight="bold",
        )
        fig.canvas.draw()

        if len(clicks) < 4:
            ax.set_title(NEXT_PROMPT[len(clicks)], fontsize=12, pad=12)
        else:
            ax.set_title("Done — see terminal for config values", fontsize=12, pad=12)
            fig.canvas.draw()

            tl, tr, br, bl = clicks
            x_out = min(tl[0], bl[0])
            y_out = min(tl[1], tr[1])
            w_out = max(tr[0], br[0]) - x_out
            h_out = max(bl[1], br[1]) - y_out

            name = Path(template_path).stem
            print(f"\nPlacement for '{name}':")
            print(f"  - name: {name}")
            print(f"    template: templates/{Path(template_path).name}")
            print(f"    fit_mode: stretch")
            print(f"    placement:")
            print(f"      x: {x_out}")
            print(f"      y: {y_out}")
            print(f"      width: {w_out}")
            print(f"      height: {h_out}")

    fig.canvas.mpl_connect("button_press_event", on_click)
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python locate.py <template_image>")
        sys.exit(1)
    locate(sys.argv[1])
