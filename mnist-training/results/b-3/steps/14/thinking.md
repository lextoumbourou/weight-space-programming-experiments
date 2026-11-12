The model hits 68.9%, the best so far, so I'm weighing whether to push the scaling factor higher, and I'm thinking of trying s=1.3. The loss is 1.05, and the wrong predictions are often only about 0.3 to 0.5 confident. I also want to look at the per-class prediction counts, since class 1 is overpredicted and class 9 is underpredicted.

I'm now checking the narrow 8s that get pulled into class 1, and the 8s that drift into class 2, and I'm thinking about adding narrow and bottom-loop variants for the 8 template. The 3 and 5 confusion looks fine to leave alone. I'm working through new bias values from the per-class counts, and I want to check whether the correction term needs rescaling once s goes up to 1.3.

Next I'm adding narrow and slanted variants to the 8 template, and I'm scaling the bias correction with the scaling factor so the two stay consistent. For the 9s, which often get confused with 4, 1 and 8, I'm adding a slanted variant with a small loop and a shorter stem.
