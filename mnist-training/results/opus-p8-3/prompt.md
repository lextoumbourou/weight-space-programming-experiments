You will write the weights of a small convolutional neural network for MNIST by hand, then improve them over
up to 50 steps. There is no gradient descent, no training data and no optimiser. You choose every weight yourself,
the way you would write a program.

After each step, your network is run on a labelled validation set of 10,000 MNIST images. You are told the
validation loss, the accuracy and the confusion matrix. You never see any images. When the run ends,
the network from the step with the lowest validation loss is scored on a separate test set that you never see.

## Task

Each input is one MNIST handwritten digit: shape (1, 28, 28) (channels, height, width), float32 in [0, 1] (the
original 0-255 pixel values divided by 255). Row 0 is the top. Ink is high (near 1) and the background is 0. As in
the standard MNIST dataset, each digit is size-normalised to fit a 20x20 box and centred in the 28x28 field by its
centre of mass.

Classes: index d = digit d, for d = 0 to 9.

## Network

The network is fixed. It is this PyTorch model (standard PyTorch semantics: convolutions are cross-correlations
with no padding and stride 1, weights indexed [out_channel][in_channel][row][column]):

    model = nn.Sequential(
        nn.Conv2d(1, 8, 5),    # conv1: 1x28x28 -> 8x24x24
        nn.ReLU(),
        nn.MaxPool2d(2),       #        8x24x24 -> 8x12x12
        nn.Conv2d(8, 16, 5),   # conv2: 8x12x12 -> 16x8x8
        nn.ReLU(),
        nn.MaxPool2d(2),       #        16x8x8 -> 16x4x4
        nn.Flatten(),          #        16x4x4 -> 256, in (channel, row, column) order
        nn.Linear(256, 10),    # fc:    256 -> 10 class logits
    )

The loss is the mean cross-entropy of the 10 output logits (softmax applied to the logits). The prediction is the
argmax. You must set all 5,994 parameters:

    conv1.weight: (8, 1, 5, 5)
    conv1.bias: (8,)
    conv2.weight: (16, 8, 5, 5)
    conv2.bias: (16,)
    fc.weight: (10, 256)
    fc.bias: (10,)

## What to send back, at every step

Reply with exactly one Python code block that defines a function `build_weights()`. It must return a dict that maps
each parameter name above to a numpy float32 array of exactly that shape. Send the complete function every time,
not a change to the previous one.

## Rules

- Your code may import only numpy and math. It has no file, network or data access.
- Drawing filters or templates directly, from formulas or from strokes you describe by hand, is fine.
- Your code must not generate a set of example inputs or feature vectors (for example random synthetic digits) and
  compute weights from them. No averaging over generated samples, gradient descent, regression, least squares,
  clustering, discriminant analysis or search, including on synthetic data you create yourself.
- Your code must not run the network or any part of it on inputs.
- The feedback after each step is the only information you get about how the network performs.
- A step whose code fails still uses up that step. You are told the error.

Before the code block, briefly explain what you are trying in this step. Comment the code so a reader can follow
which weights do what.
