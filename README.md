# Reddit New Post Feed
A docker to monitor a subreddit for new posts and post them to a Slack channel

## Configuration

* You need a Reddit account that can use the Reddit API. See the [PRAW Quick Start Guide](https://praw.readthedocs.io/en/latest/getting_started/quick_start.html) for details.
* Slack Team with an [Incoming Webhook](https://api.slack.com/incoming-webhooks) configured

## Setup
```
scriptpython/
├── requirements.txt     (requirements for python)
└── submissions.py              (script that checks for new posts)
```

Modify to set date time to execute
```
* * * * *  /home/fwump38/scriptpython.sh
 ┬ ┬ ┬ ┬ ┬
 │ │ │ │ │
 │ │ │ │ │
 │ │ │ │ └───── day of week (0 - 7) (0 to 6 are Sunday to Saturday, 7 is Sunday again)
 │ │ │ └────────── month (1 - 12)
 │ │ └─────────────── day of month (1 - 31)
 │ └──────────────────── hour (0 - 23)
 └───────────────────────── min (0 - 59)
```

## Usage

Quick Setup:

```shell
docker run -t -i -d \
  -e CLIENT_ID=xxxxxxx \
  -e CLIENT_SECRET=xxxxxxx \
  -e SUBREDDIT=askscience \
  -e WEBHOOK=xxxxxx \
  -e CHANNEL=new_posts \
  fwump38/reddit-new-posts:latest
```

### Parameters

* `--restart=always` - ensure the container restarts automatically after host reboot.
* `-e CLIENT_ID` - The Client ID of the Reddit Bot that will be checking for new posts. **Required**
* `-e CLIENT_SECRET` - The Client Secret of the Reddit Bot that will be checkig for new posts. **Required**
* `-e SUBREDDIT` - The name of the subreddit to monitor (has not been tested with high volume subreddits). **Required**
* `-e WEBHOOK` - The Slack incoming webhook that is used to write new posts to a Slack channel . **Required**
* `-e CHANNEL` - The Slack to write to. Default is submission_feed.

