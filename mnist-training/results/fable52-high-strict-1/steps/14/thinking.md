I'm at 78.7%, the best so far, with two steps left. Step 14 is an attempt at improvement, and step 15 is the final one: keep step 14 if it does better, otherwise resubmit step 13. I'm also noting the main confusions, mostly 2 versus 8 and a cluster of 9 mistaken for 7, 4, and 0.

I'm now going through the confusion pairs with their counts, like 2 to 0 and 6 to 0, and noting that the predicted totals are fairly balanced except that 0 is over by about 200. I'm weighing a low-risk bias adjustment for 0, and then looking at the 6-to-4 confusions, which have risen from 47 to 75 since OPENTOP was added.

I'm weighing a bias shift for class 4 against class 9, since 4 → 9 errors (124) far outnumber 9 → 4 (29), and I'm considering nudging the 4 bias up and the 9 bias down slightly.

I'm weighing a small bias bump for class 4 against 9, since 4→9 errors far outnumber 9→4, but I'd leave 9 alone to avoid pushing more 9s into 7. For class 3, the 3→5 confusions are twice the reverse, though a shift there could feed 2→3 and 8→3, so the gain looks marginal.

I'm weighing whether the remaining 3→5 errors come from the anti-strokes, since they were already around 111 before those were added, so I'm looking at what else might push 3s toward 5. One candidate is flat-topped 3s, which can light up the same top-bar features that drive 5 predictions.

I'm weighing a small bias shift for class 3 against 5, nudging 3 from -0.6 to -0.5 and 5 from 0.3 to 0.25. Then I'm looking at the 2 versus 8 confusion, which is balanced at 153 and 135, and wondering whether a feature separating 8's top loop from 2's top hook could help.

I'm now looking at the 2-versus-8 split again, and the center diagonal looks like the key difference: 8 has a stroke running from upper-left to lower-right through the middle, while 2 has none there. I'm considering an anti-stroke for class 2 on that center channel to separate them.

I'm checking whether a stroke running through the center from upper-left to lower-right would separate an 8 from a 2, since a 2 should lack that diagonal in the middle rows.

I'm checking whether a mid-row stroke running from upper-left to lower-right through the center would separate an 8 from a 2, since a 2 lacks that stroke while an 8 has it. I'm also wondering which other digits carry a similar center stroke, such as 3, 5, and 6, so the bonus doesn't push them the wrong way.

I'm checking the rest of the 2-versus-8 idea, noting that the mid-row diagonal is also present in 3, 5, 6, 9, and 0, so an anti-stroke for class 2 alone would be the safe choice. I'm still wondering whether some 2s with a curvy, Z-like shape could be penalized by it.

I'm wondering whether a loop at the bottom-left of a 2 would also produce a mid-row diagonal, which would blur the anti-stroke idea I was just considering for telling 2s apart from 8s.

I'm working out how a loop at the bottom-left of a 2 would show up as a short backslash segment in rows 19 to 21, which falls outside the center rows I was checking.

I'm settling on a pair of anti-stroke weights for class 2 along the middle diagonal, roughly -0.25 on each channel, since both see the same band and would otherwise double up. I'm also dropping the bias for class 0 by about 0.15, given how many confusions feed into it from 2, 6, 9, and 5.

I'm settling on a small bias bump for class 4 and a slight nudge for class 0, and I'm checking whether raising 9's hole requirement would separate it from 4 more cleanly.

I'm settling the bias for class 4 at 0.3, since the 4-to-9 confusions mostly come from closed 4s that already have a hole and can't be separated that way. I'm leaving the 9 weights alone and going ahead with the final test-set run, expecting similar accuracy.
