I'm seeing that the template lifts accuracy by about 2% with a slightly lower loss, though the class imbalance muddies that comparison, so I'm keeping the templates and wondering whether a larger α like 6 would help more. Now I'm weighing whether the template itself could be improved.

I'm weighing whether a full per-cell measured model on all 64 line cells is worth it, but with 21 steps of budget and no steps left to tune, it doesn't look like a clear win. I'm leaning toward targeted extra region stats and tuning α, γ, the biases, and the scale instead, aimed at the main confusions like 3→5 and 0→2.

I'm working through bias adjustments by comparing the predicted and true column totals from step 24, with most differences around 30–55 counts. I'm settling on small bias tweaks of roughly ±0.1 to 0.15, and I'm about to test α=6 with those tweaks applied.

I'm planning 1-D searches over α, γ, and the group weight GLINE, since the loss is deterministic and each search stays clean. I'll start with α=7 and keep going only if the loss improves.

I'm settling on keeping the biases unchanged for now so the α=7 comparison against the 0.5452 loss stays clean, since a bias tweak could shift the result by itself.
