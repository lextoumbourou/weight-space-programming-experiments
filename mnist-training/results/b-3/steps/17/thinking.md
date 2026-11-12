The accuracy is sitting at 70.45%, so I'll keep improving it step by step. The biggest mix-ups are 3 read as 5, 2 as 3, and 4 as 9, with 7, 8 and 9 also tangled up. I'm starting with the 3-to-5 case, since 5's template has a top-left vertical stroke and a top bar that the 3s seem to be getting confused with.

Now I'm checking the corrections on the per-digit counts. The 5 column comes out to 849, below the 915 actual, so the 5 bias looks too high and needs lowering.

I'm recalculating the per-digit correction terms from the log ratios, and the largest adjustments land on digits 1 and 4, while digit 5's correction is small and positive.

I'm working out the bias terms, and the 1-class sits at about -1.84 with 4 and 5 leaning positive, so the bias is roughly balanced already. That means adjusting biases won't help much more. The real trouble is that narrow digits like 8, 4, 9 and 6 keep getting pulled toward 1, probably because the wide templates carry ink that narrow images lack. I'm considering whether adding narrower variants for the other classes would fix that.

I'm considering whether a different width-handling approach could help, since narrow digits keep getting pulled toward 1 and averaging variants doesn't seem to fix that. Raising β would penalize ink-heavy templates more and might favor 1 further, while lowering it weakens the per-image ink effect, so the trade-off isn't obvious yet.

I'm noting that the bias terms are nearly balanced, so tweaking them further won't buy much. Since β only rescales a per-class constant, all the per-image signal sits in the correlation with the templates, meaning the classifier is effectively a correlation plus bias. Any real gain has to come from changing the template shapes themselves, perhaps by weighting features that are distinctive to each class.

I'm considering a hand-specified covariance with a spatial smoothness kernel plus a ridge term, so that the weights become Σ⁻¹μ_c, which would sharpen the templates toward their edges. Since this is a prior model rather than something estimated from samples, I'm wondering whether it counts as the forbidden discriminant analysis, though I think it's analytical enough to be allowed.

I'm weighing a high-pass version of each template, subtracting a blurred copy so that only the spatial variation remains, since that should approximate an inverse covariance and emphasize contours over uniform ink. Filtering the templates this way would reduce how much overall ink spread drives the correlation.

I'm going to try sharpening the templates with a high-pass filter, subtracting a blurred copy at half strength on each 8x8 grid so only the spatial contours remain. That means mapping the feature positions onto the grid, blurring, and mapping back. Since the weights change, the bias terms will need recalibrating afterward.

I'm weighing whether to renormalize the sharpened weights by dividing by (1 − α), so that smooth regions keep roughly the same effective scale as before. The bias would then come from μ·w rather than the raw template norm, which keeps the per-class constant consistent with the sharpened correlation term.

I'm going to try sharpening the templates with a high-pass filter at α=0.5, subtracting a blurred copy so only the spatial contours remain, then renormalizing so smooth regions keep their scale. Since the bias depends on the new weights, I'll recompute it from μ·w and then check whether the accuracy actually improves, reverting if it doesn't.
