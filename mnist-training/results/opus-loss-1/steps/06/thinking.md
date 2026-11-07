The ring feature's expected magnitude looks too high: loop digits 6, 8 and 9 are now under-predicted, though 4 and 5 improved, so the feature still carries useful signal. I'm checking whether it fires weaker than 1 in the data.

I'm working out the ring template's magnitude: at 1.0 the bias penalty on loop digits is too large, so I'm testing a much smaller expected value, around 0.3 to 0.4, and seeing whether a less strict ring detector helps.

I'm settling on a ring bias of -2.0 instead of -2.5, so the detector fires more often, and a ring template strength of 0.5, which keeps the penalty for loop digits near one logit while still giving a useful gain. The step-5 bias corrections stay in place, and the loss rising to 1.30 suggests the model is overconfident, which I'm fine with for now.
