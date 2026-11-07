Good improvement! 43.8% accuracy, up from 41.9%. The delta kernel helped! Loss also improved significantly (1.60 vs 1.64).

Let me analyze the confusion matrix:

Predicted column sums:
Col 0: 710+0+45+1+29+83+181+60+15+171 = 1295
Col 1: 3+937+55+75+75+67+19+74+151+71 = 1527
Col 2: 50+65+478+39+11+44+45+3+216+0 = 951
Col 3: 59+2+229+360+4+58+29+38+94+8 = 881
Now I'm tallying the remaining confusion matrix columns, working through the counts for columns 4 through 8 and starting on column 9.

Now I'm checking the rest of the per-class accuracy numbers, and the class 3 figure looks like 35.0% at this point.

I'm checking the per-class accuracy figures now, and class 8 stands out as very poor at under 9%. Class 7 has risen sharply from 12% to about 33%, while class 6 has slipped back. The biggest remaining confusion is class 7 being predicted as class 9, with 472 cases.

Class 8 is by far the weakest, with only 89 of its samples classified correctly, and the confusion matrix shows several new big errors, like 6→0 and 9→0, so class 0 looks over-predicted.

I'm working out the new bias values for each class, starting with class 0: its predicted count is 1295 against a target near 1000, so its bias gets pulled down by about 0.1.

I'm working out the bias updates for the remaining classes, using the same 0.4 * log(1000/predicted) adjustment. Class 1 comes out at about -1.42, and classes 2 and 3 move up slightly to roughly 0.92 and 0.95.

Working out the rounded bias values now, with class 2 and class 3 landing near 0.9 and 0.95.

Checking the 6→0 confusion next: both digits are round, so the question is whether the bias or the template is driving the 0 over-prediction.

Now I'm weighing whether the 6→0 confusion comes from the bias or from the templates. The ink patterns for 0 and 6 do differ, but the delta kernel may be blurring those differences, so I'll keep the kernel since it raised accuracy, and focus on the class 8 problem next.

I'm looking at digit 8 now, since it's the weakest class at 8.8%. Its template is a full ring of ink, and once centered it's close to the 0 template but with a much weaker center, so the two patterns overlap.

I'm weighing whether digit 8's template is too close to the others, since its center is only mildly negative and it overlaps with the 0, 3, and 5 patterns. I'm considering what distinctive features would separate it, like the two stacked loops.

Working out the ink template for digit 8 with a waist, so the middle rows carry less ink and the two loops stay distinct; I'm also centering it by subtracting the mean, which comes to 0.375.

I'm working out a weight template for digit 8 to separate it from digit 0. Both patterns have negative centers and positive edges, so at this resolution the main difference is the hole layout: one central hole for 0, and two smaller holes for 8.

I'm sketching the hole layouts for digit 8: the top loop should sit around rows 0–1, columns 1–2, and the bottom loop around rows 2–3, columns 1–2. Once the grid is 4×4, those might collapse onto the edge rows, so I'm redesigning the templates to keep the two holes distinct from the single central hole of digit 0.

I'm reworking the hole templates for digits 0 and 8 so they differ: 0 keeps its hole at the center, while 8 gets holes at the top and bottom loops. I'm also considering whether overlapping receptive fields will blur that distinction, but I'll keep the delta kernel since it helped accuracy, and move on to small bias corrections and a few other templates.

I'm checking why digit 6 might get confused with 0: both have ink on the left and a bottom loop, and the top-right of 6 is weak. My current 6 template is close enough to the 0 template that the overlap could explain the 181 errors.

I'm looking at why digit 6 might get mistaken for 0, comparing the signs at the side columns of each template. Digit 6 has no ink on its right side in the middle rows, while 0 does, so I'm considering a stronger left edge on the 6 template to pull it away from 0.

I'm going to adjust the digit 8 ink template so the middle rows carry an even amount of ink across all four columns, since a digit 8 with a waist should look like that. I'm also going to reduce class 0's bias, because it's being over-predicted at 1295 times.

Now I'm settling on priorities for digit 8: first trim the biases on classes 0 and 1, which are over-predicted, then work on class 8's weak discrimination, while keeping the delta kernel.

Still refining the digit 8 template: I'm shifting the weight toward the top and bottom strokes and the waist, and scaling the hole template to emphasize the loop edges.

Still working out the hole layout for digit 8, now with the top and bottom loops separated from a waist with no hole at the center.

