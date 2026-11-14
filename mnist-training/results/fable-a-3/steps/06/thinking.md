I'm setting up the outcome encoding, where each outcome is a sum of three bits for the absences at H(0,0), H(0,1), and H(0,2). Within class 0 I'm reading off the counts for each outcome, and then totaling the cases where everything is absent, which comes to 131.

Next I'm checking how often each of the three top bits is present in class 3, and the 97% for H(0,1) is already clear from the totals.

Next I'm working through classes 4 and 5: for class 4 the absent total is 912 (93%), and the three top bits come out at roughly 1.5%, 5%, and 4.2%. Class 5 is partway through, with H(0,0) around 16% and H(0,1) around 73% so far.

Now I'm checking classes 6 through 7: class 6 has 763 absent (79%), with H(0,2) present about 20.6%, and class 7 shows H(0,0) present around 70% and H(0,1) and H(0,2) both near 98%.

Now I'm going through classes 8 and 9: class 8 has H(0,0) around 15%, H(0,1) about 73%, and H(0,2) near 94%, while class 9 shows H(0,0) at roughly 16%, H(0,1) at 87%, and H(0,2) at 96%. I'm also noting that the breakdown within the all-absent stratum is being split by whether H(3,0) is present or H(3,3) is.

Now I'm checking the stratum counts for classes 0, 1, 2, 4, and 6, looking at how often the "\" and "/" strokes are present within the all-absent group.

I'm weighing whether the strict presence features carry enough signal to build a naive Bayes table, since classes 1, 4, and 6 already separate well on the top stroke. The remaining probe plan is long, so I'm looking for a cheaper way to cover the rest.

I'm weighing whether to probe all the remaining features or narrow the set to about forty of the most informative ones, since each step covers only three bits and the full list would take roughly twenty more steps. I'm also considering whether neighbouring features, especially the adjacent columns, are correlated enough to infer some from others, though that would be risky.

I'm weighing whether measuring all 64 features, at about 21 steps, is worth the cost, or whether a smaller subset would leave enough budget for tuning. I'm also checking whether four marginals could come from ten outcomes in a single step.

I'm trying to see whether four features could be read from ten outcomes in a single step, and it only works if each feature's present set lines up with a union of the groups. Without some combinations being nearly impossible, the grouping would need all sixteen joint patterns, so that route probably won't save probes.

I'm weighing whether four features could be read from ten outcomes at once by merging rare joint patterns, though that depends on which patterns are rare for each class, which I don't know in advance. I'm also considering a random-selector scheme, where the outcome picks one of several features by an independent pseudo-random choice, but finding a selector that is uniform and independent of the features looks difficult.

I'm weighing a selector scheme where the outcome is chosen by which of five unrelated features is largest, and then a bit is read from the sign of a second quantity. That could cover five features per step if the choice stays balanced, but a class could end up dominated by one selector value, leaving the others with too few samples.

I'm weighing a selector scheme where the outcome picks one of five random projections of the count features, with a smaller signed term choosing the bit. The concern is that the selector won't be truly independent of the measured features, since both draw on the same underlying strokes, so the per-class estimates could come out biased in ways I can't easily bound.

I'm thinking about checking the selector scheme for bias: the features already measured for H(0,0) through H(0,2) can go into a first five-feature step as a test, since their per-class rates are known. If they come out right, the method could cover five features per step.

I'm considering whether to use five features per step instead of one, each step choosing one of five projections and reading a bit from a smaller signed term, which would cut the probing from about 21 steps to roughly 13. The open question is whether the selector stays balanced within each class and independent enough of the measured features that the per-feature estimates aren't biased.

I'm weighing a selector built from random signed sums over the count features, but within each class the same projection would tend to win most of the time, which skews the sample sizes. I need projections whose within-class variance outweighs their class means, so that the selection stays balanced. I'm considering whether a different selector, such as one drawn from finer or less correlated features, would avoid that skew.

I'm considering whether the selector could avoid being dominated by class means: one option is a high-frequency filter whose pooled response acts like a hash of fine pixel detail, but the per-class means would still drive the argmax, so the selection would stay skewed. Reusing the eight conv1 channels for probing would mean giving up features I still need, so that doesn't look workable either.

I'm considering a deterministic stratification instead, where a single continuous feature Z that is unrelated to the measured features sets the outcome through quantile bins. The catch is that the bin boundaries would differ by class, and I don't know those quantiles in advance. I'm also wondering whether total ink might have a similar distribution across classes and stay independent of the features, which would make the bins easier to balance.

