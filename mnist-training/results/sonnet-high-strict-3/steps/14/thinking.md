I'm weighing the scores so far: step 11 is the best at 54.8%, with step 13 close behind at 54.0%. With two steps left and the last one scored, I'll lean toward keeping the best known result. Step 14 gets a modest tweak, and step 15 will just go with whichever has performed best. I'm also tallying the column sums for step 13 to check the counts.

I'm tallying the column sums and the main confusions: 1s getting read as 7s, 4s as 9s, and 7s as 9s. I suspect the slanted 1 template is part of the problem, so I'm considering a straighter one and a few bias adjustments.

I'm checking whether the emptiness weight for class 1 could help, since side cells near the stroke might still catch some ink and blur the signal.

I'm settling on a riskier setting for step 14: raising the emptiness weight to 1.5 while also straightening the 1 template and making small bias changes. That stacks several changes at once, so if it does worse I'll revert in step 15. The reasoning is that emptiness rewards classes with more blank space, like 1s and 7s, so I'd need to lower their biases to compensate for the larger reward.

I'm settling on a straighter template for the 1 class and a few small bias changes, leaving the emptiness weight alone to keep the effect of each change clear. The adjustments are a slight drop for 7 and 1, and small raises for 8, 6, 4, and 0.
