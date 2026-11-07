Accuracy fell, most likely from the gamma 0.3 change or the bias step, while the alpha change lowered the loss. I'm planning to go back to gamma 0.5 and keep alpha at 1.5 or higher, possibly 2.0. The step-7 bias was computed from the step-6 weights under gamma 0.5, so it should still hold, and I'm also wondering whether to try gamma 0.7 for the other direction.

I'm weighing gamma 0.7 as the other direction, since 0.3 may have been what hurt accuracy. Alpha 2.0 shouldn't shift the predictions, but the bias was calibrated for gamma 0.5, so a gamma change could move things regardless.
