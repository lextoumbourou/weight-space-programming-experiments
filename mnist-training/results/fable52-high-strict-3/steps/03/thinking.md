Now I'm checking how the biases are affecting the recall for 8 and 9, since they're still under-predicted and the false positives are high. The earlier −1.3 and −0.7 were too strong, while the other digit classes improved. I'm now trying a smaller adjustment, around −0.5 for 8 and about −0.2 for 9, and I want to work through the counts at b=0 to see where that lands.

I'm trying the biases for 8 and 9 at around −0.6 and −0.2, since the −1.3 and −0.7 were too strong. Recall for 9 looks poor at both settings, and its main confusions are with 4 and 5, so the penalties may be hurting real 9s that vary in shape. I'll balance the two classes at those values and then look at class 3, which is still over-predicted.

I'm weighing a bigger bias correction for class 3, which is still over-predicted, and nudging 6 down a little too. The per-class false-positive counts are high across several digits, so simple bias tweaks look like a blunt tool here, and the real gain probably has to come from better features or templates.

I'm reading the confusion counts as a sign that the templates only loosely match real digits, since the errors are spread across many pairs. Tweaking biases looks like a blunt tool, so I'm thinking the real improvement has to come from better templates or features.

I'm considering a probing approach: each intermediate step's feedback reveals per-class prediction counts, and since only the final network is scored, earlier steps can be used purely to measure something useful, like where a given feature peaks for each digit.

I'm settling on keeping things honest here: each submission should be a real attempt at a good classifier, and I'll learn only from its confusion matrix rather than turning the network into a probe that measures the dataset's statistics. Probing the feedback that way would sit uneasily with the "no training data" spirit of the task, even if tuning biases from confusion counts is the same kind of move.

I'm weighing whether to improve the templates through reasoning about what breaks cosine matching: stroke thickness, position and slant variation, and templates that sit off the true class means. Blurring the templates and pooling features over a wider area could make matching more tolerant of those shifts, and I'm considering what a structural, rule-based classifier for the digits might look like.

I'm looking at how the 9s keep getting mistaken for 4s and 5s, which suggests the narrow-loop templates for 9 are too rigid for real variation. I'm also thinking the zero class relies too much on the empty center, and that the 6 and 8 templates overlap with it. Bias tweaks only move the numbers around, so I'm considering whether the features themselves need more spatial tolerance.

I'm thinking about using mid-level parts instead: 5x5 convolutions over the feature maps that respond to half-digit-sized shapes like closed loops, corners, and crossings, each with a threshold so it acts like an AND detector.

I'm weighing parts-based detectors that use larger spatial patterns, since they would add shift tolerance on top of the current pooling. Hand-designing them without any visual check is risky, but they might capture the relational structure of digits better than whole-digit templates.

I'm weighing whether finer parts like 10x10 pixel shape detectors would tolerate deformation better than whole-digit templates, though designing them without visual checks is risky. Improving the current linear scheme doesn't really allow multiple templates per class, so I'm looking at the 2 versus 3 confusion, where the bottom stroke of a real 2 often curls like the bowl of a 3.

I'm comparing the 2-versus-3 scores on these images, where the 3 template comes out higher than the 2 template even after the bias adjustment. I suspect my 2 template may be sitting too high vertically, so its centroid doesn't match where the bottom bar actually lands.

I'm checking whether the 2-versus-3 confusion comes from the templates themselves: the 3 template seems to cover most of a typical 2 image, since its middle and bottom strokes line up with the 2's diagonal and bottom bar, and only its lower-right stroke is missing. The 2 template may therefore be too narrow to win that comparison.

I'm working out why class 3 keeps winning over 2: the 3 template covers most of a 2 image, so the fix may be to raise the weight on features only 3 has, like the lower-right stroke, and offset it with a more negative bias. In the Euclidean form, each expected feature only earns credit if it's actually present, so that presence requirement is what I'd be leaning on.

