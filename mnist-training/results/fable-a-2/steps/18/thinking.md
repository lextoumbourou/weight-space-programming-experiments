Sitting at 79.3% with loss 0.637. The biggest error is 7 being read as 9, so I need a feature that tells those two apart, and I'm starting to think about how the loop on a 9 differs from a 7.

I'm checking whether the "/" and "\" strokes in the upper-left and lower-left regions can separate 7 from 9, since the other features I've looked at mostly don't.

I'm weighing the remaining 2→3 and 2→8 confusions, checking whether a lower-left "/" stroke or the bottom-edge features separate 2 from 3 and 8, and I'm planning to probe the lower-left "/" and "\" regions next.

I'm considering "\" and "/" strokes through the centre of the digit, since an 8's crossing stroke might set it apart from 4, 9, 5, and 2. I'll probe both diagonals in the middle rows to see which separates the classes.

I'm settling on thresholds of about 0.5 and 1.4 for the diagonal features, since a diagonal stroke only crosses a couple of cells in each 2x2 region and should give a weaker response. Next step is to probe the "\" and "/" strokes through the centre.
