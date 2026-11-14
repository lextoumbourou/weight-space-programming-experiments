I tried sH=0.45 and its loss came out worse than before, so I'll go the other way and test sH=0.18. The gradient suggests dropping it by about 0.12 should lower the loss a bit more, unless the minimum is closer to 0.2. That leaves four steps: step 47 at sH=0.18, then either sH=0.1 or settling there in step 48, and a bias retune in step 49.

That leaves just the last step, 50, as a final or extra check.
