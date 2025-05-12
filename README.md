# Text Mining Reddit Web App - DATA 5420

## Katie Corcoran

This Streamlit app aims to make Reddit more searchable by aggregating search results, finding the most relevant posts, and outputting a summary to the user in a digestible format.

### Text Mining Techniques Used

#### 1. **Data Collection via Reddit API**
- Used the `praw` (Python Reddit API Wrapper) library to collect posts and top-level comments from a given subreddit and query.
- **Why**: The Reddit API allows real-time, targeted data. I filtered for relevence and posts within the last year.

#### 2. **Data Cleaning**
- Removed punctuation, lowercased text, stripped extra whitespace, and removed URLs.
- Combined post titles, post bodies, and top comments into a single aggregated field for richer context.
- **Why:** Reddit content is informal and noisy. Cleaning ensures consistent text for downstream tasks like embedding and summarization.

#### 3. **Text Embeddings**
- Used the `multi-qa-MiniLM-L6-cos-v1` model from [Sentence Transformers](https://www.sbert.net) to convert text into semantic vector embeddings.
- **Why:** Unlike traditional bag-of-words methods, embeddings capture the meaning of a sentence, enabling more accurate similarity comparisons between the search query and Reddit content.

#### 4. **Cosine Similarity**
- Calculated the cosine similarity between the query embedding and each post’s embedding.
- **Why:** Cosine similarity is effective for comparing high-dimensional semantic vectors and ranking posts by relevance.

#### 5. **Summarization (Gemini API)**
- Used the Gemini API to summarize the top 5–10 most relevant posts.
- **Why:** Reddit posts and comments can be long and repetitive. Summarization condenses the content into a digestible format, saving the user time while preserving key insights.