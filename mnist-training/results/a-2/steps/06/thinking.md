Eight never gets predicted, while seven improves a lot and a few others do better, but zero, four, six and nine get badly hurt. That points to the α tradeoff being a per-class bias issue, so the ideal would be tuning each class's bias separately. The nearest-centroid setup with mismatched template scales is only approximate anyway. I'm leaning toward setting α to 0.5, since the real feature scale is probably around that, though per-class bias errors seem to dominate.

I'm weighing whether a fundamental feature improvement would beat more knob tuning, which might only reach around 70%. I'm considering a hand-designed system with structured conv2 detectors, such as loop detectors built from oriented edges at positions around a center, which could catch the loops in 0, 6, 8, and 9.

I'm sketching the conv2 layer as a set of structured detectors: a loop detector for closed curves, plus arc detectors that are open to the left, right, bottom, or top. The idea is that loop position and arc shape can tell apart 9, 6, 8, and 0, which pure orientation templates struggle with.

I'm working out the spatial sizes now: each pooled cell covers 2 pixels, so a 5x5 conv2 window spans about 10 pixels, which fits a 9's top loop or 6's bottom loop but not the full height of a 0. For that taller shape I'd rely on the arc detectors at the top and bottom instead, and I'm setting up the coordinate mapping between pool1 cells and input pixels.

I'm sketching a loop detector for the conv2 layer: horizontal channels along the top and bottom rows, vertical channels on the left and right columns, and diagonal channels at the corners, with the center left empty so the hole in the loop is what it responds to.

I'm sketching the loop detector's weights as rings around a center: horizontal and vertical strokes on the sides, diagonals at the corners, and a negative weight at the hole. Since loops differ in size, I'm allowing a tolerant radius of about 1.5 to 2 pool cells, and I'm starting to compute each kernel position's radius and angle from the center.

I'm sketching the arc detectors next: an arc open to the left, which would respond to the right-hand curve of a 3, would be weighted toward the right half of the ring and penalized on the left side, so it doesn't also fire on a closed loop like an 8.

I'm sizing the loop detector's bias and hole penalty: a perfect loop should give about half the maximum response, so a bias of -0.25 makes it require most of the ring, while a filled center gets suppressed by a negative weight.

I'm mapping the loop's pool coordinates back to input positions, so that a 9's loop centered near (14, 9.5) lands in pool2 cells in the top-left area. I'm also sorting the digit parts: a 0 has a tall loop, with arcs at its top and bottom, which a 5x5 loop detector only partly catches.

I'm working out where the arc detectors should sit for each digit: a radius of about 4 px for the arcs, a 0 getting its top and bottom arcs (∩ and ∪) at the top and bottom, and a 3 getting open-left arcs near its two bowls.

I'm listing which digits get which arc and loop parts, like loops on 8 and 9 and open arcs on 6 and 5. I'm also noting that the arc detectors will fire on loops too, which is fine for templates. Next I'm considering whether I can generate these part-to-stroke matches automatically instead of hand-placing them.

I'm now going to make the arc detectors penalize the open side, so a closed loop doesn't also trigger them, which should separate 3 from 8. I'm still working out how to weight the part-feature channels in the final classifier.

I'm settling the part-feature weights now: each part channel gets a template that is positive where a digit expects the part and negative elsewhere, and since the logits only depend on differences, the mean subtraction doesn't change anything. I'm also checking whether the bias term should scale with each class's expected part count, so that classes with more parts don't pick up an unfair advantage.

I'm settling on a bias of -0.3 and a part-feature weight of 0.3, since a good loop should only reach about 0.3 after pooling, so the scales roughly line up.

Working out the ring and hole weights on the grid: positions near radius 2 pool cells get nearly full weight, the inner ones less, and the center gets a negative weight to suppress filled blobs.

Setting the arc detectors' angular gate: a ⊃ should weight the right side of its ring positively and penalize the open left side, using a cosine-style gate around the closed direction.

I'm normalizing the arc and loop weights so the positive contributions sum to about 1.2, and checking that the tuning factor, cos^4 summed over four channels, stays roughly constant across angles.

I'm settling the arc detectors' open-side penalty and bias strengths: loop bias at -0.25, arc bias at -0.2. Arc detectors could also respond to a single vertical stroke on their open side, like a 1's stem, but only partially.

Next I'm placing the arc detectors' part templates for each digit: the top and bottom arcs for 0, and the open arcs for 2 near the top at roughly (14, 9).

I'm assigning the parts for the remaining digits: a 3 gets two open-left arcs, one near the top and one near the bottom, and a 4 gets a U-shaped arc at the top half. A 5 gets one open-left arc near the bottom, and a 6 gets a loop at its lower part, though arc detectors with negative open-side weights should keep that loop from also firing the arcs.

I'm mapping the 8 and 9 loops to their pool cells, then placing the pool2 templates with a Gaussian falloff and computing where conv2 outputs sit in input coordinates.

Setting up the part-feature logits now: a weight scale and a bias that penalizes classes with larger template norms, so the classes compete on a fair footing.

Setting the part-feature scale and bias now, with a weight of 8 so a fully matched part gives roughly +2.5 after the bias. Next I'm writing the conv2 part-kernel builder: a 5x5 grid of offsets with radius and angle from the center, plus a ring weighting around radius 2.

Still writing the part kernel code...

Still working out the arc gating and the sign conventions for the open side. I'm setting the loop bias to -0.3 and the arc bias to -0.25, and checking that the orientation channels line up with the tangent direction.

Still writing the part-kernel code, now moving on to assembling the fc layer with the orientation templates and the part templates.
