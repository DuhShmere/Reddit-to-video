from create_video_from_text import create_video_from_text
import praw

# --- Reddit API setup ---
reddit = praw.Reddit(
    client_id=
    client_secret=
    user_agent=
)

def main():
    # Ask for subreddit; default to TIFU if empty
    subreddit_name = input("Enter subreddit name (default TIFU): ").strip()
    if not subreddit_name:
        subreddit_name = "TIFU"

    print(f"📥 Fetching top post from r/{subreddit_name} ...")
    post = next(reddit.subreddit(subreddit_name).hot(limit=1))
    print(f"✅ Found post: {post.title}")

    # Pass title + post text to the video creator
    create_video_from_text(
        text=post.selftext,
        title=post.title,  # Reddit-style title box
        background_path="Background_reddit/background.mp4",  # change this if your video file has a different name
        output_video="final_video.mp4"
    )

if __name__ == "__main__":
    main()
