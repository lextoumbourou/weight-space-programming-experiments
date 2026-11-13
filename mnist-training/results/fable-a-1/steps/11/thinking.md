Improvement is at 80.9% with loss at 0.697, so the corner features are helping. Now I'm going through the per-digit error counts and which digits each one most often gets confused with.

I'm checking the per-digit error counts against the column sums, and the pattern is that 0, 1, and 7 are over-predicted while 2, 4, 6, 8, and 9 are under-predicted. That fits corner-rich digits losing out, so I'm thinking the corner strengths or the bias need to shrink.

I'm lowering the corner threshold constant C_TYP from 0.45 to 0.3, which makes each present corner count for more evidence. I'm also considering whether a larger S_C, around 0.3, would help, since the loss dropped when S_C went to 0.2. I'll change one knob at a time to see which effect is which.

I'm weighing whether to raise the corner feature weights, since shrinking C_TYP to 0.3 and nudging S_C to 0.25 would roughly double their effective strength. That could shift the balance toward the corner-rich classes that are being under-predicted, but I'm not sure the increase isn't too large, so I want to estimate how far off class 8 is first.

I'm working out the bias term for class 8 against class 1, roughly −1.9 versus −0.5, so class 8 starts about 1.4 behind before any corner evidence. Each firing corner cell should then pull class 8 up by a much larger amount than it pulls class 1 down, so with a typical response of 0.3 I estimate a gain of about 0.13 for class 8.

I'm setting per-class bias adjustments from the column sums: pushing up the under-predicted classes 8, 2, 4, 6 and 9, and pulling down the over-predicted 0, 1 and 7.

I'm nudging the bias terms per class: pushing 8 up by about 0.3, 2 by 0.2, and 4, 6 by 0.15, while pulling 0, 1 and 7 down by 0.2 to 0.25. Then I'm thinking about lowering C_TYP from 0.45 to 0.35 to strengthen the corner evidence, though I want to be careful since that change is riskier to attribute.

Now I'm looking at the 6-to-0 confusions, which jumped from 44 to 112 after I added the corners. Two things seem to be contributing: I reduced the hole sizes to four, which weakens the hole evidence that 6s depend on, and 0's bottom corners sit where a 6's loop corners would be.

I'm weighing whether to raise the hole-detection gain, since halving the hole sizes weakened the evidence 6s rely on, so I'm considering a 1.4× boost to the slope terms only. I'm also tracking the largest confusion pairs now, mostly 9 read as 7, 8 going to 2 and 9, and 2 going to 3 and 8.

The bias adjustments are covering the remaining imbalance, and I'll check whether scaling all the logits by about 1.3 lowers the loss. I'm also thinking about adding endpoint features that encode where stroke ends point, since the corner features already moved accuracy from 78% to 81%.

I'm weighing a few options for the next step. Adding endpoint features would be semantically useful, but every conv channel is already in use, so that would mean dropping something. Calibrating the existing corner features, through the threshold, the strength, or the window, is the cheaper route and might gain a point or two.

I'm weighing a diagnostic on the corner features next, aggregating how often each corner type fires per class to see whether my annotations match what actually happens. Another option is a corner-only classifier, whose confusion matrix would show which class templates are weakest. I'll do the bias adjustments first, then the diagnostic.

I'm weighing whether the corner weights should go up by raising S_C to 0.3 and lowering C_TYP to 0.4. My guess is that corners are underweighted given how much they already helped, so I'm planning to change those together with a smaller bias adjustment.

I'm checking whether the corner features' average strength matches the threshold I set, using the hole diagnostics as a reference point for how often a loop's corners actually fire.

I'm settling on the corner threshold: if a corner is present about 70% of the time with a mean magnitude near 0.35 after thresholding, the expected value works out to C_TYP ≈ 0.35. I'll shift C_TYP to 0.35 and raise S_C to 0.25, roughly a 1.3× boost to corner weights, and trim the bias adjustments so the corner-rich classes don't overshoot.

I'm going to scale the hole slopes by about 1.3 as well, so that's four changes at once, but each one follows from the same reasoning, so I'll keep them together.
