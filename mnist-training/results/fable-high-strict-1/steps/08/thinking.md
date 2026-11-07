I've overshot: everything is now coming out as 8, mostly from the penalty drop (×0.39) combined with the template changes. The offset term looks like it's driving the logits, since Σx is large and even a small shift in offset × Σx moves them a lot. So the offsets seem to be what's setting the predictions, and the template match x·t is weak compared with the mass term.

I'm checking whether the logit formula, with λ=0.5, makes the mass term dominate when features are noisy and similar across classes. I'm also weighing a smaller step back toward the 52% configuration, with multipliers near 1, and whether to keep the new 8 template. Its smaller ellipses cut the offset by roughly 66%, which explains the jump from 41 to 10000.

I'm estimating the offset for digit 8 and finding it contributes around 7 logits, so a 66% drop would add roughly 4.7 logits to 8. That makes the sensible multiplier adjustments on the order of 5–10%, which is about 0.4–0.7 logits. Given how sensitive the gain is, I'm leaning toward small changes to the 8 multiplier with the new template.

I'm reconsidering the 8 template: keeping the new, more realistic shape but lowering its multiplier to 0.95 should cut its offset by about 20% together with the smaller mass, rather than the roughly 30% that a full revert would produce. For the others, I'm setting 7 to 0.93 and 4 to 0.96, and compensating the 0 template, which now carries more mass, with a multiplier of 0.92.

Setting multipliers around 1 and beta back to 0.15, since beta's rise also favors 8 by removing negative cells where ink is nearly everywhere.
