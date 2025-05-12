from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from src import config
from sentence_transformers import SentenceTransformer

# tokenizer = AutoTokenizer.from_pretrained(config.EMBEDDING_MODEL)
# model = AutoModel.from_pretrained(config.EMBEDDING_MODEL)

# def get_embeddings(text):
#     inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
#     with torch.no_grad():
#         outputs = model(**inputs)
#     embeddings = outputs.last_hidden_state.mean(dim=1)
#     return embeddings.squeeze().numpy()

# def embed_posts(posts):
#     posts['embedding'] = posts['cleaned_text'].apply(get_embeddings)
#     return posts

model = SentenceTransformer(config.EMBEDDING_MODEL)

def get_embeddings(text):
    return model.encode(text, convert_to_numpy=True)

def embed_posts(posts):
    posts['embedding'] = posts['cleaned_text'].apply(get_embeddings)
    return posts

        