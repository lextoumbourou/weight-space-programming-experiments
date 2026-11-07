The loss has dropped to 4.67 and accuracy is up to 36.9%, and the bias adjustment seems to have evened things out a bit. Several classes are still badly confused: 9 is still often predicted as 4, 7 gets mistaken for 1, 5 and 9, and 8 is frequently called 2, 7 or 1.

Now I'm checking the column sums again, since 4 still looks over-predicted even after the bias adjustment, and 9 may actually be over-predicted too. The 9 vs 4 mix-up seems to come from the templates: 9's closed top loop and 4's open diagonal get blurred and pooled away, so both end up matching the more generic 4 template.

Now I'm recomputing the predicted column totals to see how the bias is distributing: 4 and 1 are still over-predicted, while 0, 6, 5, and 8 are under-predicted. The next step is more bias tuning, but the bigger gains will likely come from reworking the 7, 8, and 9 templates.

I'm wondering whether the "4" template is simply too generic, since its right vertical and middle bar overlap with many digits. Pooling and per-template tweaks might be hiding the real problem. A better fix could be adding a second feature channel that captures stroke orientation or loops, so that 7 vs 1 and 9 vs 4 can be told apart.

I'm weighing a second feature channel that captures stroke orientation or loops, since that could separate 7 from 1 and 9 from 4 better than more bias tuning. I'm also planning to increase the bias correction for the persistent imbalance and redraw the weaker 7, 8, and 9 templates to be more distinctive.

I'm turning to the 7, 8, and 9 templates, since 7 keeps getting pulled toward 1, 9, and 5 despite having a clear top bar and diagonal. The sparse ink may be making its match score weak and easy to shift by bias or noise. Hand-tuned blurred templates are reaching their limit, so I'm starting to consider a more capable approach.

I'm weighing whether to add orientation channels, but repurposing the 16 conv2 channels would cost spatial detail, which seems too risky right now. Since the template refinements have been steadily helping, I'll keep tuning the templates and the bias instead.

Now I'm adjusting the bias terms on top of their current values, pulling down the over-predicted classes more strongly.

Now I'm working through the bias values class by class, pulling down 4 and 1 and nudging up the under-predicted classes such as 0, 5, and 6.

Now I'm adjusting the bias terms again, working out new values per class from the predicted totals, and I'm starting to redraw the 7 template with a bold top bar and a diagonal stroke running down to the lower left.

Still writing template code...

Still writing template code...

Still refining the 7, 8, and 9 templates and the bias values, keeping the scale at 6 so I can see how each change affects accuracy.

Still refining the 2, 5, 7, 8, and 9 templates, keeping the 0, 1, 3, 4, and 6 ones as they are, since 4 is taking matches from other digits but its template is working.

Still writing template code...

Still writing template code...

Still writing template code...

Still writing template code...

Still writing template code...

Still writing template code...

Still writing template code...

Still writing template code...

Still writing template code...

Still writing template code...

Still writing template code...

Now I'm comparing 4 and 9 more directly: 4 has a diagonal running down to the left alongside its right vertical, while 9 has a closed loop with ink on both sides and an open center.

Still refining the 7 and 9 templates, keeping the 8 as it was.
