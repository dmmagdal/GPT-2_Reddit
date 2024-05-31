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
#from transformers import pipeline, set_seed
#from transformers import TFGPT2LMHeadModel, GPT2Tokenizer, TFGPT2Model
#from transformers import GPT2Model
import happytransformer as ht


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
	#pull_data(reddit, "WallStreetBets", 100)

	# Interact with different posts and comments using a language model.
	#post_or_reply(reddit, "WritingPrompts", id, is_post)

	# Go to r/WritingPrompts and come up with a response for a post.
	writing_prompts_subreddit = reddit.subreddit("WritingPrompts").hot()
	top_10_posts = [submission for submission in writing_prompts_subreddit
					if not submission.stickied][:10]
	MAX_LENGTH = 1024
	NUM_SAMPLES = 10
	for post in top_10_posts:
		if "[WP]" in post.title:
			writing_prompt = post.title.lstrip("[WP] ")
			generate_text(writing_prompt, MAX_LENGTH, NUM_SAMPLES)

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


# Pull new posts and their comments from reddit and store it in a JSON
# file. Return the contents of the JSON file now containing the new
# posts.
# @param: reddit, reddit API wrapper instance.
# @param: subreddit_name, the name of the subreddit to interact with.
# @param: limit, the maximum number of posts to be pulled from the
#	subreddit (may not be the same as the actual number of new posts
#	saved). By default, the limit is 10 posts.
# @return: returns a json object containing the most recent "hot" posts
#	from the specified subreddit as well as their top layer comments.
def pull_data(reddit, subreddit_name, limit=10):
	# Get the desired subreddit.
	print("Accessing Top Hot Posts from r/" + subreddit_name + "...")
	#subreddit = reddit.subreddit(subreddit_name).hot()
	subreddit = reddit.subreddit(subreddit_name).hot(limit=limit)

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

	# Get the top (hot) posts from the subreddit (ignore stickied
	# posts).
	#top_10_posts = [submission for submission in subreddit 
	#				if not submission.stickied][:10]
	top_posts = [submission for submission in subreddit
				if not submission.stickied]

	# Iterate through the posts.
	#for post in top_10_posts:
	for post in top_posts:
		# Print the post title and extract each post's (top level)
		# comments.
		#print(post.title)
		#print(post)
		#print("-"*20)
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
									"author": post.author.name if post.author.name else "deleted",
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

	# Return the post data.
	return saved_posts


# Comment on or reply to posts or other comments in a subreddit.
# @param: reddit, reddit API wrapper instance.
# @param: subreddit_name, the name of the subreddit to interact with.
# @return: returns nothing.
def post_or_reply(reddit, subreddit_name):
	# Get the desired subreddit.
	subreddit = reddit.subreddit(subreddit_name).hot()
	
	# Return the function.
	return


# Use the models from huggingface to get text output from a given prompt.
# @param: input_prompt, a string that is the prompt for the text
#	generation model.
# @param: max_len, the maximum length the response is expected to be.
# @param: num_return_samples, the number of output samples to return
#	from the model.
# @return: returns nothing.
def generate_text(input_prompt, max_len, num_return_samples):
	#'''
	# Generate text given GPT-2 model pre-trained by HuggingFace.
	generator = pipeline("text-generation", model="gpt2")
	#set_seed(42)
	sample_output = generator(input_prompt, max_length=max_len, 
								num_return_sequences=num_return_samples)
	idx = 1
	#print(json.dumps(sample_output))
	print("Prompt: " + input_prompt)
	print("Samples:")
	for sample in sample_output:
		print("Sample Number {}: {}".format(idx, sample["generated_text"].lstrip(input_prompt)))
		idx += 1
	#'''

	'''
	# Generate text using the model directly. NOTE: will have to check
	# version of huggingface transformers and the required versions of
	# Python (3), PyTorch, and Tensorflow.
	tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
	# model = TFGPT2Model.from_pretrained("gpt2")
	# encoded_input = tokenizer(input_prompt, return_tensors="tf")
	# sample_output = model(encoded_input)
	model = GPT2Model.from_pretrained("gpt2")
	encoded_input = tokenizer(input_prompt, return_tensors="pt")
	sample_output = model(**encoded_input)
	print(sample_output)
	print(type(sample_output))
	'''

	# Return the function.
	return sample_output


# Train a text generation model on a particular set of data from a 
# subreddit and save it.
# @param: training_data,
# @param: subreddit,
# @param: model_name,
# @return: returns nothing.
def train_model(training_data, subreddit, model_name):
	pass


if __name__ == '__main__':
	main()