I'm at 72.2% and want to keep improving, since the template variants helped. The biggest confusions are 8→9 with 172 errors, then 2→3 and 9→4, and I'm considering whether 8's lower loop is going undetected and 9's template is pulling it in.

I'm weighing a junction or crossing detector for the 8 crossing point, but the conv2 channels are all taken, so I'd have to repurpose one. I'm also considering more variants: a looped 8 and a looped 9, a 2 with a curly base, a 4 with the closed form weighted lower, and a 3 with a flat top.

I'm considering a junction-style detector to pick up crossings, though the conv2 channels are full and I'd have to reuse one. I'm also weighing whether 8s with a small lower loop are slipping into the 9 template, and I'm thinking about adding a curly-based 2 variant at weight 0.25 and reweighting the groups.

I'm adding a few more hand-drawn variants: an 8 with a smaller top loop and larger bottom one, a 9 with a curved stem, a 6 with a bigger loop, a shorter-bar 7, and a 4 with its closed form weighted down to 0.45. I can't yet tell how much these will move the numbers, and I'm also looking at widening the shear range.

Computing the per-column sums now, to update the bias.

I'm finishing the per-column sums and log-ratio bias values, then I'll apply the 0.8 scaling factor. Since the templates are changing, the bias numbers may not hold exactly, but I'll adjust the variants and bias together.
