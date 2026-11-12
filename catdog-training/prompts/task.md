You will write the weights of a small convolutional neural network for telling cats from dogs by hand, then improve them over
up to {steps} steps. There is no gradient descent, no training data and no optimiser. You choose every weight yourself,
the way you would write a program.

After each step, your network is run on a labelled validation set of 10,000 photos. You are told the
validation loss, the accuracy and the confusion matrix. You never see any images. {stop_rule}When the run ends,
{scored} is scored on a separate test set that you never see.

## Task

Each input is one colour photo from the Kaggle Dogs vs. Cats competition (2013): shape (3, 64, 64) (RGB channels,
height, width), float32 in [0, 1] (the original 0-255 pixel values divided by 255). Row 0 is the top. The photos are
ordinary pictures of pets, taken by their owners: any breed, pose, colour, background, lighting and distance, sometimes
with people or other objects in the frame. Each photo was resized so its shorter side is 64 pixels, then centre-cropped
to 64x64.

Classes: index 0 = cat, index 1 = dog. The classes are balanced.

## Network

The network is fixed. It is this PyTorch model (standard PyTorch semantics: convolutions are cross-correlations
with no padding and stride 1, weights indexed [out_channel][in_channel][row][column]):

{architecture}

The loss is the mean cross-entropy of the 10 output logits (softmax applied to the logits). The prediction is the
argmax. You must set all {n_params:,} parameters:

{shapes}

## What to send back, at every step

Reply with exactly one Python code block that defines a function `build_weights()`. It must return a dict that maps
each parameter name above to a numpy float32 array of exactly that shape. Send the complete function every time,
not a change to the previous one.

## Rules

- Your code may import only numpy and math. It has no file, network or data access.
- Drawing filters or templates directly, from formulas or from shapes and patterns you describe by hand, is fine.
- Your code must not generate a set of example inputs or feature vectors (for example random synthetic images) and
  compute weights from them. No averaging over generated samples, gradient descent, regression, least squares,
  clustering, discriminant analysis or search, including on synthetic data you create yourself.
- Your code must not run the network or any part of it on inputs.
- The feedback after each step is the only information you get about how the network performs.
- A step whose code fails still uses up that step. You are told the error.

Before the code block, briefly explain what you are trying in this step. Comment the code so a reader can follow
which weights do what.
