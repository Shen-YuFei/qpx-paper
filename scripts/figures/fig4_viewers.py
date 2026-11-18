"""Figure 4: the same dataset opened in the QPX Explorer and in the QPX UI desktop viewer.

Lays out the two screenshots taken by scripts in
/data/shenyufei/Bigbio_data/qpx_paper_figures/fig4 (see notes.md there for how to retake them).
The images are embedded unresampled in the PDF.

Run: python scripts/figures/fig4_viewers.py [--shots <folder>]
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from qpxfig import DOUBLE, MM, RULE, save

SHOTS = Path("/data/shenyufei/Bigbio_data/qpx_paper_figures/fig4")
PANELS = [("fig4a_explorer.png", None), ("fig4b_qpxui.png", 1264)]  # file, rows kept
LABEL_SPACE, GAP = 5.0, 3.0  # mm


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--shots", type=Path, default=SHOTS)
    args = parser.parse_args()

    images = [plt.imread(args.shots / name)[:rows] for name, rows in PANELS]
    width = 183.0
    heights = [width * im.shape[0] / im.shape[1] for im in images]
    total = sum(heights) + len(images) * LABEL_SPACE + (len(images) - 1) * GAP
    fig = plt.figure(figsize=(DOUBLE, total * MM))

    top = total
    for letter, im, h in zip("ab", images, heights):
        fig.text(0, (top - 3.6) / total, letter, fontsize=8, fontweight="bold", va="baseline")
        top -= LABEL_SPACE
        ax = fig.add_axes([0, (top - h) / total, 1, h / total])
        ax.imshow(im, interpolation="none")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color(RULE)
            spine.set_linewidth(0.5)
        top -= h + GAP
    save(fig, "fig4")


if __name__ == "__main__":
    main()
