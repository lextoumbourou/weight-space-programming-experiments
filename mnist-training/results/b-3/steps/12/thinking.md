The distance model is the problem: it rewards less ink, so my templates, which I'd made too large, come out as the preferred match for "1". The predicted 8 never shows up, and the overall scale is off again. I'm now checking whether the stroke-based templates are overestimating real strokes, which look thinner than I assumed.

I'm now weighing a scale-correction: if the real features are weaker than my templates assume, the squared-norm penalty favors low-ink classes, so I could fix that with a factor β around 0.6 and a smaller logit scale. I'm still unsure whether the calibration alone will settle the bias, since the per-class diagonals are uneven.

I'm working out whether to rescale the model: with a factor β around 0.6, the bias term from the template norms shrinks, which might cut the pull toward low-ink classes like 1. Before committing, I'm considering a correlation-based approach in this feature space instead.

I'm going with the β approach since it's a single parameter: setting β to 0.55 and s to 0.45, so the product sβ comes to about 0.25.
