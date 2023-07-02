#type: ignore

import pandas as pd
import numpy as np
import random
from sentence_transformers import SentenceTransformer

SEED_VAL = 42
random.seed(SEED_VAL)
np.random.seed(SEED_VAL)


class SentenceTransformers():
    def __init__(self, model_name):
        self.model_name = model_name
        return


    def apply_transformers(self, df_train, df_val, df_test):
        model = SentenceTransformer(self.model_name)

        train_sentences = [' '.join(text) for text in df_train['question']]
        train_embeddings = model.encode(train_sentences)

        val_sentences = [' '.join(text) for text in df_val['question']]
        val_embeddings = model.encode(val_sentences)

        test_sentences = [' '.join(text) for text in df_test['question']]
        test_embeddings = model.encode(test_sentences)

        return train_embeddings, val_embeddings, test_embeddings
