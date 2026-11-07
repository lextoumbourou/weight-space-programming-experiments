I'm still trying to find a structural fix for the confusions between digits like 3→5, 5→6 and 6→0. My guess is that the line detector's max-pooled responses are being dominated by stroke thickness, since the edges of thick strokes fire strongly even when the flat regions stay at zero.

I'm working through the edge response math for thick strokes: a half-plane edge gives about 0.62 per column, against 0.85 for a stroke, so thick edges still fire fairly strongly. Then I'm turning to the 5 vs 6 and 3 vs 5 confusions in the top-left region, and noting 6→0 as another case to explain.

I'm comparing my 5 and 6 templates: the 5 has a top bar and a left vertical with an open lower bowl, while the 6 is a diagonal stroke into a full loop lower down. Real 5s often have a shorter top bar and a lower bowl, so the overlap with the 6's loop seems to be where the confusion comes from.

I'm considering whether a richer feature, like a raw ink channel alongside the orientation responses, could help, and I'm noting that the feature normalization is fine for argmax since the norm is shared across classes. I'm also wondering whether the grid coverage is the real limitation.

I'm weighing whether to build variant templates for classes with more style variation, like open versus closed 4s or loop versus no-loop 2s, though I expect that to matter less. I'm also going back to the 3→5 confusion and starting to work through the upper arc of the 3 template.

I'm checking the template geometry for the 3 and 5 by sampling points along each arc. The lower halves of both shapes come out nearly identical, so the separating detail has to be the 3's upper right arc and its middle cusp versus the 5's left vertical.

I'm weighing whether the 3 and 5 templates differ mainly in their top arcs, since real 3s with a flatter top might line up with the 5's top bar. I'm also wondering whether heavy blur is washing out the detail that separates these digits, and I'm considering a conv2-based approach to keep more of that structure.

I'm considering whether signed edge detectors, which track which side of a stroke is ink, might separate 3 from 5 better than unsigned line responses, though I suspect the gain is modest. I'm also checking how many conv2 channels that would leave for the spatial grid offsets.

I'm now looking at whether the conv2 channels could do more than pass through a single offset, since a ReLU might capture conjunctions like a horizontal top stroke paired with a left vertical, which a linear layer can't. I'm weighing whether the four unused conv1 channels could carry ink-blob or endpoint detectors, but the conv2 budget is already fully used.

I'm thinking the 67% accuracy has room to climb toward the roughly 80% I'd expect from true class means, so I'll iterate on the templates against the confusion pattern. Per-class recall shows 8 at 44% and 5 at 54%, which are the worst spots to target first.

I'm looking at the 6 confusions now: 6→0, 6→1, 6→4 and 6→8 all show up, which makes me think the 6 template's upper stroke is placed wrong. Real 6s start the curve further right at the top and run down the left side into the loop, and my template roughly does that, though the shear might be pushing it the wrong way for steeper 6s. I'm also starting on the 8s, which are matching badly against 1, 2 and 9, probably because real 8s are narrower and more slanted than my template.

I'm now going to make the 8 template more slanted with extra shear and narrow its loops, with the top one shifted right, since the 8 is matching badly against 1, 2 and 9.

I'm tweaking the 8 template's top loop and bottom loop sizes and adding a bit more shear. For the 3, I'm pulling the top arc away from the left side and extending the middle cusp leftward so it differs from the 5's vertical.

I'm moving on to the 6 template now, widening its loop a bit and making the top stroke longer and more curved, with the loop centered lower. Then I'll turn to the 9, whose loop and stem might be too upright compared to real 9s.

I'm nudging the 6, 8 and 3 templates to fix the worst confusions, and I'm working through a bias correction from the predicted-class counts. The 1s are over-predicted, so the bias term should pull them back down.
