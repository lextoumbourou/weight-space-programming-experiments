The change from 3 to 5 is the biggest gain, and the bias shift toward 5 pushed 3s the wrong way. I need a template fix for telling 3 and 5 apart. Looking at the top portion, many real 3s have a fairly flat top, and 5 has a left vertical stroke that 3 lacks, but real 3s may start their curve at the top-left in a way that looks like one.

I'm weighing whether a template change can separate 3s from 5s, since the 3 template's top-left stroke looks like the 5's vertical. I'm considering moving the 3's cusp further left and enlarging its top arc, but I can't confirm real 3s behave that way. Trying a global blur change or a cos^4 tuning, with a revert if accuracy drops, may be the better bet.

I'm settling on a 3-template redesign with the cusp moved left to about x=11.5, plus a small bias shift for 3 and 5. I'm also going to lower the blur to 4.5. Changing both the template and the blur at once muddies cause and effect, but I'll take that risk.
