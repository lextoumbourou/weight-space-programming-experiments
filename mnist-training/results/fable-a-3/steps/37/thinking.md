I'm going through the neighbour-configuration codes, mapping each numbered value to its NW-end pair, and then tallying the counts by class. For class 0 there are 980 with none and 8 in the rest group, class 1 has 1058 with none, and class 2 has 968 with none and 11 in the rest. Class 3 is the biggest at 1030, where 651 (63%) have none and one has the (1,0) neighbour.

Now I'm checking the bottom-left neighbour detections: class 5 and class 3 are the ones that show a NW-end there most often, so a hit at that spot narrows things down a lot. Class 7's large "rest" share might come from the top-left serif, which I'll keep in mind for later.

Now I'm working out how to probe the bottom-left tips: I'll check the grid cells for the southwest chain, and I notice the top-left hooks ending above y≈8.5 fall outside every cell, so those would be missed.

Next I'm checking the southwest chain cells, covering the bottom tails that end around y≈20–25, and noting that the tips beyond y≈23.5 are mostly what's being missed.

Now I'm settling the groupings for the next classifier pass: the northeast side gets eight cells plus a lower aggregate, the northwest gets eight cells plus a rest bucket, and the southwest chain is covered too.
