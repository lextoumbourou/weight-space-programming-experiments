I've hit 57%, a new best, so the forbidden regions with thin ink are helping. I'll push further by trying a slightly stronger κ of 0.2, adding more regions, and recalibrating the bias. The predicted counts are the next thing to check.

I'm checking how the 8-versus-2 confusion comes about: 8s are landing in 2's region because their left lower side is empty in 2's template. Widening 2's forbidden zone to cover that lower-left stretch might help separate them.

I'm checking the empty regions around 2 and 8: the lower-left and lower-right sides of an 8 sit where a 2 has no ink, so widening 2's forbidden zone there could separate them. I'm also considering extending 3's left-middle forbidden region to catch narrow 8s, though that may need a larger band.

I'm now looking at 5's forbidden region, which covers the upper right, and checking whether 3s hit it. Raising κ to 0.2 might strengthen that separation, and I'm also considering a forbidden band in the upper left of 3 to catch the 3-to-5 mix-up.

I'm widening 3's forbidden zone on the left to cover the upper-left and left-middle, and checking 8's sides at the waist against the 0 and 4 regions, since 8 is still absorbing images from several digits.

I'm checking the top-right corner, where 5's bar, 7's bar and 2's arc all reach, since 8's top loop leaves that corner empty.

I'm now working out the 2-versus-9 confusion: 2's base runs along the bottom, so 9's lower-left region should be forbidden for 2s, but the last row of cells falls mostly outside the grid.

I'm weighing whether to use different row windows for different channels, since the bottom crop cuts off the base of the 2 and that's why it gets mistaken for a 9. Using separate vertical taps for the ink and H maps might recover that bottom stroke without giving up the top.

I'm weighing whether separate vertical windows for the ink and horizontal-stroke maps could recover the bottom of the 2's base, which the crop currently cuts off, without losing the top strokes.

I'm weighing whether the top crop or the bottom crop costs more: the bottom cut removes 2's base and the bottoms of 6, 8, 0, 3 and 5, while the top cut removes the 7 and 5 bars and the top arcs of 2, 3, 9 and 8. A separate vertical window for the diagonal map might keep both sets of strokes.

I'm weighing whether the bottom crop or the top crop costs more, and I'm considering a split: keeping the ink and vertical maps on the upper window while moving the horizontal-stroke map to the lower window, so the base of the 2 comes back, and that would mean rasterizing the horizontal template in its own frame.

I'm weighing whether to rasterize the horizontal-stroke template in its own lower frame, centered at 3.5, so the 2's base lands within the grid. The base currently sits right at the edge of the window, so I'm checking whether it would show up enough to justify the extra complexity.

I'm working out whether the lower window could recover the 2's base. It lands at the edge of the grid, so it only helps a little, and I'll accept that the digit's full height won't fit in 8 cells.

I'm working out how to get the bottom rows of the grid into view without losing the top: several conv taps could read different 4-pixel bands, which would cover the whole digit across distinct windows.

I'm weighing a mix of row taps: one set of channels reading rows 4–7 and 8–11, then the next pair shifting down, which would spread coverage across the whole digit at the cost of some duplicated bands.

I'm weighing whether to use the full 5-band vertical coverage, which would show the whole digit at the cost of some duplicated bands. I can't afford many more experiments, so I'm judging whether the extra row coverage is worth the loss in resolution.

I'm weighing whether to drop the diagonal features and give the bottom rows their own ink map in a lower window, since that could recover the base strokes that the current crop removes.

I'm considering a bottom-covering ink map, since it might matter more than the diagonal features. Its new rows would only come from the lower window's last taps, so I'd use just those and leave the duplicated rows out.

I'm extending the ink grid to 10 rows by pulling rows 8 and 9 from the lower window's last taps, which cover input rows 20 to 25 and so reach the bottom of the digit. The top row of the digit still falls just outside the grid, so I'll rasterize the template with its center at 4 to line it up with that layout.

Still working out the rows: I'm making the lower window's last taps feed the two new rows of the ink grid, and planning to give those channels their own template placement.

Still writing the convolution weights for the ink channels...

I'm listing the forbidden regions for the remaining digits, with thin-ink boxes for 2, 3, 4, 5, 6 and 7 in the unit frame.

I'm now setting the forbidden regions for 8 and 9 on the ink grid, with the bottom-left corner marked off for 9. The mask will zero out its own ink template across all 10 rows. Then I'm recomputing the bias compensation at κ = 0.2 and setting the new bias values for each digit, starting with 0 through 8.

Writing the code now...
