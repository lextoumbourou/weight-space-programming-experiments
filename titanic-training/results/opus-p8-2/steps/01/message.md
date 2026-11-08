You will write the weights of a small neural network that predicts who survived the Titanic by hand, then improve them
over up to 50 steps. There is no gradient descent, no training data and no optimiser. You choose every weight
yourself, the way you would write a program.

After each step, your network is run on a labelled validation set of 600 passengers. You are told the validation
loss, the accuracy and the confusion matrix. You never see any passenger records. When the run ends,
the network from the step with the lowest validation loss is scored on a separate test set of 291 passengers that you never see.

## Task

The passengers come from the labelled training file (train.csv) of the Kaggle Titanic competition: 891 passengers
of the RMS Titanic, which sank on 15 April 1912. The validation and test sets are a random split of those 891,
stratified by survival.

Each input is one passenger, a float32 vector of 13 numbers, in this order:

     0 pclass_1: 1 if first class, else 0
     1 pclass_2: 1 if second class, else 0
     2 pclass_3: 1 if third class, else 0
     3 female: 1 if female, 0 if male
     4 age_decades: age in years divided by 10 (0.42 years -> 0.042, 80 years -> 8.0); 0 when age is unknown
     5 age_known: 1 if age is recorded, 0 if it is missing (about 20% of passengers)
     6 sibsp: number of siblings and spouses aboard (0 to 8)
     7 parch: number of parents and children aboard (0 to 6)
     8 log_fare: natural log of (1 + ticket fare in 1912 pounds); fares run from 0 to 512, so 0 to 6.24
     9 embarked_c: 1 if boarded at Cherbourg, else 0
    10 embarked_q: 1 if boarded at Queenstown, else 0
    11 embarked_s: 1 if boarded at Southampton, else 0 (all three are 0 for the 2 passengers with no port)
    12 cabin_known: 1 if a cabin number is recorded, else 0

Classes: index 0 = died, index 1 = survived.

## Network

The network is fixed. It is this PyTorch model (standard PyTorch semantics: nn.Linear computes x @ weight.T + bias,
weights indexed [out_feature][in_feature]):

    model = nn.Sequential(
        nn.Linear(13, 16),   # fc1: 13 passenger features -> 16 hidden units
        nn.ReLU(),
        nn.Linear(16, 2),    # fc2: 16 -> 2 class logits (0 = died, 1 = survived)
    )

The loss is the mean cross-entropy of the 2 output logits (softmax applied to the logits). The prediction is the
argmax. You must set all 258 parameters:

    fc1.weight: (16, 13)
    fc1.bias: (16,)
    fc2.weight: (2, 16)
    fc2.bias: (2,)

## What to send back, at every step

Reply with exactly one Python code block that defines a function `build_weights()`. It must return a dict that maps
each parameter name above to a numpy float32 array of exactly that shape. Send the complete function every time,
not a change to the previous one.

## Rules

- Your code may import only numpy and math. It has no file, network or data access.
- Setting weights directly, from rules, formulas or what you know about the Titanic, is fine.
- Your code must not generate a set of example inputs or feature vectors (for example random synthetic passengers)
  and compute weights from them. No averaging over generated samples, gradient descent, regression, least squares,
  clustering, discriminant analysis or search, including on synthetic data you create yourself.
- Your code must not run the network or any part of it on inputs.
- The feedback after each step is the only information you get about how the network performs.
- A step whose code fails still uses up that step. You are told the error.

Before the code block, briefly explain what you are trying in this step. Comment the code so a reader can follow
which weights do what.
