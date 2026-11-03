"""Reproduce the figure from its JSON data. Requires matplotlib, fonttools and brotli."""
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

ROOT=Path(__file__).resolve().parent
FONTS=ROOT/"fonts"
PAPER="#FBFAF6"
SHEET="#F2F0E8"
INK="#141414"
MUTED="#5C5B57"
TEAL="#2DD4BF"


def main():
    data=json.loads((ROOT/"enduro-output-weights.json").read_text())
    with tempfile.TemporaryDirectory(prefix="weight-space-fonts.") as cache:
        def font(name,weight):
            source=FONTS/f"{name}-latin-wght-normal.woff2"
            if not source.exists():return FontProperties()
            converted=TTFont(source)
            if "fvar" in converted:
                converted=instantiateVariableFont(converted,{"wght":weight},inplace=False)
            converted.flavor=None
            path=Path(cache)/f"{name}-{weight}.ttf"
            converted.save(path)
            return FontProperties(fname=path)

        display=font("shantell-sans",700)
        body=font("atkinson-hyperlegible-next",400)
        mono=font("atkinson-hyperlegible-mono",400)
        values=np.array([column["weights"] for column in data["columns"]]).T
        palette=LinearSegmentedColormap.from_list("single_highlighter",[SHEET,TEAL])
        fig=plt.figure(figsize=(12,8),dpi=160,facecolor=PAPER)
        fig.text(.055,.948,"Three hidden units Astra inspected",fontproperties=display,fontsize=28,color=INK)
        fig.text(.055,.884,"Output weights from the blind Enduro run",fontproperties=body,fontsize=18,color=MUTED)
        ax=fig.add_axes([.30,.235,.56,.565],facecolor=PAPER)
        image=ax.imshow(np.abs(values),cmap=palette,vmin=0,vmax=np.max(np.abs(values)),aspect="auto")
        ax.set_xticks(range(3),[f"Unit {c['hidden_unit']}" for c in data["columns"]])
        ax.set_yticks(range(9),[f"{i}  {action}" for i,action in enumerate(data["actions"])])
        ax.tick_params(axis="x",top=True,bottom=False,labeltop=True,labelbottom=False,length=0,pad=11)
        ax.tick_params(axis="y",length=0,pad=14)
        for label in ax.get_xticklabels():
            label.set_fontproperties(display);label.set_fontsize(20);label.set_color(INK)
        for label in ax.get_yticklabels():
            label.set_fontproperties(mono);label.set_fontsize(17.5);label.set_color(INK)
        for spine in ax.spines.values():spine.set_visible(False)
        ax.set_xticks(np.arange(-.5,3,1),minor=True)
        ax.set_yticks(np.arange(-.5,9,1),minor=True)
        ax.grid(which="minor",color=PAPER,linewidth=5)
        ax.tick_params(which="minor",length=0)
        for row in range(9):
            for col in range(3):
                ax.text(col,row,f"{values[row,col]:+.3f}",ha="center",va="center",fontproperties=mono,fontsize=22.5,color=INK)
        colorax=fig.add_axes([.905,.285,.016,.46])
        bar=fig.colorbar(image,cax=colorax,ticks=[0,.6,1.2])
        bar.outline.set_visible(False)
        bar.ax.tick_params(length=0,pad=8)
        for label in bar.ax.get_yticklabels():
            label.set_fontproperties(mono);label.set_fontsize(14.5);label.set_color(MUTED)
        fig.text(.895,.778,"|weight|",fontproperties=mono,fontsize=14.5,color=MUTED)
        fig.text(.055,.159,"Action labels were added after the blind run.",fontproperties=display,fontsize=17,color=INK)
        fig.text(.055,.112,"Darker teal shows larger magnitude; printed signs show direction.",fontproperties=body,fontsize=15.5,color=MUTED)
        fig.text(.055,.069,"Activations were not measured. These are output-layer coefficients.",fontproperties=body,fontsize=15.5,color=MUTED)
        fig.text(.055,.027,"Reader calls: unit 90 = 10, unit 87 = 16, unit 19 = 23",fontproperties=mono,fontsize=14,color=MUTED)
        plt.rcParams["svg.fonttype"]="path"
        fig.savefig(ROOT/"enduro-output-weights.png",dpi=160,facecolor=PAPER)
        svg_path=ROOT/"enduro-output-weights.svg"
        fig.savefig(svg_path,facecolor=PAPER)
        svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines())+"\n")
        plt.close(fig)


if __name__=="__main__":main()
