I'm at about 59.4% now, a small gain, with two steps left. Step 14 can be a modest experiment, and step 15 has to be safe, picking the best of 13 and 14 with gentle biases. For the 2s, the new right-middle region hurt: real 2s have ink there because the arc's right side sits lower than my template, so I'll revert that region.

I'm now checking the predicted counts against the true ones: 9 is over-predicted by about 220, and 2 is still getting confused with 9, while 8→2 hasn't moved from 322. For step 14 I'll keep it modest, mainly removing the right-middle region from the 2 template and leaving the rest alone.

I'm weighing a forbidden region in the lower-left for 9, aimed at the 2's diagonal stroke, since 9's stem partly overlaps it. The overlap is only partial, though, so the gain may be small.

I'm weighing why 8s get mistaken for 2s: the lower loop's sides and the upper loop's left side sit where the 2's arc is, and the lower-left strip is the remaining question.

I'm checking whether the 8→2 confusions come from the lower-left strip: an 8's lower-left side sits near x≈0.25, which my 2 template doesn't cover. Widening that forbidden region to x<0.3 would catch it without touching the 2's own diagonal, though I'm not sure real 2s stay clear of it.

I'm weighing a tighter forbidden region for the 2 template, widening the lower-left strip slightly so it catches the 8s' lower-left side while staying clear of the 2's own diagonal. The 2's upper-left and the lower-left shifts are the main remaining levers, and I'm also considering whether a vertical-map constraint in that same area would help.

I'm checking the 5s next: they're under-predicted at 680 against 892 true, so their bias goes up, and I'm also seeing 5→8 and 5→3 confusions. Among the other digits, 0→6 looks fine now, and 1's bias gets a small nudge for the 1→2 and 1→3 cases. I'm also weighing a forbidden region for 9 to reduce the 4→9 errors, though I'm not yet sure it's worth the risk.

I'm checking the 4→9 and 7→4 errors, which look acceptable since 9 can't gain much more from its template here. The plan for step 14 is to revert the right-middle region for the 2 template and widen its lower-left strip slightly to catch the 8s' lower-left side.

Settling on the final choice now: if step 14 improves on 13, I'll keep it with a tiny bias adjustment, and otherwise fall back to 13 with gentle biases.
