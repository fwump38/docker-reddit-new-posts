#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Reddit New Post Bot sy

'''
__author__ = '/u/fwump38'
__version__ = '2.0.0'

import os
import time
import logging
# non-standard
import praw
import requests

###################
## Config
###################

# Settings for PRAW
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
user_agent = 'python3:submission_feed bot:{} (by /u/fwump38)'.format(__version__)
SUBREDDIT = os.environ.get('SUBREDDIT')

# Settings for Slack
WEBHOOK = os.environ.get('WEBHOOK')
CHANNEL = os.environ.get('CHANNEL', 'submission_feed')

# Setup Logging
logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

###################
## Functions
###################

def build_attachment(submission):
	title = submission.title
	author = submission.author.name
	author_link = 'https://www.reddit.com/user/{0}'.format(author)
	ts = submission.created_utc
	downs = submission.downs
	ups = submission.ups
	score = submission.score
	flair = submission.link_flair_text
	comments = submission.num_comments
	reports = submission.num_reports
	url = submission.url
	permalink = 'https://www.reddit.com{0}'.format((submission.permalink).encode('utf-8'))
	
	if submission.selftext != '':
		text = submission.selftext[:130]
	else:
		text = ''

	attachment = {
		'fallback':title.encode('utf-8'),
		'color':'#36a64f',
		'title':title.encode('utf-8'),
		'title_link':permalink,
		'author_name':author,
		'author_link':author_link,
		'text':text.encode('utf-8'),
		'fields':[  
				  {  
					 'title':'Flair',
					 'value':flair,
					 'short':'true'
				  },
				  {  
					 'title':'url',
					 'value':url.encode('utf-8'),
					 'short':'false'
				  }
		],
		'footer':'Slack API',
		'ts':ts
	}
	return attachment

def check_subreddit():
	logger.info('Checking {}'.format(SUBREDDIT))
	
	# Set start time
	start_epoch = time.time() - 60 # 1 minute ago

	# Create a subreddit instance
	sub = reddit.subreddit(SUBREDDIT)

	# Get the 10 most recent posts
	logger.info('Getting the latest 10 submissions')
	for submission in sub.new(limit=10):
		# Check if it's been created in the last minute
		if submission.created_utc >= start_epoch:
			logger.info('New post detected! Title: {}'.format(submission.title.encode('utf-8')))
			# Build slack message
			payload={
				'attachments': [build_attachment(submission)],
				'channel': '#{}'.format(CHANNNEL)
			}
			# Send the response to the webhook
			response = requests.post(WEBHOOK, json=payload)

def main():
	while True:
		try:
			check_subreddit()
		except Exception as e:
			logger.error('Issue checking {}: {}'.format(sub_name, e))
		logging.info('Sleeping...')
		time.sleep(60)

###################
## Main
###################

if __name__ == '__main__':

	# Create a Reddit Instance for PRAW
	reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=user_agent)

	# Start Loop
	main()