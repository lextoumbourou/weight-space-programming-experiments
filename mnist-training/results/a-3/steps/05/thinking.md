I'm seeing that the feature values come out smaller than my scaling assumes, so the bias term dominates and the sparse class keeps winning. Shrinking the scale factor, to something like 0.7, should boost the feature contribution, or I could drop the bias reliance and use cosine normalization instead.

I'm checking whether the orientation convention of the templates matches the edge filters, since a polarity mismatch would explain why the sparse class keeps winning even though 8 should have plenty of features.

I'm verifying the orientation convention: the filter's positive weights respond where ink lies along the gradient direction, and the template's gradient points toward the stroke center, so the signs should agree. I'm also checking the coordinate ordering, that x maps to columns and the flattened layout is channel, row, column, to see whether a mismatch there could explain the sparse class winning.

I'm now checking whether the templates are too saturated: with blur from the membership width, a single stroke spreads high activation into neighboring cells, so the 8 template ends up with high values almost everywhere and its norm becomes large.

I'm tuning the template sharpness: a tighter sigma, a softer saturation, and a higher orientation tuning power, so the 8 template stops covering so many neighboring cells. I'm also lowering the scale to 1.0 and reducing the bias weight to about 0.6, since the sparse class is overpredicted, and noting the main confusions (0→2, 9→7, 8→7) to check against.

I'm settling on the tuning plan: sharpen the templates with a sigma of 2.0, use a saturation of 1 minus exp(-acc/2), and raise the orientation tuning to the fourth power of cosine, with the scale at 1.0 and the bias weight at 0.6.
