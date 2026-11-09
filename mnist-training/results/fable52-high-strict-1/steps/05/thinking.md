Checking class 8 against class 0 for input 0, the forbidden features overlap heavily and mostly cancel out, which leaves the UD constraint as the main difference.

The 0 penalty is probably coming from the UD feature, since 0 forbids it and 8 doesn't. Checking whether UD actually fires in real zeros, especially near the side walls, and whether slanted zeros make it more likely.

I'm checking whether the wall-detection measure double-counts curved strokes. Where an arc's horizontal, diagonal, and vertical responses overlap, a single curve could register as more than one wall and trip the UD feature on its own.

I'm reconciling a bit of arithmetic on the wall-detection weights, then deciding to stop theorizing and run a probe that measures how often each structural feature fires per class.

I'm designing a probe that checks three features at once by mapping their threshold results onto eight output classes, and I'm weighing whether to pack more features into each step or split them across several probes.

I'm weighing whether to probe the three structural features together, since a three-bit encoding fits in eight outputs, or to split them across separate probes and keep the layout simpler. Either way I'd like those bits validated before building on them, because the cosine baseline at 49.6% is likely held back by the unreliable structural channels.

I'm settling on a three-bit probe: left-right, up-down, and bottom-narrow features, each thresholded at about 0.3 and mapped to outputs 0 through 7. I'm weighing whether the threshold should be tuned per feature, since weak firing in a few cells could push a sum past 0.3 by accident.

I'm settling the probe's encoding now: the three features get thresholds around 0.3, and the combined logit is scaled so the output can pick one of eight classes, with the last two outputs disabled.

I'm sketching the probe's output encoding: each of three binary features maps to one bit, so the eight outputs cover all combinations, and the last two outputs are disabled. I expect the classes to land on distinct codes if the features behave, and I'll keep the conv layers from the previous step and change only the final layer.
