The loss is high at 4.38, so the model looks overconfident, probably because the scale is too large or γ is mismatched. Some digits are predicted far too often, like 3 and 1, while 8 and 9 almost never come up. That pattern would fit real features being smaller than γ assumes, so the bias term dominates and favors small-norm templates such as 1 and 7. Yet 3 is predicted often even though it has only moderate ink, which doesn't fit that story cleanly.

I'm weighing whether to raise γ or lower the bias weight, and I'm testing γ = 3 with α = 0.3 to see if the large-norm templates stop dominating. Mean-centering the templates won't help, since it shifts every class's logit by the same amount.

I'm settling on γ = 3 and α = 0.3, and I'm also considering a ramp of 1.5 px, since the strokes may be thicker than the template assumes. The conv1 bias might be suppressing too much of the stroke response, so I'm thinking about lowering it to -0.15, though that would change γ as well and make the effects harder to separate. I'll make the γ and α changes first and see how the calibration responds.

I'm checking whether the larger templates like 8 and 3 might gain even more weight at γ=3, since 8 has the biggest norm, so I'll run that test.
