import requests, json
from src import config

def summarize_posts(subreddit, query, posts):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [{"text": f"You're summarizing for an app that helps users search Reddit. The user searched the {subreddit} subreddit for {query}. Summarize the returned posts for the user: {', '.join(posts)}"}]
            }
        ]
    }
    response = requests.post(config.GEMINI_API_URL + config.GEMINI_API_KEY, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        summary = response.json()
        return summary["candidates"][0]["content"]["parts"][0]["text"]
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None       