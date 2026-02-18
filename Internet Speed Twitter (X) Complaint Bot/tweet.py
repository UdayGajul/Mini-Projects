#
# ! this python script is used to tweet on my X and is used as a module

import tweepy
import os
from dotenv import load_dotenv


load_dotenv()

# ^ all keys
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")

# ^ create a Tweepy client with API and access tokens
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_KEY_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
    # bearer_token= BEARER_TOKEN,
)


def tweet_a_post(tweet_text: str):
    """
    Post a tweet using the Tweepy client.
    Args:
        tweet_text (str): The content of the tweet to be posted.
    Prints:
        Success message, the tweet ID, and a public link if the post succeeds;
        otherwise prints an error message.
    """
    try:
        response = client.create_tweet(text=tweet_text)
        print("\nTweet posted successfully!")
        print("\nTweet ID: ", response.data["id"])
        print(f"Link: https://x.com/user/status/{response.data['id']}")
    except Exception as e:
        print("Error: \n", e)


# ^ Test tweet was successfull
# client.create_tweet(text="Test tweet! #Python #100DaysOfCode")
# print("Done! Check your profile.")
