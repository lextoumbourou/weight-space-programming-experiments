Good improvement! 45.5% accuracy (up from 44.0%). Loss slightly increased (1.597 vs 1.595) but accuracy improved. The hole detector bias change helped!

Let me analyze:

Predicted column sums:
Col 0: 722+0+25+0+9+48+84+43+4+58 = 993
Col 1: 3+856+46+64+86+62+33+57+94+85 = 1386
Col 2: 51+40+498+36+21+54+108+2+176+0 = 986
Col 3: 84+2+262+471+5+95+69+43+104+11 = 1146
Now I'm tallying the remaining predicted column sums, covering columns 4 through 8.

Now I'm checking the per-class accuracies, and the rest of the column sums look off: column 1 and column 7 are over-predicted, while column 9 is badly under-predicted.

I'm going through the per-class accuracies now. Classes 3, 4, and 7 improved noticeably, while class 6 dropped and class 8 got even worse.

The biggest remaining problem is class 8 bleeding into class 7 (401 cases), and class 7 is now over-predicted at 1471 against 993 earlier. The +0.15 bias on class 7 looks like it overshot, and class 9 is being starved at 592 predictions.

Now I'm working out the new biases, starting with class 0, which barely moves since it's close to its target count. I still need to sort out classes 8 and 9, since class 9 is under-predicted and class 8 is nearly never right.

Now I'm recomputing the bias for class 7 and running through the remaining classes, using the same log-ratio adjustment on each.

Now I'm working out the bias for class 7, which comes out to about 0.02 after the log adjustment. For class 9 I'm getting roughly 0.03. The final set of rounded biases is ready, and the biggest shifts are for classes 1, 7, and 9.

Lowering the hole detector bias from -0.2 to -0.1 should be gentler, since -0.2 may be suppressing real holes along with the false positives.

Now I'm weighing whether the hole detector bias of -0.2 is too aggressive: it cut class 7's false positives and lifted its accuracy, but classes 8 and 9 dropped, which suggests it may also be suppressing real holes. I need to find a balance between those effects.

I'm weighing a middle value for the hole detector bias: -0.15 sits between the -0.1 and -0.2 options, and it should cut the false positives without suppressing as many real holes. Since the false positives are already lower, I'd like to bring the hole template scales back up somewhat.

Now I'm weighing whether to change the digit 8 ink template, since at 4×4 resolution its features overlap with digits 0, 2, 3, and 5, and the current templates don't separate them well.

Now I'm sketching out the 8's ink pattern: the top and bottom of the two loops land in the middle columns, while the waist rows are filled across the whole grid.

Still working through the 8's ink pattern: I'm computing the first row's weighted sum against the centered template.

Still working through the 8's ink pattern, and I'm checking whether its logit beats the class 7 one.

Still working out the digit 8 logit, and I'm now checking the row 1 contributions against the class 7 template.

Still working out the digit 8 logit for class 7...

So class 8 should win on digit 8 images at 1.70 against 0.85 for class 7, yet 401 of them still land in class 7. My feature estimates must be off, and without the real features I can only tune the biases and template scales. For this step I'll lower the hole detector bias to -0.15, lower class 7's bias, and raise class 9's.

I'm thinking about lowering the hole template scales back up now that the bias is gentler. I also want to nudge classes 8 and 9 up, since they keep being under-predicted, and pull class 7 down. Next I'm considering a horizontal stroke template for class 8 at the waist, since that's the feature that sets it apart from 0.

Writing the digit 8 horizontal-stroke template...

Still working out the digit 8 template, now checking the digit 0 horizontal-stroke pattern at the top and bottom rows.

Still working through the digit 8 logit, this time with a horizontal-stroke template that emphasizes the waist.

I'm checking whether a horizontal-stroke template emphasizing the waist would separate digit 8 from digit 0, since the waist is the one feature that 8 has and 0 doesn't.

I'm settling on the concrete changes for this step: lowering the class 7 hole bias to -0.15, updating the full bias vector, nudging the hole scales back up a bit, and switching the digit 8 horizontal-stroke template to one that emphasizes the waist. I'm also double-checking whether the hole bias should move at all, since the accuracy numbers from the earlier step are what I'd be judging it against.

Comparing the hole detector bias results: classes 7, 8, and 9 together went from 538 to 644 correct, so the -0.2 setting helped overall. Class 7's gain outweighed the losses on 8 and 9. I want to keep that gain while recovering some of 8 and 9, so I'll try -0.15 and then work out the bias vector.

I'm going to set the class 9 bias a bit higher, to 0.10, since it's still being under-predicted. I'll finalize the bias vector for this step.

Now I'm considering whether the hole bias at -0.15 might be a bit more sensitive and help the digit 6 cases. The 2 versus 3 confusion is still the persistent one, with 262 cases, so I'm looking at horizontal strokes at the bottom to separate them.

I'm settling on a smaller tweak for the 2-versus-3 confusion: the bottom horizontal stroke should separate them, but my h-stroke scales for 3 may be too weak, or the 2 and 3 features may not differ enough at the bottom. I'll avoid over-tuning one pair and focus on the biggest gains, starting with setting the class 7 hole bias to -0.15.

Still writing the weight-building function...
