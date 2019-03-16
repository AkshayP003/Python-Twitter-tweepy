import tweepy
import pandas as pd

def lookup_user_list(user_id_list, api):
    full_users = []
    users_count = len(user_id_list)
    try:
        for i in range((users_count // 100) + 1):
            print (i)
            full_users.extend(api.lookup_users(user_ids=user_id_list[i * 100:min((i + 1) * 100, users_count)]))
        return full_users
    except tweepy.TweepError:
        print ('Something went wrong, quitting...')

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

ids = []
for page in tweepy.Cursor(api.followers_ids, screen_name="").pages():
    ids.extend(page)

results = lookup_user_list(ids, api)
all_users = [{'id': user.id,
             'Name': user.name,
             'Screen Name': user.screen_name,
             'Location': user.location,
             'URL': user.url,
             'Description': user.description,
             'Protected': user.protected,
             'Followers Count': user.followers_count,
             'Friends Count': user.friends_count,
             'Listed Count': user.listed_count,
             'Created at': user.created_at,
             'Favourites Count': user.favourites_count,
             'UTC Offset': user.utc_offset,
             'Time zone': user.time_zone,
             'Geo enable': user.geo_enabled,
             'Verified': user.verified,
             'Statuses Count': user.statuses_count,
             'Language': user.lang,
             'Contributors Enabled':user.contributors_enabled
             } for user in results] 
              

df = pd.DataFrame(all_users,columns = ['id','Name','Screen Name','Location','URL','Description','Protected','Followers Count','Friends Count','Listed Count','Created at','Favourites Count','UTC Offset','Time zone','Geo enable','Verified','Statuses Count','Language','Contributors Enabled'])


df.to_csv('Data.csv', index=False, encoding='utf-8')