The loss has plateaued near 0.9, so I'm suspecting the logit scale is too soft and holding back even correct predictions. A quick scan with s=6 against s=4.5 might lower the loss, though I can't tell the margin needed without more data.

I'm weighing a shift-tolerant design that uses conv2's 5x5 kernels as local template matchers, with pool2 taking the max over small shifts. I'm also considering per-class part scores, though 16 channels can't cover all ten classes times their parts. The 5→8 confusion is the largest error, so I'll look at the 5 template more carefully.

I'm weighing whether the 5 template should lean harder on its upper-right and the 8's upper loop, since the 5→8 confusion is the biggest error. Gains only matter relative to each other, so I'd emphasize the upper-right area against the lower-right, keeping the left-side weights high enough to still separate 8 from 3.

I'm now considering explicit negative weights for each class, forcing regions that should be empty to be penalized. For the 5, that means the upper-right area, and the 3 and 9 would each get their own empty zones on the left side.

I'm adding per-class "hole" penalties, negative weights on regions that should stay empty for each digit, since that gives a strong explicit cue. Those positions would be specified in drawing coordinates and shifted with the same centering offset as the other templates.

I'm now setting up the negative "hole" penalties: a per-class map of gaussian bumps at the expected empty spots, subtracted from every orientation channel after normalization. For the 0, I'm placing the holes at the center.

I'm placing the hole penalties for each digit: for the 1, the empty spots fall in the top-left and bottom-right corners, which holds for both slanted and upright versions, and the 2 has ink in those areas that I want to penalize.

I'm listing where each digit's empty regions should be, like a hole at the mid-left for 2 and at the upper-left for 3, and I'm reading the upper-right gap for 5 and 6 as the place to penalize.

I'm sketching out per-class "hole" penalties, negative weights on the orientation maps wherever a digit should have no ink, and I'm setting the hole locations for the 8 and 9 cases before shifting them with the same centering offset as the other templates.

Next I'm turning the hole penalties into zero-sum maps, so each class's negative cue reads as contrast against the average rather than a bias toward overall ink, and then I'll set the scale at 0.08.
