import tweepy
import json
from datetime import datetime, time, timedelta
import random

def connect():
    try:
        #GET YOURS FROM TWITTER DEVELOPERS, & USE ENV VARIABLES, NO PLAINTEXT SECRETS ON YOUR CODE! 
        API_KEY=""
        API_SECRET_KEY=""
        ACCESS_TOKEN=""
        ACCESS_TOKEN_SECRET=""

        auth=tweepy.OAuthHandler(API_KEY,API_SECRET_KEY)
        auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
        api=tweepy.API(auth)
        api.verify_credentials()
        print("Correctly connected!")
    except:
        print("Not connected")

def get_winners(retweeters, n_winners=5):
    message='Hey! The Winners are:'
    random.shuffle(retweeters)
    for user_id in retweeters[:n_winners]:
        message=message+" @"+api.get_user(user_id).screen_name
    return message



connect()

treated=[]
while True:

    mentions = api.mentions_timeline(count=1)
    now = datetime.now()

    for mention in mentions:
        #if now > (mention.created_at + timedelta(hours=1) + timedelta(seconds=10)):
        if mention.id not in treated:
            print ("there's a mention in the last 10 seconds")

            #Tweet from which we get the list of retweeters
            original_status=mention.in_reply_to_status_id
            
            #List of retweeters
            retweeters=api.retweeters(original_status)

            #Format the message/status to send
            message=get_winners(retweeters)

            #Post the status
            api.update_status(message,in_reply_to_status_id=mention.id,auto_populate_reply_metadata=True)

            #Send a direct message
            api.send_direct_message(mention.user.id,message)
            treated.append(mention.id)

            except tweepy.RateLimitError: #Handling twitter api limits
                time.sleep(15 * 60)
        else:
            print ("do nothing, no recent tweets/the last mention was is treated")



