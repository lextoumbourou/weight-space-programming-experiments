I'm at 59%, a new best, and there are three steps left (13, 14, 15). The last one should be a safe move since its network is scored. I'm also tracking the main confusions and their counts.

I'm working through the per-digit calibration numbers now, tallying the predicted counts for each column and checking how each digit's adjustment shifts after the update.

I'm checking which digit the 8s are being confused for: the 2 is predicted for them, and I'm comparing where the 2's strokes sit against the narrow left side of a real 8 to see what separates them.

I'm checking whether a narrow 8's side, around x=0.75, would fall inside the 2's empty zone, and it looks marginal. I'm picking tighter masks for the left and right regions so the 2's own strokes stay clear of them.

I'm weighing the 8→2 confusion against the V map: the 2 has little vertical structure, so 8s' sides shouldn't add to its score. I'm also looking at the 3→5 pair, where the 3's upper-right arc near x≈0.78 is the part I need to compare against 5's frame.

I'm checking whether the 3's upper-right arc, around x≈0.78, lands inside 5's region in its own coordinate frame, and the cell math says it does, at cell 6. The vertical band I'm testing for 5 maps to the top few rows, and the 3's arc sits in those same rows.

I'm checking whether a 3's upper-right arc lands in 5's expected region. Its V-map signal sits in the upper-right, where 5's V template is empty, so it shouldn't add to 5's score. Still, a targeted penalty on 5's upper-left might help.

I'm thinking about generalizing the forbidden regions so they can apply to a specific feature map, like the V map, rather than just ink. The idea is a V-forbidden zone for 5 in the upper right, and a matching one for 3 in the upper left, where a 5's vertical stroke would sit.

I'm checking whether the 8's top-right corner, which is marginal, picks up the end of a 5's top bar. It probably does, but only at the edge of the region, so I'll need to tighten the mask there.

I'm checking whether the 8's narrow left side, around column 0 or 1, overlaps the 5's left vertical stroke, and the answer is only at the edge. Widening the 8's waist region to catch wider 8s would start to mask real 8 ink too, so I need to balance those two.

I'm working out a 2→9 case now: I'm looking at whether the 2's lower-left diagonal lands in 9's bottom-left region, mapping its endpoint into the cell grid to check the overlap.

I'm looking at where the 2's lower-left diagonal ends, near row 7 and column 1.5, and checking whether it falls inside 9's bottom-left region. It does, but the 2→9 confusion persists, so I'm raising that region's weight to 1.3. I also want to check the 9 against the 2 more closely.

I'm reconsidering the 2→9 pair: their strokes look alike apart from the lower-left, so I'm raising that region's weight to 1.3. Next I'm looking at 0→6, checking whether the 0's right side lands in the upper-right of 6's frame and whether that region's weight should go up.

I'm bumping the 0→6 upper-right penalty up to 1.8, since the 0's right side sits squarely in that region and the confusion persists. Next I'm checking whether a slanted 1 could land in 2's left-middle region; it doesn't at mid-height, so I'm weighing whether the 1→2 confusion comes from 2's bias instead.

I'm generalizing the forbidden regions so each one can target a specific feature map, and I'm drafting the step 13 changes for the 2, 3 and 5 entries.

I'm adding a per-feature forbidden mask, so the V-map penalty for 5 applies only to the vertical-stroke map and gets scaled back against its own template. I'm setting the 6's upper-right penalty to 1.8 and the 9's lower-left to 1.3, and updating the biases to match.

I'm settling the V-map penalty for the 5: it gets a scale factor so it applies to the vertical-stroke map alone and is weighted against that feature's own template.
