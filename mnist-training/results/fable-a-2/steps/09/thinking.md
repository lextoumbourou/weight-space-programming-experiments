I'm decoding the index as b1 plus twice b2 plus four times b3, with b1 the right wall and left open, b2 the left-open right-wall variant, and b3 the full top. For class 0 I'm tallying the per-index row counts out of 991, and the b1 bit is set for indices 1, 3, 5 and 7, which sums to 591.

Now I'm tallying the remaining classes' counts for each bit: class 1 gives b1 about 0.995, class 2 about 0.825, and class 3 only about 0.37, which is lower than I expected for that upper bowl.

I'm working through the class 4 and 5 tallies now, where the b2 share comes out around half for class 5. For class 6 the b2 bit dominates at about 0.83, while class 7's b1 count is building up to 685.

I'm tallying class 8 and class 9 next, where b1 comes out at about 0.28 and 0.11 and b3 at 0.04 and 0.10. Class 9 stands out because almost none of its rows have any of the three bits set, while class 4 shows a much larger share of left-open, right-wall cases than class 9 does.

I'm checking the top-centre Bernoulli tables for these five features, where class 4 and class 9 separate clearly on LR, RL̄ and UD. Next I'll run the same probes on the bottom-centre region for those channels.

I'm planning the next probes: checking the bottom-centre region's left-open and right-wall channels, then the upper-bottom vertical channels, and finally the upper-centre UD̄ feature before a classifier.
