I'm at about 54.8% with eight steps left, so I need bigger jumps. Next I'm checking where the confusion comes from: the predicted totals show digits 0 and 3 are over-predicted, and I'm tracing which digits feed into 0.

I'm checking why digit 0 gets over-predicted, since 7, 4, and 9 send it a lot of mass. Its SLOT and CUP features could be firing on those digits, especially 4 when its arms are tall, and I'm weighing whether the orientation match is pushing 0 up too.

I'm checking whether 7 is being pulled toward 0 or 3 by the features it fires, since it's under-predicted at 407. It's missing HOLE, SLOT, and CUP, so its structural score mostly comes from BOT, while 9 and 0 each have their own requirements that the 7s don't meet.

I'm still trying to pin down why 7 loses out to 0 and 9: its structural score rests almost entirely on the bottom bar, while 0 gets its lift from the orientation template. I suspect the 7 template fits poorly and the 0 template is so broad that it matches many digits, so I'm considering per-class bias tuning and leaning more on the structural features.

I'm checking the BOT rule against the confusion counts: about 1300 errors come from digits that lack the bottom bar being mixed with ones that have it. Since BOT fires in roughly 95% of 1, 4, 7, and 9 but only about 3% of 0s and 3s, its weight looks too weak next to the other features, so I'm starting to work out how much to raise it.

I'm checking how much the bottom-row feature should count across the whole row rather than only in the expected cell, since a 7's tip might land one column off and get no credit.

I'm making the BOT feature a strong group signal: a positive weight on the bottom-row sum for classes 1, 4, 7, and 9, and a negative weight for the rest, with 2 penalized less. That should make the group gap large enough to fix most of the roughly 1300 cross-group errors.

I'm checking how 6 and 8 separate, since 6 sends about 346 samples to 8. The 8 template gets the same hole cells as 6, plus an extra right-side waist feature, so the question is whether that waist detail is what tips the decision.

I'm checking why 2 keeps leaking into 3, 0, and 8: its top-left and bottom-right features are only partly reliable, and it has no hard forbids to stop those confusions.

I'm now looking at how 5 gets pulled into 3, with 356 of its samples landing there, and checking whether 3's orientation template is too generic to separate them.

I'm checking why 5 so often lands in 3: its top gap is narrow, so the center cell for the OR feature rarely comes up empty, and that detector fails more often than it should. I'm considering whether looking at ink one step off the center would make these narrow cavities register more reliably.

I'm testing a wider version of the cavity check, looking at ink in neighboring cells so narrow gaps still register, though summing overlapping cells could overcount a diagonal wall.

I'm weighing whether to tune the cavity detectors for the narrow top gaps, since a looser threshold would catch 5s but might also fire on plain vertical strokes. With only eight steps left, I'd rather put the effort into a strong bottom-row group rule first.

I'm weighing a few more levers: class biases from the confusion counts, especially pulling 0 and 3 down, and nudging 8 a little. Looking at row 1, most of its errors go to 7, with smaller spill into 2 and 3, and I think that slant-driven confusion is an orientation issue rather than something the bottom-bar fix will solve.

I'm going through the confusion rows for the remaining digits. Row 4 leaks mostly into 0 and 9, and row 7 leaks into 0, 3, and 9, so the bottom-bar fix should recover a large share of those cross-group errors. Row 5 and row 6 are still tied to 3 and 8 through the cavity and waist features, which I'll need to revisit separately.

I'm looking at the leftover errors after the bottom-row fix, which should recover roughly 1,500 of them. Within the non-bottom group, the main confusions are 2 into 3, 5 into 3, and 6 into 8, so I'll need separate structural cues like the top opening, the bottom bar, and the top tip to tell them apart.

I'm setting a bias of about -0.5 on class 3 and a smaller one on class 0, since both are sinks for the confusions. After the bottom-row fix, 0 still picks up inputs from 2, 6, and 5, so it will remain high, and 3 would still be well over-predicted.

I'm weighing whether a probe on HOLE, OL and OR would separate the non-bottom digits, since their presence or absence should tell 0, 2, 3, 5, 6 and 8 apart.

I'm weighing whether a probe on the top gap and bottom cells would separate the rest of the digits, and I'm leaning toward spending one step on it since it would show whether the right-side cavity detector ever fires on 5s.

I'm weighing a small probe that checks whether the hole, outer-left, and outer-right cues fire where I expect, since that would separate the non-bottom digits. I'm also thinking about whether to run it now or first apply the bottom-row fix, which is the surer gain with eight steps left.

I'm planning a probe on the HOLE, OL, and OR detectors, using thresholds around 0.4 to read eight combinations of the three bits, and I'll use the step to check whether those cues separate the non-bottom digits before adjusting the classifier.
