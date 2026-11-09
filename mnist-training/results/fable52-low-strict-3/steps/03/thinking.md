Accuracy held steady while the loss dropped, but the errors now lean toward predicting 5 too often. Looking at the 5 template, it has many end points from its corners, so it may be collecting fewer end penalties, and 9 gets pulled toward 5 because the two share a top stroke.

I'm comparing the 9 and 5 templates: they share most coarse features, and the differences lie in the upper-right stroke, the bottom bar, and the end direction. I'm also wondering whether the penalty for 5 rarely fires because the window overlap pushes template values above τ, and whether raising τ to 0.25 would help. Then I'm weighing whether a discriminative weighting could work without being a disallowed discriminant analysis. For the 0→6 errors, I'm considering whether slanted real 0s produce diagonal energy that looks like a 6.

I'm checking whether real 0s, which are often slanted and wide, produce diagonal strokes that resemble a 6. I'm also questioning whether the 0 template is getting penalized for ink in the middle rows, and whether the end detectors are firing where they shouldn't.

I'm wondering whether the 0 template is failing because real 0s are slanted, which would add diagonal energy that resembles a 6. The penalty for end cells, applied across most of the 0 template, might also be firing on curve regions, though the errors persisted even with a weak penalty, so the mismatch may come from how the template itself is shaped.

I'm checking whether the 0 template is misaligned with real 0s, which tend to be slanted, so their diagonal strokes might resemble the 6's upper stroke. The 6 template lacks the top-right arc that a 0 would usually have, which should count against it, so the confusion is puzzling.

I'm checking whether the edge detectors respond to the slightly curved or steeply diagonal strokes in real 0s, since a thin stroke tilted about 20° from vertical might shift enough to trip the vertical-edge response.

I'm checking whether the 0 template fails because real 0s carry too much bar energy in the center, and considering a hand-tuned penalty on center ink to separate them from 6s.

I'm now considering a sharp center-ink channel, one that sums all bar energy with tight cells, to catch the empty hole a real 0 has and that the coarse soft cells miss.

I'm weighing a sharp total-energy channel that sums the four bar channels at the center tap, with negative weight on the central cells for the 0 template so that the empty hole of a real 0 gets rewarded. The small center cells only see stroke energy from a narrow margin, so the penalty would be linear and may be too weak for narrow 0s, but it's a simple hand-tuned feature to try.

I'm weighing whether to add positive weight on the central ink energy for 0s, since a penalty alone would only push down the 0 score, while the 0→6 errors need the 0 template to rise for 0 images relative to 6.

I'm considering a bias term for class 0 that rewards an empty center, with negative weights on the central ink so that digits with energy there score lower. I'll set the penalty and bias to rough values like k=1.0 and B=1.5, though narrow 0s could lose out. I'm also wondering whether a similar hand-set scheme over a sharp total-energy map might work more broadly.

I'm going to add a sharp total-energy channel to the template, rendering the stroke energy with a tight window and saturating it at 1. Its penalty weight would be larger than the soft channels' and applied wherever the template is empty.

Now I'm comparing the 3 and 5 templates: the upper-right and upper-left vertical strokes sit in different grid columns, so the window overlap shouldn't fully hide that, which makes the 3→5 confusion (396 errors) hard to explain from the top alone.

I'm now looking at the 3 and 5 templates, which share a top bar and a middle stroke, so the main difference should be where the upper vertical sits. The 5 template's end and corner entries overlap with what a 3 would produce on the left side, so 3 images may match 5 through those shared cells. I'm wondering whether the new sharp ink channel will separate the upper-left region, where 5 has ink that a 3 doesn't.

I'm going over the 5 template's corner marks and considering trimming their weights, since they may be drawing 3s toward 5. I'm also noting that the sharp ink cells should penalize 9s for 5s in the upper-right region. The 9 template itself might be weak, since its small loop gives little bar response, so I'm checking its shape against real 9s.

I'm weighing a bias term for the 0 template that rewards empty center cells, and I'm checking whether the ring cells in the upper right of a 0 would line up with the 6 template's expected ink there.

I'm weighing a modest ink-channel weight of around 0.7 for the template, since the normalisation should keep its contribution comparable to the bar channels.

I'm setting the ink channel's weight in the template to 0.5 so its real-stroke values come out near 0.6, and I'm holding the penalty steady at the same level with a slightly higher one for ink. Saturating the template's sharp channel at 1 keeps near-full stroke crossings at the top of the range.

I'm noticing 6 and 9 are both being over-predicted as 4, with 9→4 errors hinting that the sharp top-edge ink should penalize 4 wherever 9 has its top arc. Going ahead with the change.
