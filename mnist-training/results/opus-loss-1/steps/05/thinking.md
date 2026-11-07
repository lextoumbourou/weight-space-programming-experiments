I'm stuck on slow progress, so I want to rethink the feature design for better discrimination. One thought is to use the unused conv1 and conv2 channels, and another is that the conv2 averaged and centre features may repeat the same orientation information, so finer spatial resolution might matter more.

I'm weighing whether a learned fc layer would beat my hand templates, since the templates sit around 69% against a likely ~95% for a trained linear classifier. Without much feedback data, I'm considering features that are more discriminative by design, like a ring detector in conv2 that fires when horizontal and vertical strokes sit at the right relative positions around a loop.

I'm comparing loop-shaped features against the confusion pairs, noting that loop detectors would separate 6, 8 and 9 from the digits without loops. I'm sizing a ring kernel in conv2 so its pooled offsets match the loop diameters I'd expect to catch.

I'm laying out the ring kernel's tap positions in conv2: horizontal-channel taps at the top and bottom rows, vertical-channel taps at the left and right columns, and a diagonal channel for the corners.

I'm working out the ring kernel's tap positions for the diagonal channels, checking which pooled cells sit on a circle's tangent at each corner. The corner taps land at a distance that doesn't quite match the intended radius, so I'm trying offsets that fall between grid cells.

I'm checking the diagonal taps for the ring kernel, and I'm thinking they should sit at the inner corners, (1,1), (1,3), (3,1) and (3,3), with lower weight. To avoid firing on a single long stroke, the ring needs all four sides present, so I'm setting a bias high enough that one side alone can't reach the threshold.

I'm settling the ring kernel's weights so a single side can't fire it, with each side near 1 and the diagonals contributing less. Then I'm checking the arithmetic: a full ring lands around 2, but a lone stroke drops to zero. A taller shape like a 0 has its sides too far from the centre for these taps to reach.

I'm checking whether the ring detector can reach the taller shapes like a 0, and I'm concluding it can't with a 5-tap kernel, so the 0 stays with the existing features. I'm also noting that diagonal strokes at the corners can partially trigger the horizontal and vertical channels, and that a closed-top 4 could look like a loop.

I'm checking the ring kernel's tap offsets against the loop sizes, working out where the taps of a centre tap land in input pixels. The 0 is about 13 px wide, so its sides sit farther out than the taps can reach.

I'm checking the loop-centre coverage across the pooled grid, working out the gaps where a 9's loop centre would fall between the r=0 and r=1 cells.

I'm deciding on the ring channel's output scaling: I'll set the bias so a full ring gives about 1 and divide the other weights to match, expecting the real magnitude to be closer to 0.5. Then I'll shape the ring presence on the 4x4 grid around each loop centre.

I'm settling the ring detector's taps: horizontal taps along the top and bottom rows, vertical taps along the left and right columns, all at the same weight. I'm also considering whether to add a second, taller variant, but the kernel size caps the vertical reach, so I'll keep just the one round ring.

Still working out the ring kernel's diagonal taps and the sign of the centre tap, since a loop should have an empty middle.

I'm settling the centre tap as a negative weight on each orientation channel, since a loop's middle should be empty, and then scaling everything down by about 2.2 so a full ring lands near 1. For the template, I'm marking ring presence around the loop centres of 6, 8 and 9, and giving the 0 a weak entry because its loop sits too wide for the taps to reach well.

Now I'm tallying the column sums from the step-4 predictions to recalibrate the bias.

Now I'm tallying the column sums and checking the totals against 10000, then nudging the bias using a half-log correction on the predicted counts.

I'm now writing the template-building step, where each digit's ring-channel values come from its loop centres, scaled by strength and soft spatial weights, with a bias penalty tied to the ring template's norm.
