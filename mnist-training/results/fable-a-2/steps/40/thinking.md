I'm at 88.36% with loss 0.404 and 11 steps left, and the last cycle only gained 0.018. Tuning the scale or group weights might help as much or more. The scale has been stepped down from 0.55 to 0.40 as terms got added, and I never checked whether that was the right value, so it's a candidate for the furthest-from-optimal parameter.

I'm weighing which parameter to test first: the scale has drifted down from 0.55 to 0.40 without ever checking the optimum, and the relative weight of the line terms has grown as more were added. My plan is to lower GLINE from 0.6 to 0.45 first, then adjust based on the result, and re-tune the class biases afterward since they shift with it.

I'm weighing more probe cycles against tuning, since the gains per cycle are shrinking. A mix of one more cycle and several tuning steps looks reasonable, and the loci features may be worth single-row probes like the lines got. The most discriminative ones would be the ceiling and open-below features at rows 0 and 1, plus a few of the others.

I'm weighing whether a few of the loci features could be split into single-row probes the way the lines were, though the gain there is unclear since they're already binary. Tuning may be the better use of the remaining steps: the loss is 0.404 at 88.4% accuracy, which suggests maybe 0.01 to 0.03 could come from correcting the global scale if the model is miscalibrated.

I'm weighing whether the misclassified 0→2 pairs, which stay stubbornly high, point to a specific feature gap, and whether to spend the remaining steps on one more probe cycle or on tuning the biases afterward.

I'm checking whether the template term is driving the 0→2 confusions: my hand-drawn 2 template may match zeros better than my 0 template does, even though the sharp line features favor 0.

I'm wondering whether the 0→2 confusions come from the 2 class acting as a catch-all for outliers, since its varied styles give it a broad distribution with means near the middle of many features.

I'm settling on one more probe cycle before tuning, aiming at the unmeasured single-row features that look most promising, such as the horizontal and vertical splits on rows 0 and 3 and the two slanted strokes on row 0.

Now I'm picking which single-row features to probe next, especially the bottom-row slants and the centre columns, to separate the 7s from the 9s.

I'm now checking which single-row features could separate the confusable pairs: the bottom-left and bottom-right arcs for 0 versus 2, and the top-left bar for 7 versus 9.

I'm settling on the next probes: a single-row horizontal split on the top-left, and two slanted strokes on the bottom row, chosen mainly to separate 0 from 2 and 2 from 3. That would be probe cycle 40, followed by a classifier refit at step 42 and the remaining steps on tuning.
