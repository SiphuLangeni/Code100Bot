from os import environ
from datetime import datetime as dt
from datetime import timedelta
from time import sleep
from tweepy import OAuthHandler, Stream, API
from tweepy.streaming import StreamListener
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class LikesListener(StreamListener):

    
    def __init__(self, api, delta=1):
        self.api = api
        self.delta = timedelta(days=delta)
        self.me = api.me()
        self.start_time = dt.utcnow().replace(second=0, microsecond=0)
        self.num_likes = 0
        

    def on_status(self, tweet):
        if 'retweeted_status' not in tweet._json and tweet.in_reply_to_status_id is None:

            now = dt.utcnow().replace(second=0, microsecond=0)
            diff = now - self.start_time
            
            keywords = ['data science', 'datascience', 'machine learning', 'machinelearning', \
                        'deep learning', 'deeplearning', 'nlp', 'natural language processing', \
                        'naturallanguageprocessing', 'computer vision','computervision', \
                        'python', 'tensorflow', 'pytorch', 'bwiai', 'blacktechtwitter']
            
            if any(keyword in test.casefold() for keyword in test.casefold()):
            
            
                if diff >= self.delta:
                    self.start_time = now
                    self.num_likes = 0


                try:
                    tweet.favorite()
                    self.num_likes += 1
                    if self.num_likes % 10 == 0:
                        logger.info(f'Liked {self.num_likes} tweets in {diff.seconds / 3600:.2f} hours')

                except Exception as e:
                    logger.error('Unable to like this tweet')


                if self.num_likes == 900:
                    sleep_time = 86_400 - diff.seconds
                    logger.info(f'900 tweets liked. Sleeping for {sleep_time / 3600:.2f} hours')
                    sleep(sleep_time)
                    self.start_time = now
                    self.num_likes = 0
                
            
    def on_error(self, status_code):
        if status_code == 420:
            return False

    
def twitter_auth():
    '''
    Authenticate credentials for Twitter API
    Builds an OAuthHandler from environment variables
    Returns auth
    '''

    auth = OAuthHandler(environ.get('CONSUMER_KEY'), environ.get('CONSUMER_SECRET'))
    auth.set_access_token(environ.get('ACCESS_TOKEN'), environ.get('ACCESS_TOKEN_SECRET'))
    
    api = API(
        auth,
        wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True
    )

    try:
        api.verify_credentials()
    
    except Exception as e:
        logger.error('Unable to authenticate', exc_info=True)

    logger.info('Code100Bot authenticated')

    return api


def like_tweets(api, keyword_list):

    likes_listener = LikesListener(api)
    stream = Stream(api.auth, likes_listener, tweet_mode='extended')
    stream.filter(track=keyword_list, languages=['en'])


if __name__ == "__main__":
    
    api = twitter_auth()
    keyword_list = ['#100DaysOfCode']

    like_tweets(api, keyword_list)
    