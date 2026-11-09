I'm at 75.0% with five steps left, and I'm tallying the predicted totals for each digit along with the main confusions, like 7 being read as 9 and 2 as 8 or 0.

Now I'm going through the confusion pairs for the remaining digits, mainly 8 being read as 3 or 2 and 0 as 6, and checking the modest gains from the RTIP changes. The 2 class is still the weakest, with most of its errors going to 8 and 0, so I'm weighing whether a bigger bias on 2 would recover enough correct predictions to justify the extra false positives.

I'm comparing 2 against 0 and 8 by where the strokes sit: 0 has a left wall through the middle rows and an empty center, while 2 has neither on the left and instead has a bottom bar reaching the right corner. These orientation differences should show up in cosine templates, but my 8-pixel windows are too coarse to capture them well.

I'm considering a generic feature for ink at the image center, since 0 has no ink there while 2, 3, 5, and 8 do. That should help separate 0 from those digits, but 2→0 errors at 141 suggest the center signal alone isn't what's driving the confusion.

I'm weighing whether 2's bottom-left loop and the orientation of the strokes around the center make it look like 0 in the cosine templates, since the oriented-stroke windows in both digits overlap at the same rows. With only five steps left, I can't probe which feature is actually driving the 2→0 errors.

I'm weighing which conv2 channel to give up for a new center-ink channel, since 0 is picking up a lot of false positives from 2, 6, and 9 and misses about 175 of its own. CUP looks like the candidate, since it was only meant for 4 versus 9 and that confusion barely moved, though the orientation channels are another possibility.

I'm weighing whether a center-ink feature could help separate 0 from 6, since 6's loop sits lower in the digit, and I'm wondering if the 0-versus-6 errors come from a loop-at-the-bottom pattern on the 0 side.

I'm weighing whether to shift the bias on 9 down to cut its overprediction, since it's predicted 1190 times against 961 true, and 7 and 4 keep bleeding into it.

I'm weighing the 7-versus-9 trade-off and noting that shifting biases gives diminishing returns, so I'll need actual features to make progress on 4 and 9. I'm wondering whether the narrow-top template for 4 is being suppressed by the side-inhibition windows when the two arms sit close together.

I'm checking whether open 4s fire the narrow-top template at two columns, since the arms are usually too far apart for side inhibition to suppress them. I'm also weighing the difference between 4 and 9 at the top: 9's loop is closed and 4 is open, so a cup-shaped feature might separate them if the empty space above the loop is enough to count.

I'm thinking about making the CUP feature stricter by shifting its layout down a row so it requires a wall below the center, which would stop it from firing on closed 9 loops. The problem is that the kernel only has five rows, so the bottom wall would have to sit right at the edge of the window and would only match about half the time.

I'm sketching a version of the CUP feature with the walls at the bottom and a clear vertical channel above the center, so it fires on open 4s but not on closed 9 loops.

I'm working out whether a center-stripe check on the 4 template could be made stricter by using a vertical open channel above the bar, with the walls on either side. That should fire for open 4s and stay silent on closed 9 loops, since the empty space above the center falls outside a loop of that height.

I'm working out a stricter version of the open-channel check, where a column of cells above the center must all be empty, using a linear "no ink" term per cell so that stray strokes count against it.

Now I'm sketching an open-top channel built from a column of empty cells above the center, with a loose ink check on each wall, so it fires on open 4s and stays quiet on closed 9 loops.

I'm trying to make the open-channel check stricter by requiring the column above the center to be empty, using a strict no-ink term per cell, so that a 4's narrow cup still passes while a closed 9 loop fails.

I'm sketching an open-top channel, a column of empty cells above a center point with walls on both sides at the bottom, that would fire for 4s with a narrow cup and stay quiet on 9s because the top arc crosses the column. It would also fire on 0s, but since 0 has no bottom bar, that doesn't matter for this group, so I'd use it to replace the CUP feature for the 4-versus-9 split.

I'm checking whether the open-top channel would also fire on 9s that have an open top, since the same empty-column test might pick them up too.

Writing the open-top channel feature into the 4-versus-9 check, and fixing its center cell's row and column placement against where the 4's cup bottom should land.

I'm sketching an open-top channel for the 4-versus-9 split, a column of empty cells above a bottom point with walls on both sides, which should fire for 4s and stay quiet on 9s because the top arc crosses the column. I'm weighing how to weight the cells and where to place them so the 4's cup lines up with the kernel.

I'm sketching a feature for 7 versus 9 that checks for an empty block to the left of the stem, since 7 leaves that space open while the loop of a 9 fills it with ink.

