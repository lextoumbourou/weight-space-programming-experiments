Softening the clip hurt a little, so the extreme rates seem to be doing useful work. I'm considering the opposite direction: clipping to [0.01, 0.99] with a temperature scale of 0.72. The catch is that a measured rate of 0.001 would get pushed up to 0.01.

I'm going to run the clip at [0.01, 0.99] with the scale at 0.72, then I've got six steps left: the hole gamma next, then G_D, GAMMA_C, and finally combining the best settings.
