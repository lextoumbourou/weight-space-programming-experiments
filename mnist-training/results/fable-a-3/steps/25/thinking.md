I'm mapping the decode outcomes for the end positions, where 0 means none, 1 through 8 each point to a specific pair, and 9 is the upper half. Now I'm tallying class 0, with 891 as none and 78 in the upper half, and class 1, where 822 of 1064 are none.

I'm working through the remaining classes now, tallying how many decodes land in each bucket. Class 2 has 440 with no decode and 356 in the upper half, with the (3,3) pair accounting for 88, and the rest of the classes follow the same breakdown.

I'm checking why the bottom ends of the 1, 7, 9, and 4 strokes are mostly missed. The tip's coverage in the pooled rows seems to stop just short of where those strokes end, around y 22 to 24, so the response lands on a row the tip doesn't reach.

I'm checking whether the tip's coverage reaches the stroke bottoms: pooled row 11 falls outside its reach, so the bottoms of 7 and 9 get missed. The upper-half D-ends are another matter, since 2, 3, and 7 show them often, and that looks like a usable feature, though I only have it summed across the eight cells.

I'm working out how to move the bottom-end detector so it reaches the last pooled row, since the kernel has no row beyond the tip. Shifting the tap to kernel row 4 would cover pooled rows 10 and 11, but that leaves no way to check for anything past the edge of the image.

I'm checking whether the bottom-end detector can separate 7 and 9 from plain stem presence, and concluding it mostly can't, since the stem's V response already captures a stem reaching the bottom. The upper-half D-end is the feature worth keeping, with 2, 3, and 7 showing it far more often than the others. Next up is the left half of the upper U, which is the remaining measurement before I build the classifier, so I'm deciding whether it's worth measuring.

I'm weighing whether a U-left measurement is worth it: the left arm of the 4 could separate it from 9, and the top of a 1 in the left half might add a little more. I'm leaning toward one extra probe, "/" at (3,1), instead of rebuilding the whole U chain over the eight cells.

I'm setting up the left-half U chain over the four cells at (0,0), (0,1), (1,0), and (1,1), and adding the "/" probe at (3,1) as the extra binary. After that the classifier comes next, followed by tuning the temperature and endpoint weights.
