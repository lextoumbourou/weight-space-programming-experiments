Looking at the class-8 cases next: they're barely predicted, with only 69 correct out of about 108 predictions. Class 8 requires two HOLEs and forbids many other items, so I'm checking what class 2 looks like as a contrast, since it has few forbids.

I'm working out why class 8 gets mispredicted as class 2: my rule forbids the outer-notch cavities (OL and OR), but at the waist the 8 actually has those shapes, which is probably why it leans toward 2.

I'm checking whether the waist-notch cavities that my rule forbids for 8 also show up in 3, and I'm going through the cell boundaries for the proposed OL and OR points, since 3's right-waist notch might fire the same way.

I'm checking whether a slanted stroke like a '/' would also trigger the OL cavity for class 1, since class 1 forbids OL but gets sent to class 3, which requires it.

I'm now checking whether a steep slanted stroke, like the top flag and stem of a "1," would trigger the OL cavity, since the stroke's position relative to the cell tolerances would decide that. A '/' passes right of center at the upper sample and close to center at the lower one, so it probably doesn't satisfy both above and below, but a hooked "1" with a top flag and base might.

I'm now checking why class 1 gets sent to 7, 3, and 2 so often. A slanted "1" might look like a 7's stem, and its top tip may not be firing, but I also need to see whether the OL and OR cavities are showing up on a meaningful share of 1s.

I'm testing whether a steep slanted stroke could trip the OL cavity for a 1: placing the center cell four pixels left of the stroke, the right-hand probe lands on ink, but the upper probe sits about six pixels off the line, so the configuration doesn't hold.

I'm testing whether a 1 could trip the OL or OR cavity through a steep stroke, and the probes show it only satisfies two of the three required cells, so it doesn't fire. That leaves flagged or serifed 1s as the only plausible trigger, which I expect is a small share of the data. I'm now looking at why 1s would lose to 3 instead, since 3 needs two OL cells and a bottom-left tip that a plain 1 wouldn't have.

I'm checking whether a single stroke could ever fire the SLOT, HOLE, or CUP cavities, and it can't, since the crisp AND needs ink on both sides, and a lone stroke only gives one. The OL cavity still needs ink above, below, and to the right, plus empty space at the center and to the left.

I'm checking whether a vertical stroke sitting toward the right edge of a column could leave the center empty while still giving the upper cell some ink, since the 3x3 empty-window test on the center might pass even though the stroke runs through the column.

I'm checking whether a single vertical stroke grazing the right edge of a column could satisfy all three of the OL cell tests at once, since its ink would show up in the upper and lower cells and the center window could still be empty. The right-hand probe also lands on ink from the same stroke, so the whole OL pattern would fire for any vertical line.

I'm realizing the problem is that a vertical stroke at the edge of a column can make both the upper and lower ink cells fire while the center cell still reads as empty, since one cell can count as both ink and background. To fix it, I need the ink requirement above and below to sit directly over the center, so a stroke off to the side can't satisfy them.

I'm working on how to make the center ink and background checks mutually exclusive, so the cell tests can't both be satisfied by one stroke at the column edge.

I'm checking whether the center cell can be kept fully free of ink, using a strict emptiness test instead of the looser background check, so a grazing stroke can't satisfy the above, below, and center conditions at once.

I'm checking whether a strict emptiness test on the center cell would stop a grazing stroke from satisfying all the conditions at once, though it would also reject small holes like those in an 8. For holes, a single vertical stroke can't supply both side walls, so a false positive would need ink on the left as well, as with two strokes side by side.

I'm checking whether a wall-like stroke could fill the role of both the upper and lower ink cells for a 0, and the gap between a 0's two walls decides it: when the walls sit within about 7 pixels of each other, a center cell placed near one wall might let the upper and lower cells graze it, but the far side still needs its own ink. For wide 0s that isn't the case, so the pattern only fires in narrower loops.

I'm checking whether a strict emptiness test on the center cell would hold up, since it would reject the small holes a plain lenient test accepts. A middle option might be to measure ink only over the central pixels of the cell, so the upper and lower ink checks and the center check stay tied to the same columns.

