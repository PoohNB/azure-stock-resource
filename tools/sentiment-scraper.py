import requests
import pandas as pd
from datetime import datetime, timedelta
from textblob import TextBlob
import time

def get_monthly_posts(query, after, before, subreddit="stocks", max_posts=900):
    url = "https://api.pushshift.io/reddit/search/submission/"
    params = {
        "q": query,
        "after": int(after.timestamp()),
        "before": int(before.timestamp()),
        "subreddit": subreddit,
        "size": max_posts,
        "sort": "desc"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["data"]
    return []

def run_sentiment_analysis(posts):
    results = []
    for post in posts:
        title = post.get("title", "")
        blob = TextBlob(title)
        results.append({
            "date": datetime.utcfromtimestamp(post.get("created_utc", 0)).strftime("%Y-%m-%d"),
            "title": title,
            "score": post.get("score", 0),
            "polarity": blob.polarity,
            "subjectivity": blob.subjectivity,
            "url": f"https://reddit.com{post.get('permalink', '')}"
        })
    return results

if __name__ == "__main__":
    # Just for January 2023
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 2, 1)

    print(f"🔍 Collecting Tesla posts from r/stocks ({start_date.date()} to {end_date.date()})...")
    posts = get_monthly_posts("Tesla", start_date, end_date)
    print(f"✅ Retrieved {len(posts)} posts")

    if posts:
        df = pd.DataFrame(run_sentiment_analysis(posts))
        df.to_csv("tesla_reddit_jan2023.csv", index=False)
        print("🎉 Saved to tesla_reddit_jan2023.csv")
    else:
        print("⚠️ No posts found. Try a more active subreddit or a different month.")
