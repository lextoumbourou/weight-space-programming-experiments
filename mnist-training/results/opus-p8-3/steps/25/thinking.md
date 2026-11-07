The model's at 81.2% accuracy with loss 0.574, so I'll keep probing features. The biggest confusion is still 7 being read as 9, and I'm now checking what separates those two digits. Feature 9 shows a stronger loop response and a vertical upper-left stroke, which look like the distinguishing signals.

Now I'm weighing which features tell 9 apart from 7: 9 has a horizontal stroke along the bottom of its loop, and an upper-left slant that 7 lacks. Next I'm checking the lower-right vertical stroke, which should separate 0 from 2.

I'm choosing the probe features now: a vertical stroke in the lower-right, a horizontal stroke through the middle, and a backslash through the top rows. I'll also check whether a threshold of 0.8 works for the middle region.
