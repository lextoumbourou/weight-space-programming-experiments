The first accuracy is about 74%, but the loss of 1.53 looks high. My guess is the logits are too flat, with small differences between classes, so I'll try doubling GAIN to 6 and see what changes. I'm also seeing that class 0 is often predicted as 6, and class 8 gets over-predicted from several others.

I'm weighing a few fixes for the over-predicted 8s: penalizing end-channel energy more strongly for 8 and 0, since 8 has no ends. For the 0→6 confusion, I think 0 needs a bigger penalty for ink in its empty center, which I could add as a manual extra penalty in the center cells.

I'm thinking about the 1s that are written with a slant. Their diagonal stroke overlaps with the diagonal of 2 and 8, which explains those confusions. One option is to add a second, more slanted stroke to the 1 template, weighted at about half, so that it covers those variants.

Now I'm weighing whether 9 is being mistaken for 6 because the 6 template is over-predicted in general, given how many other classes are being pulled toward it.

I'm now raising the BETA penalty to 0.07 for bar channels and 0.12 for end channels, and bumping GAIN to 5, since the 6 template gets over-predicted and has few penalties. I'm also checking whether 9s with an open loop are being pulled toward the 7 template, which has an end facing left at the top.

I'm settling on a few concrete changes: raising the gain to 5, setting the bar penalty to 0.07 and the end penalty to 0.12, and giving the 1 template a slanted variant. I'm also checking whether the empty center of the 0 template is wide enough that its ink windows stay clear of the ellipse sides.

I'm checking how the 0 template's center cells respond to horizontal energy in the middle rows. Its side strokes sit far enough away that the middle horizontal band should count as unexpected, so raising the bar penalty there should suppress the 6-like loop.
