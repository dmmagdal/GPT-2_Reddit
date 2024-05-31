# writingpromptsBot.py
# author: Diego Magdaleno
# A bot based off of redditGPTBot.py that uses the program as a module
# to constantly download prompts and responses from the
# r/WritingPrompts subreddit and comes up with its own responses to
# those prompts and posts them.


import os
import json
import random
import praw
import redditGPTBot as rgptBot
from datetime import datetime


def main():
	# Log into Reddit account and instantiate a reddit instance. App
	# secret info can be found at https://www.reddit.com/prefs/apps/.
	# App credentials are loaded from the required json file.
	if not os.path.exists("reddit_bot_credentials.json"):
		print("Error: File reddit_bot_credentials.json not found.")
		print("Exiting program with error.")
		exit(1)
	with open("reddit_bot_credentials.json", "r") as config:
		credentials = json.load(config)
	reddit = praw.Reddit(user_agent=credentials["user_agent"],
						client_id=credentials["client_id"],
						client_secret=credentials["client_secret"],
						username=credentials["username"],
						password=credentials["password"])

	# Infinite loop.
	subreddit = "WritingPrompts"
	folder_path = "./" + subreddit
	while True:
		# Initialize static variables pertaining to using the PRAW or
		# redditGPTBot modules. This includes the subreddit (in this
		# case, r/WritingPrompts), the folder containing any post data
		# from the subreddit (usually the same name as the subreddit),
		# and the limit on how many posts to pull from the subreddit
		# (by default, use 100 unless there is no data from the
		# subreddit, then use 10000).
		limit = 100
		if not os.path.exists(folder_path) or len(os.listdir(folder_path)) == 0:
			limit = 10000

		# Pull the top results from the subreddit.
		rgptBot.pull_data(reddit, subreddit, limit)

		# Determine whether to post a response to a post.
		



	# Exit the program.
	exit(0)


if __name__ == '__main__':
	main()