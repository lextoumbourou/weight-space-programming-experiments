I'm working through the remaining pairs in the transition table, having already ruled out 7↔9 at 80.0%, and I'll write the answer in the same style.

I'm weighing the class-4 and class-0 adjustments now: penalizing a sharp top bar and the bottom bar for 4, and adding a bottom-bar weight for 0 to counter the 7→0 confusion.

I'm now handling the 0→6 and 0→8 confusions: giving class 6 positive weight on the mid-height horizontal stroke in the left-centre cells with a negative bias, and giving class 8 a weight on the centre-crossing cells.

I'm settling on the centre-ink cue for class 6 as well, so that both 6 and 8 need ink in the middle cells, with a negative bias. That should push the 0-images that were leaking into 6 and 8 back toward 0, since narrow 0s may still carry some centre ink and I need to check that case.

I'm turning to the 2-versus-3 and 3-versus-5 confusions: the earlier softer weights only reduced those errors partly, so I'll restore them to stronger values. For class 8, I'm leaning on the centre-ink requirement, though the bias needs tuning so it doesn't over-suppress 8.

I'm moving on to the global scaling idea: multiplying the output-layer weights and biases by about 1.3 should leave accuracy unchanged while lowering the loss if the model is underconfident, so I'll test that at this step.

Adjusting the class-4 bias with negative weights on the top and bottom rows, then giving class 0 a bottom-row cue and class 6 and 8 a centre-ink requirement.

I'm settling the last tweak: a short closing pass on the output weights before I stop.
