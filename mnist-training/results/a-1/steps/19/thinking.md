I'm at 73.6% accuracy with a loss of 0.90, and the best loss so far is still 0.887 at step 15. I think the scale factor s could be tuned to bring the loss down, so I'll try some variations of it later. The main confusions are 5→8, 3→5, and 8→3, with a few others trailing behind.

I'm thinking the 8 template is the problem: it has no endpoint weights, so 5s get mistaken for 8s. I'd try a negative constant on the endpoint channels for 8 and 0, roughly -0.1 per endpoint, so each one costs about 1.35 logits.

I'm now planning to address the 3→5 confusion by giving the 3 templates an explicit tip at the middle junction, pointing left, and I'm working out how to add that in the code without it affecting the center of mass.

I'm working through how the tip piece gets handled in the template code: it's appended directly to the endpoints, skipped in the stroke loop, and gets the same shear as the direction. I still need to check whether the cusp actually registers with a left-pointing tip detector at its center.

I'm checking whether the tip at the cusp registers with a left-pointing detector, since the response there should be partial but positive. The 9→3 confusion probably comes from the 9's downward stem tip resembling the 3's bottom-left tip. Adding the 8 endpoint penalty might also hurt 8 recall, so I'll test it rather than assume it helps.

I'm now weighing whether a negative constant on the endpoint channels of the 0 and 8 templates, around -0.1 each, is enough to stop 5s being read as 8s. I'll also add a left-pointing cusp tip to the 3 templates and check whether the 2 template's corner shapes conflict with the 1s.
