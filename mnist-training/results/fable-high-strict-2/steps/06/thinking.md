I'm checking the predicted counts for each digit, and 9 is clearly overpredicted at 2018. Most of the excess seems to come from the 4→9, 7→9, and 6→9 confusions, so the bias toward 9 is what I need to correct.

Bias tuning is just bouncing around, so I'll switch to smaller steps. Rather than fiddling with the 9 bias, I'm going to look at structural changes that could raise the ceiling from around 58%. The main worry is whether my coordinate assumptions for the cells and centers of mass are correct, since several confusions (8→2, 3→5, 5→3) point that way.

I'm checking the grid row spans again, and they still look right. I'm also weighing a damped bias update, since the 9 bias is overshooting and the counts suggest the others need small corrections in the opposite direction.

I'm now looking at why 9 wins so often on 6s: its loop and tail overlap the 6's loop in the middle columns, and the empty-cell penalties in the bottom-left don't push it away enough.

Comparing 6 and 9 as mirror images, I'm checking whether the penalty terms and the bias gap of 0.8 are enough to separate them. For the 4→9 confusions, I'm wondering whether the top of the left stroke is picking up horizontal-looking ink that the 9 template reads as a loop.

I'm checking the H-shaped filter's response at a stroke end: a vertical stroke centered in the filter gives about 0.2, but one that stops at the top gives a larger value, around 1.1, so the end-of-stroke response is what I need to watch.

I'm weighing whether the 4 and 9 boundary is soft because the features don't separate them well. The top horizontal stroke of a 9 is already in its template, so the real difference might lie in where 4's crossbar extends to the right and how its left side stays open at the top.

I'm looking at whether the 4 template's right vertical sits too close to the middle cell, which would explain why 4s get read as 9s. Moving that stroke a bit further right could leave that cell emptier and separate the two digits better.

I'm considering whether the 4 template's right vertical should sit further right, so that the middle cell at the top is emptier and 4s stop looking like 9s. The emptiness check would catch a gap there, though it could also penalize real 4s whose strokes sit a little lower.

I'm adjusting the 4 template's right vertical slightly lower, from y 3.5 to 3.6, and keeping the negative weight on the top horizontal for 4s. Then I'll look at whether the 9 template's tail reaching into the rightmost column is causing it to absorb 7s, since the 7's top bar sits near x 1.1.

I'm checking whether 9's loop-top and tail templates pick up 7s, since the 7's top bar and diagonal line up with several of 9's expected cells. I'm also wondering whether the empty top-left cell is enough to separate them.

I'm weighing a more deliberate approach: the 9 bias is too strong, but beyond that I'd like the template to penalize missing ink where the denser class expects it, so 9 stops winning on 7s and 6s.

I'm considering a direct penalty for missing strokes: the sparser class's emptiness channel could be weighted negatively where the denser class expects ink, so a 9 gets docked when a 7's input leaves its expected loop empty. The worry is that emptiness fires near stroke edges and could penalize the correct class too.

I'm checking how a 5x5 patch overlaps a stroke at the cell edge: a patch centered on the stroke's top gets about nine pixels of ink, so the emptiness score comes out negative there and the emptiness channel stays quiet.

I'm checking whether a patch centered on a stroke's edge reads as empty, and it only does when the stroke sits away from the inner part of the cell. A stroke running through the middle kills the emptiness score in every patch, so the channel mostly fires on genuinely missing ink.

I'm settling on a penalty of 0.1 for missing expected ink, since the emptiness channel should fire only when a stroke is truly absent from the inner part of a cell. Digits with more expected cells will take more of this penalty, which should offset the dense-class advantage before I adjust the biases.

I'm weighing a penalty for missing expected ink, so that a dense class like 9 loses score when a 7 leaves its loop empty, and I'm going to keep the damped bias values as they are for now.

I'm settling on a missing-ink penalty of 0.1 so the dense classes lose score when expected strokes are absent, and I'll keep the damped biases as they are for this step.
