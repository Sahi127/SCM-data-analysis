
import csv
import nltk

def clean(word):
	word = word.lower()
    word = word.replace(".","")
    word = word.replace(",","")
    word = word.replace("\"","")
    word = word.replace('"',"")
    word = word.replace("\n","")
	return word

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

                