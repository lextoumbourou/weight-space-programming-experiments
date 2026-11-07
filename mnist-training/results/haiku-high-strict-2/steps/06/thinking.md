Nine is being over-predicted: 886 of the 1135 ones come out as nines, along with 925 sevens and 578 nines overall. Its bias delta is +0.8, and nine has many template matches. Nudging biases by hand keeps shifting the problem, and accuracy sits at 32%, so I want to look at the feature scaling and whether the design itself needs rethinking.

I'm checking whether the Gaussian logit is being dominated by the bias term, since a faint "1" would give small dot products and let template norms decide the winner. Nine's template might carry a small norm, but the numbers so far don't clearly confirm that, so I'm still weighing whether the sign of the feature term is the real issue.

I'm now wondering whether the Gaussian logit is the real problem: for weak, low-ink inputs, the template-energy term could let whichever class has the smallest template norm win, and my +0.8 bias on class 9 would make that worse. Rather than keep nudging biases by hand, I'm considering a mean-centred linear discriminant with the bias term reconsidered.

I'm considering making each class template unit-norm so the energy term is equal across classes and the decision comes purely from correlation with the input. That would remove the pull toward low-energy templates and drop the hand-tuned bias offsets.

I'm considering centring the templates by subtracting the mean across classes, so every class shares a common baseline and only the differences drive the decision. I'd also normalise each centred template to unit norm and drop the per-class bias, which should stop the low-energy templates from winning on faint inputs.

I'm weighing whether to center the templates across classes, so each one only contributes its contrast against the average and no class gets a built-in advantage on faint inputs. Keeping the per-class bias at zero and normalising each centred template would let the correlation with the input decide the winner.

I'm checking whether centring the templates across classes would stop 1-images from being pulled toward class 4, since 4's centred template also gets positive contributions from the vertical centre. The 1 template has to stand apart through its missing horizontal and other features, and I'm working out how its negative mean-subtracted horizontal part changes the dot product for a '1'.

I'm settling on centring each class template across the classes and scaling the channels, with the per-class bias left at zero. I'm also weighing whether to normalise each class's total energy so no template gets an advantage on faint inputs.

I'm deciding between normalising each centred template to unit norm, which keeps the classifier closer to a cosine comparison, and leaving the templates unnormalised as a proper matched filter. I'm leaning toward normalising for robustness, with the scale factor set so the logits sit in a reasonable range.

Setting the per-channel weights aside for now, I'm keeping the vertical and horizontal channels at 0.6 and the sum and bias channels at 1.2, and I'm dropping the per-class offsets so they stop chasing the 9 problem.

Centring each class template across the others and normalising it to unit norm, with the per-class bias at zero, should stop the energy term from favouring low-norm templates. I'm writing the code that computes the centred, scaled weights for each channel.
