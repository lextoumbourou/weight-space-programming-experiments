Step 48 came in at .3788 and 88.64%, below the predicted .367 baseline, so raising GAMMA and ALPHA may have hurt, or the bias tweaks did. Step 47 had the same small bias tweaks and a .44 scale, and both runs landed around 88.63–88.64% against 89.04%, so I'm checking what else they share.

Step 44 already showed that scaling the biases alone doesn't move accuracy, so the scale isn't the culprit. The remaining suspects are the bias tweaks or the changed centre terms, and the step 47 numbers point at the centre terms. Since both experiments lost accuracy, I'm going back to the step 42 config and planning two more steps, starting with step 42 at scale .445 using scaled biases.

I'm now weighing whether to lower GAMMA and ALPHA instead, since raising them seemed to hurt, though the bias shift muddies that. I'll do the safe step first: step 42's config at scale 0.445 with its class biases rescaled.
