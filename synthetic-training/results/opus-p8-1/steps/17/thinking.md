The two means differ only slightly, roughly 0.549 against 0.536, so the total effect comes to about -0.045. That's small and not dramatic. A linear feature with a negative effect that saturates might point to a bounded or sigmoid-like label, or to a make_classification-style setup. Interactions could matter too, or the true model may be a threshold on a linear combination plus noise.

I'm considering whether the nonlinearity might come from interactions, perhaps a threshold on a linear combination with heavy noise, which would put a ceiling near 75%. To probe pairwise interactions cheaply, I'm looking at |x_a + x_b| terms, since they pick up the product, though each costs several units and grouping them is awkward.

I'm checking whether the nonlinearity could sit in a single feature, like a threshold or a sine shape, which the |x| probe would miss. I'm going to try a probe that separates relu(x) from relu(-x), and then test products of features, since interactions would stay hidden to these marginal probes.

I'm weighing whether the nonlinearity might be a sum of interactions or a random teacher network, and testing sign patterns across feature groups is noisy. Individual |x| probes on the six linear features look more practical, especially checking whether x7 responds only to its positive side.

I'm going to split each linear feature's effect into its positive and negative sides, starting with a probe on x7's positive side at a modest step size. The rest of the six linear features would follow one at a time, given the step budget.
