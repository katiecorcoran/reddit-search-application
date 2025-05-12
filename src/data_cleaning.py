import re

def clean_text(text):
    text = re.sub(r"http\S+|www\S+", '', text) # remove URLs
    text = re.sub(r"\[.*?\]\(.*?\)", '', text) # remove markdown links
    text = re.sub(r"’|‘|`", "'", text) # standardize apostrophes
    text = text.replace("\u200b", "") # replace other unique newline characters
    text = text.replace("x200b", "")
    text = re.sub(r"[\xa0\n\u200b]", ' ', text) # remove newline characters
    text = re.sub(r"[^a-zA-Z0-9'\s]", ' ', text) # remove special characters, keeping apostrophes until after contraction expansion
    text = re.sub("\s+", ' ', text).strip() # remove extra spaces
    return text

def aggregate_text(post):
    title = post.get('title', '')
    body = post.get('body', '')
    comments = post.get('comments', [])
    aggregated_text = title + ' ' + body + ' '.join([comment.get('body', '') for comment in comments])
    # Clean the aggregated text
    return aggregated_text

def clean_posts(posts):
    posts['all_text'] = posts.apply(lambda x: aggregate_text(x), axis=1)
    posts['cleaned_text'] = posts.apply(lambda x: clean_text(x['all_text']), axis=1)
    return posts
    