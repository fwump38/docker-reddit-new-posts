#!/usr/bin/env python
"""
Reddit New Post Bot

"""

import os
import time
import logging

# non-standard
import praw
import requests

__author__ = "/u/fwump38"
__version__ = "1.0.1"

###################
## Config
###################

# Settings for PRAW
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
user_agent = "python3:submissions bot:{} (by /u/fwump38)".format(__version__)
SUBREDDIT = os.environ.get("SUBREDDIT")

# Settings for Slack
WEBHOOK = os.environ.get("WEBHOOK")
CHANNEL = os.environ.get("CHANNEL", "submission_feed")

# Setup Logging
logger = logging.getLogger()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

class Bot:

	def __init__(self, r):
		self.r = r
		

# def build_attachment(submission):
#     title = submission.title
#     author = submission.author.name
#     author_link = "https://www.reddit.com/user/{0}".format(author)
#     ts = submission.created_utc
#     flair = submission.link_flair_text
#     comments = submission.num_comments
#     reports = submission.num_reports
#     url = submission.url
#     permalink = "https://www.reddit.com{0}".format((submission.permalink))

#     if submission.selftext != "":
#         text = submission.selftext
#     else:
#         text = ""

#     attachment = {
#         "fallback": "{}".format(title),
#         "color": "#36a64f",
#         "title": "{}".format(title),
#         "title_link": permalink,
#         "author_name": author,
#         "author_link": author_link,
#         "text": "{}".format(text),
#         "fields": [
#             {"title": "Flair", "value": flair, "short": "true"},
#             {"title": "url", "value": "{}".format(url), "short": "false"},
#         ],
#         "footer": "Slack API",
#         "ts": ts,
#     }
#     return attachment


def check_submissions():
    logger.info(f"Checking Submissions")

    # Set start time
    start_epoch = time.time() - 60  # 1 minute ago

    # Get the 10 most recent posts
    logger.info("Getting the latest 10 submissions")
    for submission in sub.new(limit=10):
        # Check if it's been created in the last minute
        if submission.created_utc >= start_epoch:
            logger.info("New post detected! Title: {}".format(submission.title))
            # Build slack message
            payload = {
                "attachments": [build_attachment(submission)],
                "channel": "#{}".format(CHANNEL),
            }
            # Send the response to the webhook
            response = requests.post(WEBHOOK, json=payload)


def main():
    while True:
        try:
			sub = reddit.subreddit(SUBREDDIT)
            check_submissions(subr)
			check_modmails(subr)
			check_reports(subr)
        except Exception as e:
            logger.error("Issue checking subreddit: {}".format(e))
        logging.info("Sleeping...")
        time.sleep(32)


###################
## Main
###################

if __name__ == "__main__":

    # Create a Reddit Instance for PRAW
    reddit = praw.Reddit(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=user_agent
    )

    # Start Loop
    main()

