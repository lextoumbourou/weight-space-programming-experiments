Training is at about 91.2% accuracy with loss around 0.313, with 23 steps left. The most frequent remaining confusions are 5→3, 8→5, and 5→8, with 2→3 and 9→7 close behind.

I'm weighing three options for the next step: tuning the scale weights, adding features like heavy strokes, or finishing the remaining measurement. I'm also looking at the 8 class, which has the weakest recall at about 85%, and its main confusions are with 5, 1, and 3.

I'm checking whether a hole detector could tell 8 from 5, since 8 has two enclosed loops and 5 has none, and I'm sketching how to build one with convolution and ReLU.

I'm working out whether a conv1 filter at the pixel level could catch small holes directly, by giving the centre a negative weight and the surrounding ring a positive one, since the ReLU and max-pool that follow would only fire when the centre is empty and enclosed.

I'm considering whether a conv1 filter could detect tiny holes directly at the pixel level, but all eight conv1 channels are already used by the orientation and threshold pairs, so that would mean giving something up. Hole detection in conv2 is the remaining alternative I'm turning to next.

I'm looking for a way to test for the two enclosed holes in an 8 with a detector built from several conv2 channels, each fixed to one ring size. Each channel would check for ink on all four sides of an empty centre, and I'm working through the possible width and height spacings of that ring across the 5x5 window.

I'm checking the ring layout: four side detectors, two vertical for the left and right walls and two horizontal for the top and bottom, combined so the output only fires when every side has ink.

I'm checking whether the top and bottom arcs of a small loop are still picked up by the horizontal filters, since a loop of radius 3 or 4 only spans about 27° of horizontal stroke on each side.

I'm checking whether a ring of four side detectors could reliably fire on small loops, since the top and bottom horizontal responses may be too weak for tiny radii, which could make it fire only on a minority of true loops.

I'm planning one probe step that tests four ring geometries at once, splitting each channel's output between the upper and lower halves of the image so a single result separates 8 from 9 and 6.

I'm sketching the ring channels for the hole detector: each one checks four sides of an empty centre, with the sides spaced to match loop sizes, and I'm working out the cell geometry so the widths and heights fit the loops of 8, 9, and 6.

I'm laying out the kernel for a ring detector: a 5x5 grid with left and right walls at varying columns and top and bottom at varying rows, with the first configurations set to width 4 and height 4.

I'm sketching the remaining ring layouts for 8, 9, and 6, with the top and bottom columns shifted because the loops are slanted, and I'm finding the offsets hard to pin down, so I'm going to stop refining the geometry.

I'm considering a softer version of the ring detector, where each side can be covered by a short run of cells rather than one exact cell, though that would make a long side stand in for a missing one. I'm also weighing whether to drop the hole idea and use the remaining conv1 capacity some other way.

I'm ruling out the saturation-pair change, since dropping the high-threshold copies would unsaturate the maps and invalidate every measured table, so I'm dropping the loop idea too. I'm considering instead whether NB's independence assumption, with its heavily correlated neighbouring cells, is distorting the weights, and whether a per-feature-group temperature could correct that.

I'm weighing cheap fixes like per-feature-group temperature weights to counter the naive Bayes correlation problem, perhaps worth a few steps for a small gain. Now I'm turning to the 5→3 confusion, looking for a feature that separates a 5's top bar and slanted vertical from a 3's shape.

I'm thinking about whether orientation-agnostic ink presence could separate the two classes, since a 5's slanted stroke might be picked up as "/", "\" or V, while a 3's upper stroke sits on the opposite side. Checking for any ink in the upper-left versus upper-right cells at that height could be more robust than relying on one orientation's response.

I'm considering an orientation-agnostic "any ink" feature, since a cell with no ink at all is strong evidence, such as an empty upper-right for a 5 or an empty centre for a 0. I'd use a narrower 3x3 window than the existing features so it stays sharp enough for those cases.

I'm sketching an any-ink feature that sums all four orientation maps over a small 3x3 block of cells, so an empty centre for a 0 would show up as a hole. I'm checking whether the windows around the 0's hole avoid its side strokes at this spacing.

I'm weighing an any-ink feature with a narrower 3x3 window, where an empty centre would show up as a hole for a 0. The 6-pixel window works for zeros, whose inner hole is wide enough, but the small loops in 8, 6, and 9 leave too little empty space, so I'm considering a smaller 2x2 kernel for them.

I'm considering whether a narrower any-ink feature, pooled over a small 2x2 block, would be too easy to satisfy since it could land between strokes, though it might still serve as a finer measure of ink coverage near each cell's centre.

