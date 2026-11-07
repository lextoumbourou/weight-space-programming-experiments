I'm fitting a parabola through the three loss points to locate the minimum, which looks to be around 1.7. I'm computing the second difference for the curvature and starting on the first derivative at the center point.

I'm working out the vertex offset from the curvature, which puts the optimum at about T=1.8 with only a marginal loss gain. Next I'm looking at structural changes, since the best loss needs to drop by at least 1% by step 15. I'm sorting the key confusions by count, with 7→9 and 2→8 at the top, and I'm starting to consider how the templates for those specific pairs could be sharpened.

I'm thinking about why 7 gets mistaken for 9, maybe because my 7's diagonal and top bar sit too close to the 9's stem. I'm also weighing whether a blur width of 3 or 2 would help discrimination, and I plan to test one parameter at a time.

I'm weighing whether the nearest-centroid weakness comes from missing ink being penalized the same as extra ink, since max-pooled features could leave stray strokes in places the template doesn't expect. I'm also considering a bigger change to the bin layout, though with only 16 channels I'm not sure there's room for it.

I'm considering narrowing the 8 template, shrinking its top loop and making the bottom loop a bit wider, so it steals fewer 2s and 3s. I'm also wondering whether giving the 2's bottom bar extra weight in its template would help separate it from the others.

I'm going to try sharpening the blur to sp=3.0 alongside T=1.8, since real class means are blurrier than my prototypes and the nearest-centroid match might be more robust that way. I'll test that first.

I'm worried that changing the blur will shift the biases, since it alters the squared norms of the templates. I could normalize to keep those terms fixed, or just retune the correction afterward.
