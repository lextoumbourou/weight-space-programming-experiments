The pairwise boost did badly, with loss rising to 1.93. The template differences seem to point the wrong way, since amplifying them inflates the scale and skews the outputs, so I'll go back to step 6. I need a more fundamentally different approach to get any further, and I'm weighing pixel-level template matching at a reasonable resolution, with the network working as a nearest-mean classifier over blurred ink. One thing I'm considering is using conv1 as a 5x5 blur kernel for that.

Still working out how to sample pool1 at distinct offsets across 16 conv2 channels, so each pooled cell reads a different block of the blurred ink map.

Still working out how the conv2 channels should tap pool1 at offsets, so that the 4x4 cells each read a different window of the blurred ink map.

Working out how the 8x8 grid comes out of the conv2 taps: each cell is a max over a 4x4 input window at stride 2, so the centers land across roughly pixels 4 to 21. Next I'd spread four conv1 feature types, each over four phase channels, to fill the 16 conv2 channels at that resolution.

Templates blurred around sigma 2.5 px should still tolerate misalignment, though a finer grid doesn't obviously win on its own. The real limit is the hand-drawn prototypes, which probably fall short of a true class-mean HOG template that might reach around 85%.

Thinking about where the pattern breaks down: the structural features helped, but several digit pairs still fail, such as 7 versus 9, 2 versus 3, and 3 versus 5. I'm considering whether a 4x4 feature spec would give more reliable distinctions for those confusions.

I'm weighing the 2 versus 3 distinction at the 4x4 level, where the bottom-left and bottom-right regions seem to separate them most clearly.

I'm considering whether a cleaner way to see what matters is sharper templates, maybe with a smaller blur, though I'm not sure that helps. Calibration might also be the issue: the loss is high at 69% accuracy because the model is overconfident on its mistakes, so lowering the global scale could reduce loss even if accuracy stays the same, and that matters since the final selection uses the lowest training loss.

I'm weighing whether to scale all the weights and biases down by about 0.7 as a pure calibration test, since the loss is high even though the argmax wouldn't change. That would tell me the best temperature before I try any new features.

I'm going to keep the calibration test pure: scaling the output layer by about 0.7 shouldn't change which class wins, so accuracy should stay at 0.6913 while only the loss moves.
