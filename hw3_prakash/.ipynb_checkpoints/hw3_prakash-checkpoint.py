import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng()

example_mean = 20.0
example_sigma = 4.0
example_n = 5000

sample = rng.normal(
    loc=example_mean,
    scale=example_sigma,
    size=example_n
)

print(sample.mean())
print(sample.std())