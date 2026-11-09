I'm checking why the model overpredicts the 8 so strongly: the features seem to outweigh the templates, which lets the large templates win. I'm also looking at whether the 8 template covers the diagonal channels heavily, since the 8 has a lot of diagonal content, and estimating how much horizontal and vertical strokes leak into those diagonal channels.

The fix I'm weighing is lateral inhibition: subtract the H and V responses from the D channel. Each stroke's cross-talk into D is about 0.87, which is why D fires for almost any stroke and does little to tell the digits apart. With the subtraction, a true diagonal stays positive while a horizontal stroke goes negative, though a diagonal next to an H stroke could partly cancel.

I'm weighing whether the bias term should go up, maybe to 0.45, since 8 wins for most inputs and 3 wins for many 3s and 5s. I'm also considering a cosine-style score with normalized templates, which would be scale-invariant and drop the need for m.

I'm weighing a cosine-style score: dividing each template's response by its norm so the comparison is scale-free and needs no m. If x equals a template exactly, its own score is the largest, since a subset template can't beat its superset by Cauchy-Schwarz, so normalizing looks safe.

I'm settling on a cosine-style score: normalize each template by its weighted norm so the comparison is scale-free and needs no m. I'll start with bias 0 and a scale around 1.5, then tune per-class offsets from the confusion matrix, where 5s are being pulled toward 3 and 1s and 7s are leaking into other digits.

I'm checking whether the mutual inhibition between the diagonal and horizontal/vertical channels is worth adding, since a diagonal only crosses the H and V bands in one or two cells, so its leakage there should stay small, roughly 0.1 to 0.2. I'll add a light inhibition of about −0.15 on those channels.

I'm checking whether horizontal strokes leak into the diagonal channel on both taps, which would make them act like side walls for the left and right detectors. That would give the L strip about 1.0 from a plain horizontal stroke, and the vertical strokes would do the same for the up and down detectors.

I'm checking the wall terms in the left-right detector: a horizontal stroke leaking into the diagonal channels gives the left strip about 1.0 on its own, and if the stroke stops short of the center, the right wall can add enough to push the score falsely positive. My proposed fix is to subtract the horizontal response from the wall term, using the vertical strokes plus a weighted diagonal contribution minus a constant offset.

I'm checking the wall terms for the left-right and up-down detectors: a horizontal stroke leaks into the diagonal channels and would give false wall responses, so I'm looking at subtracting the H and V responses from the wall term to cancel that leakage.

I'm checking the diagonal inhibition weights next: subtracting about 0.28 per tap from the H and V cross-talk should keep a true diagonal positive while pushing horizontal strokes negative.

I'm adjusting the diagonal channel so a horizontal stroke ends up negative while a true diagonal stays positive, and I'm settling on a cosine-style score with a bias of zero and scale around 1.5. I'll tune per-class offsets from the confusion matrix afterward.

I'm finishing the classifier code now, keeping the bias at zero as planned and applying the same changes as before.
