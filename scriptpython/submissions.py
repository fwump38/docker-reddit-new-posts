#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Reddit New Post Bot 

'''
__author__ = '/u/fwump38'
__version__ = '2.0.0'

import os
import json
import time
import praw
import requests

###################
## Config
###################

# Subreddit
SUBREDDIT = os.environ.get('SUBREDDIT')

# Settings for PRAW
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
user_agent = 'python:submission_feed:{} (by /u/fwump38)'.format(__version__)

# Slack Details
WEBHOOK = os.environ.get('WEBHOOK')
CHANNEL = os.environ.get('CHANNEL', 'submission_feed')

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


###################
## Main
###################

# Create a Reddit Instance for PRAW
reddit = praw.Reddit(client_id=CLIENT_ID,
					 client_secret=CLIENT_SECRET,
					 user_agent=user_agent)

# Set start time
start_epoch = time.time() - 60 # 1 minute ago

# Create a subreddit instance
subreddit_obj = reddit.subreddit(SUBREDDIT)

processed = []
# Get the 20 most recent posts
for submission in subreddit_obj.new(limit=20):
	# Check if it's been created since the script was last run
	if submission.created_utc >= start_epoch:
		# Build slack message
		payload={
			'attachments': [build_attachment(submission)],
			'channel': '#{}'.format(CHANNEL)
		}

		# Send the response to the webhook
		response = requests.post(WEBHOOK, json=payload)