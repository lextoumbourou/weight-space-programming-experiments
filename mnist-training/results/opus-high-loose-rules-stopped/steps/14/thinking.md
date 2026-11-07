The last run gave slightly worse results, with 8 gaining more predictions (5→8 at 195) and mixed outcomes overall. Several changes went in at once, so it's hard to tell which one caused what. The stronger warp may have made the 8 template blurrier and more average, which would explain why it attracts other digits. A bias step could be part of it too.

Rather than keep tweaking, I want to look for a bigger structural gain, since the current approach is sitting around 83-84%. I'm weighing a few options, starting with A.

I'm weighing a few structural options beyond tweaking. One is improving the feature extractor, perhaps with higher spatial resolution or different use of the later channels, though that's hard to pin down. Another is letting the second conv layer capture non-linear conjunctions, since the linear fc is limiting, with 5 versus 8 differing in the top-right stroke as an example. A third is pairwise boosting on the most-confused pairs, which the less-shrinkage result suggests may be fragile because the synthetic covariance doesn't match.

I'm going to revert the warp to the earlier 0.08 setting so I can isolate its effect, while keeping the two variants and the bias correction. I'm also planning a 5 variant, since the 5→8 confusions likely come from the sloping top bar and large bottom bowl.

I'm adding a 5 variant with a curved stroke that bends into the bowl, using a Bezier from the top bar down through a left-side control point.
