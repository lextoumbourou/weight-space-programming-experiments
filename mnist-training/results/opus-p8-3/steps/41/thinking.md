I'm decoding each feature from the ink positions and bit masks, starting with the first sample's sums for F1, F2 and F3. Now I'm working through the second sample's values for F1 and starting on F2.

Now I'm checking the per-sample sums for F2 and F3 across the remaining rows.

I'm weighing whether to fold in F2 and F3 as extra features, since their ink rates separate the digits reasonably well, while F1 looks weaker. The worry is that they're all near-saturated, so the log-probability contributions get clipped. I'll try adding just F2 and F3 with a small weight and revert if accuracy drops, and I'll also check a bias adjustment.

I'm adjusting the per-column bias on the digit sums: column 7 comes out low against the true total, so I'll nudge it up, while column 0 runs high and needs pulling down. The remaining columns already land close enough to leave alone.
