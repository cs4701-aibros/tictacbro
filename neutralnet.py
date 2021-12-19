import random
from tensorflow.keras import layers, Model, Input, metrics, losses
import tensorflow as tf
import numpy as np


def apply_actionmask_to_policy(p, action_mask):
    p_masked = p * action_mask
    if np.sum(p_masked) == 0:
        p_masked = m
    return p_masked / np.sum(p_masked)


class NNet:
    def __init__(self, action_size):
        x = Input(shape=(9, 9, 2))
        y = layers.Conv2D(18, 3, activation="relu")(x)
        y = layers.Conv2D(18, 3, activation="relu")(y)
        y = layers.Flatten()(y)
        p = layers.Dense(action_size, activation="softmax", name="p")(y)
        v = layers.Dense(1, name="v")(y)
        self.nnet = Model(x, [p, v])
        print(self.nnet.summary())

        def entropyLoss(y_true, y_pred):
            return -y_true * tf.math.log(y_pred + 1e-10)

        self.nnet.compile(optimizer="adam", loss={"p": entropyLoss, "v": "mse"})

    def predict(self, state):
        x = state.getObservation()
        x = np.expand_dims(x, 0)
        p, v = self.nnet.predict(x, batch_size=1)

        p = p[0]
        p = apply_actionmask_to_policy(p, state.getActionMask())
        return p, v[0][0]

    @staticmethod
    def _prepare_examples(examples):
        X = []
        pi = []
        v = []
        for e in examples:
            X.append(e.state.getObservation())
            pi.append(e.pi)
            v.append(e.reward)

        return np.array(X), [np.array(pi), np.array(v)]

    def train(self, examples):
        X, y = self._prepare_examples(examples)
        self.nnet.fit(X, y, batch_size=32, shuffle=True, epochs=3)
        return self
