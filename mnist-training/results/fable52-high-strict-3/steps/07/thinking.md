I'm checking the false-positive counts for 8: the false 8s add up to about 1,289 against 980 correct recalls, while predictions for the other digits are much more precise. I'm now wondering why 8 gets over-predicted, since its bias moved from -0.5 to -0.2 and the hole features push it up.

I'm working out why the false 8s are so high, and the hole and bay weights look like the likely cause. The 8 class has near-neutral bay weights while other classes take a penalty for unexpected bay firings, so 8 ends up winning whenever those detectors fire more than expected.

I'm now checking whether the 4s that get misread are firing bay detectors in places that favour 8, since 4's recall dropped sharply.

I'm checking whether the bay detectors are firing in places that favour 8, since 8 has near-neutral bay weights while other classes take penalties, and 4's recall has dropped sharply too.

I'm checking whether the bay detectors fire in places that favour 8, since 3's recall fell and 3s seem to be going to 8 and 5. I'm wondering if narrow-mouthed bays on 3s get read as holes, which would push 8 up and 3 down.

I'm now testing whether 2s and 0s are being read as having holes, since a 2's curled top or a narrow 0 could make a hole detector fire and push the 8 class up.

I'm weighing whether the 0→8 confusions could come from hole or bay detectors, and concluding that a tall 0 can't produce a hole reading, so the cause is more likely a positive bias on 8 (plus the bay weights for 0).

I'm checking whether 8's bias at −0.2 is simply too high for these sharper features. The jump from −0.5 to −0.2 pushed predicted 8s from about 550 to over 2,200, a much steeper response than I expected, so the system looks very sensitive to small changes in that bias.

I'm estimating the per-digit bias corrections from the log ratio of predicted to true counts, with a damping factor of about 0.3. Column 0 needs roughly +0.06 and column 1 roughly +0.07, so I'm working through the remaining columns to get the full update.

I'm working through the per-column bias corrections now: most columns need a small positive nudge, column 4 needs a large one, and columns 5 and 6 are slightly over-predicted, so they move down a little.

Now I'm checking the per-digit corrections against the 8 and 9 counts, and it looks like 8 would drop about 0.24 relative to the others, which overshoots the balance I had before. I'm wondering whether the real fix is reducing how sensitive the logits are to the biases, since the classes look nearly tied for many images.

I'm now going through the 4 confusions in more detail: 4s are getting pulled toward 8 and 9, and I'm wondering whether an open top is being read as a hole or whether the upper bay simply isn't firing for them.

I'm checking how the 4 stroke geometry looks at the top, since the left stroke runs toward the right vertical there and the gap narrows to about 6 px, which could be why an open top gets read as closed.

I'm wondering why 4s get pulled toward 8 and 9 when their bay and stroke geometry looks open enough at the top. The biases seem to be the more likely lever here: 4's bias sits near −0.06 while 9 and 8 have been nudged upward, so I'm checking how those shifts compare to what each class needed in earlier steps.

I'm looking at why 4s get pulled toward 9 and 8. The bias shifts for those classes are doing most of the work, since 4 sits so close to them in template terms, and the bay detector for 4 doesn't seem to be pulling its weight against 9's penalty.

I'm looking at the 3→5 confusions, which jumped from 24 to 113 after 3's bias dropped and 5's rose, and I don't see a bay firing in the upper part of the 3 that would explain it. I'm also noting that the 1→2 errors persist, which points to slanted 1s, and that the 7 confusions with 5 and 9 look like they were already there before. My plan is to damp-update the biases toward a balance of around 78–80%, and then adjust the structure weights where the confusions point to a specific detector.

I'm weighing whether to rebalance the biases with damped updates or to change the template scale α, since doubling α would halve the bias sensitivity but would also need larger biases to reach equilibrium. I'm leaning toward the damped rebalancing now and accepting the result, rather than reworking the loss temperature.

I'm settling the 8 bias by interpolating between the step 5 and step 6 counts in log space, which lands around −0.37, and I'm noting that the other class biases shift too, so the relative gap for 8 needs rechecking.

I'm settling the 8 bias around −0.40, since interpolating its predicted counts in log space points there, and then the 9 bias at roughly −0.03, because its counts also rise on the 4 and 7 images it draws most of its false positives from. For 4, the step 5 gap to 9 was +0.3, but in the newer run 8 and 9 both moved up, so 4 is now competing against stronger rivals.

Next I'm setting the bias for 4 at about +0.15 and checking it against the 9 and 8 gaps. For 7 the earlier steps suggest a bias well above where it sits now, so I'm working out how far to push it.

I'm settling the 3's bias at about −0.55, since its step 6 count is too low, and the drop in 3→8 confusions should push its predicted count back up anyway.

I'm now setting the biases for the remaining digits: 5 at about 0, 6 near −0.22, 0 at roughly −0.05, and 1 around −0.19, each based on where its predicted counts land relative to the targets.

I'm checking whether 1→2 errors make sense given the bias changes: step 5 had b1 − b2 = −0.25, but step 6 gave −0.18, so 1 became relatively stronger in step 6 even though 1→2 confusions rose, which doesn't line up with a simple bias story.

I'm wondering why 1s are being pulled toward 2 more often now, since the bias gap between them actually narrowed but the 1→2 confusions doubled. That suggests some structural detector is firing on certain 1s, like ones with a flag or base stroke, in a way that favors 2, and I can't yet tell which one it is.

I'm now checking whether a single diagonal stroke could register as two walls at once, since a bg cell offset up and left of it would see ink both above and beside it. That would only make a bay if a third wall were also present, so I'm wondering whether digits with a diagonal plus a nearby stroke are what's tripping the upper-left detector.

I'm weighing whether to soften the negative structure weights for the classes where the unexpected firing is hard to pin down, since the 5 versus 3 gains came from both positive and negative bay weights. Overall accuracy stayed flat even though the balance was far off, with 8 badly over-predicted.

I'm now weighing whether to soften the hole weights for 8 in the middle positions, since its loops sit mostly at the top and bottom and the 2s it attracts may be firing on the bottom loop alone. I can't cleanly AND the two holes in a linear model, so I'm considering a small reduction there instead.

I'm finishing the bias settings for the remaining classes, with 8 and 2 weighed against the 3→8 and 2→8 counts, and I'm leaning toward letting the bias reduction for 8 handle most of the 3→8 drop rather than reworking its hole weights.

I'm settling the remaining biases: 3 stays at −0.55, 4 at +0.15, 5 at 0, 6 at −0.22, 7 at +0.5 since its false positives are low enough to absorb the increase, 8 at −0.40, and 9 at −0.03. I'm now checking whether raising 1's bias to counter the 1→7 risk would also push the 1→2 confusions back up.

I'm settling the bias for 1 at about −0.08, since its false positives mostly came from 4, 8, 9, and 6, and the structure weights now push those down. I'm also considering halving 1's bay penalties, in case the 1s that cause the 1→2 confusions are the ones with serifs firing bays, and I'm weighing that alongside the 2's lower-right bay weight.

I'm dropping class 1's bay penalties to −0.3 while keeping the hole penalty at −1, in case the serif-style 1s are what triggers the bay detectors. I'm also weighing whether to lower 9's hole weight at the top, but I'm leaning toward leaving it, and then I'll submit the new biases with this 1 tweak.
