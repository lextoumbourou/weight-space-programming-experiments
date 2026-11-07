The zero-bias model gets about 73.5%, which is in the same range as the ridge result at step 4 or 5, so neither clearly wins. Now I'm tallying the column sums at step 10 to calibrate the biases with one large step.

Now I'm checking whether the bias calibration should use a scaled log-ratio at this alpha, since the logit gaps are larger and the earlier multiplier may not carry over.

Comparing against the ridge baseline of about 76.5% at step 5, which used a smaller gamma and alpha, this run without biases lands at 73.5%, so it is unclear whether it's better. I'm weighing whether to fall back to the earlier setup or to combine ridge with the edge features if accuracy stays below 83%, and I'll run the bias calibration first to see what it does.