I'm considering whether a full Euclidean form would fix the 2-versus-3 margin, since it builds in a presence requirement for expected features that cosine lacks. Under ideal conditions both forms behave similarly, so the difference would only show up with real variation.

I'm considering whether blurring the templates would give the same kind of tolerance to variation, and I'm weighing per-feature weights that down-weight strokes with high within-class variance, like the 2's diagonal and bottom bar, against the parts-based approach that might handle that variation more naturally.

I'm considering blurring the templates so they tolerate misalignment better, though that trades away some discrimination. Nearest class mean on pooled orientation features might land around 88–90%, and my current 76.6% suggests the templates are far from true class means. I'm not sure how much the confusion matrix can tell me about specific template corrections, so I'm weighing a more deliberate approach that builds explicit rule features for the key confusions.

I'm sketching a parts-based version of the second convolution: 5x5 kernels over the eight orientation maps, each meant to pick up a half-digit-sized shape like a loop, using the 10x10 pixel receptive field.

I'm sketching a loop detector for the 0, 6, 8 and 9 shapes: horizontal strokes at top and bottom, vertical strokes on both sides, and an empty center, requiring about three of the four sides to fire. I'm also considering a left-open bay shape for the 3s and 2s, though I haven't worked out its details yet.

I'm deciding against hand-designed part detectors, since I can't check them visually and only have confusion matrices to debug with. I'll stay with linear templates and improve them step by step, starting from what the average MNIST digits look like, such as the slightly tilted ring for 0 and the slanted stroke for 1.

Now I'm going through the typical MNIST shapes for each digit to see what the templates should look like, starting with the 2, which has a strong bottom bar, and the 3, with its top and bottom arcs. For the 4, the left stroke runs down to a crossbar around row 14, and the right vertical sits near column 16 or 17. I'm still working through the 5, where I'm checking how the top bar lines up.

I'm picturing how the digit shapes should look, using the average MNIST layouts: a ring for 0, a slanted stroke for 1, a loop at top with a tail for 9, and so on. The mean positions seem roughly right, so the weak point is probably how well the features pick up curved and thick strokes.

Thinking about the stroke thickness now: MNIST digits are fairly bold, often 3 to 4 pixels wide and sometimes 5 or 6, and my bar filter only peaks cleanly for about 3-pixel strokes. Thicker strokes would give doubled ridges with weaker responses, and the ending detectors would miss them too. Since cosine is scale-invariant, the real trouble is the biases and the noise, so I'm considering an edge-based orientation detector that responds to gradients and is less sensitive to width.

I'm weighing a different kind of feature: edge detectors that respond to the gradient at each side of a stroke, so their response doesn't depend much on stroke thickness. That would use both polarities per orientation, roughly eight channels, though I'd lose the ending detectors and I'm not sure how much those contribute.

I'm weighing whether to keep the edge-polarity idea: a stroke's two sides would give features that don't depend on its width, though I'd lose the ending detectors. Making the bar filter wider doesn't fit a 5x5 kernel for strokes that are 5 pixels thick. The alternative would be dropping the endings to free up channels for thickness-robust bar detectors.

I'm weighing how stroke thickness affects the filters: the typical MNIST stroke is about 3 pixels wide, so the 3-pixel bar filter fits most digits, though bolder ones probably suffer. I can't confirm that from the confusion matrix alone, so I'm not sure where the 1→2 and 1→7 errors are coming from.

I'm adding a slanted variant to the 1 template, since strongly tilted 1s overlap with the diagonal stroke of the 2, and I'm weighing how much the wider coverage would weaken the penalties for 1.

I'm weighing a different idea: whether a Euclidean distance with biases could work better if the bias scaled with each template's magnitude, since bold and thin digits produce feature vectors of different sizes and a fixed bias suits some of them poorly.

I'm now considering a bias that scales with the total feature energy: subtracting a constant from every weight of a class, so broad templates lose score on any image in proportion to its overall intensity. Centering each template (zero-mean, normalized) would give a correlation-style match that handles bold and thin digits more evenly.

