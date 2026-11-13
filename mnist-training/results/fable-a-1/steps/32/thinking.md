Accuracy is at 88.3% with a loss of 0.395, and I have 19 steps left. Now I'm tallying the misclassifications, mapping each true class to the classes it gets confused with and how often.

I'm now deciding how to use the last 19 steps: more measurements, finer corner features, knob tuning, or pairwise tweaks. I'm leaning toward calibrating the loss first by testing a global scale on the logits, since accuracy won't change from that but the loss will.

I'm comparing the features that separate 4 from 6, since that confusion still accounts for 68 errors. The strongest contrasts are in the D1 and D3 diagonals and the horizontal corner measurements, so I'm weighing which of those to tune first.

I'm wondering whether the 4→6 confusions come from unusual 4s rather than a systematic gap, since the features that separate the two look strong on paper. Diagnosing individual cases isn't working, so I'm considering using the remaining steps on knob tuning, starting with raising the orientation trust from 0.4 to 0.55.

I'm weighing a coarse search over the corner trust, the hole weight, the bias adjustment, and the probability clipping, each costing one step, against spending the steps on more measurements. Adding the other checkerboard half would bring in correlated features, so the gain may be small for its cost.

I'm checking whether the 7→2 confusions, at 69 errors, can be explained by a feature the earlier measurements already show: a 7 with a foot or serif at the bottom, or a European crossbar, would be pulled toward 2 by the bottom-horizontal and lower-left corner evidence.

I'm weighing whether the 7→2 confusions could come from a crossbar sub-mode, since those 7s would look like 2s on the mid-horizontal and corner features. A linear model can't carve out separate sub-templates, so I'd have to tune knobs instead of adding channels.

I'm weighing a bias adjustment alongside a change to the orientation trust, moving it from 0.4 to 0.5. Since the bias shift should have a predictable small effect, I'm inclined to test both together for step 32, even though I won't be able to tell which one caused any change in loss.
