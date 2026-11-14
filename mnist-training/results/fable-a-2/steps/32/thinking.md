I'm checking the decoding rules for each bit position against the index-0 sample, working through the weighted sums for bit one, bit two, and bit three.

Now I'm working through the weighted sums for bit one, bit two, and bit three across the remaining samples.

Now I'm tallying the bit-three scores for the remaining samples, where sample 8 comes out highest at .787, followed by 9 at .548 and 5 at .528.

Now I'm comparing the candidate bit markers across samples, and the bit-three marker stands out with sample 8 scoring highest. I'm checking the remaining sample scores for the other markers and working out a Gaussian fit for the first decoding rule.

Now I'm computing Gaussian means for the remaining rules, the "/"(r2,L) rule peaking at sample 8 and the "\"(r1,L) rule still being worked out.

Now I'm testing a few candidate probes for the remaining confusions, especially 3 versus 5, where the new right-side rule already separates them clearly.

I'm weighing which new probe best separates the remaining confusions, like 0 versus 2 and 7 versus 9, and the "\"(r2,R)" rule looks useful for 2 versus 3 and 9 versus 8.

I'm now looking at which probe would separate the remaining pairs, like 4 versus 8 and 0 versus 2. Candidates include a left-side arc from row 2 and a right-side arc from row 2, plus a top-left arc that could catch the long stroke on 6.

I'm settling on three more probes for the remaining confusions: a right-side arc on row 2, a slanted right-side arc on row 2, and a left-side slanted arc on row 1, with the threshold kept at 0.6.
