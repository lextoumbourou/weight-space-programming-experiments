Accuracy came out at 83.1% with loss at 0.554, so the bias adjustment helped. Next I'm comparing predicted class counts against the true counts to check balance, and the first class is already showing a shortfall of about 43.

I'm now weighing how to trade off the remaining probe steps against bias and scale tuning, since the largest errors are in the 3↔5 pair.

I'm checking which class pairs still cause the most errors, and the 0↔2 confusion is strange given how different their features look on paper. I suspect the template or the weak centre response on "/" is the cause rather than the features themselves.

I'm thinking the empty centre might separate 0 from 2: I'd check the horizontal and vertical energy in the middle rows and columns, since 0 should look hollow there while 1 and 4 don't. The 9-related confusions are mostly smaller now, so I'll leave those for later.

I'm thinking the centre horizontal and vertical energies would help separate 0 from the others, and I'd also check the top and bottom corner rows where 5 and 7 differ from the loops of 3 and 5. Each probe will use a single threshold on a few-cell region sum.

I'm going to probe three new regions: the centre horizontal energy, the centre vertical energy, and the bottom-right horizontal segment, with thresholds of 1.0, 1.2 and 0.8. The centre vertical threshold is higher because many digits have strokes running through the middle. I'll hold off on a classifier and bias retune until after these probes.
