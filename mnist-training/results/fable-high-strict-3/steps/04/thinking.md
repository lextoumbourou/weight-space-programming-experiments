I'm checking the predicted digit counts against the true counts, and the model is over-predicting 3, 4 and 5 while under-predicting 8 and 9.

I'm now working through the bias updates with damped steps, and the accumulated biases show digit 4 and 5 running high while 6 is running low. I'm also tallying which digits get confused for which, with 3 and 5 swapping most often and 8 tending to be read as 2 or 3. I'm starting to suspect the 8 template is too narrow to separate it from those digits.

I'm checking whether 9 can be told apart from 4 by the top of the loop, since a real 9 has ink at top center while the 4 template leaves that gap open.

I'm weighing whether hand-tuned discriminative weights could fix the 9/4 mix-up, since the loop top on a real 9 has ink where the 4 template stays open. Adding negative weights to the 4 template at top center, or otherwise moving past plain nearest-centroid matching, looks like a way to separate them.

I'm looking at pairwise-specific subtraction for the discriminative weights, where each class template gets a fraction of the templates it is confused with, like W_9 = μ_9 − 0.3 μ_4.

I'm defining the pairwise adjustment: each template gets reduced by a fraction of the templates of classes it is confused with, scaled by how often that confusion happens. For the 9→4 case, that means pulling W_4 back by about 0.22 of the 9 template, which lowers the 4 score on images that look like 9s.

I'm working out how to apply the pairwise subtraction carefully, since removing a fraction of a confusing class's template will also pull down that class's overall scores and shift the biases I just calibrated.

I'm weighing how much the compensation term should offset the bias shift, since the pairwise subtraction pulls down each class's overall logits by about as much as it gains discriminatively.

I'm settling the pairwise weights as W_d = s(μ_d − Σ α_dc μ_c), with the bias offset by the matching μ_c·μ_d term so class-d images stay balanced on average. The open question is the value of β that sets each α_dc.

I'm working out the pairwise weights, with each class template reduced by a fraction of the templates it gets confused with, scaled by how often that happens. The biggest cases are 9→4, 3→5 and 6→5, at roughly 0.26 to 0.3 each, and I'm still checking that the bias offsets compensate for the over-predicted digits.

I'm now working through whether the bias correction should be damped too, since the pairwise subtraction already pulls down the over-predicted digits and I don't want to correct the same confusions twice. The 8 template is the one I keep coming back to: it's built from two full loops, so its norm is large and the half-norm penalty probably hits it hardest, and that might explain why 8s drift toward 2 and 3.

Now I'm widening the 0 template a bit, since the real 0 ring is wider and that might explain the 0→6 confusions. Then I'm listing the pairwise adjustments by hand, with the largest ones for 4→9, 5→3, 5→6 and 3→5.

I'm calibrating the per-class biases after the pairwise changes, landing on roughly +0.95 for 0, +1.35 for 4, and −0.55 for 6, with 3 and 9 near zero.

I'm writing the code that computes the pairwise dot products between class templates, summed across the feature maps with their scales.
