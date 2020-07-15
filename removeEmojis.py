#!/usr/bin/env python
"""
Remove emoji from a text file and print it to stdout.
Usage
-----
	python remove-emoji.py input.txt > output.txt
"""
import re
import sys

def removeAllEmojis(string):
	emoji_pattern = re.compile("["
						   u"\U0001F600-\U0001F64F"  # emoticons
						   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
						   u"\U0001F680-\U0001F6FF"  # transport & map symbols
						   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
						   u"\U00002702-\U000027B0"
						   u"\U000024C2-\U0001F251"
						   "]+", flags=re.UNICODE)
	return emoji_pattern.sub(r'', string)

def removeFirstEmoji(string):
	emoji_pattern = re.compile("["
						   u"\U0001F600-\U0001F64F"  # emoticons
						   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
						   u"\U0001F680-\U0001F6FF"  # transport & map symbols
						   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
						   u"\U00002702-\U000027B0"
						   u"\U000024C2-\U0001F251"
						   "]+", flags=re.UNICODE)
	return re.sub(emoji_pattern, r'', string, 1)

if __name__ == '__main__':
	operation = sys.argv[1]
	text = open(sys.argv[2]).read()

	if (operation == '--all'):
		text = removeAllEmojis(text)
	
	if (operation == '--first'):
		text = removeFirstEmoji(text)

	print(text)