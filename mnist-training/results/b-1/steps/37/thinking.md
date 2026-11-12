The loss reached 0.8409, its best so far, even though accuracy is only 73.2%. Classes 4 and 8 are still over-predicted, so I'm recalibrating in the hope that accuracy rises. Next I'm tallying the per-class column counts.

I'm now working through the per-class adjustments: class 4 gets the biggest downward shift and class 9 a sizable one, though the log-linear estimate may be rough for changes this large.
