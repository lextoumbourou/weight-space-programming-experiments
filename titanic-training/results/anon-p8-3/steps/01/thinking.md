I'm looking at the Titanic dataset: 891 rows, 13 features in random order, binary survived outcome with 549 died and 342 survived, plus 600 validation rows. Since the feature identities are unknown, I'm planning to use the early steps to probe each one individually by checking how the logit difference and loss respond.

I'm settling on a first probe: a single feature with weight 1.0 and a prior bias of about -0.47, then checking whether accuracy beats the 61.6% baseline and loss beats 0.666. I'm also writing the code so the feature index and coefficient are general.