I'm checking whether an empty region to the left of the 7's stem can separate it from a 9, since the 9's loop fills that space. The open-left feature I had already fires on 9s because its lenient check at the left still passes when the loop is wide enough, so I'm weighing how to make the empty area to the left wider and stricter.

I'm working out a feature for 7 versus 9 that uses a wide empty area under the bar, since a 7 leaves at least eight pixels open there while the inside of a 9's loop is narrower.

I'm checking an empty strip four pixels under a horizontal stroke, which should separate a 7 from a 9. Since the bar in a 7 is only about eight pixels wide at that depth, I'm considering a shorter four-cell version of the empty-row check.

I'm trying to separate 7 from 9 with an empty strip under the bar, since a 7 leaves about eight pixels of clear space there while a 9's loop interior is narrower. The problem is that a 9's loop might still pass a three-cell check at its edges, so I'm weighing how tall the empty area needs to be to rule it out.

I'm working out a feature called UNDERBAR for the 7-versus-9 split, checking for a strict ink cell above a vertical empty column. Since a 9's loop wall would cross that column, it should fail for 9s while a 7 keeps the space to the left of its stem clear.

I'm checking whether a strict ink cell right under a horizontal bar, followed by a stack of empty cells below it, can tell a 7 apart from a 9, since the 7's clear space under its bar is wider than the loop of a 9.

I'm settling on a bar-and-clear-column check under the bar: one ink cell at the top, then three empty cells stacked below, so a 7's open space under its bar passes while a 9's loop wall crosses the column.

I'm checking whether a strict ink cell at the top plus a stack of empty cells below it could separate 7 from 9, since a 9's loop bottom wall lands inside that column for taller loops and only partly passes at the edges.

I'm settling on an underbar check for 7 versus 9: one strict ink cell at the bar, then a stack of empty cells below it, and I'm weighing whether adding a few more empty cells across the far row would keep the loop's bottom wall from slipping through.

I'm checking whether an ink cell in the bar plus a stack of clear cells below it can single out a 7, and I'm noting that the 7's HOLE feature is firing more often than it should, so I want to see which neighboring cell is catching the serif on the bar's left end.

I'm thinking about adding a strict ink requirement at the bottom-left diagonal cell, so that a 7 with a serif, which is open there, no longer passes the hole check while a 9's loop closes off that corner.

I'm weighing a single loose-ink cell at the lower-left diagonal to tell the 7's open corner from a 9's loop arc, since the arc would hit that spot and the serif-7 would leave it empty.

I'm weighing whether to add loose-ink checks at all four diagonal corners of the hole detector, since a closed bottom-left corner might separate a 9's loop from a serif 7, and the same tighter corners could cut false positives on 2, 3, 4 and 5.

I'm now treating the HOLE detector as an eight-direction ring, requiring ink at all four diagonal corners too, since that should keep open shapes from passing while a real loop still registers. I expect the closed digits to hold their accuracy, with the open-shaped ones losing some false positives.

I'm weighing whether tightening the hole detector into an eight-direction ring with loose diagonal checks would cut false positives on the open digits while keeping real loops intact. I'm estimating the HOLE weights for 7, 4, 3, 5, 0 and 2 against that change, though a strict requirement could also reject genuine holes if the alignment slips.

I'm turning the hole detector into an eight-direction ring, with loose checks at the four diagonal corners so open shapes stop passing. I also want to swap the cup check for an open-top check for the 4s, then nudge a few biases, 9 down and 2 up. That's two detector changes at once, so if accuracy drops I'll revert them one at a time.

I'm working out an open-top check for the 4s: strict empty cells across the middle of the column, with loose ink at the left and right edges, so the 4's open top passes while a closed loop does not.

I'm checking whether the open-top test for the 4s holds up, since five empty cells down the middle plus the grazing walls might add up to zero even for a real channel, so I'm trying a version with fewer empty cells.

I'm settling on a four-cell clear column below the midline, with loose ink at the left and right edges, so a 9's loop wall or a graze from the top bar would fail it. I'm also softening the threshold so a narrow 4 with a slight wall graze still passes.

I'm settling on the open-top check for the 4s: a clear column below the midline with loose ink on each side, and I'm estimating a bias that gives roughly 1.0 for a channel at least four cells wide. I'm also setting the cup-bottom placement at row zero for the 4s, with a +1.3 weight on those cells.

I'm settling the open-top check for the 4s: a few clear cells down the middle of the column with loose ink on each side, and a per-class adjustment that gives the cup-bottom placement a boost for the 4s while pushing 9, 7 and 1 down in the same rows.

I'm changing the hole detector to an eight-direction ring with loose checks at the diagonal corners, and I'm also dropping the old cup feature in favor of an open-top check for the 4s.

Now I'm writing the code for the updated hole detector and the open-top check.
