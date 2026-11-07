Loop detection is firing far too broadly now, including on 3s and 7s, probably because it picks up stroke crossings and thick strokes near the edges. Even the 1s are triggering it about 17% of the time, so the threshold at 1.7 looks too loose.

I'm working through why the 7's corner gets flagged: the bar above and stem to the right and below give three ink sides, which adds up above the 1.7 threshold, so it's a concavity rather than a true loop. HB1 never wins against LOOP because of the scaling, so it tells me nothing there. The takeaway is that the summed-tap approach can't reliably separate three sides from four, so I'm considering a sharper ink channel in conv1 to make the taps closer to binary.

I'm working out a way to clip the ink values to a [0,1] range using two conv1 channels with offset thresholds, subtracting one from the other. Because max-pooling commutes with this monotone ReLU, the pooled result stays clipped too, which would give a near-binary ink map.

I'm checking whether a clipped ink channel works: the difference of two shifted ReLUs gives a bounded value, and max-pooling commutes with that monotone function. With background at one and four saturated ink sides, the loop score separates cleanly from three sides, so the remaining question is how steep the saturation has to be.

I'm weighing a way to make each side tap contribute a clean yes-or-no. Summing two taps per side could let one side count twice and break the four-side test, so I'm leaning toward one tap per side at a single offset.

Continuing the saturated-ink idea, I'm setting the background channel as a clipped ReLU of one minus the blur, pooled so it stays bounded. The per-side taps and the channel budget for conv1 are what's left to pin down.

I'm sketching a steep-saturation bg channel, ReLU(1 − 2.5·blur), so the hole reads near one, and now I'm moving to the small loop detector: the background at the center plus the four saturated side taps, compared against a threshold of about 4.4.

I'm now setting up the four-side detectors at a larger offset, plus horizontal and vertical pairs that check for ink on both sides with background in the middle. I'm also starting to sketch concavity detectors that require three sides and an empty gap on the fourth.

I'm defining "open" detectors that fire when ink is present on three sides and the fourth side is empty, which picks out the cavity shapes like the two gaps in a 3, the bowl of a 5, and the top gap of a 4.

I'm defining "open" detectors that fire when ink sits on three sides of a point and the fourth is empty, which picks out cavities like the 3's gaps and the 2's top arc. For those cavities the spacing is wider, so I'm setting the offset to 2 to reach the ink on each side.

Next I'm writing out the offset-2 taps for the 2-pixel-away directions and the matching kernel positions, then working through the 15 total conv2 channels and how the 10 new ones fit in.

I'm going to skip hand-probing the new channels and instead guess templates for the clean topology features, since the saturated design makes my guesses about shape more reliable than any threshold estimate. I'll run the classifier on those guesses and only probe again if the results look off.

I'm now writing out the expected-presence tables for each digit's cell pattern, treating the template values as probabilities and weighting the topology channels separately, since the scale mismatch will get absorbed later.

Working out how large the hole has to be before the small loop detector can see it: holes with stroke centers roughly 2 to 6 px from the center on all four sides would count, which is a fairly wide range. The 0's interior is tall, so the vertical taps won't both land on ink, and the small detector will mostly miss it. The large-offset version doesn't help either, so the 0 has to be identified through the horizontal and vertical bar features instead.

I'm filling in rough presence guesses for the new loop and bar channels: the small loop detector mostly lights up on the 6, 8, and 9 and weakly on the 0, while the large one only picks up the 0's interior.

Now I'm writing down the template estimates for the horizontal and vertical bar channels at both offsets. For the 0 the whole middle band lights up, while the 4's top rows and the 6, 8 and 9 loops carry most of the signal. The 7 gets a small horizontal response in its upper row, which I'm noting as probably coming from its bar shape.

I'm now filling in the vertical-bar template values for the larger offset: the 3's cavities and the 5's top-right and bottom-left pockets should light up most strongly, with a weaker signal in the 2's lower-right pocket and near the 0's interior top and bottom.

I'm now filling in the expected presence for the open-side features: the 3's two cavities and the 5's bottom bowl should light up OPEN_L, the 2's middle-left region a bit less so, and the 9 gets nothing there. For OPEN_R, the 5's top gap is the strongest case, with the 6's upper part giving a weaker signal.

Next I'm filling in the open-side guesses for the four-direction cases, mostly the 4's top gap and the 2's top arc, and I'm admitting that 9 and 3 are uncertain there. Then I'll set the template weights, with the topology channels scaled up by 1.5 so they count for more in the classifier.

I'm going to skip the extra probing for now and just run the classifier on these guessed templates, then check the results against the earlier probes.
