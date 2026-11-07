Accuracy sits at 47.5%, which is a reasonable starting point. The confusion counts show the model guessing "1" far too often, over 3000 times, mostly on 8s, 6s, 5s and 2s, and it over-predicts "7" as well.

Now I'm weighing whether to normalize each template by a fixed weight per cell instead of equalizing total weight, since sparse digits like 1, 7 and 4 are reaching their maximum on just a few features shared with other digits.

Now I'm considering stronger negative weights for the sparse digits, since a 1 template with few cells can still fire on an 8 through its center column, and I'm thinking of spreading a larger negative total across the many empty cells so stray ink actually pulls the logit down.

Now I'm considering a fixed per-cell negative weight, around -0.3 for each empty cell, instead of normalizing it. That would make a stray 8 in a 1's empty cells pull the logit down a lot, and the same reasoning covers the empty center cells for 0.

Now I'm checking whether an 8 can fool the 1 template: the 1's ink sits in the center columns, and the 8's template covers those same cells at the top, middle and bottom rows, so its positive weights would fire too. The separation has to come from the orientation channels, since the 8's horizontals at the top and bottom center are missing from a bare 1.

I'm checking whether a 7 could also trip the 1 template: its diagonal runs through the center cells, so some of its ink lands where the 1 expects it, though the 7's top bar falls outside the 1's cells and should keep the score down.

Weighing a fixed per-unit positive weight against stronger per-cell negatives for the sparse digits, to see whether a 7 can still beat a 1 on its diagonal channel.

I'm checking whether an 8 could beat a 3 on the template score: 3's ink sits inside the 8's right side and center, so the 8's template fires on part of it, but the 3's own template is a bit smaller and should match it fully, so the two scores come out close.

I'm weighing whether an 8 could beat a 3 through the orientation channels, since the 8's left-side verticals and diagonals aren't there for a 3. A plain ink-based negative doesn't cover that, so I'm considering penalizing orientations that a template expects but that never show up in a cell.

I'm considering a conv1 "empty" channel that fires where the input is blank, so that a 3 gets rewarded for its empty left side while an 8 gets nothing there because it expects ink. That would tilt the comparison toward the 3 without relying only on the missing ink.

I'm weighing a conv1 "empty" channel that rewards blank regions, since it could favor a 3's empty left side over an 8, but its max-pooled response may still fire partially on an 8's strokes.

I'm working out a conv1 "empty" channel with weights of -0.2 over a 5x5 patch and a bias of 1.2, so a fully blank patch fires near 1.2 while a patch crossed by a stroke goes to zero. Max pooling over the cell's patch positions would keep it firing unless the stroke fills the whole region, which makes it a weak but useful signal alongside the negative ink weights.

Now I'm settling on the mechanics: each cell gets a fixed positive weight per unit rather than normalized totals, and I'm looking at whether an "empty" channel can reward blank regions without firing on stray strokes.

I'm running the same comparison with fixed per-unit weights: a 1 template comes out around 6.4 on its own ink, while an 8 on an 8 input would score roughly 27, and an 8 on a 1 input lands near 8, which is still under the 1's own score of 12.

I'm settling on the weights now: a smaller fixed positive value per unit and a larger negative penalty for empty cells, which keeps the 8's logit from overwhelming the others. The 1 still wins by a few points on a 1, and on an 8 its own negatives push it far below zero. Since the logits get large, I'm thinking of scaling them down and adding a per-class bias to balance things out.

I'm weighing a middle ground where each class's positive weight scales with the square root of its template size, so small templates like 1, 7 and 4 aren't drowned out by dense ones. Negative weights would stay fixed per empty cell, though that could penalize a 1 heavily for any stray ink, like a slanted stroke or a base.

I'm sketching a slanted variant of the 1 template, so a stroke running diagonally from the lower left to the upper right isn't penalized as stray ink. Layering a vertical and a slanted 1 into one template would widen its coverage, with the slanted version weighted lower.

Now I'm settling the 1-template layout with a slight slant, so the stroke runs from the lower left to the upper right. I'm leaving the biases near zero, since the earlier over-prediction of 1, 7 and 4 came from the normalization I'm replacing. For the empty channel, I'm weighing a fixed weight per empty cell against the ink, so dense digits with fewer empty cells don't get an unfair edge.

Now I'm weighing the empty channel's reward against the fixed negative weights: a sparse class like 1 collects a lot of emptiness credit on inputs with blank regions, which helps separate it from denser digits like 8. The bigger effect comes from classes whose empty cells sit where another digit has ink, since those cells only contribute when the input is actually blank there.

I'm settling the empty-channel magnitudes: a weight of -0.25 with a bias of 1.5, so a fully blank patch fires at 1.5 and a patch with six inked pixels drops to zero, with a two-pixel edge still giving around 1.0.

I'm settling on per-class positive weights that scale with the inverse square root of each template's total mass, so the sparse 1 doesn't get swamped. For the 1 that comes out to about 0.07 per unit, and for the 8 about 0.04.

Now I'm checking the negative weights: at 0.12 per empty cell, a 1 on an 8 input takes about -7.7, but a 0 on an 8 only drops to around 6, which still sits close to the 8's own score. Adding an empty-cell reward of 1.5 per unit would give the 0 a bonus only where its center stays blank, and an 8 input fills that center, so the 0 gets nothing there.

I'm weighing the empty-channel reward at about 0.08 per cell and checking whether sparse digits gain too much from blank regions on every input. I'll keep it in and watch how it shifts the 9 versus 4 and 9 versus 7 confusions, since the loop at the top of the 9 template may need a shift too.

I'm checking the 9 against the 4: the 4's right vertical and crossbar line up with the 9's loop bottom and right side, and the 4 mostly sits inside the 9's ink except for the top horizontal of the loop. Since the 9 template fires fully on a 9, the weighting should still favor the 9.

I'm checking the 4 against the 9 in more detail: the 4 seems to expect empty space in spots where the 9's loop side is inked, which should push its logit down on a 9. I'm also looking at the 7 next to the 9, where the 7 expects blank cells in the upper middle that the 9's loop side fills, so that should work against the 7 on a 9 input.

I'm checking the confusions involving 3 and 6: the 3's template is weak, so its classes keep getting picked over it, and the 6 seems to fire on 1 mainly through its curved top stroke, which the 1 template only partly covers.

Lowering the positive weight scale from 3.0 to 2.5 should keep the full-match logits in the 8–10 range and temper the confident errors behind the 2.16 loss. I'm leaving the biases at zero, since the sqrt normalization already gives the denser 8, 9, 5 and 3 templates a fairer share.

Now I'm settling on a softer orientation filter: positive weights summing to 5 and negative flank weights summing to -3, so a thick vertical stroke still yields a clear positive response instead of canceling to zero, with a small bias of -0.3.

I'm settling the orientation filter with a softer shape: negative flank weights summing to -3.0 and a bias of -0.5, so a thick stroke still gives a clear response of about 1.5 rather than canceling out, while an ideal thin stroke reaches about 4.5.

Writing the convolution code now, with the orientation filter and the empty-cell channel wired into the template scoring...

Still writing the convolution weights...

Still settling the empty-cell weights: a 1 template's emptiness penalty lands at about 0.3 in either grid, which I'll accept. I'm keeping the scale factor at 2.5 for the cross-entropy.
