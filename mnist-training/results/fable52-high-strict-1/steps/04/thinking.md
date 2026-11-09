Now I'm seeing the loss jump to 4.1 with much worse results, and classes 8 and 3 are dominating again. I'm going through which forbidden transitions each class has, like the ones for classes 8, 3, and 0, to work out where the penalties are coming from.

I'm checking whether the 0s, 1s and other classes are triggering their forbidden transitions when they shouldn't. A single vertical stroke seems to leak enough response into the diagonal and horizontal detectors that the LR and UD rules fire next to almost every stroke, which would explain why the penalties are so large.

I'm working out the fix for the wall measure: the vertical stroke's own response leaks into the diagonal detectors, so I'm subtracting that cross-talk before combining them, which leaves the wall response dominated by the vertical component.

I'm trying to rebalance the wall measure so a vertical stroke doesn't score 1.44 while a diagonal drops to about 0.64. The cross-talk from the diagonal detectors still isn't being handled cleanly.

I'm settling on the wall measure as a weighted mix of the vertical and diagonal responses minus the horizontal one, with the weights chosen so a pure vertical stroke reads about 1.2 and a diagonal about 1.0. Working that through, the vertical weight comes out near 0.42 and the horizontal penalty needs to be at least 0.73 so horizontal strokes get pushed below zero.

I'm checking the wall measure's cross-talk on a soft vertical stroke, estimating about 0.8 from the diagonal detectors, which puts the main-cell response around 0.8 to 1.2. The neighbouring cell picks up a partial vertical response and broader diagonal leakage, so I'm trying to see whether that spillover pushes the total too high.

I'm checking how the D1 kernel responds to a vertical stroke when it's shifted one column over, adding up the responses from the neighbouring columns.

I'm checking the leftover estimate for a single crisp wall, working out how much the diagonal cross-talk from the vertical stroke adds at the neighbouring cells. Using the sum over the three nearby columns, the spillover drops to about 0.1, so a crisp single wall lands near 1.5 total. That's still well above where the earlier design put it, which is why the LR rule kept firing on single walls.

I'm working out the wall measure's constants so that horizontal strokes go negative, and I'm checking the neighbouring-cell spillover, which comes out around 0.3. A single crisp stroke should land near 1.5, which leaves the LR rule marginal, so I'm raising its threshold to 2.5 for more margin. The UD rule gets the same treatment with the roles of horizontal and vertical swapped.

I'm weighing whether to reduce the forbidden penalties in this step too, since my estimates for the detectors are rough. I'm leaning toward a middle setting, with the attraction term at 1.0 and the forbidden-transition penalty at 0.5, rather than committing fully to the stronger values until I've rechecked the tip detectors.

I'm checking the neighbouring cells for the tip detectors: a 3-pixel stroke sitting at a particular offset gives 0.67 ink in the adjacent cell rather than the 0.33 I'd assumed, so I need to recheck the other side as well.

I'm now checking the tip detectors' neighbouring cells, where the side cells pick up 0.67 ink on one side and 0.33 on the other, so the weights I assumed were too small. The corner and row-0 contributions then add up to roughly −0.73 instead of the −0.6 I had estimated.

I'm checking the tip detectors' neighbouring cells for thicker strokes, where the side cells pick up more ink and the total suppression comes out to roughly −0.2, so the tips still work for thin strokes and are weaker for thick ones.

Now I'm reconsidering the thresholds so single walls don't trip the LR rule, since the pooled maximum could catch a worst-case alignment. A crisp wall can reach about 1.5 on the wall measure, and I want to make sure that stays under the firing level.

I'm checking the peak response for a single wall: a profile like [0,1,1,1,0] gives about 1.3, and mixed-intensity edges come out lower, around 0.65.

I'm estimating the wall measure's response for ideal and typical strokes, which gives about 1.5 at most, so the LR and UD thresholds at 2.5 keep single walls from firing. Typical two-wall configurations land around 0.4, which is weak but usable. I'm considering scaling the wall weights up by about 1.2 to lift those cases.

I'm settling the wall gain and threshold: a bias of −2.5 keeps crisp single walls below firing, though typical double walls land weak around 0.4. I'll raise the gap-channel gain to 1.5 and lower their threshold to 0.15 to compensate.

I'm settling the detector gains at GA=1.5 and TH=0.15, and keeping A at 1.0. The forbidden penalties then land around −0.3 to −0.9, which I think is a reasonable middle ground. I'm also holding the class 8 bias near −0.3 and treating the 3 over-prediction the same way, since both templates lean heavily on the UD and UDL rules. Last, I'm checking the UDL rule, where the veto on the left cells could flip sign when horizontal strokes sit there.

I'm making sure the veto on the left cells doesn't flip sign when horizontal strokes sit there, so I'm balancing the D-channel cross-talk against a compensating positive term on the horizontal input.

I'm setting the veto weights for the left-side cells so horizontal strokes don't flip the sign, using about 0.75 to offset the cross-talk from the diagonal detectors. Then I'll write the LR channel with a bias of −2.5, and the UD channel with the roles of horizontal and vertical swapped.

I'm settling the remaining details: the forbidden-transition penalties stay as they are, the gap-channel gains go to 1.5 with a 0.15 threshold, and the attraction term is set to 1.0.
