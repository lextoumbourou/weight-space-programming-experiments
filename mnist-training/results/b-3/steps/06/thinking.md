The bias values are way off: class 4 is overpredicted by about 2.2, and class 8 is underpredicted by about 1.1. Since bias is so sensitive, it looks like the main problem. I could calibrate it from the confusion matrix by iteratively adjusting each class by the log of its true-to-predicted count ratio, and the predicted column totals are already in hand, with class 4 well above the rest.

Now I'm working out per-class bias corrections from the true-versus-predicted counts, using half the log ratio so the step stays moderate. Class 8 has a huge ratio, so I'm thinking about capping its adjustment.

I'm settling on a damping factor of about 0.6 with a cap of +1.3 on class 8, since its ratio is so extreme. Class 9 needs a notable bias increase, which makes sense because its main competitor, class 4, has almost no predictions left, so lowering 4 should help it too. I'm also noting that calibrating the biases is a short-term fix, and a stronger design will be needed for better discriminability.

I'm considering a zero-sum constraint on each row of the final layer's weights, though that's a loose idea I'll set aside for now.