I'm considering whether a zero-mean, normalized correlation could replace the constant biases. A broad template like the 8 would have a larger mean, so it would get a bigger uniform penalty on any image, which seems fairer than the fixed offsets I've been tuning.

Now I'm weighing a zero-mean normalized correlation in place of the constant biases, which would be scale-free and handle thin and bold digits more evenly. I'm also thinking about scaling the bias by the total feature energy so it adjusts with each image's intensity, though that would mean another round of tuning against the confusion matrix.

Now I'm weighing whether to convert the constant biases into an energy-proportional form, where each class's weights get a uniform offset that scales with the image's total feature sum. The catch is that the typical sum is unknown, so I'd still be tuning by feedback. I'm leaning toward keeping the constant biases and adjusting them against the confusion matrix. The 9 row looks like the most useful signal, since it's confused with nearly every other digit, which suggests its template is off rather than just its bias.

I'm comparing the 9 and 8 biases against the earlier runs, where the −0.7 setting cut correct predictions from 720 to 504. I suspect the penalties on unexpected features are hurting 9 most, since its variations fall outside its template. I'm also looking at 8, whose recall stayed around 521 while it kept pulling in 3s, 6s, 2s and 5s. A zero-mean normalized correlation might handle the broad-versus-narrow balance more cleanly than hand-tuned constant biases, and I'm starting to test how a 1 image would score against the 8 template.

Now I'm wondering whether a slanted 1 gets matched by the 8 template, since its diagonal runs through the center where the 8's crossing strokes sit. The 8 would still get a modest positive score there after mean subtraction, but the slant mismatch seems to explain why so many 1s were pulled toward 8 in the first step.

I'm giving the 1 template a fan of slanted variants, since an 8 has a long diagonal through its center that a slanted 1 would otherwise match. I'd set the slants to roughly 3°, 17° and 31° with weights of about 0.7, 1.0 and 0.7, which should cover the range of real slants without overlapping too much at the center.

I'm picturing the 1 template as a bow-tie of slanted variants, with the vertical and the upper-right and lower-left diagonals meeting at the center. I'm also wondering whether giving every digit a couple of slant variants would make the templates more robust, though I'm unsure whether that counts as building synthetic samples.

I'm weighing whether to keep the constant biases and retune them against the confusion matrix, or switch to a zero-mean normalized correlation. I'd rather keep the biases for now, so I'm proposing a few targeted shifts: 8 goes from −1.3 to −0.6, 9 from −0.7 to −0.2, and 3 from −0.8 to −1.1, with 6, 5 and 2 nudged as well.

I'm considering whether the 0 and 6 confusion comes from their upper strokes: real 6s often have a more vertical left stroke, while slanted 0s lean right at the top, so the 6 template may need to match that shape more closely.

I'm looking at whether a 6's upper stroke could be told apart from a 0's right-leaning top by adding explicit penalties for the upper-right vertical stroke on the 6 template, since its coverage may currently let that stroke through.

I'm adding explicit penalties to the 6 template on the upper-right stroke, since a 0's top arc curves down that side and the 6's coverage there currently lets it through. For the 0 template, I'm marking the middle band, where the 6's loop crosses, as negative.

I'm looking at how the 0 and 6 templates could be separated: the 0 should have an empty center band, and the 6 should be penalized on the upper-right stroke where a 0's arc would sit. I'm also checking why 9s are being pulled toward 4, since a round loop top should count against the 4 template more than it currently does.

I'm now looking at why the 5 template keeps attracting 9s, 7s, 8s and 3s. The top bar of a 7 seems to line up with the 5's top bar, and I'm checking whether the 5's bowl on the right side is what's pulling those other digits in.

I'm adding a crossbar variant to the 7 template, since its mid-level bar lines up with the 5's bowl and is what keeps pulling 7s toward 5. For the 5 template, I'm also looking at penalizing the upper-right vertical region, where the 9's loop and tail sit.

I'm noticing that the penalty on the upper-right region would keep 5 from matching 9s, 7s, 3s and 8s, since 5 has nothing there below its top bar. The problem is that the current weighting still leaves that region almost uncovered for 5.

