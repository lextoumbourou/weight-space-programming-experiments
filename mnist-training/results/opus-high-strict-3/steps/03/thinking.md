I'm weighing a discriminative fix: the current cosine only rewards matching positive templates, so I want to also penalize ink appearing where a class template is empty, and I'm testing a weight form that does that.

I'm checking whether a class-specific negative term can actually help, since any shared background term just cancels out in the argmax. Adding a common subtraction only reweights the positive template toward common locations, so linear positive-only templates look limited. I'm now considering whether mixing in other classes' templates with class-specific coefficients could work, or whether better, more varied templates would do more.

I'm now trying a class-specific negative term: subtracting a scaled amount wherever a class's template is empty but the average of the other classes has ink, so the penalty depends on the class and doesn't just cancel out in the argmax.

I'm looking at the template fixes now: for 5→6 and 4→9, the empty-area penalty should help, and for 0→6 I'm widening the zero template to about rx 6.5 with a slight slant, since real zeros run wider.

I'm weighing whether to build templates from hand-drawn slant variants for the 1s, since a single straight template misses the 1s that lean. Averaging renders of several slants could blur it into something closer to real data, but I'm not sure that counts as allowed, so I'm leaning toward drawing one template with a bit more built-in breadth instead.

I'm settling on a fix of γ around 0.7, subtracting a penalty only where a class template is empty and the mean template has ink, and I'm going to normalize the weights after building them.

I'm setting the negative term to relu of the mean template minus the class template, scaling it at about 0.7 with the logit scale at 8, and leaving the biases at zero for now. I'm also widening the zero prototype to rx 6.5.
