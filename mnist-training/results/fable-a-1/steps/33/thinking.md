At 89.2% with loss 0.374, things are improving and I have 18 steps left. I'm weighing whether to spend roughly 6 to 9 of them on more measurements instead of tweaking knobs, and I'm starting to sort out which measurement would be worth the most.

I'm weighing some options for the remaining steps: more measurements on the other checkerboard half of the features, corner features per row, or tuning the gain and clip knobs, each with a rough guess at how much accuracy it might add. The 7-to-2 confusions are still the hardest to explain, so I'm going through the naive Bayes contributions for a typical crossbar 7 to see where the 2-like evidence comes from.

I'm working out what a typical crossbar 7 looks like under the naive Bayes scores, since its bottom-left cell firing would push it toward 2 by a fair margin. I'm also checking how a missing bottom-right stroke for 7 would cost it against 2.

I'm checking whether the corner evidence is double-counting when several cells light up at once, so I'm considering a higher NBAR or a lower GAMMA_C to damp it. I'm also weighing whether to raise the orientation weight G_O further, since the last increase helped, and I'd rather change one knob at a time.

I'm deciding whether to spend the next six steps on measurement rather than knob tweaks, and I'm weighing the value of more features versus tuning gain or clip. Once the measurements are in, I'd rather adjust the knobs against the new feature set.

I'm sizing up the remaining error pairs, the big 7→2 and 9→7 confusions in particular, to see which kinds of features would help most. Corner cells per row look like the next thing to weigh against the other checkerboard half.

I'm considering measuring row-level corner presence instead of the zone-level version, since that would pin down vertical position for the loop-shaped confusions like 4 versus 6 and 9.

I'm checking whether the row-level corner idea would actually help with the 8→6 errors, and it looks like it wouldn't much: those 8s have small or filled upper loops, so they're missing the upper corner evidence altogether, which a finer vertical measurement can't recover.

Weighing whether more features or knob tuning will move accuracy more, both look like gains of under a point. I'm also wondering whether a discriminative correction could help with the mixed-mode classes, but I can't train here, so that's out. Recalibrating the output temperature might still shave a little off the loss at 0.374.

I'm going to try nudging the orientation weight G_O up to 0.62 next, since the last increase helped, and I'll keep the other knobs fixed so I can tell what each change does.
