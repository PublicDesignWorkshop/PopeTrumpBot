from twython import Twython, TwythonError
from threading import Timer
from secrets import *
from random import randint

import csv
import datetime

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


name = "Pope_Trump"

def getFollowers():
    """
    Gets details about followers of the bot
    """

    names = []                  #Name of follower
    usernames = []              #Username of follower
    ids = []                    #User id of follower
    locations = []              #Location of follower(as listed on their profile)
    follower_count = []         #How many followers the follower has
    time_stamp = []             #Date recorded

    datestamp = datetime.datetime.now().strftime("%Y-%m-%d")


    names.append("Display Name")
    usernames.append("Username (@)")
    ids.append("User ID")
    locations.append("Location")
    follower_count.append("# of their Followers")
    time_stamp.append("Time Stamp")

    next_cursor = -1

    #Get follower list (200)
    while(next_cursor):
        get_followers = twitter.get_followers_list(screen_name=name,count=200,cursor=next_cursor)
        for follower in get_followers["users"]:
            try:
                print(follower["name"].encode("utf-8").decode("utf-8"))
                names.append(follower["name"].encode("utf-8").decode("utf-8"))
            except:
                names.append("Can't Print")
            usernames.append(follower["screen_name"].encode("utf-8").decode("utf-8"))
            ids.append(follower["id_str"])

            try:
                print(follower["location"].encode("utf-8").decode("utf-8"))
                locations.append(follower["location"].encode("utf-8").decode("utf-8"))
            except:
                locations.append("Can't Print")

            follower_count.append(follower["followers_count"])
            time_stamp.append(datestamp)
            next_cursor = get_followers["next_cursor"]

    open_csv = open("followers.csv","r",newline='')                         #Read what has already been recorded in the followers file
    

    # names[0] = "@%s has %s follower(s) (%s)" % (str(username),str(len(follower_count)),str(datestamp))

    rows = zip(names,usernames,ids,locations,follower_count,time_stamp)     #Combine lists

    oldFollowerIDs = []                                                     #Store followers that have already been recorded in the past

    oldFollowers_csv = csv.reader(open_csv)

    for row in oldFollowers_csv:
            oldFollowerIDs.append(row[2])

    open_csv.close()

    open_csv = open("followers.csv","a", newline='')        #Append new followers to the followers file
    followers_csv = csv.writer(open_csv)
    for row in rows:
        if not (row[2] in oldFollowerIDs):                  #if the ID isn't already in the follower list
            followers_csv.writerow(row)

    open_csv.close()