I'm checking which digits get predicted as 8: 4s and 9s are landing there a lot, while the actual 8s are only recognized 89 times, so the class 8 score is probably too high for other digits and too low for true 8s.

Digit 8's row is spread across many wrong classes: 2 (216), 7 (187), 1 (151), 5 (141), and only 89 correct. So its template isn't matching real 8s well, even though 4s and 9s keep landing in class 8.

I'm wondering whether digit 8's features look different now that the delta kernel sharpens them, since the templates were tuned for the smooth kernel. Maybe the ink concentrates in fewer positions, which would change the spatial pattern. I'll try adjusting a few templates and see whether that helps, and then look at the unused FC channels for step 8.

Next I'm adding a bottom-right corner detector on channel 10, placing it at row 2, column 3 for digit 4 and row 0, column 3 for digit 7.

Now I'm checking the corner channels, starting with channel 12 for top-right corners, which would combine a top edge with a right edge. Channel 10 is the bottom-right corner, and I'm reviewing how these combinations map onto the edge channels.

Now I'm wondering if I should drop the corner templates altogether and focus on the bigger changes. Something is off with the 8→2 confusion, 216 errors, which seems too strong to be random, so I'm going to look at the templates for that.

Now I'm checking the centered ink values for digit 2's template, and comparing them against what a digit 8 image's features would look like.

Checking the digit 2 logit sum: it's a weighted dot product of the centered template against the 8 image features, and the partial sum is still being added up.

I'm checking the digit 2 logit by hand: the weighted sum over the centered template comes to about 0.61, and with the class 2 bias of +0.9 the total lands near 1.5, so the template's bottom bar is pulling digit 8 toward class 2.

Checking the digit 8 logit the same way, the weighted sum over its centered template is being worked out now, and the result still has to be scaled and combined with its bias.

Checking the class 2 logit now: the bottom-boundary channel adds its own weighted contribution on top of the template, and the upper-boundary term is still being worked out.

Now I'm weighing whether the edge and stroke templates for class 2 are what lets digit 8 images pick up extra logit there, since their bottom-row features overlap with the bottom loop of an 8. The fix I'm leaning toward is to make the class 2 template less sensitive to that bottom-row overlap.

Now I'm looking at digit 8's edge templates, which should be more distinctive than class 2's. I'll give class 8 horizontal strokes at both the top and bottom, which the 2 template lacks, and keep the strength uniform across the middle rows.

I'm reconsidering the bias explanation: class 2's +0.9 bias is close to what its 951 predictions call for, so the bias itself isn't the problem. The real issue is that class 8's templates need to produce stronger logits for actual 8 images.

I'm going to raise the overall template scale from 0.35 to about 0.45, which makes the template logits matter more against the biases. The biases would then need to shrink too, roughly by a factor of 0.7, so the net effect stays in check.

I'm trying a larger template scale, around 0.45, and shrinking the biases by about 0.8 so the templates carry more weight against them.

I'm settling on scaling the templates up to 0.45 and shrinking the biases by 0.8, then nudging each class's bias by its prediction-count correction. Class 0 comes out near 0.02 and class 1 near -1.29, and I'm still working through the rest of the list.

I'm settling on a template scale of 0.45 and recalibrating the biases to match, so that the class counts still line up.

Next I'm reducing the biases proportionally and adjusting them, then improving digit 8's templates. I'll also keep the delta kernel. Digit 8's horizontal stroke template is changing from uniform half-strength rows to full strokes at the top and bottom, with the middle rows set negative, which should match the two-loop shape better. I'm also starting to work out the same kind of change for digit 0.

Now I'm comparing the horizontal stroke templates for 0 and 8, since they look nearly identical, which is a problem. I want to tell them apart by hole count, one central hole for 0 versus two holes for 8, and by the waist, with 0 wider and 8 narrower in the middle. I'm about to check the vertical stroke templates for those same differences.

Still working out the vertical-stroke templates for digits 0 and 8, which are identical in pattern right now. For 8, I'm giving the vertical strokes only at the top and bottom rows, leaving the waist open, so it can be told apart from 0.

Still adjusting the digit 8 hole template, which now puts holes at the top and bottom instead of spreading them evenly.

Still working out the digit 0 hole logit, with its centered template scored against an image that has holes in the middle rows.

Checking the digit 0 hole logit now, with its centered template scored against an image that has holes in the middle rows.

