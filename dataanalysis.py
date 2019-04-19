"""
TODO: Only select tweets from these four celebrities 
desired_accounts = ("Ariana Grande", "Katy Perry", "Oprah", "Taylor Swift")
"""

import csv
import nltk
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

import matplotlib.pyplot as plt

def clean(word):
	word = word.lower()
	word = word.replace(".", "")
	word = word.replace(",", "")
	word = word.replace("\"", "")
	word = word.replace("\\", "")
	word = word.replace('"', "")
	word = word.replace("\n", "")
	return word

def clean_list(adjectives):
	for i, adj in enumerate(adjectives):
		# If the adjective is an @ sign, delete it
		if adj == "@":
			del adjectives[i]
		# If the adjetive contains a stop word, delete it
		if adj in STOPWORDS:
			del adjectives[i]
	return adjectives

def create_wordcloud(words):
	adjectives = " "
	
	for k, v in words.items():
		adjectives = adjectives + " ".join(v) + " "
	
	# Create and return the wordcloud
	w  = WordCloud().generate(adjectives)

	return w

def find_positive_adjectives(adjectives):
	positives = []
	# For every mention in the dictionary
	for k, v in adjectives.items():

		# For every adjective listed for this mention
		for i, adj in enumerate(v):
			
			# Find the sentiment of the adjective
			blob = TextBlob(adj, analyzer=NaiveBayesAnalyzer())
			
			print(blob.sentiment.classification)
			# If the sentiment is not possitive, delete the adjective
			if blob.sentiment.classification != "pos":
				del v[i]
		
		# Override the adjectives for this mention and move on to the next one
		adjectives[k] = v
	
	return adjectives

filename = "text_clean.csv"
MAX_USERNAME_LENGTH = 15
ADJECTIVE_TAGS = ("JJ", "JJR", "JJS")

# Dictionary to track just adjectives used for a person being mentioned
# key: the person mentioned
# value: list of adjectives
mention_adjectives = {}
count = 0

# Read CSV file
with open(filename, "r+") as rows:
	content = csv.reader(rows, delimiter=",") 
	for i, row in enumerate(content):
		if i == 20:
			break

		# Ignore empty rows
		if len(row) == 0:
			continue
		tweet = row[0]
		
		# Only read the tweet if it contains a mention
		if "@" in tweet:
			# Extract the mention
			mention = tweet.split("@")[1].split(":")[0]

			# Make sure mention only contains 1 username
			mention_split = mention.split(" ")
			if len(mention_split) != 0:
				mention = mention_split[0]

			# Check for handles that are longer than the max twitter handle length
			if len(mention) > MAX_USERNAME_LENGTH:
				# Only select the first 15 characters	
				mention = mention[0:15]
			
			# Tokenize tweet
			tweet_tokens = nltk.word_tokenize(tweet)
			
			# Find the adjectives and associate them with the person that was mentioned
			tags = nltk.pos_tag(tweet_tokens)
			adjectives = []
			for word in tags:
				# If the word is tagged with any of the adjective tags...
				if word[1] in ADJECTIVE_TAGS:
					# ...lean the word and add it to a list of adjectives
					adjectives.append(clean(word[0]))
			
			adjectives = clean_list(adjectives)

			# Associate the current mention with all of the found adjectives and
			# move to the next tweet. If they were already previously mentioned
			# add the newly found adjectives to the preexisting array.
			# If the adjective list is empty or only contains an @ sign, ignore it
			# And move to the next row
			if len(adjectives) == 0 or (len(adjectives) == 1 and "@" in adjectives):
				continue
			
			if mention in mention_adjectives:
				if len(mention_adjectives[mention]) != 0:
					mention_adjectives[mention].extend(adjectives)
			else:
				# The mention does not exist in the hash table yet, add it and associate
				# the adjectives that were just extracted from the tweet in the current row
				mention_adjectives[mention] = adjectives


# Create and display the generated wordcloud
plt.imshow(create_wordcloud(mention_adjectives)) 
plt.axis("off")
plt.show()


# Create a bargraph using only positive adjectives
# mention_adjectives = find_positive_adjectives(mention_adjectives)

# objects = ('Ariana Grande: @ArianaGrande', 'Katy Perry: @katyperry', 'Oprah: @Oprah', 'Taylor Swift: @taylorswift13')
# y_pos = np.arange(len(objects))
# performance = [10,8,6,4,2,1]
 
# plt.bar(y_pos, performance, align='center', alpha=0.5)
# plt.xticks(y_pos, objects)
# plt.ylabel('Usage')
# plt.title('Programming language usage')
