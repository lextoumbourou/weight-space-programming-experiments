The bias is very sensitive: shifting it by 0.05 seems to move the dog probability by about 16%, going from 63% dog at 1.55 to 46.5% at 1.75. That means the logit difference is spread fairly narrowly, so the logits are small in scale, and scaling them up might lower the loss without changing accuracy. The best so far is 0.6456, with a slight cat lean at 46.45% dog.

I'm weighing whether to try a darkness feature for the cat side, since black cats often show up darker. Its weight would move the logit by a lot, so the calibration would be rough and would need a recheck next step. I'm also considering a structural change: separating center and border features, since the animal tends to sit in the middle while the border mostly shows background.

I'm going to scale the whole classifier up by 1.3x and adjust the bias to keep the cat lean, which should mainly show up in the loss calibration. I'll leave the whiteness weight alone for now so the change is easier to attribute.
