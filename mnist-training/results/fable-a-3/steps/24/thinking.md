I'm working out how to decode the R-end values, mapping each code from 0 to 9 to a specific pair or to none. Then I'm tallying the two classes: class 0 has 991 items with 933 of them showing none, and class 1 has 1064 with 982 showing none.

Now I'm going through the per-class tallies, where class 2 has 567 with no pair and its main pairs are (3,3) and (2,3), and class 3 has 929 with none.

I'm finishing the tally for the last few classes, noting that R-end features are only moderately useful and some of them are misleading for the 2, 5, 7 and 8 shapes. Next I'll move on to the D-end checks on rows 2 and 3, then the U-left step, and after that the classifier.

I'm settling on how to aggregate the D-end cells for outcome 9, leaning toward summing the row 1 cells and possibly row 0, across all eight cells.
