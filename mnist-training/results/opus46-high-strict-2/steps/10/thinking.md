Step 9: 43.98% accuracy, 1.5946 loss. Slightly better than step 7 (43.78%, 1.6015). The revert worked and the small bias improvements helped.

Let me analyze the confusion matrix:

Predicted column sums:
Col 0: 670+0+40+1+22+69+155+53+14+147 = 1171
Col 1: 3+930+45+68+67+56+17+76+145+73 = 1480
Col 2: 44+85+480+39+10+44+45+4+243+1 = 995
Now I'm totaling the remaining predicted columns, from column 3 through column 7, and working out each sum from its row of counts.

Still tallying the remaining column sums to check the balance.

Now I'm checking the per-class accuracy figures. Class 1 is clearly the strongest at 87%, while classes 8 and 9 are close to 10%, and class 7 is also weak.

Now I'm checking the top confusions and how the bias correction changed the class 8 and 9 predictions, which dropped from 1273 to 1048 for class 9. Classes 7, 8 and 9 still have very low per-class accuracy.

With six steps left, the goal is to fix the worst classes. Classes 7, 8 and 9 are the weakest, under 31% accuracy each. The biggest confusions all point into class 9: digit 7 is mislabeled as 9 (479 times), 3 as 9 (281 times), and 9 is itself confused with 8 (377 times). That suggests class 9 is absorbing too many other digits.

I'm also noticing that class 8 is spreading its predictions across several other classes, mostly 2, 5 and 1, without capturing enough of its own digit. So I'm going to compute bias corrections for each class using the update new = old + 0.35 × log(1000 / predicted). Class 0 comes out around 0.095, class 1 around -1.537, and class 2 around 0.902, and I'm working through the remaining classes now.

Next I'm computing the bias update for class 8, which is still working through the same formula.

The biases are nearly stable at this point; the main shifts are class 1 going to about -1.55 and class 7 rising to about 0.15. The templates still don't separate the digits well enough at this resolution, so I'm nearing the limit of what this approach can do.

I'm weighing whether fixing the specific confusion pairs could help more than the bias tweaks, starting with the 7→9 mix-up, where 479 sevens are labeled as nines. My next step is to see why digit 7's features line up with class 9's template at certain grid positions, possibly by coincidence, and then the 8s, which are almost never classified correctly.

Now I'm comparing the digit 7 and digit 9 templates, centering the 7 grid around its mean of about 0.19 to see whether its ink lines up with the 9 pattern.

Now I'm centering the digit 9 template around its mean of about 0.34 to compare it against the centered 7 grid.

Next I'm working through a rough digit 7 feature grid, with the strong top bar and the diagonal peaks, to see what its class 7 logit comes out to.

Still computing the feature-by-template products for digit 7 and working through the row sums.

Now I'm working out the class 9 logit from the same digit 7 features, with the first two rows coming to about 2.3 and 0.02.

Checking the class 7 and class 9 scores on the same digit 7 features: the class 7 total comes out ahead by about 3.2, and with the bias terms it's 3.62 against 0.32. The hole contributions are the last piece still to work out.

Checking the class 7 and class 9 scores on digit 7 features makes me think the feature estimates must be wrong, since class 7 should clearly win. Yet 479 of 1090 sevens land in class 9, so the real features must look quite different from what I've been imagining, and the delta kernel may be producing patterns I haven't accounted for. Next I'll work through the 8×8 conv2 output more carefully.

Now I'm working out how the 2×2 max-pooling windows map onto the 12×12 grid, starting from the block at rows 2–3 and columns 2–3.

Working through how the 2×2 max-pooling windows map back onto the conv1 grid, with the row and column ranges for the second pooling stage.

Now I'm checking how the 8×8 receptive fields line up for digit 7: the bar sits in rows 4–8 and the diagonal runs down toward row 24, so each pooled cell only sees part of the stroke.

Now I'm checking how the bias of -0.15 affects the conv1 output, which only fires where the ink is strong enough. The bar sits in conv1 rows 0-8, so the first maxpool positions pick up its signal, while positions 4-5 mostly catch the start of the diagonal. For the delta kernel, the 2×2 window at maxpool1 rows 2-3 and columns 2-3 is what I need to work out next.

Now I'm checking the top-left pooling windows for digit 7: each one overlaps the bar's ink, so they should all come out positive.

Now I'm revising the digit 7 feature estimates: the top bar should register strongly across all four columns, and the diagonal energy sits on the right side of the upper rows and drifts toward the center-left lower down. I'm working out the class 7 logit from these revised features.

Still computing the digit 7 class logits with the revised bar-heavy features.

Still working through the class 7 and class 9 logits for digit 7, with the revised bar-heavy features.

Still working through the class 9 logit for digit 7, with the rest of the row sums and the bias terms to add.

