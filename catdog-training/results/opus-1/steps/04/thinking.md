Texture looks like the problem: its term is pulling toward dog and dominates the combined score. Flipping its sign should help, though green also points to dog, so I'm working out how the two combine after the flip.

I'm recalculating the centering after the flip: texture now pushes toward dog by about 0.3 on average, so I'm shifting the bias toward cat by 0.15, making cat 0.25 and dog -0.25. The texture term also dominates, so its variance is likely part of why the score moved.
