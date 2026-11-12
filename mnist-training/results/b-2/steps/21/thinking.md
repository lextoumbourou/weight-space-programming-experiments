I'm working out the orientation bins from thresholds at 0.3 and 1.2, with most top-right values landing in bin 2 and several running higher than expected. I'll take representative values per bin and compute their means, though the upper end of bin 2 is unknown. The rest of orientation looks slow at seven more steps, so I'm wondering whether the top-left and top-right horizontal measurements are worth keeping, and I want to compare the class distributions before deciding.

I'm tallying the class distributions now, pairing each class's top-left and top-right orientation counts so I can see how they shift between classes.

I'm tallying the per-class counts for the two orientation measurements, and the top-right values pile up heavily in the highest bin for most classes. The bin thresholds look too low for this data, which makes the mean estimates unreliable for the high values.

I'm estimating the mean values for each class's top-left orientation bins using representative values of 0.15, 0.75, and 1.8, and I'm working through the arithmetic for the first few classes.

Now I'm working out the top-right orientation means for each class, using the same representative values, and most of them land around 1 to 1.6.

I'm estimating the top-right orientation means for each class with the same representative values, and most of them come out around 1.3 to 1.8. The rest of the plan is to measure the remaining channels' top and bottom quadrants, and I'm weighing whether to move to wider thresholds for better resolution.

I'm switching to wider thresholds of 0.5 and 1.5, with representatives at 0.2, 1.0 and 2.0 for the new bins. Next I'll move on to the horizontal bottom quadrants, bottom-left and bottom-right.
