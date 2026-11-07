I'm looking at the per-class prediction counts now: classes 8 and 6 get over-predicted, while the sparse classes 5, 3 and 0 are under-predicted, with class 5 only predicted 67 times overall.

I'm weighing a middle exponent of about 0.25 for the positive weights, plus per-class biases, since the real problem is sub-shape containment that the missing-ink penalty only weakly handles.

I'm weighing whether raising the empty-cell reward from 0.08 to around 0.25 would let the emptiness channel better penalize cases like class 5 against class 6, where 6 expects ink at the left side that 5 mostly shares, while the top-left cell is where 6 expects blank and 5 has ink.

I'm comparing 5 and 6 at the coarse 4x4 level, where they overlap in several cells, so the difference comes down to only a few features like the top bar and the bottom loop. Since those differences are so small, I'll have to lean on per-class biases to fix the remaining errors, and I'm going to base those on the confusion counts.

I'm estimating a per-class bias from how far each class's prediction count sits from its true count, with class 5 needing the largest push and class 6 and 8 pulled down.

I'm weighing a moderate exponent of 0.25 along with class biases, but the scaling change is only about 10% per class, so the biases will do most of the work. Given how sensitive the results were to the earlier 20% rescaling, the logits must be fairly large, which means the bias corrections need to be applied carefully.

I'm estimating the logit scale at roughly 7 to 9, so per-class biases of 1 to 2 would matter without swamping the signal. I'm also noticing that classes 4, 9 and 7 keep confusing each other. Next I'm considering raising the empty-cell reward and the missing-ink penalty so that sparse classes are favored over dense ones when the input is sparse, starting with how class 8 expects ink in the middle columns.

I'm checking whether 5 is nearly a subset of 8 at this coarse resolution, since most of 5's ink cells also appear in 8's template, with the top bar and the lower-right part overlapping.

I'm comparing 5 and 8 cell by cell, and they overlap almost entirely, with the only real difference being the upper-right vertical in 8 that 5 lacks. Since that gap is so small, a per-class bias pushing 5 up and 8 down would fix some of the 5-to-8 confusions, though it would also start misclassifying some true 8s. Then I'm noting that 5 leaning toward 6 is another case of this same pattern.

I'm comparing 5 and 8 at the coarse grid, where the cells they occupy are nearly identical, so I'm checking whether the middle horizontal stroke, which 5 has and 8 lacks, could separate them.

I'm settling on a moderate exponent of 0.25 and raising the empty-cell reward and the missing-ink penalty a bit, so that sparse classes are favored when the input is sparse, and I'll add the per-class biases on top.

I'm settling the per-class biases at a moderate size, with the largest push going to class 5, a smaller one to class 3, and slight pulls down on classes 6 and 8. I'm also making class 2's bias smaller so it doesn't worsen the 1-to-2 confusions, and I'm turning to the 0-to-6 errors next, looking at how far class 0's ellipse extends vertically.

I'm checking how 6's loop and top curve overlap with 0's interior cells, since the curve seems to cut through the center region where 0 expects empty space.

I'm trying to explain why 0s get pulled toward 6 when the template seems like it should reject that. Real zeros look narrower than the template's ellipse, so the top arc should land in the upper-left cells, not the grid's center column. That shift would explain why 6 scores higher than it should.

I'm settling the 0-versus-6 margin with a bias shift of about 1.1, giving 0 a +0.6 boost and 6 a -0.5 cut, and I'm leaving the 4-versus-9 confusion to the biases too. I'm also nudging 9 down by 0.3 to reduce the 7-to-9 errors.

I'm raising the empty-cell reward to about 0.14 to penalize sub-shape confusions, and I'm writing the code with the new biases and exponent while keeping the rest unchanged.
