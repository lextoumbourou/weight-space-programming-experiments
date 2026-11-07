I'm checking the per-class confusion figures, and 72.9% is the running accuracy. The biggest confusions are 3→5, 5→8, and 2→8. Class 5 looks like the weak spot, with errors toward 8, 6, and 3, so I suspect my template for 5 is drawn poorly and I'm comparing it against how a real 5 is usually written.

I'm going through the bowl shape of the 5 template and whether its center of mass sits too high. Next I'm planning a few bias adjustments: raising the 5 and 2 biases, lowering the 8 and 1 biases, and nudging the 4 bias slightly, since those classes are under- or over-predicted.

I'm settling on a set of bias values for the classes that are off, raising the 5, 2, and 4 biases, lowering the 8 and 1 biases, and skipping the blur or conv1 changes so this step's effect is clear. I'm leaving the 5 template as it is for now.