Now I'm checking the class 9 total for digit 7 against the earlier estimate, which gives a gap of about 2.4 in favor of class 7, so my feature values must be off somewhere. But 479 of the 1090 sevens still land in class 9, so the real features must differ from what I've been picturing, and I want to figure out which part of the image is driving that.

I'm checking whether the hole template for class 9 could be picking up false positives from the top bar of the 7. Digit 7's own hole template has negative weights, so any hole detections there would push its score down while boosting class 9, which could explain some of the misclassification.

I'm thinking the hole detector might be firing on the corners of the 7's bar, producing false "holes" that raise class 9 and lower class 7. That could explain the 7→9 confusion. To address it, I could either weaken the hole weights for classes 7 and 9, or make the hole detector more selective by adding a bias to conv1 filter 7, which currently has none.

I'm adding a negative bias of -0.2 to the hole detector (conv1 filter 7) so it only fires on clear holes and produces fewer false positives. I'm also planning to reduce the hole template scales for classes 7 and 9, and I'll keep the other biases as they were in step 9. Then I'll look at the 8s, which seem to match class 8's ink template poorly.

Now I'm working out what a digit 8 looks like at the 4×4 grid level: the top loop should register in the upper-middle columns, the sides of the loops on the outer columns, and the waist in the center.

Now I'm working out whether the 8×8 receptive field at maxpool1 rows 2–3 and columns 2–3 actually reaches the ink of the upper loop, since that depends on how large the digit is. The digit 8 case is still too uncertain to pin down from these estimates. For step 10, I'm planning to add a bias of -0.2 to the hole detector (conv1 filter 7) so it fires less on false positives.

Next I'm planning step 10: updating the biases, shrinking the hole template scales for classes 7 and 9, and trying a more selective hole detector.

I'm halving the hole template scales for classes 7 and 9, since the false positives from the bar's edges are probably inflating class 9 and penalizing class 7. Then I'll work through the updated weights.

I'm halving the hole template weights across all classes, since the detector's false positives seem to be inflating the wrong logits. Combined with the more selective bias on the hole detector, that should cut down the spurious 7→9 signal.

I'm checking whether a slight negative bias on the hole detector would still leave real holes firing. At actual holes the output should stay positive after the shift, so the detector would keep working while dropping weak edge responses.

Now I'm working out the step 10 changes: a more selective hole detector with a -0.2 bias, which should keep true holes firing while killing the weak edge responses through ReLU. I'm also looking at digit 8, which is classified as almost anything except 8, with only 95 of 1009 correct and the largest confusions going to 2, 5, 1, 3, and 7.

I'm weighing whether to increase the ink template scale for digit 8 or rework the template so it better matches the sharper features the delta kernel produces.

I'm sketching what digit 8 might look like on the 4×4 grid: ink at the top and bottom edges of each loop, and ink through the middle rows for the sides and the waist crossing. That pattern is nearly identical to digit 0's, and the only real difference is that 8 has ink in the center where 0 is empty.

Now I'm comparing the class 0 and class 8 ink templates, which differ mainly in the center cells: 0 has negative weight there while 8 has a mild positive one.

Working through the digit 0 logit by hand now: the top and bottom rows of the template line up with the strong edge values, which pushes the score up, while the two middle rows partly cancel it out.

Working out the class 8 logit on the same 4×4 grid: the top and bottom rows and the middle rows each contribute, and the sum comes to about 0.75 for the middle rows and 0.875 for the top row.

Checking the class 2 logit for the digit 8 features against class 8 now.

Now I'm finishing the class 2 logit for the digit 8 features, with the remaining rows of its template still to add.

I'm finishing the class 2 logit for the digit 8 features, which lands at about 1.51 once its bias is added, nearly tied with class 8 at 1.56. Next I'm running the same check for class 5 against that digit 8 pattern.

Now I'm working through the class 5 logit against the digit 8 features, starting with the top row's contribution.

Checking the class 5 logit against the digit 8 features, the last rows come to about 0.7 once the 0.35 scale is applied. That is still to be combined with its bias.

I'm weighing whether class 5's high bias of +1.0 is what pushes it above class 8 on digit 8 images, since its template match is only modest. That would explain much of the 8→5 confusion. The likely fix is to lower class 5's bias or strengthen class 8's template response, rather than leaving every bias fixed.

I'm picking step 10 back up: I want to add the bias on conv1 filter 7 as the next change, since I've already concluded that the bigger issue is the 4×4 resolution making digit patterns too alike.

Now I'm trimming the hole detector's bias to -0.2 so it stops firing on edge responses, and halving its template scales to cut false positives. I'm also dropping class 5's bias from +1.0 to +0.8, since its high bias is what pushes it above class 8 on digit 8 images. Class 8's bias goes up from 0.42 to 0.5 to close that gap, and the other biases get small corrections.

Now I'm settling on the step 10 biases, so I'll write the code with the updated values.