I'm trying a narrower ink test for the up and down cells, limited to the center column, so a stroke off to the side can't satisfy them. The center cell's empty-space check would then stay tied to those same columns.

I'm checking whether a stroke running just beside the center could fool the up and down ink cells, and I'm limiting those tests to the central columns so a stroke off to the side can't satisfy them. Keeping the left and right checks to the middle rows would then make a single parallel stroke unable to trigger both pairs at once, though I still need to see how much the partial background term weakens the center test.

I'm checking whether a vertical stroke running through the right side of the cell could still light up the right-hand and upper cells at once. Its ink would overlap the right probe's columns, so the right-hand check would pass even though the stroke sits outside the center.

I'm settling on a sharper background test, where each window counts as empty only if none of its pixels have ink, so a single inked column in the window rules it out.

I'm checking whether a strict emptiness test on the center window can be paired with column-strip ink tests for the up and down cells, so that a stroke grazing the side can't satisfy both at once. I'm still working out whether the window's own columns overlap the strip columns closely enough to keep the two tests exclusive.

I'm checking whether splitting the ink tests into column and row strips, with a strict empty-window test at the center, keeps a single parallel stroke from satisfying both sides at once. The next step is redefining the channels so the background test is sharper.

I'm weighing a strict 3x3 emptiness test for the center against column-strip ink tests for the up and down cells, which should keep one grazing stroke from satisfying both at once. The open question is whether the saturated strip channels can fit in the few free channels I have.

I'm trying to get around capping a saturated strip signal, since a plain unsaturated strip mean drops to about 0.67 for a 2-pixel wall and weakens the AND. I'm considering a complement channel that measures absence of ink in the strip, so that the cap comes from construction instead of an extra pair of channels.

I'm weighing how to make the center-column and center-row ink tests exclusive, since a single saturated pair of channels is all I have left, and I'm still deciding which of the existing channels to repurpose.

I'm checking whether a full-3x3 saturated ink test for the up cell, paired with a lenient center emptiness test, still lets a grazing stroke through, and it looks like one column of overlap could push the up-cell signal to about 0.33.

I'm weighing a gain of about 1.5 on the full 3x3 ink test, since a grazing stroke can only reach one column of the up cell's window and would contribute roughly 0.33 at most, while a real wall above gives a clearly higher value.

I'm settling on a saturated ink measure for the up and down cells, scaled so that a grazing stroke contributes only about 0.2 while a real wall reaches full strength. That would keep one stray stroke from satisfying both sides, and I still need enough free channels to hold the two terms that produce it.

I'm settling the center-background channel: keeping it lenient and weighted toward the middle, since the saturated strip channels already stop one stray stroke from triggering both sides. I'm also checking that a steep slanted stroke can't satisfy the outer-notch test by itself.

I'm checking whether a stroke running diagonally could satisfy the up, down, and right cells at once. A vertical line near the center column would graze the up and down windows and still fall fully inside the right cell's range, so I need to see whether the grazing contribution keeps those inks from adding up.

I'm checking whether a steep slanted stroke could span the up cell's window at about 2 columns, which would push its ink signal high. I'm testing where a stroke at column 3 would sit relative to the center window and whether the slope keeps it inside the up probe's range.

I'm reworking the saturation so a stray stroke can't push the up and down cells to full strength, and that would also clear up the mistakes on 1s, 7s and 9s.

I'm checking whether the 7s picking up 0, 9 or 3 comes from the same stem-grazing false positive, since a stroke near the center column could fire OL or HOLE in a 7 and pull the vote away from the right class.

I'm checking the 4s and 7s that land on 0 and 9, which I suspect comes from the arms and stem tripping the slot and outer-notch tests. The next step is fixing the saturation so grazing strokes stop firing, then revisiting the waist notches on the 8s.

Checking the waist notch on the 8s now: the left notch center sits about four pixels above and below the top and bottom loops' left edges, with the crossing four pixels to its right. The center window should still be mostly empty, though only just.

I'm checking the 3's right waist notch next: the upper and lower arcs should both have ink nearby, with the middle bar making the center left side non-empty, so an OR detector at that spot could fire for a 3 as well.