I'm still weighing whether a selector built from position-dependent features, like which shifted unit wins a max-pool, could act as a near-random split that doesn't depend on the class.

I'm checking whether the pooled column parity could act as a selector: comparing total V-mass on even versus odd pooled columns gives a difference that is roughly centred at zero. For centred digits like "1", though, the stroke sits at a fixed pixel offset, so that parity might be constant rather than random.

I'm working out whether a selector could split the image into parity groups by comparing column mass on even and odd pooled columns, but for centred digits the stroke sits on a fixed pixel grid, so the difference would sit near zero rather than vary. I'll set that aside and keep the simpler plan of three features per step with clean results, even though it means roughly 21 more steps.

I'm noticing that if H(0,0) is present then H(0,1) almost always is too, since the patterns with H(0,0) alone are nearly empty. Similarly, when the first two cells of the row are present, the third is usually present as well, so the presence patterns along a row look like contiguous runs, and I'm starting to count how many such run patterns four cells allow.

I'm noting that the non-contiguous run patterns are rare, so one row of four cells can be encoded almost completely with the outcomes. For vertical strokes I'm checking whether runs along a column behave the same way, with the digit 3 as a possible exception.

I'm checking whether the vertical runs are contiguous too, since that would make column-wise patterns easier to encode than row-wise ones. Rows look like they might produce non-contiguous patterns for digits like 3 and 8, so I'm leaning toward working along columns and then figuring out how to map each pattern to an outcome with linear logits.

I'm weighing whether to drop one of the eleven contiguous 4-cell patterns, like the single-cell 1000 case, so the ten remaining outcomes cover the row. Any image with a disallowed pattern would get pushed to the nearest allowed one, which slightly biases the marginals.

I'm noting that a dropped pattern like 1000 would get pushed to either 0000 or 1100 depending on the margins, which introduces a small error into the b1 and b2 estimates. I'll have to accept that for the other rows, since their presence patterns are still unknown.

I'm mapping out the feature groups by row and column, with row 0 needing only its last cell. Along the diagonals I'm sorting cells by their anti-diagonal sums, where the four-cell line is the one that can hold most contiguous patterns.

I'm settling on a grouping for the diagonal cells: the four-cell anti-diagonal can hold nearly all its run patterns, and the shorter diagonals would need a few more steps, leaving about five in total for that direction.

I'm checking whether horizontal runs of the same diagonal orientation stay contiguous too, since overlapping windows might make them behave like the vertical case, though I haven't confirmed that for strokes that are separated by a gap.

I'm considering whether the run-pattern encoding might still be biased when a non-contiguous pattern like 1001 shows up in the vertical or diagonal groups. I can't measure that bias directly, so I'll check it against the known row 0 data: re-measuring those cells with the run-pattern method should reproduce the marginals I already have, and it would also give me the missing (0,3) cell.

I'm weighing whether a coarser grouping could cut the count further, but the row structure doesn't offer more than about four cells per step, so the saving stays small. I'm now considering whether the full set of 64 features is actually needed, or whether I can order them by importance and stop once accuracy is good enough, and I'm starting to sketch that classifier.

I'm weighing whether a learned classifier over these 10 pattern categories would beat independent bit estimates, since the joint row distribution might carry information that the per-cell marginals miss.

I'm weighing whether to validate the run-pattern method on row 1 or to measure row 1 directly, since validating would cost a step without adding new features.

I'm setting aside the validation idea for row 0, since it wouldn't tell me anything about the vertical or diagonal groups where contiguity is less certain, and I'll pick up (0,3) later in a leftover triple. Each four-cell line has eleven possible run patterns, and I'm leaning toward dropping one of the single-cell end patterns, since those look rare for row 1.

I'm settling on which run pattern to drop: the single-cell pattern 1000 looks rare, since a stroke at only the far-left column of row 1 seems unlikely, so I'll leave it out. That leaves ten outcomes for the four cells, each encoded as a 4-bit pattern across columns 0 to 3.

I'm fixing the schedule now: drop the 1000 pattern, decode the bit marginals from the ten outcomes, and assign the remaining probes row by row, then column by column, then the two diagonals, with the leftover (0,3) cell picked up at the end before building the classifier.

I'm looking at which run pattern to drop for the vertical columns, and I'm checking the far-left column near x≈7.5, where the left side of a 0 would sit. I'll decide which single-cell end pattern is rarest there before fixing the eleven patterns for those four rows.

