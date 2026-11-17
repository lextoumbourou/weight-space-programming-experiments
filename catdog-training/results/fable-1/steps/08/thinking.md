I'm weighing the vertical-minus-horizontal edge signal: it separates dogs from cats by about 14 points, and I'm wondering whether vertical energy alone is driving the dog prediction more than the combined texture features are.

Now I'm working out the variance for the vertical-minus-horizontal signal, using the class z-scores to get a separation of about 0.37. Solving the loss equation gives a spread near 0.074 and an optimal weight around 4.4. That adds roughly 0.015 to the loss gain. Next I'm checking how texture and this signal combine, and whether probing the diagonal against the average of horizontal and vertical helps.

I'm picking up the third direction to probe: the diagonal channel against the average of horizontal and vertical, with a guessed offset since the diagonal energy in natural images tends to run lower. I'll scale it by 4 and accept that the offset is rough, so the confusion matrix may drift if the guess is off.

Next I'm setting up the diagonal-versus-average probe with a rough offset, then I'll fold everything into one combined baseline and add more probes step by step.
