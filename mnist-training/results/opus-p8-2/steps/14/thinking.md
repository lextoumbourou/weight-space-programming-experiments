The model reached about 70% improvement with a loss near 0.96, but column 4 is badly overpredicted, with a total of 1772. I'm going to recalibrate the biases, and I'm working through the column sums to see where the errors sit.

I'm working through the per-column sums and log-ratios, and I'm applying a partial 0.8 correction to the biases, especially for column 4, which is far too high.
