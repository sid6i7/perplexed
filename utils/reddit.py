import praw
import os

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

key = os.environ['GEMINI_API_KEY']
genai.configure(api_key=key)

class Reddit:
    """
    A class for interacting with Reddit API.
    """
    def __init__(self) -> None:
        """
        Initializes the Reddit class.

        Initializes Reddit instance and defines a filter for common bots.
        """
        self.reddit = self.get_reddit_instance()
        self.bot_filter = {
            #TODO: find more such common bots
            "AutoModerator",
            "GPT-3_Bot",
            "RemindMeBot"
        }

    def get_reddit_instance(self):
        """
        Gets an instance of Reddit.

        Returns:
            praw.Reddit: An instance of Reddit.
        """
        client_id = os.environ['REDDIT_CLIENT_ID']
        client_secret = os.environ['REDDIT_CLIENT_SECRET']
        username = os.environ['REDDIT_USERNAME']
        user_agent = f"Perplexed:v1.0 (by /u/{username}"
        try:
            reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        except Exception as e:
            print("Unable to get reddit instance", e)
            
        return reddit


    def search(self, query: str, subreddit="all", limit=5):
        """
        Searches for comments on Reddit based on the query.

        Args:
            query (str): The search query.
            subreddit (str, optional): The subreddit to search in. Defaults to "all".
            limit (int, optional): The number of comments to retrieve. Defaults to 5.

        Returns:
            list: A list of dictionaries containing information about the top comments.
        """
        search_results = self.reddit.subreddit(subreddit).search(query, limit=limit)
        all_top_comments = []
        for submission in search_results:
            comments = self.get_top_comments(submission)
            all_top_comments += [self.parse_comment(comment) for comment in comments]
        all_top_comments = sorted(all_top_comments, key=lambda comment: comment['score'], reverse=True)

        return all_top_comments


    def get_top_comments(self, submission: praw.models.Submission, limit=5):
        """
        Retrieves the top comments from a Reddit submission.

        Args:
            submission (praw.models.Submission): The Reddit submission.
            limit (int, optional): The number of top comments to retrieve. Defaults to 5.

        Returns:
            list: A list of top comments.
        """
        submission.comment_sort = 'best'
        submission.comments.replace_more(limit=0)
        comments = submission.comments.list()
        filtered_comments = [comment for comment in comments if str(comment.author) not in self.bot_filter]

        return filtered_comments[:limit]


    def parse_comment(self, comment: praw.models.Comment):
        """
        Parses a Reddit comment.

        Args:
            comment (praw.models.Comment): The Reddit comment to parse.

        Returns:
            dict: A dictionary containing information about the comment.
        """
        return {
            "body": comment.body,
            "score": comment.score,
            "url": f"https://www.reddit.com{comment.permalink}",
        }