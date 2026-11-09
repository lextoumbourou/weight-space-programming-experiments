Hit 74% on the first try, so now I'm digging into where the mistakes come from. Class 8 gets over-predicted the most, with about 874 false positives, and class 3 comes next with roughly 670. I suspect 8's broad template is pulling in too many inputs, since cosine similarity gives a broad template decent scores against nearly anything, and I'm checking 1→8 errors in particular.

I'm weighing a bias adjustment for classes 8 and 3, since the logits scale with the feature norm. I'm also considering a Euclidean-style formulation, because a 1 has a small norm and would lose out to 8's large template norm once the bias is applied.

I'm working through a Euclidean-versus-cosine hybrid, scaling the dot product by the template norm and subtracting a penalty tied to that norm. I'm also wondering whether the real feature scale differs from the template scale, which would shift the right trade-off.

I'm checking the 2 and 5 confusions with 3, since 3's template overlaps heavily with both and it wins more often than its accuracy justifies. Its near-perfect recall suggests a bias down for 3 and probably 8, and 9 looks over-favored against 7 and 4. I still need the logit scale before picking how large those bias corrections should be.

I'm considering a norm-based bias, setting each class's bias proportional to its template norm so that broad templates like 8 and 3 get pushed down, which is exactly where the over-predictions are. Small-norm digits like 1, 7, and 4 would be left less penalized, which lines up with their under-prediction.

I'm weighing whether the Euclidean penalty should be scaled down, since if the real features are smaller than the templates it would over-penalize broad ones like 8. I'm also comparing plain Euclidean scoring against dividing by the template norm, to see which handles an 8 image better.

I'm checking whether the raw score scale changes things: with a feature-norm factor c, the 8-template's large norm penalizes its score too much if c is small. I'm weighing a norm-based penalty as a hedge, since it would push down broad templates like 8 and 3 but I can't yet pin down c.

I'm looking at why 1s get mistaken for 8s: my 1 template is narrow, so a slanted or shifted 1 mismatches it, while the broad 8 template still matches. A norm penalty would help here, since 1 images have small feature norms. I'm also considering making the 1 template more robust by blending in slant variants.

I'm weighing whether the norm penalty will be enough for the 2→3 and 5→3 confusions, since 2, 3, and 5 have similar template norms and the penalty won't separate them much.

I'm now looking at the 2-versus-3 confusion: 2 has a diagonal running through the lower-left and a bottom bar that ends pointing right, while 3 has a stroke on the lower-right and a middle junction with its ending pointing left. Real 2s often have a loop at the bottom-left that might be shifting the diagonal lower, which could explain why they look like 3s to the template.

I'm thinking about adding discriminative weights for the 2-versus-3 confusion, penalizing features that other classes use but this digit doesn't have, so the templates separate on the parts that actually differ.

I'm wondering whether a penalty that only amplifies the features unique to each class would help, since shared features mostly cancel in the difference between two templates. It would mainly sharpen weak but exclusive fringe features, which acts a lot like increasing the scale α on those parts.

I'm looking at why 5s get called 3s: both share the bottom bowl and the top bar, so the difference comes down to the upper-left vertical in a 5 versus the upper-right stroke in a 3. Real 5s often have a short upper vertical near the center, which may be why the template misses them.

I'm weighing a negative bias on class 3, since its recall is about 96% while 2 and 5 only reach 55% and 49%, so the 2→3 and 5→3 errors are probably coming from 3 winning too easily. Trimming its logit should convert a lot of those mistakes, and the blur between 5's near-center vertical and 3's upper-right curve is the likely source of the overlap.

I'm settling on explicit negative biases for classes 8, 3, and 9, since the confusion matrix shows them absorbing most of the errors. To pick the size, I need a sense of the logit margins, and the loss of 0.9176 at 74% accuracy hints they're moderate, around 1 to 2 in log space.

I'm settling on explicit biases here: a larger negative for classes 8 and 3, a smaller one for 9, and small ones for 6 and 0, since the confusion matrix shows those classes absorbing most of the errors. Logit margins look like they're around 1 to 2, so a shift of about 1.2 should flip plenty of false 3s while costing few correct ones, which makes this look like a net gain.

I'm going to fold in some structural changes to the templates alongside the bias fix, since any of them should help. The 7 class is the weakest, with only 58% recall, and it's bleeding into 9, 3, 5, and 0. My 7 template is probably mispositioned, so I'm looking at the top bar and stem placement against how real 7s are drawn.

I'm checking whether the 7 template's top bar is hooking down on the left, since that tick would make real 7s look like 9s. Lowering the 9 bias and tightening the 4 template's top closure would address the 4→9 overlap too.

I'm considering a set of hand-written veto rules on specific regions of the digit grid, with negative weights for particular classes. For class 9, the question is what 7 has that 9 lacks: a left-pointing ending at the top-left, with no loop. I'm also looking at the 7 template's upper-left vertical and mid-row horizontal, since those are where a 9's loop would sit.

