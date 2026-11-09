The bias tweaks barely moved the false positives for class 8: it dropped from 1289 to 1092 even though its bias went from −0.2 to −0.4. Classes 4 and 7 actually rose slightly under their own bias increases, so sensitivity to bias looks low now, which contradicts what I thought before. That makes me suspect the overprediction of 8 comes from structural features like holes instead.

I'm checking why a hole detector would fire inside a 0, since its ink-neighbour test seems like it shouldn't be satisfied there. The interior of a narrow 0 has walls on the left and right at every row, but the up and down neighbours only line up near the ends of the loop, so the test should fail in the middle. I'm now wondering whether the ink check is being satisfied by max-pooled raw ink from elsewhere.

I'm working through whether a tilted narrow ellipse could let a horizontal and a vertical chord through an interior point both stay under about 10 pixels, which would mean the up/down neighbours could also be ink for a slanted 0.

I'm working out whether a 30° tilt still lets both the horizontal and vertical chords through the interior point pass the width test, using the same ellipse-chord formula with the major axis tilted from vertical.

I'm checking whether tilted or narrow 0s could fire the hole detector: a 30° tilt pushes the vertical chord just past the width limit, so the test is borderline. That would mean some 0s get a large boost toward 8 while losing score themselves, which fits the 207 misclassifications. The same narrow-mouth pattern seems to explain the 3s and 4s getting pulled toward 8 and 9 as well.

I'm weighing whether to scale back the hole-feature weights and shrink the penalties on other classes, so holes act as supporting evidence for 6, 8 and 9 rather than a decisive signal. I'm also comparing the structure-free run against the structured one, where adding holes seems to bring in roughly 500 correct 8s and about 1000 false ones.

I'm now weighing how much the hole features should count: the structure-free run gained about 500 real 8s but also roughly 1000 false ones once holes were added. Since hole detectors fire on 0s, 2s, 3s and 4s, I'm considering shrinking the hole weights for 6, 8 and 9 and softening the penalties other classes take from them, so holes act as supporting evidence rather than a decisive signal.

I'm weighing whether the hole detectors deserve smaller weights, since they fire in 0s, 2s, 3s and 4s and their per-cell contributions are large enough to override the other evidence. I'm considering which classes almost never contain holes, like 1, 5 and 7, as a basis for softening the penalties they take from hole features.

I'm now weighing whether the hole features can separate 8 from 0, 6 and 9 at all, since a 0's hole sits at the same image height as a 9's or 6's. Holes seem to fire in tilted 0s as true topological holes, so they can't be decisive on their own and would need position or other evidence to tell the classes apart.

I'm now deciding how much each hole position should count for each class: 8 should need holes at the top or bottom positions, 9 at the top, and 6 at the bottom, with center holes giving a small boost to 0 and weaker penalties for 2 and 4.

I'm settling on a smaller base bias for class 8, around −0.42, and I'm scaling the hole weights down by about 0.3 per channel so that one firing hole no longer outweighs the other evidence for class 3.

I'm estimating how specific each hole feature is to its class: holes fire in roughly 70% of 8s, 6s and 9s but also around 20 to 35% of 0s, 2s, 3s, 4s and 7s. That gives a likelihood ratio of about 3 to 1, which is a meaningful signal but far from decisive. Since my per-channel weights stack up to a margin that's larger than that ratio justifies, I should scale them back further.

I'm reducing the hole-feature table values by about 0.3 and softening the penalties other classes take from holes, so that a single firing doesn't outweigh the other evidence. I'm working through the per-class numbers for 0, 2, 3, 4, 5, 7 and 1, with the aim of a rough log-likelihood ratio around 1.

I'm checking the bay features next: they worked well for separating 5 from 3, but the 3→5 confusions went up to 104 once the 3s bias dropped to −0.55, so the bay weights may need the same scaling-back as the holes.

I'm now looking at why 1s get read as 2s: lowering the penalties on 1's bay features and raising its bias barely changed the 1→2 confusions, so the model seems to see something in those digits that resembles a 2. My guess is that the 1s with a base line or a slanted flag, which are rare, end up sharing the 2's diagonal, and that is what drives most of the 154 errors.

I'm now checking whether restoring the three-stroke fan from before would help: the 1→2 confusions were small back then, and the structure features now penalise class 1 strongly enough that the extra 1 false positives might be manageable.