Now I'm working out the digit 0 hole logit: the centered template gives 0.54 times a sum of 6, so about 3.24. For digit 8's hole template, I'm scaling the new pattern by 0.36, and it is already zero-mean, so I'm starting the same calculation on it.

Working out the digit 8 hole logit next: with holes at the top and bottom rows, the same template gives a positive contribution there, and I'm about to finish that sum to compare it against the digit 0 result.

Still working out the digit 8 hole logit: with its holes strongest at the top and bottom rows and weaker through the waist, the centered template gives a positive value that I'm about to set against the digit 0 result.

Now I'm working out the digit 0 hole logit against digit 8's hole template, with the centered pattern scored on the holes at the top and bottom rows and then the middle rows.

Still working out the digit 8 hole logit, now using its new template with the holes at top and bottom, where the top row carries the largest response.

Now I'm checking the digit 8 hole logit on a digit 9 image, which has holes only at the top, so the top row carries the response.

Now I'm checking the digit 9 hole logit against the digit 8 template, which comes out higher for 9, so the new template discriminates correctly. I'll go ahead and implement this change.

I'm setting the template scale to 0.45 and rebuilding the digit 8 templates: the hole, horizontal-stroke, and vertical-stroke patterns each move to top-and-bottom emphasis. I'll keep the delta kernel and then check whether the digit 6 hole template needs the same kind of adjustment.

Still working through the digit 6 hole logit, now checking the bottom-half holes against the template with its zero-mean centering.

Working through the digit 6 hole logit against the digit 8 and digit 0 templates, the same image gives a clear separation.

Still working through the digit 9 ink template, which needs centering before it can be compared against the others.

Now I'm checking the centered digit 9 ink template against a typical image: the top of the loop lights up in the middle columns, the loop sides and stroke fill the middle rows, and the bottom rows pick up the stroke.

Still working out the digit 9 logit, now scoring the ink template against its features row by row.

Now I'm adding the row-3 contribution to get the digit 9 logit, which totals about 4.79 before scaling by 0.45.

Now I'm checking the digit 7 image against the same digit 9 template, where the top row lights up strongly and the response comes out lower than for a true 9.

Now I'm finishing the digit 9 logit against a digit 7 image, row by row: the top row comes out to about 1.76, the middle rows drop negative, and the total is lower than for a true 9.

Still working out the digit 7 logit against its own template, with the centered values coming out largest in the top row.

Still working out the digit 7 logit against its own template, with the top row carrying most of the response.

Still working out the digit 7 logit against the digit 9 template, which comes out around 2.87 after the bias, so the class 7 score is higher.

Now I'm checking the digit 7 hole logits, which are zero for both classes since a 7 has no holes. I'll look at the horizontal-stroke template next, expecting strong top-row features for a 7.

Now I'm checking the digit 7 horizontal-stroke logit, with the top row of the centered template scored against the strong top-bar features.

Now I'm checking the digit 7 h-stroke logit, where the top row's strong bar gives about 2.15 for the class 7 template. The class 9 h-stroke template comes out to 0.45 for the same image.

Now I'm adding up the digit 7 contributions: the digit 9 h-stroke comes to about 0.81, so the 7 template leads by roughly 1.34. The ink, hole, and edge terms still need totaling to see the full margin.

Class 7 should clearly win by a wide margin on paper, yet the confusion matrix shows 472 sevens going to class 9. That gap suggests my feature estimates are far from what the real digits produce at this grid size. Hand-designed templates at 4×4 may be hitting their limit without actual data, so I'll keep tuning biases and look for structural changes.

Now I'm weighing whether the h-stroke channel's smoothing hurts here, since it's the one piece still not using the delta kernel, and whether switching the combination channels to it would fix the spatial overlap.

Now I'm checking whether the smoothing in the h-stroke channel hurts here: a thick top bar puts its two boundaries a few rows apart, so an exact-position match might miss both, while a 3×3 average could still catch them together.

Next I'm settling the step 8 plan: the smooth kernel stays for the combination channels, since it's what catches thick horizontal strokes whose top and bottom boundaries sit a few rows apart. Then I'll set the biases for the output layer.

Still working through the digit 8 templates: the hole, horizontal-stroke, and vertical-stroke patterns each get split into separate top and bottom pieces.

Now I'm adjusting the template scales for a few of the digit templates before writing the code.
