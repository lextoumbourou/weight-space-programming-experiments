The first pass gave 8 the most predictions, which makes sense since it's a broad template and covers many cells. The normalized correlation still seems to favor these broad templates, because inputs with spread-out ink match them well. I'm considering a distance-based score that subtracts a scaled template energy, with the scale α estimated rather than fixed at 1, since α=1 pushed everything to one class.

I'm weighing a distance-based score where the scale α is tuned rather than fixed at 1, since α=1 collapsed everything toward a single class. Lowering it to around 0.3 might keep the penalty on the true template's energy from swamping the correlation term, and I'd still need to work out what typical correlation values look like before picking the value.

I'm checking whether the coordinate mapping from the first conv layer to the input is shifted, since the 7 template may sit in the wrong place. Working through the pooling and stride steps, the input centers for each pooled cell come out as 4s+2ai+4 through 4s+2ai+7, so I want to confirm that against where my 7 strokes actually land.

I'm double-checking the coordinate mapping from conv1 to the input, and it holds: each pooled output lands on input centers 2Y+4 through 2Y+7. Digits are size-normalized to a 20-pixel-tall box, so the widths vary, with 1s narrow and 0s around 14 to 16 columns wide. I'm also thinking about whether one template per class is enough, since the logit is linear and averaging variants just blends them into one template anyway.

I'm now weighing a distance-style score that subtracts a scaled template energy, and I'll try a fixed scale around 0.3 since 1 collapsed everything to one class. The 8 bias likely comes from cosine normalization, so centering each template against the class mean is another option to test.

I'm settling on a distance-style score with α around 0.3, since that's roughly where the correlation term and the template-energy penalty should balance, and I still need to pick the scale value carefully.

I'm settling the scale as α=0.3 with s=1.0, since α=1 collapsed everything to one class, and I'll see how the loss responds to that choice.
