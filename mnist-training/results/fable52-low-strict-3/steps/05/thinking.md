The cues seem to be pushing too hard: the model now over-predicts 3 and 9, so the sharp V cues at ±0.8 look large next to the logit gaps. I'll scale them down. Next I'm looking at the 3 cues, since the ones for (2,3) and (1,3) are pulling 2s toward 3, and I need to separate 2 from 3 before adjusting further.

I'm settling on a smaller set of 3-cue weights, with the upper-right bonus shared between 2 and 3 so it no longer favors 3, and I'm checking whether a lower-left diagonal could separate the two digits.

I'm weighing the 3 cues against 5 now: the belly bonus at (2,3) might help 5 stay separate, and lowering the 5 bias a bit should keep it from losing ground.

I'm now weighing a 7-versus-9 split: the 9 cues on the upper right and the bias are rewarding 7-like shapes, so I'm considering trimming those weights rather than adding to the 7 side.

I'm tuning the 9 and 7 cues next: trimming the 9's upper-right and corner weights, adding matching upper-right and inner weights to the 7, and dropping the 9 bias a bit. For the 0s, I'm thinking the center cells aren't firing enough, so I'll raise the bias to 3.2 and the scale to 2.5, since 0 has few false positives to lose.

I'm working out whether the center cells really stay empty for the 0s, since the narrow strokes may still land in the 10–17 column range the filter covers. A tap at a specific offset could give a cell that spans only columns 12–15, and I'm thinking about how the vertical extent of the hole would be handled across the rows.

I'm checking whether a tap at a fixed x-offset could give a cell covering only columns 12–15, which would catch the center without picking up the narrow strokes of the 0s, while the y-taps keep the standard row grid. Other digits like 1, 7, 4, and 9 do have ink in that region, so the center-cell idea still needs testing against them.

I'm testing a narrower center channel: a tap at a fixed x-offset would cover only columns 12–15, which should avoid the narrow strokes of the 0s. The new bias and gain would need to balance against single-crossing digits like 1, so I'm weighing a higher threshold.

I'm tightening the center-cell idea for the 0s: I'll set the bias to 3, the gain to 2.5, and keep the channel's threshold high enough that a single-crossing 9 doesn't get pushed toward 0. For the 6s, I'll lower the bias to -0.1, since the 6-versus-8 confusion comes from the upper-right side of the 8's top loop.

I'm adjusting the bias for digit 8 downward to -0.3, since it's already getting over-predicted. I'm also lowering the 9 bias to 0.2 and the 5 bias to 0, because 5 is leaking into 3 and 8.

I'm going to try a gain change later, once the bias and cue adjustments are settled.
