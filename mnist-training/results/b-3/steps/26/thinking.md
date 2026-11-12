I'm looking at a 74% score and thinking about smaller, incremental changes. Many of the 2s have a loop at the bottom-left, so I'm considering giving that position a higher loop probability for both loop types and exempting 2 from the negative loop. I'm also noticing that conv1 channels 6 and 7 are free while conv2 is fully used, so I'm wondering whether a redundant channel could be swapped out.

I'm weighing whether to push the endpoint weight for the 2s up and then recalibrate the biases, though I'm not sure which change will help most.

Recalculating the log-ratio corrections for each digit's column sum, which shifts the bias values for several classes.

Odd that the biases keep drifting the same way for class 1, even as I lower its bias; it seems class 1 is just weakly sensitive to bias, since narrow images push its logit very high. That's fine for now. I also need to remember that the endpoint change shifts the pre-compensation term automatically, by about -0.15 times the endpoint gain times the mass.
