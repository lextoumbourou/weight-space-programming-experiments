Everything is coming out as 1, which suggests the feature magnitudes are much smaller than the template norms, so the -0.5|T|² term dominates and the smallest-norm template always wins. I could normalize the templates to unit length so it behaves more like a cosine comparison, with the bias at zero or small, or keep the bias but scale it by α.

I'm settling on normalized weights, dividing each template by its norm and dropping the bias to zero, so the logits reflect cosine-style similarity. The scale factor is the open question; I'm going to try s=4 and keep the conv1 bias at -0.2.
