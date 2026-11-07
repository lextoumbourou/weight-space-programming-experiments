Back to the 41.75% configuration, the best so far, with three steps left (13, 14, 15). Step 15 is the one that counts for the test score, so I can experiment in 13 and 14 and then set 15 to the best setting. I'm looking at the main confusions, like 1→7, 9→4, and 8→2, to see if any experiment is worth trying. One idea I haven't tested yet is using conv2's extra channels to comp

I'm weighing a fix for the 1→7 confusion, the largest error at 518. The idea is that a real 1 has a bottom base serif while a 7 has no ink there, so a mild negative on 7 at the bottom-center could penalize 1-like inputs.

I'm weighing whether a mild negative on 7 at the bottom-center could cut the 1→7 errors without hurting 7 much, since 7 has no ink in that base area. The earlier mild-negative tests hurt the self-digit scores after normalization, but here the aim is fewer false 7s, which should lift 1's recall even if 7's recall dips a bit.

Checking whether a mild negative on the 7 template's bottom-center would cut the 1→7 confusions. I'd expect 7 to have little ink there, so it should mostly penalize 1-like inputs, though I'll have to watch how much 7's own recall drops.

I'm weighing whether a mild negative at the bottom row of the 7 template, where 1s have their base but 7s have no ink, would cut the 1→7 errors. The catch is that other digits like 2, 3, 5, 6, 8 and 0 also have bottom-center ink, so I'd need to check how much that penalty pulls down their scores too.

I'm weighing a bottom-center negative on template 7, since 1s have base ink there and 7s don't, and the penalty would mostly fall on 1-like inputs. The same ink also shows up for digits like 2, 3, 5, 6, 8 and 0, but their 7-column confusions are small, except for 8→7 at 110, which would drop too. I'll test this in isolation as the step 13 experiment, changing only template 7 and keeping the step 10 setup.

Still weighing the bottom-center negative on template 7, and whether the 7 template's own ink stays clear of it. I'd expect true 7s to have no bottom ink, so they should be barely affected, and I'm planning to tune the 7 template at row 9 next.

Checking the 7 template's bottom rows against the 1's base serif, to see whether the anti-ink idea stays clear of 7's own strokes.

I'm checking where the 7 template's ink sits in the bottom rows, and it does reach the lower-center columns, so the 1's base overlaps it there. Adding a negative only on the right-hand bottom cells, where 1's base extends past 7's stroke, might separate them better. I'm also considering whether to target the upper area instead, since 7's top bar is the distinguishing feature a 1 lacks.

I'm weighing a targeted negative on the right-hand bottom cells of template 7, where 1's base extends past 7's stroke, since those cells stay empty for 7 and should penalize 1-like inputs.

I'm settling on the anti-ink placement for template 7: the bottom-row cells at columns 3, 6, 7 and 8, where a 1's base extends but a 7's stroke does not. I'll leave columns 4 and 5 alone since that's where 7's own diagonal reaches the bottom.

I'm adding a few negative cells to the bottom row of template 7, at columns 3, 6, 7 and 8, where a 1's base extends but a 7 has no ink. I'm leaving columns 4 and 5 alone since that's where 7's own stroke reaches the bottom. It's a small isolated change, so if it regresses I'll revert it in the next steps.

Next I'll try a small change to template 7, adding negative weight only at the bottom-right cells where a 1's base extends but a 7 has no ink. It's a limited experiment, and I'm keeping 41.75% as the fallback if it doesn't help.
