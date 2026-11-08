## Step 33: add a second interaction for low x12 combined with low x10

**What step 32 showed:**
- w[9] = 0.65 made the loss worse: 0.4594, against 0.4510 at 0.40.
- So I set w[9] = 0.35.

**This step:** I add a second interaction unit.
- x12 has a negative weight once the other features are in the model.
- If x12 behaves like a continuous variable, very low values among low-x10 rows may form a high-class-1 pocket. The linear model cannot represent such a pocket.
- New hidden unit 3 = ReLU(−x12 − x10 − 1.8). It fires only when x12 is very low (below about −1.1 for low-x10 rows) and x10 is low.
- It is effectively off for high-x10 rows, because their x10 value of about +1.36 pushes the sum negative.
- Its output enters the logit difference with weight +1.5.

```python
import numpy as np

def build_weights():
    # linear score z = w . x  ->  contributes z to logit(class1) - logit(class0)
    w = np.zeros(13, dtype=np.float32)
    w[10] = 1.50   # strongest positive predictor
    w[4]  = -0.60  # strong negative predictor
    w[1]  = 0.15   # small after controlling for others
    w[9]  = 0.35   # optimum between 0.15 / 0.40 / 0.65
    w[5]  = 0.15   # continuous/skewed positive
    w[2]  = 0.15   # moderate positive
    w[11] = 0.00
    w[0]  = -0.05  # weak negative
    w[3]  = -0.40  # conditional negative
    w[12] = -0.35  # conditional negative
    w[7]  = 0.00
    c = -0.45      # intercept

    # interaction unit A: fires only when x10 high AND x4 high
    INT_THR = 1.2
    INT_W = -0.8

    # interaction unit B: fires when x12 very low AND x10 low
    LOW_THR = 1.8
    LOW_W = 1.5

    W1 = np.zeros((16, 13), dtype=np.float32)
    b1 = np.zeros(16, dtype=np.float32)
    W2 = np.zeros((2, 16), dtype=np.float32)
    b2 = np.zeros(2, dtype=np.float32)

    # hidden 0 = relu(z), hidden 1 = relu(-z): linear part
    W1[0, :] = w
    W1[1, :] = -w
    W2[1, 0] = 0.5;  W2[1, 1] = -0.5
    W2[0, 0] = -0.5; W2[0, 1] = 0.5

    # hidden 2 = relu(x10 + x4 - INT_THR)
    W1[2, 10] = 1.0
    W1[2, 4] = 1.0
    b1[2] = -INT_THR
    W2[1, 2] = INT_W / 2
    W2[0, 2] = -INT_W / 2

    # hidden 3 = relu(-x12 - x10 - LOW_THR)
    W1[3, 12] = -1.0
    W1[3, 10] = -1.0
    b1[3] = -LOW_THR
    W2[1, 3] = LOW_W / 2
    W2[0, 3] = -LOW_W / 2

    # intercept
    b2[1] = c / 2
    b2[0] = -c / 2

    return {
        "fc1.weight": W1,
        "fc1.bias": b1,
        "fc2.weight": W2,
        "fc2.bias": b2,
    }
```
