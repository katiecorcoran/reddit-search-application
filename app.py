import pandas as pd
from src import reddit_api, data_cleaning, embeddings, similarity, summarize
from pathlib import Path
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent / "data"

def main():
    st.title("Reddit Search App")
    subreddit = st.text_input("Enter subreddit (e.g., FoodNYC):")
    query = st.text_input("Enter search query (e.g., best restaurants Manhattan):")
    
    if st.button("Search"):
        with st.status("Fetching data...") as status:            
            # Check if the data already exists
            try:
                filepath = DATA_DIR / f"{subreddit}_{query.replace(' ', '_')}.json"
                data = pd.read_json(filepath)
                print("Data already exists. Loading from JSON.")
            except FileNotFoundError:
                print("Data not found. Fetching new data.")
                data = reddit_api.fetch_reddit_posts(subreddit, query)
                data = pd.DataFrame(data)
                data.to_json(filepath, index=False)
            status.update(label="Data fetched", state="complete")
        
        with st.status("Processing data...") as status:
            # Clean the posts
            posts = pd.DataFrame(data)
            posts = data_cleaning.clean_posts(posts)

            # Get embeddings
            posts = embeddings.embed_posts(posts)
            query_embedding = embeddings.get_embeddings(subreddit + query)
            status.update(label="Data processed", state="complete")
        
        with st.status("Getting top posts...") as status:
            # Rank posts by similarity
            top_posts = similarity.rank_cosine_similarity(query_embedding, posts['embedding'].tolist(), posts)
            status.update(label="Top posts retrieved", state="complete")
                    
        with st.status("Summarizing posts...") as status:
            # Summarize the posts
            summarization = summarize.summarize_posts(subreddit, query, pd.DataFrame(top_posts)['cleaned_text'])
            status.update(label="Posts summarized", state="complete")
        st.success("Search complete!")
        st.write(summarization)
        st.subheader("Top Posts")
        for post in top_posts:
            with st.expander(f"{post['title']}", expanded=False):
                st.write(post['body'])
                st.markdown(f"[View on Reddit]({post['url']})")
            
if __name__ == "__main__":
    main()