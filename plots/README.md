# Plots

The two weight heatmaps from the post. Each script reads the JSON next to it and writes a PNG and SVG.

```sh
pip install matplotlib fonttools numpy
python3 plot-breakout-input-weights.py
python3 plot-enduro-output-weights.py
```

The post uses Shantell Sans and Atkinson Hyperlegible. To match it, put their variable `*-latin-wght-normal.woff2` files in `plots/fonts/`. Without them, the scripts use matplotlib's default font.

`breakout-input-weight-norms.json` is computed from the authors' released Breakout weights (CC BY 4.0). `enduro-output-weights.json` is from my DQN Enduro checkpoint.
