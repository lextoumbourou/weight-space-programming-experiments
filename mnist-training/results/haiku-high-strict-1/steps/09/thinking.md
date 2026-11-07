Class 4 is now the one collapsing everything toward it, and the zero-mean approach with the drawn oriented templates still produces that sink. I suspect the features carry a strong shared component that I don't yet understand, maybe one channel dominating or the ink feature firing across regions where every digit has it. A sink toward one class would then mean some feature direction lines up with 4's prototype across images, though I haven't checked that yet.

I'm working out why the centering matters here: the score may be picking up the average image's spatial pattern, which is center-heavy, so a class whose prototype aligns with that mean pattern would absorb everything. Subtracting the mean feature map would remove that bias, but I'd have to estimate it without the data, perhaps from the average of my drawn prototypes.

I'm switching to the mean-centred form: the score becomes f·(mu_d − m̄) minus a class-dependent bias, where m̄ is the average of the ten drawn prototypes. That is the same Gaussian-equivalent rule I worked out earlier, just with the bias term m̄·(mu_d − m̄) included rather than dropped.

I'm checking whether the centering actually matters: subtracting the mean prototype would remove the central bias, but that reduces to the nearest-prototype rule, so the sinks must come from a mismatch in feature scale rather than the centering itself. Class 4 still pulls everything in, which suggests its prototype overlaps the average feature pattern too strongly.

The mean feature pattern f̄ is non-constant and center-heavy, so w_4 lines up with it best and pulls most images toward class 4. Subtracting f̄ from the features, which means carrying the term −f̄·w_d as a class-dependent bias, should remove that sink.

I'm settling on the centered form: subtracting the mean prototype m̄ from both the features and each class prototype, with the bias b_d = −m̄·w_d so the mean-pattern pull is cancelled. That gives a centered dot product, and I'm checking whether it avoids the class-4 sink or just reproduces the nearest-prototype rule.

The centered form only cancels the sink if the −2f·m̄ term is truly the same for every class, and it is: the centering moves the classes by the same constant, so the ranking over d stays exactly that of the uncentered Gaussian. That means centering by itself can't remove the class-4 sink; the bias has to come from somewhere else.

Subtracting the mean prototype only reproduces the Gaussian rule, so the centering alone won't clear the class-4 sink. Dropping the norm term favors dense digits, and keeping it leaves the scale mismatch unresolved. With 43.6% as the current best and seven steps left, I'm wondering whether the feature design itself is limiting things, such as the ink features.

Next I'm checking for a bug in the code itself: the conv1 and conv2 biases and the background response both come out to zero, so that part looks fine. I also want to confirm the flatten index mapping, since the (16,4,4) layout should give c*16 + h*4 + w.

Checking the conv weight shapes and the orientation filters next: the anti-diagonal pattern using |r+c−4| should trace the right line, and the pixel-center coordinates should line up with the conv windows.

Weighing a fallback: the earlier zero-mean hand-template approach scored best at 43.6%, even though its grid geometry was off, so I'm considering whether to lean on it again. Feedback on the sink classes could be used to nudge per-class biases, which seems a reasonable manual calibration.

I'm weighing a bias correction from the confusion pattern, though that only treats the symptom rather than the prototype itself. A better route is to fix the common component of the features, by centering each feature on its typical value so the shared part stops favoring one class.

I'm checking whether dropping the norm term while keeping the mean-centred dot product avoids the sink. Prototypes far from the mean would get larger scores, so the question is whether a typical zero image still lands on its own class or gets pulled toward a high-norm prototype.

I'm checking whether centering the features and prototypes around the mean prototype gives a classifier that avoids the class-4 sink, with score_d = (f − m̄)·(mu_d − m̄) and a bias term. My concern is that dropping the norm term could favour prototypes with large norms, so the sinks might just move to a different class.

I'm going to normalize each prototype's centered vector, so the score depends only on alignment with the mean-removed features and no class gets favored just for having a larger norm.

Writing the fully-connected weights now: each class gets its centered prototype, normalized to unit length, and the bias is set to subtract the mean prototype's projection so the score reflects only alignment.

Writing the fully-connected weights next: each centred prototype gets normalised to unit length, with a bias that cancels the mean-pattern projection, so the score reflects only alignment.

Next I'm making the classifier centred by subtracting the mean prototype, with each class vector normalised so no class wins just by size, and I'm admitting this is still a guess.
