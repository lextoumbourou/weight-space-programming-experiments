Accuracy is at 38.65% with loss 4.24, so progress is slow. The 7 class is still failing badly, with only 7 correct and most predicted as 1, 5, and 9. My new 7 template made things worse, dropping from 31 correct to 7, so the diagonal template hurt and I'm considering reverting it. The 9s are mostly being called 4, and the 8s are landing on 2.

The 7 template change backfired: accuracy on 7 fell from 31 to 7, and 7 is now under-predicted, with only 199 predictions. The 1, 2, 4 and 9 classes are over-predicted, and the diagonal template seems to pull toward 1 and 9. Reverting 7 to the earlier version looks worth trying, though that one was also weak, so 7 may just be hard to capture with this template.

I'm weighing whether 7's top bar should count for more and 1's vertical stroke for less, though 1 sometimes has a top serif that muddies that. Since further template tweaking seems to be giving diminishing returns, I'm starting to consider whether it's worth investing in a different approach.

I'm weighing whether the architecture itself needs changing. Right now only one conv1 channel carries ink, and the fc layer's 256 inputs are all spent on ink-offset features, so any orientation detector would mean giving some of those up. Splitting the conv2 channels between spatial ink offsets and orientation features might help with 7's diagonal and 1's vertical stroke, but hand-designing those weights is risky.

I'm considering whether a sharper, full-resolution ink map would beat the blurred version I'm using now, since the 3x3 averaging and pooling may be smearing away the distinctions that separate 7 from 1 and 8 from 2.

I'm thinking about swapping the 3x3 averaging for a single-pixel delta in conv1, so each pooled value would just say whether any ink sits there, giving a sharper, binary-style 12x12 map. Whether that sharper silhouette separates 7 from 1 better than the blur does is the open question.

I'm going to keep refining the templates and bias for a few more steps since those are cheap and low-risk, focusing on 7, 8, and 9. I'll revert the 7 template, and if accuracy still plateaus after that, I'll look at orientation features.

I'm going to try a different 7 template: a strong top bar with the stroke coming down from the right end, so it doesn't line up with 1's central vertical or 9's loop.

Still sketching the 7 template: a thick top bar across the first two rows, then a short diagonal dropping down-left. The aim is a bar that 1 and 9 don't share, though the 9's top loop might still look similar from a distance.

I'm settling on a plan to add orientation channels to the conv layers: a horizontal-bar detector, a vertical-bar detector, and possibly diagonals, alongside the existing ink density. I'd keep most of the spatial offsets for the ink map and reserve a few conv2 channels for orientation summaries, such as horizontal-edge density in the upper region.

I'm weighing whether to add orientation channels, but a full redesign feels too risky at this stage. For now I'll keep the architecture and focus on refining the 7, 8, and 9 templates and the bias, since the spatial approach still has room to improve from 38%.

I'm going back to the 7 template to fix the overlap with 1 and 9. The idea is to put the ink on the top bar and the diagonal toward the bottom-center, and leave the mid-left empty, since that's where the 9s put their loop. I'll sketch a clean version directly.

Still sketching the 7 template as a grid, with a thick top bar and a diagonal stroke dropping down-left toward the bottom-center.

I'm checking the 7 template against the others: the thick top bar should separate it from 9's loop, but the diagonal runs through the same center-right columns as 1's vertical stroke and 9's tail, so some overlap remains. I'll rely on the bar as the main discriminator, and I'm also going to look at how 1's serif affects that.

Re-tuning the biases from the last pass' prediction counts: digit 0 is under-predicted so its bias goes up, while digit 1 is over-predicted and needs a sizeable cut.

Now I'm recalculating the biases from the last prediction counts, with digits 5 and 6 pushed up and 4 pulled down.

Bumping the bias for 7 makes sense given its near-zero recall, and I'm weighing whether a better template plus that boost nets out positive. The 8-versus-2 confusion is next on the list, and I'm comparing their top loops.

Still refining the 7 template as a thick top bar with a diagonal down-left. Also using bias 4's sharp cut to ease the 9→4 confusion. Next I'll write out the updated template and biases.

Checking the row widths of the new 7 template: each row I've verified so far comes to exactly 12 characters, so the grid is well-formed. Writing the 7 template out.
