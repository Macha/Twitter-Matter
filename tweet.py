#!/usr/bin/python

import json
import sys
import urllib
import urllib2

class CLITweet:
	
	username = 'USERNAME'
	password = 'PASSWORD'


	def run(self):
		try:
			func = getattr(self, sys.argv[1])
		# Command not found
		except AttributeError:
			print "The command", sys.argv[1], "doesn't exist"
		# No action defined, show help
		except IndexError:
			self.help()
		else:
			if callable(func):
				try:
					func()
				except IndexError:
					print "Missing argument for command '" + sys.argv[1] + "' check help"

	def setup(self):
		# Prepares API call that needs authentication
		password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
		password_manager.add_password(
			None, 'https://twitter.com/', self.username, self.password
		)
		auth_handler = urllib2.HTTPBasicAuthHandler(password_manager)
		opener = urllib2.build_opener(auth_handler)
		urllib2.install_opener(opener)
				

	def tweet(self):
		# Tweet to API
		self.setup()
		tweet = ' '.join(sys.argv[2:])
		if len(tweet) > 140:
			print "Tweet is too long. Please limit yourself to 140 characters"
			sys.exit(1)

		params = urllib.urlencode({
			'status': tweet
		})
		try:
			data = urllib2.urlopen('http://twitter.com/statuses/update.json', params).read()
			print data
		except urllib2.HTTPError, e:
			print e.code
			print e.read()

	def mentions(self):
		# Gets latest @replies.
		self.setup()
		if len(sys.argv) == 3:
			number_of_tweets = str(sys.argv[2])
		else:
			number_of_tweets = str(10)
		
		
		try:
			data = urllib2.urlopen('http://twitter.com/statuses/mentions.json?count=' \
			+ number_of_tweets).read()

		except urllib2.HTTPError, e:
			print e.code
			print e.read()
			sys.exit(1)

		self.print_tweets(data)

	def friends(self):
		# Get latest tweets from friends
		self.setup()
		if len(sys.argv) == 3:
			number_of_tweets = str(sys.argv[2])
		else:
			number_of_tweets = str(10)

		try:
			data = urllib2.urlopen('http://twitter.com/statuses/home_timeline.json?count=' \
			+ number_of_tweets).read()

		except urllib2.HTTPError, e:
			print e.code
			print e.read()
			sys.exit(1)

		self.print_tweets(data)

			
	def print_tweets(self, tweets):
		# Prints a group of tweets fetched from another function.
		tweets = json.loads(tweets)
		for tweet in tweets:
			print tweet['user']['screen_name'], ': \t', tweet['text']
			print

	def help(self):
		# Print help information
		print
		print "Usage:"
		print "\t tweet <tweet> - Sends a tweet"
		print "\t friends [<num>] - Gets latest <num> tweets from friends"
		print "\t mentions [<num>] - Gets latest <num> @replies
		print "\t help - Prints help information"
		print

CLITweet().run()