I'm setting up the 8 template now, with an outer-left and outer-right notch at the waist, and I'm weighing whether to forbid those cells for 8s or give them only a light penalty.

I'm checking the 8's outer-notch template: the notch center sits left of the crossing, so I'd give OL and OR a moderate weight for 8s and drop the class bias to zero, since 8 has few predictions.

I'm settling the saturation numbers: with the ink channel at 3m minus 0.8 and the complement at 3m minus 1.8, the difference stays small for light grazing and reaches full strength for a real wall. I'll also require the ink input for the up cell and penalize the emptiness input, so the HOLE check depends on a wall sitting well inside the cell.

I'm checking the hole-width constraint now: with a 2-pixel grid, a 5-pixel wall gap only works if the center lands exactly on the grid, so narrower holes could slip past the detector. Wider gaps around 8 pixels leave enough room for the center to fall within tolerance, so I'm checking the 6-pixel case next.

I'm weighing whether a saturated strip test can still catch the wide zeros, since holes wider than about 11 pixels would fall outside its tolerance. Loosening the gain would recover them, but it risks letting grazing strokes back in, so I'm trading off the two.

I'm loosening the saturation to ReLU(3m − 0.6), capped at 1, so a grazing stroke gives about 0.4 while a real wall reaches full strength. Checking the outer-left and HOLE sums with that, the grazing cases still come out negative, so they stay silent.

I'm checking whether a wide zero, with walls more than about 11 pixels apart, can still fire the slot test, since the kernel only spans five cells and can't reach both sides of such a gap.

I'm estimating how wide MNIST zeros typically are, since a horizontal cross-section through a slanted zero comes out narrower than its bounding box. My guess is that most fall around 12 pixels, which is right at the edge of what the stricter saturation can span, so the zero detector may miss a good share of them.

I'm checking whether a looser saturation could be built from the existing channels, since the stricter one may miss wide zeros. A min(1, 4m) shape would need a kink at 0.25 that my current thresholds don't provide, so I'm looking at whether the mix of m, a and e can produce it.

I'm trying a looser saturation that keeps more wide zeros in range: a linear mix of the ink, the first ReLU channel and the second, S_loose = 2.5m − 0.5a − (1/3)e, which rises to 1 at about m = 0.6 and then stays flat.

I'm weighing a looser saturation for the left and right walls in the zero detector, since a linear mix of the ink channels can reach full strength at a lower threshold. Grazing strokes wouldn't create false positives for that slot test, so the looser version seems safe there, though I still need to check the hole detector.

I'm checking the horizontal case now: a loose saturation on the left and right walls would let horizontal strokes, like the bars in a 3, 5 or 2, graze a HOLE check and push its score up. So I'm keeping the up and down walls strict while the side walls can be looser.

I'm weighing whether the left and right walls for the outer-notch test should use the strict saturation or the looser one. The loose version would let a real wall register at a wider range of offsets, and a horizontal stroke above or below the cell is too far away to graze it, so I'm leaning toward loose there.

I'm settling the loose saturation for the side walls: the ink channel at 2.5m, minus half the first ReLU channel, minus a third of the second, which reaches full strength near m = 0.6 and stays flat after that. I'm keeping the up and down walls strict and using the loose form only for left and right, and I'm checking that it still hits 1.0 at high ink.

I'm picking the saturation for the side walls: a looser ink-based version works for left and right, since grazing strokes can't create false hits there. For the up and down walls I'm keeping the strict version. Next I'm revisiting the fully-connected rule weights for classes 8 and 3, including whether a small right-side notch point belongs in the 3's template.

I'm reconsidering the hole detector's thresholds for class 3 and 4, including a small notch point on the right side of the 3's template at low weight. I'm also weighing how the forbid penalty for 4 on the slot test interacts with the bottom-bar rule for 0.

I'm switching the code to the planned changes: adjusting the conv1 channels, adding the need_ink function, updating the prototype points for classes 8 and 3, and lowering the OL and OR forbid penalties for 8, with the 3's OR penalty reduced to 0.7.
