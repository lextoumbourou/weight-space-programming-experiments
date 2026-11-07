The loop detector isn't firing at all in the first four columns, which is a useful result. The horizontal-bar detector does respond, but oddly: it fires on the 0s across the rows, and the 7s give a huge count on row 1. For the 7s, a stroke only shows up in the center region, so I'm wondering whether the detector is catching the edge of a stroke near the center rather than the bar itself.

I'm trying to work out why the horizontal-bar detector fires on the 7s at row 1, since a 7's top bar sits above that row. My guess is that the pooling and blur spread the stroke far enough sideways that a diagonal stem catches the taps on both sides. That would also explain the 9s and 6s firing in the upper rows.

The loop detector never fires in the first four columns, while the horizontal-bar detector fires on the 0s across rows and on the 7s at row 1. I'm still puzzled that a 7's top bar, which sits above that row, would trigger a horizontal-only detector, and I'm wondering whether the pooling and blur are spreading the stroke far enough sideways to catch something on both sides.

The threshold is the problem: with the blurred background and four taps at about 0.5 ink each, the sum tops out near 2.0, just under the 2.2 cutoff, so the loop detector never fires. Dropping it to around 1.6 would let a crossing stroke register while a single stroke still wouldn't.

I'm lowering the loop threshold to about 1.7, since the sum tops out near 2.0 and crossing strokes would otherwise never register. A single stroke should still stay below that cutoff, while a crossing with four inked taps would clear it.

I'm planning the next probe: check the loop detector at the lowered threshold and the first horizontal-bar detector across rows 0–3, plus a "none" option. After that I'd check the vertical-bar detectors and use the per-class firing histograms to build templates from the data.

I'm tallying how often the horizontal-bar detector fires in each row for each digit class. The 0s fire fairly evenly across all four rows, the 4s and 9s peak at row 1, the 6s at rows 1 and 2, and the 7s again show that odd spike at row 1.

I'm going to rerun the loop detector with the lower threshold, along with the first horizontal-bar detector across rows 0 through 3, and scale their outputs so the numbers are comparable.