I'm checking which single-cell pattern to drop for the vertical columns, since a lone cell at either end of a column window could be common for digits like 7 or 2. Neither end looks clearly rarer than the other, so I'm weighing whether an interior single cell would be the safer pick to remove.

I'm weighing whether single-cell patterns are common enough that dropping one would hurt, and I'm considering mapping a dropped pattern like 1000 to its nearest allowed neighbour, which would shift the b0 or b1 marginal by at most its probability.

I'm weighing whether to drop the 1111 pattern or accept a mis-binned outcome, but full runs are common for V columns 1 and 2, so I'd keep it and accept some error from mapping the dropped pattern to its nearest neighbour. Before settling, I'm checking whether a vertical run along column 0 for classes 3, 5, or 8 would actually fit the contiguous pattern.

I'm considering that 3's right-side strokes sit in two separate runs with a gap at the waist, so in the vertical window they'd show up as non-contiguous patterns like 1001 or 1011. My contiguous encoding would misread those, shifting some probability mass by flipping a bit, which could matter a lot for 3 at column 3.

I'm weighing whether splitting the vertical columns into triples would handle the non-contiguous patterns on the right side of the 3 and 8 better than the four-cell grouping, even though it means more probe steps.

I'm weighing whether the four-cell run encoding saves enough steps over triples, since the vertical and diagonal groups could hit non-contiguous patterns for the right side of 3 and 8 and the bias might cost more accuracy than the 4-step saving is worth.

I'm checking the vertical columns next, where the central columns should be mostly contiguous, but the right side of the 3 and 8 may produce split patterns at columns 2 and 3 because of the waist gap.

I'm checking whether a waist gap in a 3 could split a run along a column, and since the gap is only about 3 px while the windows are 8 px wide with 4 px spacing, the pattern should stay contiguous. A non-contiguous pattern would need two same-orientation strokes at least 7 or 8 px apart with nothing between them, which looks rare for vertical columns. I'm now turning to the diagonals, where an "/" in an 8 could plausibly produce split patterns along a row.

I'm checking whether contiguity holds for each orientation: a split pattern needs two same-direction strokes at least 8 px apart with nothing between them. That seems unlikely for vertical strokes along a column, but for "/" strokes along a row, the 2's top arc and neck could land in separate cells.

I'm checking whether "/" strokes could split along a column, since in a 2 the top-left arc and the bottom-left neck end could be eight pixels apart with nothing between them, which would give a non-contiguous pattern.

I'm checking whether "/" strokes could split along a column or a diagonal, since in a 2 the top-left arc and the neck could land in separate cells, and I'm testing the anti-diagonal cases on the next example.

Checking the diagonals now, I see that a slanted 0 could put a "/" run on one anti-diagonal with gaps between its ends, so run encodings aren't safe there. I'll either group the diagonals in triples or accept some bias.

I'm weighing whether to use run patterns for the horizontal rows and vertical columns and accept some small error on the diagonals, since non-contiguous patterns are probably rare enough that the marginal error stays under about 8%.

I'm looking at whether the diagonals could be handled as triples or measured only partly in their central cells, and I'm considering whether to drop 0001 or 1000 for the vertical column patterns, since both single-cell ends seem fairly rare.

I'm weighing whether to drop a single-cell pattern like 1000 or 0000 for the vertical columns, accepting that a mapped pattern would bias one marginal by at most its probability.

I'm going back and forth on whether to drop a single-cell pattern like 1000 or 0000, since any dropped pattern has to be mapped onto a neighbour and that shifts one marginal. The trouble is that an all-empty image would be sent to one fixed outcome, so I can't cleanly separate it from the pattern I'm keeping. I'll settle on dropping whichever end-cell pattern looks rarest per column and accept the bias that comes with it.

I'm weighing whether to cut the remaining budget by using run patterns for the horizontal rows and vertical columns, with triples for the diagonals, since that would leave room for a checkpoint classifier before the tuning steps.

I'm going with run patterns for the horizontal rows and vertical columns, since those look mostly contiguous. I'm deciding to measure row 1 next, where I'll drop the 1000 pattern, and then I'll write out the pattern list for the encoding.

I'm settling on the ten run patterns for the encoding and writing out the scoring formula, logit_o = G·Σ s_m(0.5 − E_m) with G = 100. I'm also checking which outcome the dropped 1000 pattern falls into, comparing the 0000 and 1100 logits, since the difference works out to 2G(a0 + a1).

Now I'm going to write the code for the encoding and the scoring formula.
