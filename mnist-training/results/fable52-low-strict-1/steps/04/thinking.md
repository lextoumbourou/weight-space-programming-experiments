Next I'm adjusting the templates for the confused digits. The 0 template seems too narrow: real MNIST zeros are wider and rounder, so I'm considering widening its horizontal radius to around 0.36, and the 6 template may need a stronger loop in its lower part.

I'm now considering negative strokes in the templates, so that features like the 0's right-side stroke actively suppress the 6, and a horizontal bar at the top suppresses the 9 for the 4. I'm also weighing a slanted "/" 1 template alongside the vertical one to better match the slanted 1s that get confused with 2s and 7s.

I'm fixing the 4 template by adding a negative horizontal stroke across its top, so it suppresses the 9 pattern. For the 5 and 6 pair, I'm weighing negative strokes on each: a left-lower vertical for the 5, and a right-upper vertical for the 6 to counter the 0. For the 2, I'm thinking about its lower-left loop and base, and a negative in that area to separate it from the 3.

I'm adding a negative vertical stroke on the upper-left of the 7 template to separate it from the 9's left loop, and I'm considering a middle horizontal negative as well.

I'm thinking about making the negative strokes orientation-agnostic, so a "no ink here" blob deposits into all four orientation channels, and I'm considering a 9 negative in the lower-left as the first case to implement that way.

I'm now listing the negative strokes for each digit template: an empty-centre blob for the 0, a lower-right stroke for the 2, and a left-side stroke for the 3 to separate the 5 and 8 patterns.

I'm also giving the 4 template an oriented negative horizontal stroke across the top, between the arms, so it doesn't fire on the 9 pattern. For the bottom-left of the 4, I'm placing an all-orientation negative blob, since that region should suppress the 2 and 8 patterns.

I'm adding negative strokes for the remaining digits: a lower-left blob for the 5, an upper-right vertical that suppresses 3, 8 and 9, and an upper-right stroke for the 6 to counter the 0. For the 7, I'm putting a negative in the upper-left, plus a lower-right one.

I'm settling the negative strokes: a centre blob for the 0, an oriented horizontal stroke at the top of the 4, and all-orientation blobs in the lower-left of the 9 and a few other spots. Each negative gets subtracted from the weights with a fixed κ, while the centring is still computed from the positive strokes only. I'll also widen the 0 template and consider a slanted 1 variant.

I'm going to code the negative strokes now, with "all" blobs depositing into every orientation channel at a weight of 0.7, and the same shear applied to them as to the positive strokes.
