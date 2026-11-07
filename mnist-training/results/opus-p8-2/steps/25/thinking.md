I'm checking how the crossing change affected column 8: its recall went up to 675, but its predicted total now sits at 1629, well above the 974 target. A partial bias correction might still leave the net effect positive, so I'm weighing whether to lower WX to 0.5 and apply a lighter correction, which means two parameters to tune at once.

I'm weighing whether to keep WX at 1.0 and apply a bias correction to column 8 alone, since its ln ratio is about -0.41 in pre-temperature units. I'm also considering applying the full correction vector from the step 24 counts, scaled by 0.8, but I haven't settled on the factor yet.

I'm settling on a factor of 0.9 for the full correction, since most of the imbalance sits in column 8.