I'm deciding to strengthen the penalties by hand rather than only raising the global weight, with explicit absence rules for each digit at specific row and column positions. I'm now listing the row and column centers I'll use for those rules, and I still need the per-digit geometry in pixel coordinates before writing the actual values.

I'm computing the centerline midpoints and lengths for each stroke of the 5 prototype, so I can place the penalty rules at the right pixel positions.

Now I'm computing the centroid of the 5 prototype's stroke midpoints, weighted by segment length, to get its center of mass for placing the penalty rules.

Next I'm working out the upper-right region for the 5 template: I'd rule out any vertical or down-right stroke there in rows 8 to 13, since a 5 has nothing in that area below its top bar, and I'm starting a rule to encode that.

I'm setting up a rule for the 5 template that rules out vertical and diagonal strokes in the upper-right region at the middle rows, since a 5 has nothing there beyond its top bar. The bowl's top-right edge starts to appear near the middle row, so I'm checking how far that rule should reach before it starts penalizing the bowl itself.

I'm writing a rule for the 5 template that rules out vertical and diagonal-down strokes in the upper-right region at the middle rows, since a 5 has nothing there below its top bar. That should also cover the 7's stem, the 9's loop side, and the 3's upper arc.

I'm checking which left-side strokes a 3 is missing, since 2, 5 and 8 are all pulling toward it. A 3 has nothing on its left at rows 9 to 13, so the 3 template may need an explicit absence rule there, and I'm also looking at whether the bottom-left end of a 3 is what's letting 2s through.

I'm adding a rule for the 3 template that rules out vertical and diagonal strokes on its left side in the upper-middle rows, since a 3 has nothing there, and that should cut down the 2s, 5s and 8s pulling toward it. I'm also considering a second, weaker absence rule for the lower-middle left region.

Now I'm working out which left-side strokes a 3 should be missing, so I'm weighing a penalty on vertical and diagonal strokes in the lower-left region at rows 10 to 13 for the 3 template.

I'm working out the 2's diagonal at the lower left, estimating where its stroke runs at a few points down the digit to see whether it reaches the columns where the 3 template should be penalized.

Now I'm going through the miss counts by class: 7 is confused with 9, 4, 0, 3 and 2, and 8 is drawn toward 3, 6, 2 and 5, so I'm laying out the next steps as a plan. The first step is rebalancing the biases, then adding a 1 fan template, a crossbar variant for 7 at weight 0.4, and a few hand-set negative rules for 5, 3 and 0.

I'm setting up hand-tuned negative rules for the 4 template: a horizontal stroke near the top in the middle columns, since 9s are being pulled toward 4 and a 9's round top shouldn't be matched by that bar.

Now I'm checking whether a crossbar or a horizontal stroke near the top of the 4 template is what's pulling 9s toward it, and whether a diagonal in the upper-right would separate the two better than the current weighting does.

I'm working through the rule for the 9 template: a horizontal stroke at rows 14–15 on its bottom-left closing stroke would be partly captured by a window at the right-middle, so I'd add a weak negative for H there. I also note that 4's two upward-pointing endings at the top don't appear in a 9, so the 9 side is already penalized for those.

Now I'm weighing how much weight to give the penalty rules against the automatic penalties, and I'm settling on an absolute value around −0.7 so they can override the current positive weights.

Now I'm setting the bias values: 8 goes to about −0.6 and 9 to about −0.2. For 6, the false positives outnumber the misses, so I'm moving it from −0.4 to about −0.6, and I'll check how a new rule on the 0 template changes that.

Now I'm settling the bias values: 6 goes to about −0.6 since its false positives come mostly from 9, 8, 4 and 5. For 0 I'll keep it near −0.3, and 2 stays at 0.3 since the fan template should cut the 1→2 confusions. For 4 I'm moving the bias to about −0.1, because the 9→4 mix-up will be handled by the rule and the stronger 9 bias. I'm keeping 7 at 0.3 and expecting the crossbar variant to help, and for 1 I'm noting that the fan template will widen its norm and shrink those entries, which is acceptable.

