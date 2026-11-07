Accuracy is up slightly, to 53.8%. Most of the errors come from 7 being read as 9, 5, or 4, and from 8 being read as 2, 3, or 9.

Still weighing why real 7s get pulled toward 9: their top bar lines up with the top of the 9's loop, and the steep diagonal overlaps the loop's right side and tail. Even with the slightly stronger weight on 7's own template, roughly 30% of 7s still come out as 9s, so the diagonal's angle and position may be off.

I'm checking whether the feature templates could explain the 7-to-9 pulls, since the stroke coverage per cell looks almost the same across the two digits. I'm also considering whether the ink channel might be saturating along the bar and diagonal of a 7.

I'm checking whether the ink channel causes the problem: a real 7's ink covers almost entirely the same cells as a 9's loop and tail, so it looks like a subset of the 9. Orientation features should be what separates them, since the 9 has vertical strokes on the left of its loop and a horizontal stroke along the bottom of the loop.

I'm working through why a 7 keeps getting scored as a 9. The penalty term for the 9 template scales with the input's total ink, so a sparse 7 gets a weaker penalty than it should, which could be pulling it toward the denser 9 template.

I'm now thinking the sparse-digit penalty is the real culprit: it scales with the input's total ink, so a 7 gets a weaker penalty against the denser 9 template. I'm considering mixing that ink-scaled term with a fixed bias, and estimating the right strength from the uniform offset per weight.

I'm estimating the scale of the feature weights now, since the uniform offset per weight would need to match a fixed bias. The ink channel should sit around 1.1 on the template side, while orientation responses for a well-aligned stroke are less certain and vary with how the stroke is measured.

I'm working out whether the fixed bias can replace the input-mass-scaled penalty, which depends on a scale factor γ. The earlier run with γ near 1 favored sparse classes, so I'm leaning toward a value somewhere around 0.7 and considering a hybrid of the two penalty terms.

Splitting the penalty into a fixed bias and an input-mass term, with a fixed bias of about 0.175 and an even split between the two, should soften the pull toward dense templates on sparse digits like 1 and 7.

I'm settling on a per-class multiplier tweak: pulling the 7 template down to 0.90 and the 8 template to 0.98, since 8's recall is poor and should gain from the penalty change.
