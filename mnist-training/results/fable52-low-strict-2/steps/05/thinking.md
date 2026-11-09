Still checking whether the 69% comes from a systematic mismatch, and I'm looking at how the real feature map might differ from the template model in strength across cells, especially near the borders.

Checking the conv1 orientation and the conv2 index mapping, both come out consistent, so the pipeline itself looks right and the shortfall probably lies in the template quality. The weak 2 template is pulling in several other digits, which suggests its shape is too generic. I'm also wondering whether the saturating tanh makes the templates so blurry that they lose discriminative power.

I'm thinking about switching from the saturating tanh to a plain linear response with a wider Gaussian, since a single stroke saturates the templates into blurry blobs. Scaling the templates down and using σ=2.5 should preserve more discriminative detail, and I'll add shear variants at 0, 0.2, and 0.4 to cover slant instead.

I'm weighing shear variants at around -0.05, 0.15, and 0.35 to cover slant, and I'm considering halving the biases since the template change will shift them, though I'll keep them roughly as they are for now and just test the new setup.
