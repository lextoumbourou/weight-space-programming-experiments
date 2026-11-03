"""Plot the supplied JSON norms. Uses the blog fonts and matplotlib/fonttools."""
import json
import tempfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.font_manager import FontProperties
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
import numpy as np

ROOT = Path(__file__).resolve().parent
FONTS = ROOT / "fonts"
PAPER, INK, MUTED = "#FBFAF6", "#141414", "#5C5B57"


def main():
    data = json.loads((ROOT / "breakout-input-weight-norms.json").read_text())
    with tempfile.TemporaryDirectory(prefix="weight-space-fonts.") as cache:
        def font(name, weight):
            if not (FONTS / f"{name}-latin-wght-normal.woff2").exists():
                return FontProperties()
            converted = TTFont(FONTS / f"{name}-latin-wght-normal.woff2")
            converted = instantiateVariableFont(converted, {"wght": weight}, inplace=False)
            converted.flavor = None
            dest = Path(cache) / f"{name}.ttf"
            converted.save(dest)
            return FontProperties(fname=dest)
        display = font("shantell-sans", 700)
        body = font("atkinson-hyperlegible-next", 400)
        mono = font("atkinson-hyperlegible-mono", 400)
        fig = plt.figure(figsize=(17, 7.5), dpi=180, facecolor=PAPER)
        fig.text(.04, .93, "How Breakout shows up in the input weights", fontproperties=display, fontsize=27, color=INK)
        fig.text(.04, .86, "Same 10 × 10 grid and channel meanings supplied to Astra and Opus. No network execution.", fontproperties=body, fontsize=17, color=MUTED)
        cmap = LinearSegmentedColormap.from_list("teal", ["#F2F0E8", "#2DD4BF"])
        for i, channel in enumerate(data["channels"]):
            ax = fig.add_axes([.055+i*.310, .29, .225, .44])
            values = np.array(channel["l2_norms"])
            im = ax.imshow(values, cmap=cmap, vmin=0, vmax=float(values.max()))
            ax.set_title(channel["name"], fontproperties=display, fontsize=20, color=INK, pad=17)
            ax.set_xticks([0,1,8,9]); ax.set_yticks([0,1,8,9])
            ax.tick_params(length=0)
            for label in [*ax.get_xticklabels(), *ax.get_yticklabels()]:
                label.set_fontproperties(mono); label.set_color(MUTED); label.set_fontsize(12)
            ax.set_xticks(np.arange(-.5,10,1), minor=True)
            ax.set_yticks(np.arange(-.5,10,1), minor=True)
            ax.grid(which="minor", color=PAPER, linewidth=2)
            ax.tick_params(which="minor", length=0)
            for spine in ax.spines.values(): spine.set_visible(False)
            cb = fig.colorbar(im, ax=ax, fraction=.045, pad=.04, ticks=[0,float(values.max())])
            cb.outline.set_visible(False); cb.ax.tick_params(length=0)
            cb.ax.set_yticklabels(["0", f"{values.max():.2f}"])
            for label in cb.ax.get_yticklabels(): label.set_fontproperties(mono);label.set_fontsize(11)
        fig.text(.04, .19, "Each cell = L2 norm of its 32 first-layer coefficients. Separate scales: compare positions within each panel.", fontproperties=body, fontsize=16, color=INK)
        fig.text(.04, .125, "Agent coefficients concentrate on playable row 8; reward-target coefficients concentrate near the top.", fontproperties=body, fontsize=16, color=INK)
        fig.text(.04, .07, "This supports a paddle-and-bricks interpretation; it does not measure activations or establish causation.", fontproperties=body, fontsize=15, color=MUTED)
        fig.text(.04, .025, "Source: Takehi et al. (2026), released Experiment 1, rounded W1 values; CC BY 4.0. Plot: NotesByLex.", fontproperties=body, fontsize=12, color=MUTED)
        plt.rcParams["svg.fonttype"] = "path"
        fig.savefig(ROOT / "breakout-input-weights.png", dpi=180, facecolor=PAPER)
        svg = ROOT / "breakout-input-weights.svg"
        fig.savefig(svg, facecolor=PAPER)
        svg.write_text("\n".join(l.rstrip() for l in svg.read_text().splitlines())+"\n")
        plt.close(fig)


if __name__ == "__main__":
    main()
