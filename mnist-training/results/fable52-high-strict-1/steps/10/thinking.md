The accuracy has climbed to about 72%, with six steps still to go. Next I'm going through the remaining errors, starting with the predicted totals per class and the biggest confusions: 7 predicted as 9 and 4 predicted as 9, with 9 being over-predicted overall, plus 2 mistaken for 0.

Next I'm working through the remaining confusion pairs, where 2 is the most frequent source of errors, and 6, 5, and 8 each show their own major mix-ups. I'm also checking why 0 is over-predicted, with many 9s, 7s, and 2s being labeled 0, and whether the BOT feature is failing or 0's score is simply too high.

I'm now checking whether the 0 over-prediction comes from the cell-level features. A feature that fires across several cells adds up, so one feature can push a score well past what it should contribute, which is a broader weakness in how the evidence is combined.

I'm tuning the SLOT feature so it only counts when it fires broadly across many cells, since a real 0 has a large interior. Using a weight of about 0.5 per cell with a threshold near 1 would give real 0s a modest boost and keep partial firings from adding much. I still need to decide whether to keep the current −0.3 class bias for 0 once SLOT is recalibrated.

I'm recalibrating the SLOT weights to a scale of about 0.6 per unit with a threshold near 0.9, so a real 0 with a broad firing still gets a clear boost while weak partial firings contribute close to nothing.

I'm settling on a recalibrated SLOT scale, around 0.6 per unit with a threshold near 0.9, so that real zeros with broad firing still get a clear boost while partial firings contribute almost nothing. I estimate a real zero's summed SLOT activation at roughly 2 to 5, which that scale would reward without letting weak firings push the score too high.

I'm looking at how the 7 and 4 errors toward 9 interact with the features: 9 usually shows a hole at the top and a loop on the left, but 7 also trips the loop checks often enough to get pulled toward 9. I'm going to check whether an orientation template can separate them, since the raw feature rates overlap too much.

I'm comparing 7 and 9 on whether the loop's left wall is present: a 9 closes a loop on the left around rows 9 to 15, while a 7 has nothing there below the bar, so that open left side might separate them more reliably than the raw feature rates.

I'm now looking at the left side of the 7 and 9 shapes: a 9 has a closed loop on the left around rows 10 to 15, while a 7 has nothing there. I'm checking whether vertical and diagonal stroke channels at those left columns could be used as a negative signal for 7.

I'm checking whether a 9's left loop wall, around column 8 in rows 9 to 15, is absent in a 7, since a 7's stem sits far to the right and only a serif at the bar's left end might reach that column.

I'm weighing whether an open-right cavity test can separate 7 from 9: 9 has one inside the loop's left end, while 7 shows it only about a third of the time, so forbidding it for 7 could help.

I'm weighing whether an open-right cavity can separate 7 from 9, and whether to tighten the bias so 7 gets a boost and 9 gets pulled back.

I'm checking the remaining 2 errors next: 2 leaks into 0, 8, 9, and 3, and I'm looking at whether the top-left and bottom-right open-stroke features are letting that happen.

I'm checking whether a flat bottom stroke with a right-pointing tip can tell 2s apart from 8s and 0s, since many 2s have a loop at the bottom-left that confuses those features. I'm also considering lowering the bottom-stroke weight for 2s so it stops pushing them toward 9.

I'm now checking whether a horizontal stroke detector can separate the flat bottom bar of a 2 from the curved bottoms of 3, 5, 8, 0, and 6: a 2's bottom bar has empty space both above and below its right half, while the other digits curve up at the bottom right.

I'm testing whether a horizontal-stroke detector can isolate the flat bottom bar of a 2 from the top bar of a 7 and the bar of a 5, by checking for ink with empty space above and below it.

I'm checking whether a horizontal-stroke detector can tell a 9's top arc apart from the bars of a 7 and 5. The worry is that the loop under a 9's top arc would look empty below it, the same as an isolated bar.

I'm checking whether a 9's top arc would look like an isolated horizontal stroke, since the loop beneath it could leave empty space above and below the arc's apex. Then I'm looking at how the arc's left side, a few pixels over, responds to the same kind of horizontal detector.

I'm checking whether a bottom-bar detector would also fire on the curved bottoms of 0, 3, 5, 6, and 8, since a wide arc can look locally flat over a few pixels.

I'm checking whether a right-tip detector, looking for ink that stops at the right end of a bottom bar with nothing beyond it, could tell a 2's flat base apart from the upward-curving bottoms of other digits.

I'm checking whether a right-tip detector could separate the bar ends of 2s from those of 5s and 4s, since a bar end pointing right with nothing beyond it should fire for 2s at the bottom, 5s at the top, and 4s in the middle.

I'm checking where the right-tip kernel should sit so it catches the 2's bottom bar, which at rows 20 to 22 falls inside the lower band, and I'm thinking about whether moving the tip row lower would cover bars that sit a little further down.

I'm weighing whether a right-tip kernel placed lower, at kernel row 3, could catch a 2's bottom bar, but then the top-right tips of 5s would fall outside its reach. Covering both would take two separate kernels, and I'm deciding whether to swap out an unverified channel or the slot channel to make room.

I'm checking whether a right-tip kernel placed higher could catch the top-right end of a 5's bar as well as the bottom bar of a 2, since one kernel row can't cover both.

I'm settling on a single right-tip channel and reading its response by row: the top bar of a 5 at kernel row 0, the bottom bar of a 2 at row 3, and the middle bar end of a 4 at rows 1 or 2.

I'm checking where the right-tip reading lands for each class: the kernel should give a strong response at the 2's bottom bar and the 5's top bar, with the 4's middle bar end in between. The main risk is 6's upward-pointing top stroke, which could look like a tip, though its narrower top should separate it from a 5's wide bar.

I'm weighing the right-tip detector as a replacement for the unverified top-tip channel, since a bar end pointing right with an empty beyond-column should separate 2s and 5s from other digits. The detector is still untested, so the beyond-column check needs to hold up in practice.

I'm weighing a right-tip detector for the 2's bottom bar and the 5's top bar, though its flick-up risk could cut the response. I'm leaning toward giving it moderate weight rather than spending one of my remaining steps on a probe.

I'm weighing a bias adjustment for the 6 and 0 confusion: 6 is being predicted as 0 more often than the reverse, and the SLOT recalibration may be weakening 0's response, so I'm considering setting 0's bias to zero.

Next I'm tuning the classifier: softening the SLOT recalibration, swapping the top-tip channel for a right-tip detector, and adjusting a few class biases.

Next I'm adjusting the biases: nudging 2 down a bit, then raising the weight that rules out 9 for 7s and 9s, and tightening the forbid term for 7s.

Writing the right-tip channel kernel now...

Writing the right-tip channel kernel now...

Next I'm switching the SLOT channel to a lower weight and tuning its threshold, and I'm setting the per-point bias for each located channel so the slot detector contributes less to the overall score.