I'm going to restore the three-stroke fan for class 1 with weights around 0.6, 1.0 and 0.5, and drop its bias to about −0.25, since the 1→2 confusions have held steady at 154 even after I lowered the bay penalties. I'm also keeping the hole penalties on 1 comparatively strong, because the fan could pull in false 1s from 4, 8 and 9 that the holes would otherwise catch.

I'm now looking at why the 7s get pulled toward 5, since that confusion has stayed around 100 across several runs. The 7's lower stem drifts toward the bottom-left, which is where a 5's bowl would be, so the two shapes share some of the same evidence.

I'm raising class 7's bias to about +0.65, since its false positives are still low and each small bump has added recall. Next I'm wondering whether the 7→9 confusions, around 177, come from hole detectors firing on 7s.

I'm now trying to pin down why 7s get read as 9s, which has stayed high across runs. The 9's closed loop is what sets it apart from a 7, and in a 7 the space under the bar and to the left of the stem is open. I'm considering a corner-shaped bay detector that fires on walls above and to the right with the left and bottom open, to separate them.

I'm now checking whether a corner-shaped detector could separate 7s from 9s, since a 9 has a closed loop and the 7 leaves the area below its bar and left of its stem open. The same region sits at a different height in each class, so the position of the corner should tell them apart.

I'm weighing a corner-shaped bay detector to separate 7s from 9s, since it would capture the open space under a 7's bar that a 9's loop fills. I'm considering replacing the tiny-hole channel with this corner feature to make room for it.

Still writing the corner detector weights...

Still working out the corner detector weights for class 0, since its interior at the upper right could also register as an open corner.

Still working out the corner weights for class 5, since its bowl's upper-right interior could register as an open corner too.

Still working out the corner weights for the upper-right interior of 5 and 0, checking whether the 5's bowl could trigger the same open-corner detector.

Checking the 1-stroke case now: for a slash-shaped 1, a background cell placed just below the stroke sees ink above it but not to its right, and a cell placed to the left of the stroke sees ink to its right but not above, so the corner detector shouldn't fire there.

Checking whether a corner detector that fires on upper-right walls with open space to the left and below would also fire on the outer lower-left curve of a 0 or on a left-slanted stroke.

Still working out the corner weights for class 9's and 8's upper loops, since their lower-left arcs could also register as a diagonal stroke.

Still working out the corner weights, now restricting them to the middle columns so the lower-left arcs of 0s and 9s don't fire the detector.

Still working out the corner weights for class 5, now checking whether its bowl's upper-right interior and bay features add false firings alongside the 7→5 and 3→5 confusions.

I'm checking the bay detector positions for class 5: its upper-right bay should sit at column 2 in the top rows, while the 3's between-arms vertex falls in a lower row, so the two shouldn't overlap as much as I feared.

I'm refining the bay weights: class 5's upper-right bay should sit at the top rows, while the 3's sits lower, so they can be separated by row. I'm also reducing the hole weights for class 4 and checking whether a stronger upper bay for 4 would help it against 9 and 8.

I'm settling the bias values now: with the hole weights cut, I'm setting 8 around −0.35 and watching whether its false positives fall without losing recall. For 9 I'm still weighing the bias against the 7→9 and 4→9 confusions, and I want the corner detector to take some of that load before I commit a number.

I'm settling the remaining biases now: 3 goes up to −0.45 since it's missing mostly to 8 and 5, 5 comes down to −0.08 to cut its false positives from 3, 7 and 9, and 2 stays at 0. I'm also keeping 0 at −0.05 and 6 at −0.22, since both have few false positives, and I'm leaving 1 with the fan at −0.2.

I'm settling the remaining biases: 4 goes up to +0.3 since its false positives are low and the lighter hole weights should let it recover more recall. I'm also checking the 2→8 confusion, where the bottom loop might need a smaller weight, but the x-position overlap makes that hard to separate cleanly.

Now I'm writing out the final hole-channel weights per class, with the channel scaling applied and an exemption for class 2 in the lower-left region.

Still working out the corner weights for classes 0 through 7, scaled by 0.8 and applied only where the column index is at least 1.

Still working out the corner detector's weights, and now setting the per-class bias values with the revised hole, bay and corner tables.

Still working out the bias values for each class.
