I'm at 68.7% now, and the hole changes help a little. I'm wondering whether holes are still rarely firing, and whether the real problem is that the raw pixels get pooled before the hole check.

The biggest remaining confusions are 5→8, 5→3, 3→5, 4→9, and 7→9, plus several smaller ones.

I'm weighing whether to shift the orientation weight higher and tighten the hole threshold a bit more, while keeping an eye on false positives for 3, 5, and 2.
