Now I'm checking the model's accuracy at 77%, with four steps still to go. The predicted totals are spread across all ten digits, and digit 3 is the most frequently predicted. The biggest mix-up is 8 being read as 3, followed by 8 as 2.

Now I'm weighing the remaining confusions, especially 8 read as 3 and the over-predicted 3s. The fix I'm considering is raising the bias for 8 and lowering it for 3, and checking whether the left-side ink can tell the two apart.

Now I'm working out how to separate 3 from 8 using where the ink sits on the left side, testing whether a location-specific rule for 3 in the left columns would help.

Now I'm checking whether a location-specific rule could tell 3 apart from 8, since 3's open upper cavity might pick up stray ink on the left side.

Now I'm looking at whether the left-side strokes can separate 8 from 3: 8's loops have walls on the left in the upper and lower halves, while 3 has no stroke there, so I'm testing that as a vertical-band check.

Now I'm weighing a bias shift for the two classes: nudging 8 up and 3 down by roughly 0.3 each, since 8 is under-predicted and 3 is over-predicted.

Now I'm reconsidering the bias values, moving 8 up by about 0.4 and pushing 3 down further, since 3 is over-predicted and 8 is under-predicted. I'm also weighing whether to loosen the HOLE requirement, because it helped 7 and 2 but cost 8 some correct predictions.

Now I'm tuning the bias values: 9 looks under-predicted and 7 over-predicted, so I'm nudging 9 up a little and 7 down. I'm also looking at 6 being mistaken for 4, which is new and suggests the open-top rule is firing on 6's upper stroke.

Now I'm checking whether the open-top rule might be firing inside a 6, since the stem and loop could leave a gap that looks like an open column.

Now I'm checking why the open-top rule might be pushing 1s toward 4: a single thick stroke shouldn't leave two separate wall hits eight pixels apart, so I'm trying to pin down which other change could explain the jump.

Now I'm working out how to pull the 4 threshold back, weighing a stricter open-top requirement against losing real 4s, and settling on a middle value.

Now I'm going through the remaining bias tweaks for the 2, 3, and 5 classes, noting that 2 needs a small boost and that the 3 and 5 confusion is symmetric, so I'm looking at whether orientation-based weights could separate them.

Now I'm assigning the vertical-stroke windows for the 5 template, placing its column near 10 after a small shift, and checking which channel taps land there.

Now I'm assigning the vertical-stroke anti-weights for class 5 near the top-right, since 3's upper arc is the only real stroke there.

Now I'm working out the anti-stroke weights for 3 and 5 at the top of the image: a negative weight on the vertical column near the top-left for class 3, and one near the top-right for class 5, each around half the size of the template weights.

Now I'm looking at the lower-left stroke as a way to separate 8 from 3, since 8's bottom loop has a left wall that 3, 5, and 2 lack, while 6 and 0 also have one.

Now I'm adding the extra lower-left stroke weights: a penalty for 3 and 5 there, a smaller one for 2, and a bonus for 8.

Now I'm sketching weights for the lower-left stroke: rows 2 and 3 in the vertical channels, column 1 for channel 2 and column 0 for channel 3. The reasoning is that 8, 0 and 6 have a left wall there while 3, 5 and 2 don't, so I'm adding a penalty for the latter and a bonus for 8.

Now I'm assigning anti-stroke penalties for the upper-left column: 3 gets the strongest, 2 a lighter one, since its hook start is only diagonal there.

Now I'm checking the upper-right stroke for each digit: 2, 9, 4, 0, 8, and 7 all have a vertical wall there, while 5 and 6 don't, so I'm penalizing 5 there and lightly penalizing 6.

Now I'm setting the bias values and the extra anti-stroke weights for the 3 and 5 classes, planning to apply them after the main weight loop.

Still writing the anti-stroke weight list...

Still writing the extra weight list...

Now I'm checking whether a vertical stroke near the bottom of the window in the 5 template might be overlapping the lower-left window and skewing the penalties.

Now I'm settling on the final bias values and the extra anti-stroke weights for the 3, 5, 2, 6 and 8 classes, and I'm also adjusting the hole weights for 8 and the open-top threshold for the code I'm about to write.
