I need to hand-design weights, so first I'll aim for something reasonable. The loss should start near log 2, since there are only two logits rather than ten. I'm looking for simple cues that separate cats from dogs, and I'm weighing whether color or the setting, like indoor versus outdoor backgrounds, might help.

Still defining the convolution filters for the first layer...

Still working out the conv3 pass-through and the fc layer; I'm thinking a single greenness cue for dog could be a good first probe, scaled small so the loss doesn't get worse.

Still settling the edge filters on luminance, with the response scaled so each per-channel weight comes out small. For the fc layer, I'm thinking a dog logit that rises with the mean green channel and a cat logit that falls by the same amount, with the weight spread across the 25 positions to get roughly a unit logit gap on green-heavy images.

I'm setting the greenness weights so each position contributes evenly, with the dog logit rising and the cat logit falling by the same amount. The expected pooled greenness for grass-heavy images is around 0.15, so the logit gap should come out to roughly one unit there. I still need to center the bias, so I'll adjust the dog bias to offset the average greenness.

Still weighing the bias offsets: I'll set the dog bias to about +0.125 and the cat bias to -0.125 so the net is centered. I'm leaving the edge-energy feature out for now and keeping only the greenness probe, so the result stays easy to read.
