I'm checking whether s=0.30 beats s=0.25: the loss is slightly worse (0.2720 vs 0.2713) with accuracy at 91.59, so the change is flat and I'll revert to s=0.25. Next up is the sH test, either 0.45 or 0.15. Since adding the heavy vote earlier lowered the loss (0.3129 to 0.3016) at a small accuracy cost, I'm leaning toward trying sH=0.45.

I'm planning to try sH=0.45 and, if that comes out worse, test 0.2 next. Five steps remain, covering sH, a possible split of the scale for presence groups, a bias retune, and a final pass. For now I'm setting s=0.25 and sH=0.45.
