from os import environ
from tweepy import OAuthHandler, Stream, API
from tweepy.streaming import StreamListener
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class LikesListener(StreamListener):

    
    def __init__(self, api):
        self.api = api
        self.me = api.me()


    def on_status(self, tweet):
        if 'retweeted_status' not in tweet._json and tweet.in_reply_to_status_id is None:

            try:
                tweet.favorite()
                logger.info(f'Liked a tweet from user @{tweet.user.screen_name}.')

            except Exception as e:
                logger.error('Unable to like this tweet')

            
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
    keyword_list = ['#100DaysOfCode', '#66DaysOfData', '#BWIAI']

    like_tweets(api, keyword_list)
    