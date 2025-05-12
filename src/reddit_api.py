import praw
from src import config
from datetime import datetime
import pandas as pd

def fetch_reddit_posts(subreddit_name, query, limit=100, comment_limit=10):
    reddit = praw.Reddit(
        client_id=config.REDDIT_CLIENT_ID,
        client_secret=config.REDDIT_CLIENT_SECRET,
        user_agent=config.REDDIT_USER_AGENT,
    )
    # Search subreddit using the query
    subreddit = reddit.subreddit(subreddit_name)
    # Search posts -- probably want to mess around with searching by relevance, top, etc.
    results = subreddit.search(query, limit=limit, sort='relevance', time_filter='year')
    
    posts = []
    for submission in results:
        # Fetch comments for each post
        submission.comments.replace_more(limit=0)
        sorted_comments = sorted(submission.comments, key=lambda c: c.score, reverse=True)
        top_comments = [
            {'id': c.id, 'body': c.body, 'score': c.score}
            for c in sorted_comments[:comment_limit]    
        ]
        
        # Append post data to the list
        posts.append({
            'id': submission.id,
            'title': submission.title,
            'body': submission.selftext,
            'url': submission.url,
            'date': datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d'),
            'subreddit': subreddit_name,
            'comments': top_comments,
        })
    return posts
        
