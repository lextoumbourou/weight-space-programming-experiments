I'm checking the progress at 78.95% and listing the row recalls for each digit. Next I'm working through the column sums, starting with column 0 and column 1.

Now I'm working through the column sums and the big flows between digits, checking which transitions carry the most counts. I'm starting to weigh the 3→5 flow of 119 against its per-class ideas.

I'm weighing the 3→5 flow of 119 against the bay detector's response: 5s fire it at the upper rows, and 3s fire it too at k=1, between the arms on the right of the middle vertex.

I'm weighing the 3→5 flow against the bay detector again, and the trouble is that both a 3 and a 5 land on the same bay position. The difference has to come from the left-side bay: 3s seem to fire it weakly, 5s fire it negatively, so the net sign separates them only slightly. I'm considering a compromise weight setting for both digits, a step between the two earlier tested values.

I'm adjusting the bias terms to fix the 3→5 confusion: the 5 weight is over-predicted (1119 vs 915 actual) and the 3 weight is under-predicted (972 vs 1030 actual), so I'm nudging 5 down and 3 up.

I'm nudging the 3 and 5 biases a bit more: 5 down to about −0.48 from −0.52 and 3 holds steady. Then I'm turning to the 4→9 confusion, which is the biggest persistent flow: 136 of the 652 4s are read as 9s, plus sizable leaks into 8, 6 and 2. I'm raising the bias for 4 from +0.40 to about +0.5, and I'm wondering whether my 4 template's geometry is simply off compared with how 4s actually look in MNIST.

I'm comparing the 4 template against the 9 template: both have a left vertical and a lower crossbar, and they differ mainly in the top closure at row 7 and in how the crossbar and right stroke end. Since 4s are wide, with the left stroke near x≈7–8 and the right vertical near x≈16–17, I'm checking whether those positions actually match how 4s are drawn.

I'm looking at why 4s get read as 9s: the two templates share a left vertical and a lower crossbar, and the main difference is the closed top of a 9. Many handwritten 4s have converging tops, so the hole or top detector may be firing on them, and I'm wondering how to separate the two from the top shape.

I'm now comparing the crossbar's shape against the 9's loop bottom, since the 4's crossbar runs straight past the stem to the right while the 9's loop curves back in.

I'm thinking about whether a cross-shaped detector could tell a 4 from a 9: a 4's crossbar runs straight through the stem and out to the right, while a 9's loop bottom stops at the stem.

I'm sketching a "right spur" detector to tell a 4's crossbar, which runs past the stem to the right, from a 9's loop bottom, which stops at the stem. I'm weighing whether to check the ink two or three cells to the right of the stem at crossbar level, since the extension is often short.

I'm considering whether a cross-shaped detector could work: the rest of the stem's ink wouldn't distinguish a 4's crossbar from a 9's loop bottom without a precise spur test. I'm leaning toward skipping that and instead looking at whether the open top of the 4's bay can separate the two.

I'm checking whether a closed top on a 4 would make the hole detector fire mid-interior while the bay detector stays silent, since the upper ink would block it. If the top is closed, a 4 could look like a 9 on those two channels, so I can't separate them from the top structure alone.

I'm weighing whether the 4→9 confusion comes from closed or converging tops on handwritten 4s, which would make the top hole detector fire where it shouldn't. I'm settling on a small bias bump for 4 and leaving the rest of the geometry alone. The 4→2 leak looks tied to the corner detector firing lower on the left side, so I'm checking that next.

I'm now checking the 7 confusions: 7s are misread as 9s and 5s, and the 7 bias sits at +0.66. I'm wondering why the 7→5 leak persists, since the bar-and-stem region that would fire the left bay detector should push against a 5, so those 7s must be getting to 5 some other way.

I'm asking why 7s would be read as 5s, and my guess is the serif tick at the bar's left end looks like a 5's upper-left vertical. Checking the 5's bay test, it needs a wall on the left, the bar above, and the bowl below with the right side open, so the 7's tick and bar could partly match that pattern.

I'm checking whether the 5 bay detector separates 7s from 5s, since 5s need a bottom arc across the lower rows that 7s don't have.

I'm settling on a bias shift for the 5 class: since 5s need a bottom arc that 7s and 9s lack, I'm considering a positive weight on the bottom horizontal region for 5, paired with a lower bias to balance it. The balance looks delicate, so I'll need to check it against the real 5 responses.

