The temperature change to 1.25 made the loss slightly worse than 1.1, so the best setting looks like about 1.15, and tuning it further won't give much more. With 17 steps left I need a different kind of improvement. One idea is to repurpose the unused conv1 channels 6 and 7, perhaps for a thick-ink or edge-polarity detector.

I'm weighing whether the vertical stroke near the top-left of the 5 and the open left side of the 3 are already captured by the current features, and whether tuning the endpoint and loop gains again at temperature 1.15 would help more than another structural change.

I'm settling on a combined change: temperature 1.15, endpoint gain 3.0, and the diagonal weight raised to 1.4. I'd rather not stack too many changes at once with so few steps left, so I'll keep the bias recalibration small. The per-column ink totals from step 33 are what I'll use to set it.

Now I'm recalculating the per-column bias corrections from the step 33 counts, working through the log ratios for columns 1, 3, and 6.
