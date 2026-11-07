I cut the 25% step too far: swapping the 8 template and its bias together pushed "6" into being the dominant magnet, while 0, 2, 7 and 8 dropped back to zero. Lowering b8 to -0.4 is what removed 8 entirely. The result is very sensitive to these two changes, so I'll move on to step 8.

Reverting to step 8 seems like the safer baseline, since it gave the best accuracy so far at 36.9%. From there I'll try smaller nudges: lowering b8 slightly, trimming b7, and raising b5 and b6 a little to see whether they recover.

Trying a smaller adjustment this time: nudging b6 up to -0.05 and b5 up to -0.15, while dropping b8 to -0.05 and b7 to +0.15. Step 9 showed b6 is very sensitive, so a +0.5 jump there was far too big.

Keeping step 8's template and changing only the biases, I'm now nudging the bias values gently: b3 and b4 up a little, b5 and b6 toward zero, b7 and b8 down, and b9 up. The earlier sensitivity means a half-unit change is enough to flip a class into a magnet, so I'll keep each adjustment small.

I'm settling on a set of bias values by nudging step 8's numbers rather than changing the templates: a modest raise for 3, 4, 5, 6, and 9, and a drop for 7 and 8, with 0, 1 and 2 left alone. I'll also restore the 8 template to all-ones, since changing it earlier is what caused the instability.

I'm keeping the 8 template as all-ones, since that's what step 8 used. With b8 lowered to -0.05, the 8 class should pull less weight, which is the point of the change.
