I'm working out the decoding scheme for the NE end, where 0 means no value and 1 through 8 map to specific coordinate pairs, with 9 for the lower half. Then I'm tallying how often each code shows up in Class 0 and Class 1, with Class 1 at 1064 total and (0,3) reaching 19%.

Now I'm going through the per-class code counts, where most classes show the "none" code dominating and the lower-half code picking up 10 to 15 percent in several of them. Class 6 stands out: its lower-half count is high, but its top stroke barely registers at under 1 percent. I'm considering whether that's a geometry problem, like the tip sitting past the covered area or the stroke running nearly vertical there.

I'm checking whether the 6's top stroke falls outside the area the filters cover: its tip may sit at rows 2 to 4 after the centre-of-mass shift, which would put it in range of the top-row filter but still miss the tip taps.

I'm trying to work out why the 6's top stroke barely registers with the NE-end filters, even though its tip should fall within the covered rows after the centre-of-mass shift. The horizontal and right-hand endings at the top are rare for the 6 too, so the stroke probably isn't ending cleanly in the way these filters expect.

I'm looking at why the 6's top stroke goes undetected: its top end sits around columns 1 to 2 and looks like a V plus a diagonal, which normally would register. My guess is the tip rises above the rows the top-row filters cover, so it falls outside their reach.

So the 6's top sits too high for the tip taps to catch it: the centre-of-mass shift pushes the top end into the first pooled row, where the partial response gets suppressed. That explains the missing detection, and I'll leave the NE-end reading there.

I'm weighing whether the NE-end filters add much beyond the U-ends, since they already catch most of the 4's arms and part of the 1's top. The NE lower-half counts for 2, 3, 5 and 6 look modest, so I'm considering whether the NW-end or SW-end would be the more useful next step, given the tails of the 5 and 3.

I'm setting up a probe for the NW end, with cells covering the bottom-left tails of the 5 and the 3. The tails should sit inside the covered rows, so I expect it to help separate 5 from 8. I'll check the SW end next if this works.
