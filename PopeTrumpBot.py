from twython import Twython, TwythonError
from threading import Timer
from secrets import *
from random import randint

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


def getTrumpTweet():
	"""
	Saves Trump's most current tweet
	as a string
	"""
	trump_timeline = twitter.get_user_timeline(screen_name="realDonaldTrump",count=1)
	for tweet in trump_timeline:
		#print(tweet['text'].encode('utf8')).decode('utf8')
		print("Got Trump Tweet!")
		return tweet['text'].encode('utf8').decode('utf8')


def getPopeTweet():
	"""
	Saves the pope's most current tweet
	as a string
	"""
	pope_timeline = twitter.get_user_timeline(screen_name="Pontifex",count=1)
	for tweet in pope_timeline:
		#print(tweet['text'].encode('utf8')).decode('utf8')
		print("Got Pope Tweet!")
		return tweet['text'].encode('utf8').decode('utf8')


def getPopeTrumpTweet():
	"""
	Saves the bot's most recent tweet
	"""
	pope_timeline = twitter.get_user_timeline(screen_name="Pope_Trump",count=1)
	for tweet in pope_timeline:
		#print(tweet['text'].encode('utf8')).decode('utf8')
		print("Got PopeTrump Tweet!")
		return tweet['text'].encode('utf8').decode('utf8')




def makeNewTweet(popeWords, trumpWords):
	"""
	Takes takes 2 lists of words
	and combines them
	"""
	numEdits = 0											#counter of number of changes made to tweet
	newWords = []											#put new tweet in this list
	index = 0

	whoFirst = randint(0,1)									#if 0, pope first. if 1, Trump first
	# print(whoFirst)
	if(whoFirst == 0):												#if the Pope is first
		print("Pope First!")
		halfPopeWords = popeWords[:len(popeWords)//2]				#Get the first half of the Pope's tweet
		halfTrumpWords = trumpWords[len(trumpWords)//2:]			#Get the latter half of Trump's tweet

		currLen = len(' '.join(halfPopeWords + halfTrumpWords))		#get the character count of the combined tweets
		while(currLen > 140):										#Make sure that the count doesn't go over 140
			if len(halfPopeWords) > len(halfTrumpWords):			#If it does, take off one word
				halfPopeWords = halfPopeWords[:-1]					#from the half with the most words
			else:
				halfTrumpWords = halfTrumpWords[1:]
			currLen = len(' '.join(halfPopeWords + halfTrumpWords))	#update character count

		newWords = halfPopeWords + halfTrumpWords					#set the tweet to the new combined tweet
	else:															#If Trump is first
		halfTrumpWords = trumpWords[:len(trumpWords)//2]			#Get the first half of trump's tweet
		halfPopeWords = popeWords[len(popeWords)//2:]				#and the latter half of the pope's tweet

		currLen = len(' '.join(halfTrumpWords + halfPopeWords))		#get character count of combined tweets
		while(currLen > 140):										#check if character count goes over 140
			if len(halfPopeWords) > len(halfTrumpWords):			#If over, take off word from
				halfPopeWords = halfPopeWords[1:]					#half with more words
			else:
				halfTrumpWords = halfTrumpWords[:-1]
			currLen = len(' '.join(halfTrumpWords + halfPopeWords))	#update character count

		newWords = halfTrumpWords + halfPopeWords					#set tweet to new combined tweet

	newLen = len(' '.join(newWords))						#the length of the new tweet
	print("Character Count:",newLen)
	return newWords											#return the new tweet


	

def tweet(tweet):
	"""
	Tweets a string
	"""
	twitter.update_status(status = tweet);



def runBot():
	print("Bot running!")

	trumpTweet = getTrumpTweet()				#Get Trump's latest tweet
	#trumpTweet = ""
	try:
		print(trumpTweet)
	except:
		print("Cannot print Trump tweet")


	popeTweet = getPopeTweet()					#Get the pope's latest tweet
	# popeTweet = ""
	try:
		print(popeTweet)
	except:
		print("Cannot print Pope tweet")


	lastTweet = getPopeTrumpTweet()				#set the last tweet to the bot's latest tweet

	#Edit the tweets
	newTweet = ' '.join(makeNewTweet(popeTweet.split(), trumpTweet.split()))

	if newTweet != lastTweet:					#make sure the bot hasn't edited the tweet before
		
		try:
			print(newTweet)
		except:
			print("Cannot print new tweet")

		if not debug:							#if not in debug mode
			try:
				tweet(newTweet)					#tweet the new tweet
				print("I just tweeted!")
			except:
				print("Ran into a problem tweeting!")
	else:
		print("No new Tweet!")




def setInterval(func, sec):
	def func_wrapper():
		setInterval(func, sec)
		func()
	t = Timer(sec, func_wrapper)
	t.start()
	return t


debug = False
runOnce = True

runBot()
if not runOnce:
	setInterval(runBot, 60*60*1)		#runs every hour