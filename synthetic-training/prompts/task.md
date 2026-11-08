You will write the weights of a small neural network for a binary classification task by hand, then improve them
over up to {steps} steps. There is no gradient descent, no training data and no optimiser. You choose every weight
yourself, the way you would write a program.

After each step, your network is run on a labelled validation set of 1,000 rows. You are told the validation loss,
the accuracy and the confusion matrix. You never see any rows. {stop_rule}When the run ends, {scored} is scored on a
separate test set that you never see.

## Task

The data is synthetic: it was generated for this test from a hidden random process, so it is not a dataset you could
know. The labels depend on some of the features, possibly not linearly, and some features may be irrelevant. The
validation and test sets come from the same process.

Each input is one row, a float32 vector of 12 features, x0 to x11. Each feature has been standardised to mean 0 and
standard deviation 1 over the 1,000 validation rows.

Classes: index 0 = class 0, index 1 = class 1.

## Network

The network is fixed. It is this PyTorch model (standard PyTorch semantics: nn.Linear computes x @ weight.T + bias,
weights indexed [out_feature][in_feature]):

{architecture}

The loss is the mean cross-entropy of the 2 output logits (softmax applied to the logits). The prediction is the
argmax. You must set all {n_params:,} parameters:

{shapes}

## What to send back, at every step

Reply with exactly one Python code block that defines a function `build_weights()`. It must return a dict that maps
each parameter name above to a numpy float32 array of exactly that shape. Send the complete function every time,
not a change to the previous one.

## Rules

- Your code may import only numpy and math. It has no file, network or data access.
- Setting weights directly, from rules or formulas, is fine.
- Your code must not generate a set of example inputs or feature vectors (for example random synthetic rows) and
  compute weights from them. No averaging over generated samples, gradient descent, regression, least squares,
  clustering, discriminant analysis or search, including on synthetic data you create yourself.
- Your code must not run the network or any part of it on inputs.
- The feedback after each step is the only information you get about how the network performs.
- A step whose code fails still uses up that step. You are told the error.

Before the code block, briefly explain what you are trying in this step. Comment the code so a reader can follow
which weights do what.
