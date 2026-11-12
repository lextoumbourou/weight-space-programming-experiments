I'm checking the zero-bias baseline, which came out at 60%, and tallying the predicted counts per digit. Next I'm computing the calibration bias for each class as 0.6 times the log of the true count over the predicted count, starting with digits 0 through 2.

Now I'm refining the calibration by checking the sensitivity of the column sums to the bias change, which suggests a damping factor of about 0.7 rather than 0.6.
