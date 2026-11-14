I'm at step 49 with a best score of .3688 and one step left. I'm weighing a final small tweak in the opposite direction of step 48, lowering GAMMA and ALPHA by about a third of the earlier change, on the assumption the loss is locally linear.

I'm considering a small step in the opposite direction, but a parabola fit suggests both directions would hurt near the optimum, so it's risky though harmless. I'm also looking at the per-class bias errors, where class 2 seems to over-attract, and shifting its bias down by about 0.1 might net a few more correct predictions.

I'm weighing whether to combine a bias tweak, lowering class 2 by about 0.08 and raising classes 0 and 1 slightly, with a GAMMA/ALPHA reduction. The bias change looks like the safer bet with a small positive expected gain, while the GAMMA/ALPHA direction is uncertain.

I'm reasoning that a small decrease in GAMMA and ALPHA probably helps a little if the loss is smooth, since the last increase made accuracy worse, though it could be flat at a minimum. I'm planning to combine that with the bias adjustment and settle on GAMMA 0.52, ALPHA 4.85 alongside the per-class bias shifts.

I'm settling on the final tweak: GAMMA 0.52, ALPHA 4.85, plus per-class bias shifts, and I'll keep the rest as in step 49. I'll check the earlier step 47 and 48 tweaks again, since their results were mixed, but they're confounded so I'm treating them as only a rough signal.