I'm checking whether row patterns of ink presence across the four cells of a slice separate digits: a 0 should show ink at the two ends with empty cells between, since its sides sit about 11 pixels apart.

I'm considering whether to pick only the most informative cells, such as the centre and the upper and lower corners, instead of encoding all sixteen as triples, since two-run row patterns are needed for 0 and 4 and run encoding wouldn't capture them safely.

I'm picking up the corner cells that matter for the 5 versus 3 and 9 versus 8 splits, and I note the existing oriented features already separate much of that. An any-ink OR combination might add a bit of robustness, maybe half a percent. I'm also looking at 8, the weakest class at about 85% recall, and where its confusions with 5, 3, 9, and 0 come from.

I'm now trying to pin down what makes an 8 distinct: its loops closing both top and bottom, with ink in all four corners of its box. Compared with 5, 3, 9, and 6, each of those is missing at least one closure, so "ink in all four corners" might separate it.

I'm testing whether an AND feature that requires ink on all four sides of a cell's box would separate 8 from the others, since each of the confusable digits is missing at least one of those sides. That would make 0 and 8 the main matches, and the remaining question is how to tell them apart.

I'm planning an AND feature at conv2 that needs four side indicators within a 10-pixel window, so I'm placing taps for the upper and lower loop sides at rows 0-1 and 3-4, with left and right sides at the outer columns.

I'm planning a short sequence for the remaining 23 steps: first a few scale-tuning runs to see how loss and accuracy respond, then a measurement pass on either the any-ink family or the heavy-stroke family, and finally a few steps on the leftover "/" cells before a last round of tuning.

I'm considering a discriminative reweighting for confusable pairs, where a second-stage step would use the current classifier's logits to focus on the images it gets wrong or is unsure about.

I'm considering a second threshold on the same underlying stroke amount, so a "heavy" level alongside "light" could capture stroke length as a three-level ordinal feature, which might help with the digits that differ mainly in how much ink they contain.

I'm considering heavy-stroke versions of the vertical and horizontal features, since a long stem in column 2 would mark 1, 4, 7, and 9 while the short curved bits in 2, 3, 5, and 8 would not. A heavy level on the same underlying stroke amount could separate 9 from 8 and 7 from 3 more cleanly. I'm planning to cover the nine central cells in columns 1 to 3 and rows 1 to 3, either as triples or as column runs.

I'm weighing whether heavy-stroke versions of the vertical features would help: a long stem in the centre columns would mark 9 against 8, while 8's short curves would not register at the heavy level. Since the presence features already cover 8's side strokes well, the gain from this could be modest, perhaps around a percent, and it would cost five or six measurement steps.

I'm estimating how a heavy-stroke threshold on vertical strokes might separate straight stems from curved loops: a 9's stem should register at the heavy level while an 8's short curves would not. That could clear up a good share of the straight-versus-curved confusions, perhaps around 150 errors.

I'm considering heavy-stroke versions of the horizontal features as well: a long top bar would separate 7 from 9, 3 and 2, and a heavy bottom bar could split 2 from 3. Since 5's top bar is often short, a heavy threshold on it might also help with the 5-versus-3 confusion. I'm thinking of implementing this by replacing the count channels with heavy-level presence probes, so a probe would only register when the stroke amount passes the higher threshold.

I'm checking whether requiring the minimum over shifts to exceed 4.5 is too strict, since a stem centred in the window gives about 5.7 but drops to about 2.8 when it lands in a half-weight column for one of the shifts.

I'm checking whether a stem has to cover most of the window height to count as heavy, and whether a slanted stem still stays within the centre columns. A lean of 15 to 20 degrees shifts about 1.5 cells over the window height, so it should still register.

I'm working out the heavy-stroke probes for the vertical strokes, with a threshold that fires only on long, straight stems in the central columns. I'm planning four steps for the vertical columns and a few more for the horizontal bars.

I'm weighing whether the heavy-stroke vertical probes are worth doing over the any-ink variant. A heavy vertical probe should fire only for long stems, since a single long stroke can cover a few overlapping cells, so the features won't be mutually exclusive.

I'm weighing a quick scale test before committing to the heavy-stroke family, since the loss of 0.313 suggests the classifier may be overconfident and shrinking the scale further could help. I'm estimating how the loss splits between correct and wrong predictions to judge which direction to try.

I'm checking how the loss splits between correct and wrong predictions to judge whether the scale is off. Scaling everything by 1.25 would be a quick test of calibration, though the final choice mostly depends on accuracy, so I'll weight that more heavily.

I'm setting up the first heavy-stroke probe for the vertical strokes, with the threshold tuned so it only fires on long stems in the centre columns, starting with column 2 over the first few rows.

Still writing the heavy-stroke probe weights...
