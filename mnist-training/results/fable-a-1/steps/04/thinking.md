The change gains are modest: recall dropped on the loop classes (6, 8, 9), so the bias penalty seems to be hurting them. I'm wondering whether the hole detector is firing at all, or whether its alpha is too low to compensate.

The per-class counts make it look like the hole detector rarely fires, since the 6s and 4s moved the wrong way despite the bias terms that should have helped. I'm checking the column sums too: 5 is now over-predicted (1214 against roughly 915), while 6 is under-predicted (721 against roughly 967).

I'm working out the geometry of the hole detector's corner filters: for a square hole of inner size n, the top-left and top-right filters sit n−1 pixels apart, so the pooled separation grows from about 0.5 px for 2-pixel holes to 3 px for 7-pixel ones. I'm about to check whether the thick strokes and small holes in real 6s and 8s would actually produce that separation.

I'm working through the hole geometry at small sizes: a 2-pixel hole gives only half-pixel separations, so whether the corner filters land cleanly depends on the pixel parity, while 3-pixel holes line up neatly at one pooled pixel. I'm also wondering whether the loop holes in real 6s, 8s, and 9s are even that size.

I'm estimating the inner hole sizes in real 6s, 8s, and 9s, which look like roughly 1 to 5 pixels, and checking which corner-pair separations that would produce. Tiny holes raise the question of whether a plus-shaped crossing of thin strokes could trigger all four corner types in the same pooled cell.

I'm checking the corner separations for the hole detector: with a crossing of strokes, the corner filters end up at least 1.5 pooled pixels apart in reversed order, so a plus shape shouldn't set off the detector. I'm also weighing whether the amplitudes still hold with the corner responses at −0.9.

I'm weighing whether the corner response amplitudes are strong enough: with real loops each corner probably lands around 0.5 to 0.8, so the sum is marginal against the threshold. Lowering the threshold might catch the loops, but it would also let U-shapes through, so I'm considering whether the corner outputs could be pushed harder instead.

I'm estimating what a real corner response would be: a typical MNIST stroke ramps up over about six pixels, so an arm that sits on the stroke core gives roughly 0.8 to 1.0 per arm. That puts a corner's raw sum around 1.6 to 2.0, which is close to the threshold.

I'm estimating the blank-block penalty more carefully: gray pixels inside a small hole pull each corner's raw score down by a few tenths. That would leave the four corners of a small loop summing to roughly 1.6 to 2.8, so a threshold of 2.0 would still miss many real loops, and holes of 2 pixels are even weaker.

I'm weighing the bias magnitude against the threshold: dropping the blank-block penalty to around −0.8 would make a bare wall score about 0.2, so a U-shape's two corners plus its walls could reach roughly 2.0, the same as a loop's four corners at about 2.4 to 3.6. The margin between U-shapes and loops depends on how much the corners outweigh the walls, so I'd keep the threshold near 2.0 for now.

I'm checking whether the loop threshold can be reached by balancing the blank-block bias against the corner weights. If the bias sits near the wall response, U-shapes gain nothing, and a threshold around 2.0 would separate loops from U-shapes.

I'm settling on the threshold question: a loop's four corners add up to about 2.0 to 2.8, and a U-shape's two corners plus walls reach a similar range, so a sum threshold near 1.7 would catch most loops at the cost of letting some U-shapes through. I'm considering accepting that as a soft feature and letting the fully connected layer weight the hole score linearly.

I'm settling on a lower threshold of 1.7 and a smaller blank-block penalty of −0.4, and I'm picking a set of eight hole sizes that covers the inner sizes of 6s, 8s, and 9s.

I'm checking for false positives in the all-zero case: whether an X crossing of diagonal strokes could set off all four corner types in one pooled cell. Each corner filter needs ink along two perpendicular arms, and at the crossing's quadrants those arms don't line up the right way, so I'm still working through the details of the lower-left and lower-right arms.

I'm checking whether a diagonal edge, with its arm cells and one blank cell, could push a corner's score high enough to match the detector's threshold. With the old blank penalty the score lands around 0.17, so it wouldn't fire, and I still need to recheck that calculation with the new penalty.

I'm checking whether a diagonal "/" stroke could set off the corner filters: its lower-right side gives a top-left-type response of roughly 0.2 to 0.4 once the blank penalty changes, so it sits close to the threshold. I'm now asking whether the pixels beyond the stroke need to be ink for the filter to fire.

I'm checking whether a diagonal "/" stroke could trigger the corner filters, since it would give the top-left and bottom-right responses about 0.3 near its edges. The wrong arrangement of those two corners relative to a hole should keep it from matching, but I still need to confirm that for the (0,0), (0,1), and (1,0) cases.

I'm checking whether an X crossing of diagonal strokes could set off the corner filters in the same spot. Each quadrant gives a partial corner response, and an 8's crossing might trigger the smallest hole filter, which is fine for an 8, but I still need to check the other shapes.

I'm weighing whether to keep refining the hole detector at all, or to first run a diagnostic that uses only the hole features, so I can see whether the detector fires correctly before tuning its settings further.

I'm thinking about running a diagnostic probe that uses only the hole features, so I can see directly whether the detector fires for each true class, which would show whether tuning the detector further is worth it.

I'm thinking about running a diagnostic that bins the total hole magnitude at a low threshold, so I can see how each true class's hole signal is distributed before deciding how far to push the detector's settings.

I'm sketching how the hole features could feed a combined classifier: one argmax over a "no hole" logit plus upper-level and lower-level logits, so the detector's level and side are both read off a single decision.

I'm sketching the quantizer for the hole levels: each level gets its own logit scaled by the hole magnitude, with thresholds around 0.02, 0.3, 0.8, and 1.6, so the argmax reads off how strong the hole signal is.

I'm now setting up a diagnostic that maps the hole signal to classes: no hole, upper-dominant levels, or lower-dominant levels, with thresholds around 0.02, 0.3, 0.8, and 1.6. Running it would show how each true digit's hole signal is distributed, which tells me whether the detector's settings are worth tuning further.

I'm weighing whether a diagnostic that bins the hole signal by level would show how each class's detection is distributed, which would tell me whether tuning the detector's thresholds is worth doing. Running it on a permissive threshold would reveal the levels most clearly.

I'm weighing whether to test the detector in a diagnostic run with a permissive threshold, using a single configuration. I'm stuck on whether to include the (0,0) corner: it would fire on most complex junctions, but it would cost me the upper-versus-lower position signal, which I need to tell a 6 from a 9.

I'm picking eight hole sizes for the probe, dropping the (0,0) case because it would blur the upper-versus-lower signal I need to tell a 6 from a 9.

I'm setting the hole-level thresholds at 0.02, 0.4, 1.0, and 2.0, and I'm noting that with a threshold of 1.5, a loop-like corner sum would land in the first or second level, so the quantizer should still separate weak and strong holes.

I'm setting the quantizer for the upper and lower hole levels with a steep scale factor, so that the larger of the two sides wins the argmax and the level it lands in reflects how strong the hole signal is.

I'm writing the probe's weight setup: the upper and lower hole levels get scaled logits, the no-hole class sits at zero, and the blank penalty stays around -0.5 so the solid-region and thick-wall checks still come out below threshold.

I'm deciding whether to drop the template code for this step, since I'll need to resend the full thing later anyway and only the probe itself matters now.
