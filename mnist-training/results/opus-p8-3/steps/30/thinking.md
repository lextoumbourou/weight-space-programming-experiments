The β=1.5 setting still looks best, though the loss is higher at β=0, which makes me suspect the NB part is overconfident. I might try scaling everything up, but I'm not sure that would help. With 21 probes left, I need to choose three more features each, aimed at the remaining confusions: 3→5, 7→9, 0→2, 3→2, and 7→2.

I'm weighing which features to probe next for the remaining confusions, especially 0 vs 2, where the mid-row gap between strokes looks promising. I'd like to check that gap in the left mid rows, since it's high for 0 and low for 2, and I'll use a lower threshold for these topology features.

I'm sketching three topology probes for the 0-vs-2 gap, with thresholds around 0.05. Then I'll try a set of ink-based corner features, and a third set on the diagonal and the center column, before building the features.
