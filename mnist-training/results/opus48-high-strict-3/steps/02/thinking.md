I'm seeing that the model's predictions are dominated by classes 4 and 8, with some 1s, giving 19% accuracy and a loss of 2.96. The loss being above ln(10) means the wrong predictions are overconfident. I suspect the templates for 8 and 4 produce a higher overall response, so they're pulling everything toward them, and I'm now looking at how strongly those templates are biasing the output.

I'm still weighing why the dense 8 template wins: its large central ink mass correlates with any centered digit, and since the background penalty is too weak, its dot product stays systematically higher. I'm considering lowering the scale to tame the overconfident wrong predictions and making the templates more discriminative, though the root cause looks like the 8 template's raw overlap.

I'm going to normalize each centered template to unit L2 norm so dense templates like 8 stop winning just by covering more ink, and then I'll apply the scale. I'll also consider adding a bias term to counteract whatever bias remains, but I want to fix the templates first.

I'm going to zero-center each template and scale it to unit norm, so dense templates like 8 can't win just by covering more ink. With unit-norm templates the dot products become comparable across digits, and I'll pick a scale that keeps the logits in a reasonable range.

I'm settling on the magnitude: after unit-norm, zero-mean templates, the per-cell values are small, so the logit gap is roughly scale times 0.3. To get a useful spread I'd want a scale around 10, but given the overconfident wrong predictions I'll start lower, around 4 or 5, and tune from there.

I'm working out the expected dot product per feature: ink positions carry a positive template weight and a positive feature value, background positions carry a small negative weight with a small feature value, and with redundant feature sampling the ink-driven term will still dominate the sum.

I'm estimating the raw dot products for the correct template versus a wrong one, and they come out only about 1 to 2 apart. That means unit-norm templates already give a usable logit gap, so I'll set the scale to around 2 instead of the earlier 0.3.

I'm switching to unit-norm, zero-mean templates so the dense 8 stops winning on ink coverage, and I'll set the scale to about 2 since the raw dot-product gaps are already around 1 to 2.
