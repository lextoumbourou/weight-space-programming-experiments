I'm suspecting something has gone wrong numerically, since every output has collapsed to 8 while the loss is around 13, which would point to very large logits. I'm wondering whether a unit() normalization is dividing by zero or producing NaN somewhere in the rendering path.

I'm checking the `ellipse` signature and the protos call, which look fine. The question now is why 8 dominates: it picks up several positive additions from the part templates, and since those templates are compact, their overlap with dense ink could push the logits far apart.

I'm weighing whether to revert to the step-15 weights, since that's a safe baseline at 74.51, in case the early-stopping rule halts the run right after this step. I'm also thinking about a small, careful change that might push accuracy past roughly 75%, while making sure the step I submit doesn't break anything.

I'm now thinking about making the discriminative updates much gentler, using only the balanced two-sided pairs at a much smaller scale, so the cosine differences against the dense ink don't push the logits apart again.

I'm weighing whether a smaller step size, around 0.08, with only the balanced two-sided pairs, would keep the discriminative update from pushing the logits apart again.
