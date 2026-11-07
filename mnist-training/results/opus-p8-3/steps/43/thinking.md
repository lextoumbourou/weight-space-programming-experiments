I'm decoding the two sets of readings: F1 is the '/' value from bit0, F2 the '\' value from bit1, and F3 the ink count at (2,0) for bit2. For the first set, that gives F1=534, F2=859 and F3=985. I'm now working through the second set, where F1 comes out to 593 and F2 to 11.

I'm now working through the remaining readings in the second set, computing F1, F2 and F3 for each row. That covers rows 3 to 9 and the ink count at (2,0), which comes out to 26 at the end of the list.

I'm checking the ink percentages against each other and the F2 readings, and they look clearly separated. I'm then setting up the build with these three features at λ_s=0.4, using m=0.8 for the single-cell F3 and m=1.6 for F1 and F2, with calibration to follow.