def getMentionsRetweets():
    """
    Gets details of mentions/retweets of the user
    """

    names = []                  #Name of user who retweeted/mentioned
    usernames = []              #Their username
    ids = []                    #Their user id
    locations = []              #Their location (as listed on their profile)
    tweetIDs = []               #ID of the retweet/mention
    tweets = []                 #The retweet/mention text
    time_stamp = []             #Date the retweet/mention was created

    datestamp = datetime.datetime.now().strftime("%Y-%m-%d")

    names.append("Display Name")
    usernames.append("Username (@)")
    ids.append("User ID")
    locations.append("Location")
    tweetIDs.append("Tweet ID")
    tweets.append("Tweet Text")
    time_stamp.append("Time Stamp")

    #Get mentions (200)
    mentions_timeline = twitter.get_mentions_timeline(screen_name=name,count=200)
    for mention in mentions_timeline:
        try:
            print(mention['user']['name'].encode("utf-8").decode("utf-8"))
            names.append(mention['user']['name'].encode("utf-8").decode("utf-8"))
        except:
            names.append("Can't print")
        usernames.append(mention["user"]["screen_name"].encode("utf-8").decode("utf-8"))
        ids.append(mention["user"]["id_str"])
        try:
            print(mention["user"]["location"].encode("utf-8").decode("utf-8"))
            locations.append(mention["user"]["location"].encode("utf-8").decode("utf-8"))
        except:
            locations.append("Can't Print")
        tweetIDs.append(mention["id_str"])
        try:
            print(mention['text'].encode("utf-8").decode("utf-8"))
            tweets.append(mention['text'].encode("utf-8").decode("utf-8"))
        except:
            tweets.append("Can't Print")
        time_stamp.append(mention["created_at"].encode("utf-8").decode("utf-8"))

    #Get retweets (200)
    retweetedStatuses = twitter.retweeted_of_me(count = 100)                                    #Get tweets from the user that have recently been retweeted
    for retweetedStatus in retweetedStatuses:
        statusID = retweetedStatus["id_str"]
        retweets = twitter.get_retweets(id=statusID,count=100)                                  #Get the retweets of the tweet
        for retweet in retweets:
            try:
                print(retweet['user']['name'].encode("utf-8").decode("utf-8"))
                names.append(retweet['user']['name'].encode("utf-8").decode("utf-8"))
            except:
                names.append("Can't print")
            
            usernames.append(retweet["user"]["screen_name"].encode("utf-8").decode("utf-8"))

            ids.append(retweet["user"]["id_str"])

            try:
                print(retweet["user"]["location"].encode("utf-8").decode("utf-8"))
                locations.append(retweet["user"]["location"].encode("utf-8").decode("utf-8"))
            except:
                locations.append("Can't print")
            
            tweetIDs.append(retweet["id_str"])
            
            try:
                print(retweet['text'].encode("utf-8").decode("utf-8"))
                tweets.append(retweet['text'].encode("utf-8").decode("utf-8"))
            except:
                tweets.append("Can't print")
            
            time_stamp.append(retweet["created_at"].encode("utf-8").decode("utf-8"))


    open_csv = open("mentions_retweets.csv","r",newline='')
    

    # names[0] = "@%s has %s follower(s) (%s)" % (str(username),str(len(follower_count)),str(datestamp))
    # print(len(names))
    rows = zip(names,usernames,ids,locations,tweetIDs, tweets,time_stamp)

    oldMentionsIDs = []                             #Record mentions/retweets that have already been recorded before

    oldMentions_csv = csv.reader(open_csv)

    for row in oldMentions_csv:
            oldMentionsIDs.append(row[4])

    open_csv.close()

    open_csv = open("mentions_retweets.csv","a", newline='') #Append new mentions/retweets to the list
    mentions_csv = csv.writer(open_csv)
    for row in rows:
        if not (row[4] in oldMentionsIDs):          #if the ID isn't already in the mentions list
            # print(row)
            mentions_csv.writerow(row)

    open_csv.close()

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
    numEdits = 0                                            #counter of number of changes made to tweet
    newWords = []                                           #put new tweet in this list
    index = 0

    whoFirst = randint(0,1)                                 #if 0, pope first. if 1, Trump first
    # print(whoFirst)
    if(whoFirst == 0):                                              #if the Pope is first
        print("Pope First!")
        halfPopeWords = popeWords[:len(popeWords)//2]               #Get the first half of the Pope's tweet
        halfTrumpWords = trumpWords[len(trumpWords)//2:]            #Get the latter half of Trump's tweet

        currLen = len(' '.join(halfPopeWords + halfTrumpWords))     #get the character count of the combined tweets
        while(currLen > 140):                                       #Make sure that the count doesn't go over 140
            if len(halfPopeWords) > len(halfTrumpWords):            #If it does, take off one word
                halfPopeWords = halfPopeWords[:-1]                  #from the half with the most words
            else:
                halfTrumpWords = halfTrumpWords[1:]
            currLen = len(' '.join(halfPopeWords + halfTrumpWords)) #update character count

        newWords = halfPopeWords + halfTrumpWords                   #set the tweet to the new combined tweet
    else:                                                           #If Trump is first
        halfTrumpWords = trumpWords[:len(trumpWords)//2]            #Get the first half of trump's tweet
        halfPopeWords = popeWords[len(popeWords)//2:]               #and the latter half of the pope's tweet

        currLen = len(' '.join(halfTrumpWords + halfPopeWords))     #get character count of combined tweets
        while(currLen > 140):                                       #check if character count goes over 140
            if len(halfPopeWords) > len(halfTrumpWords):            #If over, take off word from
                halfPopeWords = halfPopeWords[1:]                   #half with more words
            else:
                halfTrumpWords = halfTrumpWords[:-1]
            currLen = len(' '.join(halfTrumpWords + halfPopeWords)) #update character count

        newWords = halfTrumpWords + halfPopeWords                   #set tweet to new combined tweet

    newLen = len(' '.join(newWords))                        #the length of the new tweet
    print("Character Count:",newLen)
    return newWords                                         #return the new tweet


    

def tweet(tweet):
    """
    Tweets a string
    """
    twitter.update_status(status = tweet);



def runBot():
    print("Bot running!")

    try:
        getFollowers()
    except:
        print("Couldn't get Followers")

    try:        
        getMentionsRetweets()
    except:
        print("Couldn't get Mentions/Retweets")

    trumpTweet = getTrumpTweet()                #Get Trump's latest tweet
    #trumpTweet = ""
    try:
        print(trumpTweet)
    except:
        print("Cannot print Trump tweet")


    popeTweet = getPopeTweet()                  #Get the pope's latest tweet
    # popeTweet = ""
    try:
        print(popeTweet)
    except:
        print("Cannot print Pope tweet")


    lastTweet = getPopeTrumpTweet()             #set the last tweet to the bot's latest tweet

    #Edit the tweets
    newTweet = ' '.join(makeNewTweet(popeTweet.split(), trumpTweet.split()))

    if newTweet != lastTweet:                   #make sure the bot hasn't edited the tweet before
        
        try:
            print(newTweet)
        except:
            print("Cannot print new tweet")

        if not debug:                           #if not in debug mode
            try:
                tweet(newTweet)                 #tweet the new tweet
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
runOnce = False

runBot()
if not runOnce:
    setInterval(runBot, 60*60*5)        #runs every 5 hours