I'm making the 1 template a fan of three strokes through the center with different slants, and I'm keeping the bias at 0 since the fan is symmetric and won't shift the centroid.

Still refining the 1 template and the 7 crossbar, with a weight of 0.4 and the crossbar placed across the stem.

Now I'm writing a rule for the 5 template that penalizes vertical and diagonal strokes in the middle rows of the upper-right region, since a 5 has nothing there beyond its top bar. I'm also checking whether the top bar of a 5 might tilt up to the right and leak into the diagonal features at that height.

Now I'm working through the rules for the 3 template, planning to penalize vertical and diagonal strokes in the upper-middle rows.

Now I'm checking the 3 template's top-left start, which runs up and to the right and could match a diagonal rule there. Its angle makes it fairly strong at rows 2 and 3, so I'll limit the penalty to those rows.

Now I'm looking at whether a 3 should be penalized for vertical and diagonal strokes on its left side at the middle rows, since a 5 or 2 might have a stroke there that's pulling it toward the 3 template. I'm estimating how much of that stroke would fall inside the 3's left window, and whether it's strong enough to justify a penalty around −0.56 across those features.

Now I'm settling the rule for the 3 template, looking at whether vertical and diagonal strokes at the left-center upper rows should be penalized, and I'm weighing a weaker penalty of about 0.4 there since a narrow 3 can leak a little into that region.

Now I'm checking the 0 template's sides at the middle rows. Its left and right edges are nearly vertical with a slight tilt, so I'm weighing a penalty for horizontal and diagonal strokes in the central-lower rows to keep 6s and 7s from matching it.

I'm working out a rule for the 0 template: a horizontal or upward-diagonal stroke in the lower-middle rows, on its inner sides, weighted at about 0.6. A weaker 0.3 penalty for the other diagonal, since it only partly reaches that region.

Now I'm adding a rule for the 6 template on its upper-right side, where the top stroke starts and a diagonal could leak in, and I'm weighing a penalty of about 0.6 for the nearer rows and a weaker 0.3 for the next column over.

Now I'm checking the 6 template's top stroke, which at its lower end sits around x 11 to 13 in the middle rows, so a rule on the inner side at that column could catch it.

Now I'm checking the 6 template's top stroke: it could fall within the 5 and 3 windows, so I'm limiting the penalty to the vertical and diagonal features at the far-right column in the upper-middle rows. Next I'm turning to the 4 template, which I'm writing up as its own rule.

Now I'm working through the rule for the 9 template: a horizontal stroke in the lower-middle rows, on the loop's bottom side, at about weight 0.3, and I'm checking where the loop's mean row falls to pin down its window.

Now I'm dropping rule R7 for the 9 template, since its bottom stroke overlaps too much with the 9's tail at the right edge. I'm going with a rule for class 7 instead: a vertical or diagonal stroke along the loop's left side, in the middle rows, at weight 0.5.

I'm settling the 7 template now, weighing a vertical or diagonal penalty at the left-center rows. Its stem sits too far down to matter in the middle rows, so I'm keeping that penalty limited to the lower-middle rows.

Now I'm checking whether a 2's bottom bar and upper-right arc could pull a 2 toward the 3 or 8 templates, so I'm looking at which rows and columns on the right side should be penalized for vertical and diagonal strokes.

Now I'm finishing the rule for the 2 template, weighing a vertical-stroke penalty on its right side in the lower-middle rows at about 0.6, and leaving the less-reaching column at zero.

I'm checking the 9's confusion pairs now: its loop bottom sits near the 0 template's middle rows, so I'm keeping the 0 penalty there, while the 7 and 5 penalties already cover the rest.

Now I'm working out the bias values for the final version, and since the new rules add more penalties for 3, 5, 6, and 0, I'm considering easing some of those biases a bit.

Now I'm writing the code, with the bias values for the final version set to the list I settled on.
