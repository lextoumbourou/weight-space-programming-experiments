I'm weighing whether k is too small, since the 8 attractor persists and a larger k would penalize big templates more. I'm considering trying k=2.2 next, though I'm conscious that I'm running low on steps with 39 left.

I'm checking the sign conventions for the shifted ink grids, since a flipped ky direction would explain the poor accuracy, and the offsets and centering look right on inspection. I'm also wondering whether the templates are simply drawn badly, because class means at this resolution should do noticeably better than what I'm getting.

I'm wondering whether the orientation channels are throwing off the distances, since their magnitudes may not match the ink features and would bias some classes. A clean test is to drop them from the fully connected layer and run nearest-centroid on ink alone, using k=2.0 and no hole rule, with s=1.
