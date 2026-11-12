The 8 predictions dropped to 320, so the loop templates for 8 may be set too high compared with the features that actually show up, and that mismatch is drawing a penalty. The detection rate is low. Its ink features shifted only because the ink offsets were reduced. In a nearest-centroid setup with a constant penalty, I'm now looking at a feature whose expected value is 0.9.

I'm weighing whether the loop features should carry their own weight instead of feeding into the bias through the template norm. The penalty for the loop channel comes to roughly 0.78 logits at step 19, which is large enough to explain why 8 is losing out. So I'm considering reverting to step 19 and decoupling the loop weights, letting positive weights favor the loop classes and small negative weights handle the rest.

I'm now weighing decoupled loop weights rather than letting the loop templates push the bias through their norm. The idea is to give loop classes a positive weight proportional to their templates, about 1.5 logits per fired loop, with no penalty, and leave the other classes at zero weight for now.

I'm dropping the loop bias for 8 and instead using step 20's bias corrections, lowering 8 by 0.4 and 9 and 6 by 0.2 each.

I'm dropping the loop bias for 8 and using step 20's bias corrections instead, lowering 8 by 0.4 and 9 and 6 by 0.2 each, since their loop penalty is gone and they'd otherwise get boosted.
