The model only reached 38% accuracy, and it leans hard on certain classes: 6 gets predicted far too often, while 3 and 4 almost never show up as predictions. Class 7 also seems to pull in predictions from several other digits.

I'm re-deriving the convolution indexing to see whether the template-to-image mapping is off by a shift. Tracing the taps through both conv layers and the pooling, the centres come out as rows 2R+6 through 2R+9, which gives the same y-to-template mapping I had before, so the geometry checks out.

I'm now wondering whether the templates are biased by how the mean subtraction and clipping treat digits with a lot of ink, since the geometry itself checks out. Max-pooling also makes real strokes look thicker than the templates, which could be skewing the matches toward 6 and 7.

I'm checking whether the mean-centering makes the thin templates clash with the dilated real strokes, and I'm asking why the "1" images go to 2 and 7 instead of 1. Looking at the center column, several digits (3, 5, 6 and others) have ink there, so the vertical stroke of a 1 may partly match their templates.

I'm estimating how strongly the center column pushes "1" images toward class 1 versus class 2: the ink from 1's vertical stroke and the low average there give class 1 a sizeable boost, while class 2's template has positive cells at its top, diagonal, and bottom but negative cells across the rest of that column.

I'm checking whether the templates are actually aligned with the image: the indexing for the second conv layer and the pooling seems right, but I want to confirm the mapping from template cells to pixel positions and whether the fully connected weights use the matching row and column offsets.

I'm checking the filter orientations in the first conv layer: a horizontal filter should respond to horizontal strokes, and the mapping from its output to the next layer looks consistent. I'm also wondering whether the response is too weak for thicker strokes, since a stroke that is a few pixels too wide could cancel out in the negative lobes.

I'm thinking the 6-bias may come from the clipping normalization, since digits with dense ink like 8 would saturate their templates differently from the rest.

I'm weighing whether the templates' mean-centering and clipping could favour digits with lots of ink, since the template for 6 and the ink-heavy digits sit on the same bowl-shaped regions. If the centered templates correlate best with dense-ink images, a digit's total ink would push the logits in a consistent direction.

Now I'm checking why the 3 templates score so poorly, since 3 → 6 comes out at 445 while 3 → 3 is zero. I suspect the 3 template is badly placed or too weak, so I'm going back to its definition.

I'm checking the 3-template's score: its logit depends on how its centred cells line up with the image, and the template looks well-formed from its parametric definition, so I'm working out why it still never wins.

I'm checking whether the templates' mean-centering makes the ink-heavy digits win on total ink alone, since a uniformly inked image would score each class by its ink minus the average.

I'm checking why class 2 wins so often on these 1-images when the vertical filter should favour class 1. Both templates cover roughly the same number of cells in that centre band, so the tie should go to the vertical match, which makes me suspect the vertical filter isn't responding the way I expect.

I'm now considering that the real 1 strokes are slanted, which the vertical filter's negative side lobes penalize, and that the 1→7 confusion may come from the hook at the top of many 1s. That points to a broader robustness problem, so I'm thinking about making the templates thicker and the orientation filters less strict.

I'm weighing whether to thicken the templates and soften the orientation filters, since real strokes are wider than my thin templates and a slightly off-angle stroke can land in a negative lobe. A flatter response across orientations would lose selectivity, so the trade-off is unclear, and I'm considering whether a learned linear classifier on the 8x8 ink would simply do better.

Blurring the templates to about 2 to 2.4 pixels should bring them closer to the real class means, since those are much fuzzier than my thin strokes. I'll also add per-class biases to counter the drift toward 6 and 7, though I want to see how the blurred templates change the confusion matrix before tuning those.

I'm going to settle on mild per-class biases for now: pushing 6 and 7 down, and nudging 3, 4 and 9 up, and I'm holding off on bigger changes until I see the new confusion matrix. I still want to understand why 6 keeps winning, since that's what makes the fix trustworthy.

I'm asking why the 3 templates score so low even though its shape checks out. Its thin stroke is narrower than the real 3s, which spread further to the right, so the template probably misses much of the ink that actually matches.

Checking the template geometry, the arc points and scaling look right, so the problem may be elsewhere. Since the logit for each class is a sum over the centered template, a uniformly inked image favors classes with more total template ink. I'm thinking about whether the indexing or the centering has a subtle bug.

I'm checking the horizontal and vertical filters against a stroke of three rows: a stroke sitting centred on the profile scores highest, and an offset one scores lower, so max pooling keeps the best-aligned position. That means the orientation response itself looks sound, and the vertical filter should favour clean vertical strokes.

I'm checking whether the vertical filter's response holds up for a stroke that's slanted by about 15 degrees: the shift across five rows is small enough that the stroke should still sit mostly within the central columns. I also want to confirm the horizontal response, since the orientation template values look consistent with the real ink. Next I'm asking why the 3 and 4 templates never win, given that their middle ink should be contributing.

I'm considering whether the centre-band weights are the real culprit: many digits cross the middle, so subtracting the full mean pushes 3 and 4 toward zero or negative there. Scaling the mean down (say by 0.6) and normalising each template's energy might let those classes compete on fair terms.

I'm now realizing the bias term matters: the nearest-centroid score should subtract half the squared norm of each class template, which I left out, so classes with more ink like 0, 8, 6 and 2 get an unearned boost. I'm considering using the blurred templates directly as class means and adding that norm-based bias, which would only be right if the image scale roughly matches the template scale.

I'm switching the templates to be the class means themselves, with a per-class bias of minus half their squared norm. Subtracting the overall mean doesn't change the argmax, since that term is the same for every class, so my earlier centering was doing nothing for classification and the bigger-ink classes were winning by default.

I'm noticing the classifier is effectively doing raw template matching without the per-class norm correction, so classes with more template ink get an unearned advantage. Adding a bias of minus half each template's squared norm should fix that, and thicker templates would bring them closer to real class means.

I'm turning the class templates into smoothed class means, scaled so stroke centers sit near 0.9, and the orientation maps get the same treatment at about 0.8 on the matching strokes. With a nearest-centroid score that subtracts half the squared norm of each template, the bigger-ink classes lose their unearned edge, and I'm setting the ink and orientation scales to 0.3 and 0.2.

I'm settling on the orientation features as a secondary signal, weighted down to about 0.15, to see whether they help separate pairs like 1 and 7 without adding too much noise. I'm also keeping the 1 template straight with a uniform blur of about 0.8 cells, since slant variation makes the class mean a fatter vertical band.

I'm setting each template's stroke to about 1.25 cells, so neighbouring cells sit around 0.5 to 0.8, which should match how the max-pooled features actually look. I'll then give each class a bias of minus half the weighted squared norm of its template, so the nearest-centroid score stops favouring classes with more ink.

Still tuning the template setup, keeping conv1 and conv2 as they are.
