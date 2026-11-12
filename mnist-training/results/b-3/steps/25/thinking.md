The model is at 73.45% accuracy with loss 0.843, a modest improvement. Eight classes are now overpredicted, most notably 3 being predicted as 8 in 149 cases. I'm tallying the column sums to see where the bias is coming from so I can recalibrate it.

Still computing the column sums and the log-based corrections...

I'm checking whether adding negative endpoint weights for classes 0 and 8 will reduce the 3→8 confusion, since those classes have endpoints too. I'm weighing a uniform penalty of about 0.3 on all cells, and I'm also adjusting the compensation term to account for the larger endpoint gain.
