I'm at 76.2% accuracy with a best score of 0.7842 and eight steps left. Since the temperature was tuned under the earlier config and the optimum may have shifted with better accuracy, I'll test a gscale of 0.54 with recalibration.

Now I'm computing the per-class counts and their log-slope estimates for the step-42 recalibration.

I'm weighing whether to combine the recalibration with a temperature change, but that would make it hard to tell which one caused any loss increase. Since recalibration usually helps a little and the temperature shift would be small, I'm leaning toward doing the recalibration alone at gscale 0.53 first.
