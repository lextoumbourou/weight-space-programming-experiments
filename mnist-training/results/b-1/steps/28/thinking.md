I'm checking the loss at 0.85, which is 0.872, and I'll try 0.7 later. Comparing against the values at 1.0 and 1.2, the slopes between those points look like they're increasing, so I'm fitting a parabola through the three points to locate the minimum.

The derivative estimate is pointing to a negative minimum, which isn't physically sensible, so the parabola fit isn't reliable here. The loss is still dropping, so I'll test a lower temperature of 0.65 and pair it with an image-template tweak for the digit 5, keeping both if the loss improves.

I'm weighing whether to lean on the upper-left region, but that's hard to target directly. The 4-to-9 and 9-to-4 confusions are worth a look too. I suspect the representation is capping accuracy near 73%, and getting past that likely means features that capture stroke endpoints or open sides, since the 3-versus-5 decision hinges on the difference between their weight vectors.

I'm weighing whether tweaking the 5 template would help, since real 5s often have a disconnected top bar, but I'm inclined to accept the accuracy ceiling for now. The loss is the thing I can still work on, so I'm considering lowering the global temperature and possibly softening the overconfident hole-rule logits, since both would scale down the confident errors.

I'm separating the temperature for the hole rules from the one for the template part, and I'm going to try a global temperature of 0.7 and compare the hole scale next.
