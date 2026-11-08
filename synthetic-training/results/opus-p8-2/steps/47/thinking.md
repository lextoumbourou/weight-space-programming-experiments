I'm working out the bias value that gives the lowest result, using the three points I have: 0.4794 at +0.1, about 0.4768 at 0, and 0.4759 at -0.1. I'm fitting a parabola through them to estimate where the minimum falls.

I'm checking the parabola's minimum more carefully: the slope works out to about +0.0175 per unit of b, giving a minimum near b = -0.103, so -0.1 is roughly the best bias. Further gains from the other features look minimal.

I'm weighing whether the +0.1 check on x1 and x9 at a -0.3 setting could beat the current configuration, since both had shown positive effects at the null baseline. Those could be tried together with the bias recentered afterward.
