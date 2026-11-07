I'm seeing that the model is at about 52% accuracy and the errors are concentrated in a few specific digit pairs. The biggest confusions are 0 being labeled as 6, 8 being mistaken for 2 and 3 (and 8 is rarely predicted at all), and 7 being confused with 9, 5, and 3. Smaller clusters show up between 3 and 5, 5 and 6, and 1 and 2.

I'm treating the class 8 problem as a template-geometry issue: its two-loop shape gives a large mass and penalty offset, while real 8s are narrower with smaller top loops, so the overlap is lower than the template implies. Rather than keep theorising, I'll tune a per-class penalty multiplier from the confusion matrix, lowering it for under-predicted classes (8, 7, 4, 1, 0) and raising it for over-predicted ones (2, 3, 5, 6, 9).

I'm setting per-class penalty multipliers from the column sums against the true counts: class 8 gets the biggest cut (about 0.3), 7 and 4 get smaller ones, and the over-predicted classes 2, 3, 5 and 6 get increases.

I'm going to tweak the templates for class 8 as two smaller ellipses, a narrower top loop and a wider bottom one, since real 8s look more like that than the circles I used, and the side features should then line up better with the cells.

I'm checking why 0 keeps losing to 6 even though 6 is mostly contained in 0's shape: the stem and the mass penalty seem to favour 6 when the real 0s may be narrower or taller than my ellipse.

I'm checking whether 0 and 6 are really the issue here: my ellipse for 0 may be too narrow and too short compared with real 0s, which are wider and taller, so the mass penalty ends up favouring 6. I'm also noticing that 7 sits near 9 and that 4's top, with its two verticals and crossbar, can look like a 9's loop, so both 7 and 4 probably need a lower penalty as well.

I'm checking the 7 versus 9 confusion: a 7 has no ink in the lower-left where 9's loop sits, so the missing template strokes only cost a little penalty. I'm also raising the negative-evidence weight to 0.25 and setting per-class penalty multipliers from the column sums.

I'm checking whether scaling class 8's penalty down to about 0.14 would overshoot, since it might then get over-predicted, so I'm considering a more moderate version of the formula-based multipliers.

I'm hardcoding the per-class multipliers from that formula, which gives class 8 about 0.39 and class 2 about 1.2.
