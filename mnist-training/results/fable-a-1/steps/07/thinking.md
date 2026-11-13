The zero digit results favor the "wider" variant by a large margin, so real zeros must be wider than I had assumed. Working the skeleton width through, about 14.7 pixels plus stroke gives the ink extent I'm checking against.

The slant counts for the 1s average out to roughly 14 degrees, which suggests a shear near 0.2 rather than the 0.10 I had been using for every digit. A sheared 0 could also account for the "wider" template winning, since the slant pushes its diagonal content outward.

I'm estimating typical ink widths for each digit from MNIST-style stats, roughly 13 to 15 pixels for most, with 1s much narrower. Subtracting the stroke leaves the skeleton widths I need to compare against my drawings.

I'm checking the rough width math here: a base zero comes out near 0.70 of its height, about 12 pixels of skeleton, which is narrower than the 5-to-1 "wider" win would suggest. That leaves two possibilities, either real MNIST zeros are closer to 16 to 18 pixels of ink, or the blur in the features favors the wider templates.

I'm working out the zero mixture now, weighting the wide template most heavily, around 0.6, with the narrow one at about 0.25 and the rest spread across the others.

I'm settling on the structure for the zero digit: rather than blending all the strokes into one shape, each variant gets rendered on its own, and the final probability is the weighted sum across variants. That keeps each variant's bounding box intact, so the placement doesn't get distorted. I'd put most of the weight on the wide template, with the narrow and base ones sharing the rest.

Next I'll run tournaments for the other eight digits to learn their width and slant styles, since the zero result showed that width matters. I'll use about four probe steps, two digits at a time, with a handful of variants each, and then build the mixture templates from what they show.

Next I'm setting up variants for the digit 2 and digit 3 probes, varying width and slant. For 2 that means the current shape at widths 1.0 and 1.2, a looped version with the base rising, a round-top swash version, and a narrow upright one. For 3 I'll try the current round shape at two widths and a flat-top version.

Next I'm weighing a few more variant shapes for the digits 2 and 3, then running another tournament between them and the 5 and 6 variants so I can see which widths and slants actually win.

I'm drafting the digit 2 variants now, starting with the current shape and a looped version whose base rises toward the right.

I'm drafting the digit 2 loop variant now, tracing the neck down to the bottom-left corner and then looping up and around before the base runs off to the right.

I'm drafting the digit 2 variants in more detail, including a round-top shape that reaches down toward the middle of the height before the stroke sweeps back to the base.

Now I'm laying out the variant set for digit 2: five versions covering the current shape at two widths, a looped base, a round-top shape, and a narrow upright one. For digit 3 I'm starting on a flat-top variant as well.

I'm laying out the variants for digits 2 and 3 now, with a middle-bar version of 3 that extends further left, and I'll use the same five-variant layout for each: different widths and slants, one of each shape, and a narrow upright option to check against the wider ones.

I'm setting up the next probe run: the implementation will place each variant separately and scale x by the width factor before applying shear, using a fixed skeleton size of 17.5 since larger values hurt the zero results. I'll write the five variants for digits 2 and 3 with that structure.
