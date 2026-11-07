I'm checking that cosine similarity favors the broad template, which fits my expectation, and the loss is a little better. Next I need to calibrate the bias, so I'm totaling the per-column counts for step 5, starting with column 0 and column 1.

Now I'm working through the log ratios for each class to set the bias adjustment, with the largest gap showing up for class 4.

I'm weighing whether to center the templates by subtracting their mean before the cosine, which would cut the broad template's advantage since its shared parts cancel out. I think that's the more principled change, so I'll center now with zero bias and recalibrate afterward.

I'm comparing the nearest-mean score with the centered-template version, and the mean-subtracted form may still favor the bias, depending on how the shared part cancels. I'll test a bias calibration at 0.7 times the log ratios on the step 5 setup to see its real potential, and I'm leaving the logit scale as it is since the loss looks moderate.
