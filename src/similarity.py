from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def rank_cosine_similarity(query_embedding, post_embeddings, posts):
    query_embedding = query_embedding.reshape(1, -1)
    post_embeddings = np.vstack(post_embeddings)
    
    similarities = cosine_similarity(query_embedding, post_embeddings)[0]
    top_indices = np.argsort(similarities)[::-1]
    top_posts = [posts.iloc[i] for i in top_indices[:10]]
    return top_posts