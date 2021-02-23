# redditGPTBot.py
# author: Diego Magdaleno
# This is a Reddit Bot that will use NLP language models like GPT-2 and
# BERT to understand language, subjects, and post reasonable responses.
# Python 3.7
# Windows/MacOS/Linux


import os
import json
import praw
import random
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

	# For debug only.
	#reddit_api_basics(reddit)

	# Scrape posts and comments for data collection.
	start = datetime.now()
	pull_data(reddit, "WallStreetBets")
	print("Took {} to scrape the top 10".format(datetime.now() - start) +\
			" posts (and their comments) from r/WallStreetBets")

	# Interact with different posts and comments using a language model.


	# Exit the program.
	exit(0)


# Go through the basics of using the Python Reddit API.
# @param: reddit, reddit API wrapper instance.
# @return: returns nothing.
def reddit_api_basics(reddit):
	# Access a specific subreddit.
	python_subreddit = reddit.subreddit("Python")

	# Can access subreddit contents in specified filter of "hot",
	# "new", "rising", "controversial", "top", etc as well as pass in a
	# limit.
	hot_python = python_subreddit.hot(limit=5)

	# Iterate through the results.
	for submission in hot_python:
		# Print the thread IDs returned. Each thread ID has a lot of
		# attributes with the dir() function.
		print(submission)
		#print(dir(submission))
		# print(submission.title)

		# Can check if submission is stickied.
		if not submission.stickied:
			print(submission.title)

			# Other popular attributes to check for include ups, downs,
			# visited.
			print(submission.ups)
			print(submission.downs)
			print(submission.visited)

			# Note that you can also take actions on submissions such
			# as upvote, downvote, reply, and subscribe/unsubscribe.
			#submission.upvote()
			#submission.downvote()
			#submission.reply()
			#python_subreddit.subscribe()
			#python_subreddit.unsubscribe()

			# Can pull comments from a submission.
			comments = submission.comments

			# Much like the submissions, the comments are also PRAW
			# objects and thus, have attributes
			for comm in comments:
				print("*"*20)
				#print(dir(comm))
				print(comm.body)
				if len(comm.replies) > 0:
					for reply in comm.replies:
						print("REPLY: " + reply.body)
			print("\n" + "-"*72 + "\n")

			# Alternative way of iterating through the comments. The
			# list() function takes all top level comments, lists them
			# out, and does that for the all sub level comments.
			comments = submission.comments.list()
			for comm in comments:
				print("-"*20)
				print("Parent ID: {}".format(comm.parent()))
				print("Comment ID: {}".format(comm.id))
				print(comm.body)

	# Return the function.
	return


# Pull new posts and their commentsfrom reddit and store it in a JSON
# file.
# @param: reddit, reddit API wrapper instance.
# @param: subreddit_name, the name of the subreddit to interact with.
# @return: returns nothing.
def pull_data(reddit, subreddit_name):
	# Get the desired subreddit.
	print("Accessing Top Hot Posts from r/" + subreddit_name + "...")
	subreddit = reddit.subreddit(subreddit_name).hot()

	# Check for the existance of a data file for that subreddit. If a
	# file exists for the subreddit, load it in, otherwise initialize
	# an empty dictionary.
	if not os.path.exists("./" + subreddit_name) or not os.path.isdir("./" + subreddit_name):
		os.mkdir("./" + subreddit_name)
	if not os.path.exists("./" + subreddit_name + "/posts.json"):
		saved_posts = {}
	else:
		with open("./" + subreddit_name + "/posts.json", "r") as data_file:
			saved_posts = json.load(data_file)

	# Get the top 10 (hot) posts from the subreddit (ignore stickied
	# posts).
	top_10_posts = [submission for submission in subreddit 
					if not submission.stickied][:10]

	# Iterate through the posts.
	for post in top_10_posts:
		# Print the post title and extract each post's (top level)
		# comments.
		print(post.title)
		print(post)
		print("-"*20)
		post_comments = [comment for comment in post.comments.list()
						if not isinstance(comment, praw.models.MoreComments) and \
						comment.parent_id == comment.link_id]

		# Add posts to the saved post data if the post id does not
		# appear in the saved posts.
		if post.id not in saved_posts:
			# Parse post comments.
			comment_dictionary = {}
			for comment in post_comments:
				comment_dictionary[comment.id] = {"comment_body": comment.body,
													"comment_author": comment.author.name if comment.author else "deleted",
													"comment_author_is_mod": comment.author.is_mod if comment.author else False,
													"comment_id": comment.id,
													"score": comment.score,
													"stickied": comment.stickied}

			# Parse post data and save it to the saved post data.
			saved_posts[post.id] = {"title": post.title,
									"author": post.author.name,
									"author_is_mod": post.author.is_mod,
									"url": post.url,
									"flair": post.author_flair_text,
									"text": post.selftext,
									"subreddit": post.subreddit.display_name,
									"subreddit_id": post.subreddit_id,
									"score": post.score,
									"number_of_comments": post.num_comments,
									"comments": comment_dictionary}
			#print(json.dumps(saved_posts[post.id], indent=4))
			#break

	# Save post data to json file.
	with open("./" + subreddit_name + "/posts.json", "w+") as data_file:
		json.dump(saved_posts, data_file, indent=4)

	# Return the function.
	return


# Comment on or reply to posts or other comments in a subreddit.
# @param: reddit, reddit API wrapper instance.
# @param: subreddit_name, the name of the subreddit to interact with.
# @return: returns nothing.
def post_or_reply(reddit, subreddit_name):
	# Get the desired subreddit.
	subreddit = reddit.subreddit(subreddit_name).hot()
	
	# Return the function.
	return


if __name__ == '__main__':
	main()