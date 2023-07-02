#type: ignore

import numpy as np
import random
import tensorflow as tf
import keras_tuner as kt
from tensorflow import keras
from keras.optimizers import Adam

SEED_VAL = 42
random.seed(SEED_VAL)
np.random.seed(SEED_VAL)
tf.random.set_seed(SEED_VAL)
tf.config.experimental.enable_op_determinism()


class Lstm(kt.HyperModel):
    def __init__(self, vocab_size, max_sequence_length, metrics, weights):
        self.vocab_size = vocab_size
        self.max_sequence_length = max_sequence_length
        self.metrics = metrics
        if weights:
            self.weights = weights

    def build(self, hp):
        model = keras.Sequential()
        model.add(keras.layers.Embedding(self.vocab_size, input_length=self.max_sequence_length, output_dim=self.max_sequence_length))
        model.add(keras.layers.LSTM(hp.Int('units', min_value=8, max_value=96, step=8),
                                    hp.Choice('activation1', ['relu', 'sigmoid']),
                                    kernel_initializer=tf.keras.initializers.glorot_uniform(seed=SEED_VAL)))
        model.add(keras.layers.Dropout(hp.Float('rate', min_value=0.1, max_value=0.5, step=0.1),
                                       seed=SEED_VAL))
        model.add(keras.layers.Dense(self.vocab_size, 'softmax'))

        model.compile(optimizer='rmsprop',
                      loss='categorical_crossentropy',
                      metrics=self.metrics)

        return model


    def fit(self, hp, model, *args, **kwargs):
        
        weights = self.weights = {}
        if self.weights:
            weights = self.weights
        else:
            weights = {0: 0.5, 1: 0.5}

        return model.fit(
            *args,
            batch_size=hp.Choice("batch_size", [8, 16, 24, 32]),
            epochs=hp.Int('epochs', min_value=4, max_value=64, step=4),
            class_weight=weights,
            **kwargs,
        )
        