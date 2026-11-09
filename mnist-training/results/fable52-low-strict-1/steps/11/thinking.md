I'm at 0.7432 with five steps left, so I'm looking for structural gains. The step 9 finding is that real digits have ink where my templates are empty, which suggests the templates are too narrow. I wonder if the digit shapes are off in scale, since many digits like 2, 3, and 5 may be wider than the 12 pixels my template gives the 2.

I'm weighing the template widths against the evidence: the 2, 3, and 5 templates may be too narrow, and the 8 looks slim too. I'm also considering whether to adjust the negative blob strength or sigma, and I'm leaning toward tweaking the 1 and 8 biases and the 4 scale.

I'm weighing a bias refinement against a sigma increase to 3.0. Changing sigma could shift the balance through the norm and mean, so a bias-only tweak is the safer bet with an expected gain near 1%. Sigma is the riskier move with a bigger possible payoff, and with five steps left I'll try it now alongside the bias changes.
