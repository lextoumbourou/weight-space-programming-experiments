Shear at 0.2 helped digits 0, 5 and 9 but hurt 8, 6, 2 and 7, and the loss went up. I'm considering a per-digit shear, maybe 0.2 for 0, 5, 9 and 1 and 0.12 for the rest, though that would be a drawing choice. Now I'm comparing the per-class scores from step 19 to step 20.

I'm comparing the per-class changes from step 19 to step 20, and the bias shifts muddy some of the gains. Classes 0, 1, 3, 5 and 9 look like they improved, while 2, 6, 7 and 8 dropped. I'm weighing a per-class shear split along those lines, though I'm not sure the cross-class interactions allow it to isolate the effect.

Now I'm settling on the bias values for the per-class shear setup: I'll keep the step 20 biases for most classes, but reconsider the ones tied to classes 6 and 7, and keep the bias for 9 as it is.

I'm settling the bias list: keeping most of the step 20 values, but moving the class 6 and 7 entries back to their step 19 values.
