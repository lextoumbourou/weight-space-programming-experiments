I'm at 70.8% and need bigger gains, so I'm suspecting the feature design. The line detector kernel might be the weak point: its row profile has a strong positive center, small positive neighbors, and negative outer rows, and I'm checking whether a typical MNIST stroke width fits that profile well.

I'm checking how the kernel's row profile handles thicker strokes, since a width-4 stroke would only get about half the response and a width-5 stroke none at all. That's a problem because many MNIST digits are bold. I'm considering a non-zero-mean kernel that responds to ink more broadly, though it would be less selective for orientation.

I'm weighing a middle-ground kernel: negative flanks only at the outer offsets, with weights like [-0.5, 0.5, 1, 0.5, -0.5]. That would still respond to 4- and 5-pixel strokes, though a perpendicular stroke would then score much closer to a matched one, so orientation selectivity would suffer.

I'm working through the thick-stroke case: a 4-wide stroke only partly matches this kernel, and a 5-wide one barely matches at all, so I'm testing whether shifting the detector to the stroke's edge recovers some response.

I'm checking whether thicker strokes lose response too: with a zero-sum Gaussian kernel, a stroke sitting on the detector's edge gets only about a third of the matched response, and the bias term shrinks that further. So thick strokes would still be weakly detected at their edges, which may be acceptable for position but not for overall strength.

I'm wondering whether the thick-stroke problem is the real limit, since I can't tell yet. One option is an orientation-agnostic ink channel added to all four orientation maps, though that's a bit of a hedge. Looking at the error pairs, the biggest are 5→6, 3→5, and 2→8, and the 8 template as two ellipses probably fails on slanted 8s, which show up as 8→1 and 8→2.

I'm now looking at the 8 template, which is probably too upright, so I'm considering slanting the two loops and thinning them. Several other digit templates (9, 1) might need the same slant. I'm also reviewing the per-class bias sums, where 1 and 6 look over-predicted and 4, 5, and 8 look under-predicted.

I'm considering shearing all the digit prototypes slightly, about 0.1, so the tops lean right the way real digits usually do. I'm also thinking about giving 1 a union of a vertical and a slanted stroke to cover its variants.

I'm working through the kernel's row weights at σ=1.1, with a partial mean subtraction of 0.8×mean to keep some response to thicker strokes, and checking how the sums come out per row.

I'm checking the perpendicular case: with this window the kernel scores a 3-wide perpendicular stroke at about 0.57 of a matched one, so orientation selectivity is weak no matter how I set the mean subtraction. I'm weighing whether to keep the original kernel and let the bias term handle thick strokes instead.

I'm weighing whether thick strokes really matter here, and I'm leaning toward keeping the kernel as is since most MNIST strokes are narrow. I'll focus on the templates instead: slanting them, adding variants where needed, and adjusting biases, and I'm considering a slightly blurrier template to see if it helps.

I'm now going through the digit templates: applying a slight shear to all of them, slanting the 8 more strongly, and building the 1 as a union of two strokes. I'm also planning to nudge the per-class biases, lowering 1 and 6 and raising 4, 5, and 8.

I'm setting the final parameters: the blur goes to 4.0 for a modest smoothing, with the per-class biases tuned to offset the template changes.
