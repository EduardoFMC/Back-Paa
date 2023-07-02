#type: ignore

import math
import numpy as np
import joblib

class Similarity():
    def __init__(self):
        return 


    def apply_cosine_similarity(self, df_train, df_val, df_test, desc_train_embeddings, desc_val_embeddings, desc_test_embeddings, correct_desc_train_embeddings, correct_desc_val_embeddings, correct_desc_test_embeddings):
        train_similarity_list = []
        val_similarity_list = []
        test_similarity_list = []

        for row in range(len(desc_train_embeddings)):
            train_similarity_list.append(self.define_cosine_similarity(desc_train_embeddings[row], correct_desc_train_embeddings[row]))

        for row in range(len(desc_val_embeddings)):
            val_similarity_list.append(self.define_cosine_similarity(desc_val_embeddings[row], correct_desc_val_embeddings[row]))

        for row in range(len(desc_test_embeddings)):
            test_similarity_list.append(self.define_cosine_similarity(desc_test_embeddings[row], correct_desc_test_embeddings[row]))
        
        df_train['SIMILARITY'], df_val['SIMILARITY'], df_test['SIMILARITY'] = self.normalize(train_similarity_list, val_similarity_list, test_similarity_list)

        return df_train, df_val, df_test


    def define_cosine_similarity(self, vetor1, vetor2):
        # Define initial value of inner product
        inner_prod = 0
        
        # Calculate cosine distance between 2 vectors
        for i,valor in enumerate(vetor1):
            inner_prod += valor*vetor2[i]
        norma_vetor1 = math.sqrt(sum([x**2 for x in vetor1])) 
        norma_vetor2 = math.sqrt(sum([x**2 for x in vetor2])) 
        cosine_distance = inner_prod/(norma_vetor1*norma_vetor2)
        cosine_similarity = 1 - cosine_distance

        # Return cosine similarity
        return cosine_similarity
