The stricter features made things worse, with sparse-template classes favored and class 8 collapsing, so I'll revert the threshold to 0.6. Lowering it to 0.4 might help, but I'm not sure it's worth the extra saturation, so I'll keep 0.6 and look for gains elsewhere, since the results have plateaued.

I'm weighing whether to add a second set of orientation features on a shifted grid, plus loop and corner shapes, and I'm considering using the conv2 channels in a graded way where the feature values scale down to about [0, 1]. I'm now sketching out what the 16 features could be, with end-stop features as one option.

I'm sketching out endpoint features now, since stroke ends separate several digit pairs: a vertical end at the top, a bottom end, and horizontal ends each get a template that is positive at the center and negative around the continuation. The templates would need guessed probabilities, so I'll check whether the idea is worth the effort before committing to it. I'm also weighing a shifted orientation grid, though it would double-count correlated features and need the log-likelihood weights adjusted.

I'm now checking which digit pairs the endpoint idea would separate, starting with 6 versus 0 and 9 versus 0, since 6 has a stem end at the top and 9 at the bottom while 0 has none. The pairs 5 versus 6 and 3 versus 5 look like they hinge on which corners the strokes end at.

Endpoint detectors look like the strongest lead, since stroke ends separate most of the confusable pairs. I'm now sketching how the up-end detector would respond to ink below a point and none above it.

I'm working out a concrete up-end detector: it scores high when there's ink at the center and just below, and gets penalized for ink above. The weights are rough guesses, so I'll check how it responds on a stroke that ends versus one that continues.

I'm checking how the up-end detector behaves: on a vertical stroke's middle it cancels out, but at the top end it fires strongly. A horizontal arc at the top of a loop gives only a weak response, since nothing sits below it.

I'm settling on a threshold of 1.2 for the up-end detector, so it only fires when there's ink both at the center and directly below. I'll add small weights on the cells beside that one, and I'm checking whether a corner or a horizontal stroke can still trigger it by accident.

I'm sketching the endpoint detectors more concretely now, with the up-end case as the example. For each digit I'm noting where a stroke stops, though I'm still unsure how to phrase the direction of a curling start like the one in 2.

I'm working through which digits have stroke ends at which positions, checking 2 and 3 in particular, since their start and end points differ in direction and location.

I'm defining four endpoint detectors, one for each direction a stroke can stop, and I'm sizing each one by where the continuing stroke sits relative to the endpoint. For 3's bottom end, the stroke runs down-right from the endpoint, so it partly triggers both the up-end and left-end detectors, and the diagonal cell only contributes a small amount.

I'm defining the endpoint detectors by the direction the continuing stroke lies in, starting with the top-end detector: it gets a strong weight on the cell just below and smaller weights on the diagonal cells beside it, with opposite-side cells negative. I'm checking which digits have a top endpoint, and so far that's 1, the two tops of 4, and the top of 6, while 9, 7, 5, 2, 3, 8 and 0 don't have one there.

I'm working out which digits have a stroke end pointing down and which pointing right, along with the bottom endpoints of 1, 4, 7 and 9, and I'm treating the start of 2 and the top-left start of 3 as partial matches for the bottom and right-facing detectors.

I'm narrowing the endpoint idea to the four most separating detectors, with the right-facing and left-facing ends being the ones that tell the remaining digit pairs apart.

I'm weighing whether to keep the orientation features clipped, since unclipped ones would overcount on thick strokes. The endpoint detectors would need 5 slots, which doesn't fit alongside the loop feature, so I'm considering dropping the loop or using unclipped single-channel features to reach 16.

I'm settling the loop and endpoint features to fit the 16-slot budget: the loop and small-loop features stay unclipped with a gain of 2, and I'm writing the endpoint detector for a top endpoint, which only needs ink below it, weighted at 0.4 on each of the two cells below and a small base offset.

Still working out the top-endpoint detector, weighting the cells below the endpoint and penalizing the sideways and upper ones, to see how strongly it fires on a vertical stroke's top.

I'm checking the top-endpoint detector against a horizontal stroke's topmost point, where the ink sitting directly below it is what decides whether it fires.

I'm checking the endpoint detector on a diagonal stroke end, like the bottom of 7's stem, where the continuation runs up and to the right, and I'm weighing how much the diagonal cells should count against the straight-down ones.

I'm sketching the endpoint templates for the top-end direction, giving weight to the stroke ends for 1, 4, and 6 and leaving 9 and 3 near zero. Then I'll rotate that same pattern to cover the other three directions.

I'm placing the endpoint detectors' target weights for each digit, with the bottom-end detector covering 1, 4, 7 and 9 most strongly and 2 and 3 only partially.

I'm setting the endpoint templates' peak weights for each digit, then laying out the channel map: the loop and small-loop features, the four endpoint detectors, and the remaining slots left empty. The orientation features will be paired differences, while the parts stay single-channel, and I'm keeping the prior correction as it was.

I'm defining the endpoint detectors by rotating one base weight map: the top-end pattern gets flipped for the bottom ends, transposed for the right-facing ends, and mirrored again for the left-facing ones.

Writing the endpoint detector code now...
