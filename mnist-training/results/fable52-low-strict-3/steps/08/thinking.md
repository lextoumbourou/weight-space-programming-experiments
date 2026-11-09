Now I'm weighing how to detect loops or closures at the top of the image, so 9, 7 and 4 can be told apart with the six remaining conv2 channels.

Now I'm checking which features separate 9 from 7 near the top of the loop, using the upper-left cells where the loop's left side would sit.

Now I'm checking whether the 7s actually have energy in the rows 10-13, cols 8-11 cell, since my cue for 9 made 7→9 worse; that would mean my centring assumption for 7 is wrong, because its diagonal shifts the lower stroke toward the left-centre.

I'm still checking whether the 7s have any energy in that lower-left cell, since that would explain why the cue pushed 7 toward 9. The shear and the bias might account for most of it instead, so the cue alone may not be the culprit.

Now I'm considering whether to try multi-variant templates, since the model is linear and the variants could simply be summed, as I did for 0 and 1. I'm thinking about the real shapes that matter most: some 7s have no top-left stroke and a more vertical diagonal, some have a middle bar, and some 9s have a straight stem with a smaller loop or an open top. The 2→3 confusions look like they come from 2s whose bottom stroke curls, so I'd tell them apart by the ink at the lower-left.

Now I'm looking at the lower-right region to tell 2 from 3: a 3 has a vertical arc there while a 2 has nothing on the right side between the middle and the bottom bar. I'm also considering an ink-energy cue in that cell, which should favour 3.

Now I'm trying a negative cue on the lower-right cell to push 2 away from 3, and I'm weighing whether to tweak the bias for the other digits too. I'll keep the remaining confusions (0→6, 0→8, 6→0) on the list for later, since they need a different approach.

I'm looking at the zeros that get misread as 8s: the narrow ones may be picking up the hole penalty and getting pushed toward 8. I'm considering lowering the penalty and bias weights, or building a proper hole detector from paired side-V channels with an empty centre.

Now I'm thinking about separating 0 from 8 with a hole detector built from paired side-edge channels with an empty centre, averaging over six pixels of height so it fires on zeros but not on the upper loops of 8s.

Now I'm working out how the hole detector should sample height, using rows 1-3 of the taps so a zero's empty centre is checked over a 6-pixel span. The zero's centre should land in the middle cells, while the 8's loops and the 6's loop sit higher or lower and only partly overlap.

Now I'm sketching a "narrow hole" channel that fires on enclosed spaces: zeros and sixes light up in different rows, while nines and fours light up higher up.

Now I'm thinking a "bay/hole" channel could help separate 7 from 9 and 4, and 2, 3 and 5 from 8. Since the taps span only about 8 pixels, I'm considering whether the pooled columns can cover a wider gap by dilation.

I'm settling on the output formula for a narrow-hole channel: average the two side-V responses over rows 1–3 and subtract twice the centre energy, then a bias of about -1.2. A pair of strokes about 8 pixels apart with an empty middle should give a positive value of roughly 0.2, even for slanted sides.

Now I'm settling the threshold for that lateral-edge channel at about 1.25, adding diagonal contributions to the side energy so slanted strokes still count, and checking that a single straight vertical stroke can't trigger it.

Now I'm assigning per-class weights to the hole channel by row: 0 gets positive weight in the middle rows, 9 and 4 in the top rows, 6 in the lower rows, 8 at the top and bottom, and 7 and 1 get negative weight everywhere.

Now I'm weighing whether 4's open top really makes the hole channel fire, since its left stroke is a slanted diagonal and the sides sit about 7 to 9 pixels apart. I'm setting the per-class weights so that 7 gets a strong negative value on that channel, and 2, 3 and 5 get negative values too, with 5 softened in the lower rows where its belly closes.

Still writing the hole channel weights...

Still writing the channel weights...

Now I'm settling the threshold for the hole channel at about 1.15, scaling the diagonal contribution down so a single straight stroke can't trigger it, and checking that slanted sides still get past the threshold.

Still working out the vertical taps, and I'm switching to just rows 1 and 2 so the sides don't need to be as tall.

Now I'm assigning the hole channel's weights by row: zeros get positive weight across all four rows, while nines get a strong positive in the top two rows and a negative in the bottom two.

Now I'm assigning per-class weights to the hole channel by row, with the sides of 4 and 6 weighted against each other and 7 and 3 pushed down across every row.

Now I'm adding the ink cue for 2 and 3 on the lower-left.
