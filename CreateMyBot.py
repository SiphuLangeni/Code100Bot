from os import environ
from datetime import datetime as dt
from datetime import timedelta
from time import sleep
from tweepy import OAuthHandler, Stream, API
from tweepy.streaming import StreamListener
import logging


logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger()


# Enter list of hashtags/search terms e.g. ['#HelloWorld']
hashtag_list = []

# Enter keywords to further refine your search e.g. ['Python', 'CodeNewbie]
keywords = []

'''
Customize your LikesListener class
==================================
You can change some of the default arguments to get the
desired behavior from your auto likes Twitter bot (line 43) or
pass the parameters while creating an instance (line 155)

max_likes
Maximum likes allowed daily = 1000
default is set to 900 to allow some headroom

log_interval
Change the frequency of the logs.
default creates a log every 50 tweets

delta
Change the time interval that tweets are liked.
Remember, rate limits are based on daily values.
default is 1.0 day
'''

class LikesListener(StreamListener):
    
    def __init__(self, api, keywords=keywords, max_likes=900, log_interval=50, delta=1.0):

        self.api = api
        self.keywords = keywords
        self.max_likes = max_likes
        self.update_interval = update_interval
        self.delta = timedelta(days=delta)
        self.me = api.me()
        self.start_time = dt.now().replace(second=0, microsecond=0)
        self.num_likes = 0
        

    def on_status(self, tweet):

        if 'retweeted_status' not in tweet._json \
        and tweet.in_reply_to_status_id is None \
        and tweet.user.id != self.me.id:
            
            now = dt.now().replace(second=0, microsecond=0)
            diff = now - self.start_time
            
            if diff >= self.delta:
                self.start_time = now
                self.num_likes = 0


            try:
                tweet_text = tweet.extended_tweet['full_text']
            
            except:
                tweet_text = tweet.text
            
            if any(keyword in tweet_text.casefold() for keyword in self.keywords): 
                
                try:
                    tweet.favorite()
                    self.num_likes += 1
                    if self.num_likes % self.log_interval == 0:
                        logger.info(
                            f'Liked {self.num_likes} {self.plural(self.num_likes)} '
                            f'at {dt.strftime(now, "%H:%M")}\n'
                        )

                except Exception as e:
                    logger.error(f'{e}\n')


                if self.num_likes == self.max_likes:
                    
                    start_time_str = dt.strftime(self.start_time, '%H:%M')
                    start_date_str = dt.strftime(self.start_time, '%b %d')
                    pause_time_str = dt.strftime(now, '%H:%M')
                    pause_date_str = dt.strftime(now, '%b %d')
                    sleep_time = 86_400 - diff.seconds
                    
                    resume_at = now + timedelta(seconds=sleep_time)
                    resume_time_str = dt.strftime(resume_at, '%H:%M')
                    resume_date_str = dt.strftime(resume_at, '%b %d')


                    logger.info(
                        f'Liked {self.num_likes} {self.plural(self.num_likes)}\n'
                        f'Sleeping for {sleep_time / 3600:.2f} hours\n'
                        f'Code100Bot will resume at {resume_time_str} on {resume_date_str}\n'
                    )
                    sleep(sleep_time)
                    self.start_time = now
                    self.num_likes = 0
                

    def plural(self, num_tweets):
        
        if self.num_likes == 1:
            plural = 'tweet'
        else:
            plural = 'tweets'
        
        return plural


    def on_error(self, status_code):
       
        if status_code == 420:
            return False

    
def twitter_auth():
   
    auth = OAuthHandler(environ.get('CONSUMER_KEY'), \
        environ.get('CONSUMER_SECRET'))
    auth.set_access_token(environ.get('ACCESS_TOKEN'), \
        environ.get('ACCESS_TOKEN_SECRET'))
    
    api = API(
        auth,
        wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True
    )

    api.verify_credentials()
        
    return api
        

def like_tweets(api, hashtag_list):
    '''
    Auto like tweets by hashtag

    :param hashtag_list: Hashtags to filter live stream by
    :type hashtag_list: list
    '''

    likes_listener = LikesListener(api)
    logger.info('Code100Bot authentication successful\n')
    stream = Stream(api.auth, likes_listener, tweet_mode='extended')
    logger.info('Searching tweets...\n')
    stream.filter(track=hashtag_list, languages=['en'])


if __name__ == "__main__":
    
    api = twitter_auth()
    
    try:
        like_tweets(api, hashtag_list)
    
    except Exception as e:
        logger.error(f'{e}\n')
        