I'm looking at the predicted digit counts, which put the model at 54.3%, a new best. The main mix-ups are 8 being read as 2, 3, and 5, and I'm noting where the 9s go.

Now I'm going through the confusion pairs, and the 9-to-4 mistakes stand out as persistent. The 4 is over-predicted while the 9 is under-predicted, so I'll pull the 4 down and nudge the 9 up. The 3-versus-5 mix-up runs both ways, which points to templates that look too similar, and the 8 is undercounted with its left side going unmatched, so its template width may be off.

I'm working out where the 5's top bar lands after centering: at this scale it falls just outside the grid, so the top stroke of both the 5 and the 3 gets clipped, which would explain why those two keep getting swapped.

The window looks lopsided: the digit's top gets clipped while the bottom has room to spare. Shifting the sampling up by one cell should center it around the center of mass, with about the same amount cut at both ends.

I'm weighing whether to shift the sampling window by one cell, since the top-heavy features like the 5's and 7's bars and the 2's and 3's arcs would lose more with one cut than the bottom-heavy ones would with the other.

I'm weighing whether shifting the sampling window down or up would be better, since the top-heavy digits lose their bars and arcs at the top edge, while the bottom-heavy ones lose their bases and loops at the bottom.

I'm weighing whether the two-row windows could be split across the even and odd channels, so the vertical resolution doubles without cutting more of the digit at either edge.

I'm settling on the crop: shifting the sampling window up by one cell looks like the most even trade-off between what gets clipped at the top and at the bottom, even though neither edge can be fully saved.

I'm comparing the crop options: shifting the window up keeps about 0.5 cell cut at the top but 1.5 at the bottom, while the current setup does the reverse. Since the top strokes of the 7, 5, and 2/3 get clipped either way, I'm leaning toward the top being the more informative edge to protect.

I'm checking why the 9→4 mix-up is so persistent: the 9's top loop sits at the very top edge of the sampling grid, so it gets clipped away, and that leaves the 9 looking like an open-top 4.

I'm switching the row taps to {1,2} so the window shifts up one cell, which moves the center of mass to row 4.5 and keeps the column taps at {2,3}.

I'm checking the bias adjustments next: 8 gets the biggest boost, and 3, 4, and 5 get pulled down.

I'm moving on to the bias values, which I'll keep moderate given that the crop change may shift things. I'm also considering whether to narrow the 8 template slightly, though I'm not sure real 8s are that narrow, so I'll leave it alone. Next I'm checking whether the 0-versus-6 confusion might ease now that the top stroke is visible.