I'm working through the remaining confusions by hand: some penalties on the 7 template's upper-left vertical and the 4 template's top closure, plus bias adjustments for the pairs where 8 and 9 keep absorbing errors. The 0→8, 4→8/9, 9→8/6, and 2→8/3 counts all point to the same broad-template problem.

I'm going to rely on bias adjustments as the most dependable fix, and I'll only add a few discriminative rules where I'm reasonably sure of the effect. I'm starting with a rule for separating 4 from 9 by looking at the top center.

I'm weighing a penalty for class 4's top crossbar: a horizontal stroke near the top center would push a 4 toward a 9, so I'm working out how negative that weight should be relative to the typical template scale.

I'm checking the 4-versus-9 case next: a penalty on a horizontal stroke across the top center would push a 4 toward a 9, so I'm working out how large that weight should be relative to the usual template scale.

I'm adding a mild negative weight for class 7 on the vertical strokes at the left-middle, since a 7 should have nothing there, though the serif tick at the top-left makes that boundary a bit fuzzy.

I'm estimating where the 9's left loop side would sit in the template grid, working out its column position from the digit's centroid, so I can compare it against the 7 template's left-side features.

I'm narrowing the class 7 penalty to rows 10 through 14 on the left side, since the serif tick at the top-left would otherwise trip it. That range should catch the loop's left edge of a 9 without penalizing the tick.

I'm considering a more general fix: sharpening the discrimination by subtracting, from each class template, the features that other classes strongly expect but that class itself leaves uncovered. That would make the weights for each digit more exclusive, though I'd still want to check how strong the subtraction should be.

I'm considering a broader idea: penalizing each class's template on features that other classes expect but that it leaves uncovered, which would make each digit's weights more exclusive. The catch is that this doesn't help the 1→8 case, since a clean 1 gets no penalty either way, so the bias adjustment still has to handle that.

Now I'm defining a coverage map for each class by dilating its template over neighboring rows, columns, and orientations, so that penalties only hit features a class truly lacks.

I'm defining a penalty for each class wherever its template has no coverage but another class does, scaled by how relevant that feature is. Keeping the relevance weight at 1 would penalize noise evenly, but that risks biasing against narrow classes, so I'm weighing whether to scale it by the strongest class expectation instead.

I'm settling on a penalty scale: each feature that a class's template doesn't cover but another class does gets a negative weight, scaled to the typical template norm so that a full unexpected stroke adds roughly one to two logits against it.

I'm weighing whether to add the unexpected-feature penalties now alongside bias changes, since the penalties will shift the balance toward narrow classes like 1, 7, and 4, which are already under-predicted. Shifting biases to compensate would mix two changes together and make the effect hard to read. Doing the bias adjustment alone first is the cleaner path, with penalties added in the next step.

I'm going with both changes together this step, the bias adjustment and the unexpected-feature penalty at a moderate strength, since the next confusion matrix will show how much each bias needs to move. I'm also treating the 1→8 errors as a thick-stroke problem: a 1 drawn heavily gives a weak filter response with no ending signal, so the broad 8 template wins, and a strong negative bias on 8 should help.

I'm setting the biases to push down the broad classes: 8 most, then 3, 9, 6, and 0, with the rest left at zero. I'm also checking whether the penalties already handle the 2→3 and 5→3 confusions, since those features belong to 2 and 5 but not to 3.

Checking the 2 and 5 images against class 3's features now: the 2's diagonal strokes near the lower left would only partly register as unexpected for 3, and a 5's vertical stroke at upper left has no counterpart in 3's template at all, so I expect some penalty there.

I'm settling on the bias values for this round: a firm negative on class 8, a smaller one on class 3, and milder ones on 9, 6, and 0, with the rest at zero. I'm also checking that the unexpected-feature penalties already cover the 2→3 and 5→3 confusions, since a 5's upper-left vertical stroke has no real counterpart in class 3's template.

I'm defining the coverage for each orientation feature by taking the maximum over neighboring rows, columns, and adjacent orientations, with row neighbors counting fully, column neighbors at 0.6, and adjacent orientations at 0.7.

I'm turning to the coverage check for endings: the same dilation over rows and columns, with adjacent directions weighted at 0.7, and I'm testing whether a penalty scaled by the template norm lands at a sensible strength.

I'm settling the penalty strength at μ=0.5, since a fully unexpected stroke then costs about 1.1 logits, which is modest but meaningful. I'm also making sure the code is built from the templates first and the weights second, so the setup order stays clear.

Still writing the coverage code...

Still writing the coverage code...

I'm setting the biases for the next round: a small negative on class 0, a mild positive on 2 and 7 since they're under-predicted, firm negatives on 8 and 3, and smaller negatives on 6 and 9, with 1, 4, and 5 left at zero.
