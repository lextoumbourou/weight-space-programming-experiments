The model is at 59.5% and the gain is marginal. Class 1 is still over-predicted, at 1813 predictions, even after the bias change. Most of the misfires are other digits being called 1, especially 8s. I want to know why 8s would be pulled toward 1.

I'm checking whether 8s would actually get penalized by the 1's side-column rule. Their side strokes should land in those cells, so on paper the penalty looks large enough to rule them out. I suspect the 1 wins when every class scores poorly on an unusual 8, because the 1 has a large emptiness reward and few expected cells.

I'm considering a class-specific boost to the penalty for ink in the side columns when the class is 1. I'm also weighing whether to lower the emptiness reward and raise the side-column penalty across all classes, which would mean adjusting the biases to offset the shift for sparse classes.

I'm working out the bias offsets for the compensation. Sparse classes like 1, 7 and 4 lose about 1.3 from the emptiness change, dense ones about 0.4, so the net shift favors 1 and 7, which is what I want. Class 4 is already balanced, so it needs roughly +0.6 back, and I'm also noting that 2, 9 and 6 are a bit under-predicted.

Checking the per-class error counts, I'm noticing that 8s are getting confused with 2s and 1s in both directions, so the issue looks like the 8 template itself rather than one bad penalty. I'm also thinking about whether a structural change to the features would help more than further tuning the biases, though I haven't settled on one yet.

I'm now looking at which digits the errors fall on. The 3-vs-5 confusion runs in both directions, so I'm checking whether the top-left stroke is what separates them.

I'm checking the 3-vs-5 case next: 5 lacks the upper-right stroke that 3 has, so the side-column penalties should separate them, and the bias gap already nudges things toward 3. For 9 versus 7, the loop's left side should cost 7 about -2.5 in penalties, but 9 still loses 212 cases to 7, so I'm wondering whether 9's own template score is the weak point.

I'm checking the center-of-mass shift for the 9 template: the loop and tail should put its center near x=1.97, but the digit needs it at 2.5, so the +0.5 offset may be too small.

I'm checking whether the 9's tail really puts its center of mass at the right place, which would mean the shift of about +0.5 is correct. The digit's extent of roughly 0.7 to 5.3 still fits the 28x28 frame, so the placement looks fine if the loop-to-tail mass ratio holds for real 9s. The next step I'm turning to is strengthening the penalty for the 1 class.

I'm testing whether the 1 template fires on 8s through its side-column penalty, working through the expected penalty for an 8's side strokes. Then I'm wondering whether the 8s are narrow enough to dodge those cells, and I'm considering that a fallback effect may be at play, where the 1 wins when everything else scores poorly.

I'm now checking whether narrow 8s slip past the 1's side-column penalties, since at this grid resolution their strokes can fall between the cells I expect to be empty, so the 1 template ends up looking like a plausible match.

I'm going to add a horizontal-channel penalty for the 1 class, so that digits with horizontal strokes in the center column get pushed down, since a 1 should only have vertical ink there.

I'm weighing a horizontal-stroke penalty for the 1 class, since a 1 should only have vertical ink in its center column while narrow 8s would show horizontals there. For the 7 class, I'm considering similar horizontal penalties in the middle region, to counter 9s whose loop bottom would otherwise match.

I'm weighing a few smaller tweaks now: nudging the biases for 6, 2 and 9 up and for 1, 7 and 8 down, shifting 3 slightly above 5, and trimming the emptiness and negative weights a bit while leaving the 1 and 7 compensation intact.

I'm adjusting the bias offsets now: the dense classes get a small boost to offset the emptiness change, class 4 gets a larger one, and class 1 gets a slight cut, with a couple of per-class nudges layered on top.

I'm settling the final bias values: the dense classes get a small boost to offset the emptiness change, class 4 gets a larger one, and class 1 and 7 come down slightly. I'm also deciding to make many of these changes at once, since time is limited.