I'm looking at a possible bias trick for the 5 class: adding a positive weight on the bottom arc features and offsetting it with a lower bias, so that true 5s stay roughly neutral while images without the arc are pushed down. I'm weighing whether 9s with curled tails would also get pulled toward 5, since the 3s share the same bottom arc and this won't help with 3→5.

I'm working out the bottom-arc requirement for the 5 class: at row 7 of the grid, a window of about 0.4 weight over three cells gives roughly 0.8 for true 5s, so I'm setting the offset near 0.6 to keep them neutral. Images without that arc, like 7s and straight-tailed 9s, would then be pushed down.

I'm weighing whether the 5 bias trick is worth it: a bottom-arc weight would help with 7→5 and 9→5, but it could cost real 5s with weak bottoms. I'm leaning toward a modest version, and I'm also thinking about whether a more targeted approach would do better than this.

I'm now looking at the 8 false positives, which total around 270 across 0, 2, 3, 4 and 5, and the 8 bias barely moves the predictions. That suggests the extra 8 predictions come from the image features themselves, likely the hole detector firing on those digits, so I'm checking which images are triggering it.

I'm weighing a bias cut for class 8, since its extra predictions likely come from the hole detector firing on 0s, 2s, 3s, 4s and 5s. A "two holes required" rule would need a lower bias, but that risks losing 8s whose loops aren't detected, so I'm leaning away from it.

I'm weighing whether to lower 8's hole weights, but the 0→8 confusions don't seem to come from the hole detector at the center, since 0s fire the holes at k=1 and 2 and the relative balance still looks fine. The 0→8 errors probably come from the template matching narrow, tilted 0s whose diagonal strokes resemble 8's, so a weight change won't fix them cleanly. I'm settling on a simple bias shift for class 8 instead, lowering it by 0.1.

I'm considering a few other ways to improve the template matching, such as adding variants for digits like 4, 7, 9, and 2 that have different stroke shapes, since a variant helped with the 1s earlier.

I'm now going to look at the 0 class, which has the most varied shapes: narrow tilted ovals get confused with 8s, 2s and 6s. I'm considering adding a narrower, tilted 0 variant alongside the current round template so the fit covers both shapes.

I'm thinking about adding a serif tick variant to the 7 template, a short stroke at the upper left of the bar, so that 7s with ticks get credit for it and stop being penalized there. I'm also considering a curled-tail variant for 9s.

I'm thinking about the 9 template: adding a curled-tail stroke at the bottom might give 9s some of the bottom-arc evidence that 5s and 3s have, which could cut the 9→5 and 9→3 errors, though it may pull 5s and 3s toward 9 in return. For 2s, the bottom-loop variant and the curvy base are on my list, but the 2→0 confusions may just be looped 2s, so I'll probably skip that one. The 3→8 errors are harder to pin down, and I'm not sure how to address the 6→0 ones yet.

I'm now looking at the 6→0 confusions, which total 79. My working guess is that 6s with large loops and short tops get read as 0s, and the difference should show up in the upper right region, where a 0 has a diagonal stroke and a 6 has nothing. Adding a dedicated channel for that would take more features than I have.

I'm now tuning the class biases with a damped update, since the sensitivity is low at this point. The adjustments for classes 0 through 4 are small, with class 3 getting the largest cut.

I'm recalculating the bias updates for each class, with the largest moves on 4, 7 and 8. I'm also weighing three template variants, for 0, 7 and 9, to see whether they help.

I'm weighing whether a broader 0 template would pull in more 6s, 2s and 9s, and I'm thinking about offsetting that with a small bias cut. The narrow, tilted 0 variant worries me, since its strokes run near the center like an 8's diagonal or a slanted 1, so I'm wondering whether the hole structure would keep it apart.

I'm considering a narrow, tilted 0 variant at a low weight, and I'm leaving the 3 and 5 bias adjustments to handle the BayR confusion. For the 2→8 errors, I'm thinking about raising 8's hole weight in the lower region so that it fires more strongly on 2s' loops.

I'm weighing the last few tweaks: a small bias bump for class 1, since 1→2, 1→7 and 1→4 confusions are sizable, and wondering why 4 draws 1s at all. I'm also checking whether scaling the logits would help the loss, though I can't tell yet whether the model is under- or over-confident.

I'm settling the 0 class with three ellipse variants: the existing round one, a narrow tilted one, and a round upright one, each at its own weight. Since the template function applies a single slant to every stroke, I'll precompute the slanted points for each ellipse and pass zero slant.

I'm adding a serif tick to the 7 template and a curled tail stroke to the 9 template, each at a low weight so they nudge the fit without dominating it.
