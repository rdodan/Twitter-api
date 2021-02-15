import tweepy
import time
import requests
from twilio.rest import Client
from creds import * 

auth = tweepy.OAuthHandler(API_key, API_key_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth)

client = Client(SID, token)





def retweet(hashtag, delay):
    while True:
        for tweet in tweepy.Cursor(api.search, q = hashtag, count = 20).items(2):
            try:
                tweet_id = dict(tweet._json)["id"]
                tweet_text = dict(tweet._json)["text"]
                api.retweet(tweet_id)
            except tweepy.TweepError as error:
                print(error.reason)
            
        time.sleep(delay)


def getuser(userid):
    tweet = api.get_user(userid)
    print(userid + "'s name is: " + tweet.name)





def timeline(userid, delay):
    checkFirstTweet = False
    oldStatus = api.user_timeline(userid, count = 1)
    for old in oldStatus:
        oldStatusID = old.id
    while True:
        try:
            for statuses in api.user_timeline(userid, count = 1):
                getNewID = statuses.id
                if (getNewID == oldStatusID):
                    print("Nothing new")
                else:
                    lowerCaseString = statuses.text.lower()
                    oldStatusID = getNewID
                    if (lowerCaseString.find("doge") != -1):  
                        print("Text: " + lowerCaseString)
                        msg = "Elon Musk posted: " + statuses.text
                        api.retweet(getNewID)
                        message = client.messages.create(
                            body=msg,
                            from_=mytwilio,
                            to=myphone
                        )
                        print(msg,'\t',message.sid)

            
        except tweepy.TweepError as error:
            print(error.reason)

        time.sleep(delay)



#retweet("#dogecointothemoon", 3600) 
#getuser("@elonmusk")
timeline("@elonmusk", 30)