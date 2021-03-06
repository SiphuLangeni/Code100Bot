from os import environ
from datetime import datetime as dt
from datetime import timedelta
from time import sleep
from tweepy import OAuthHandler, Stream, API
from tweepy.streaming import StreamListener
import logging


logging.basicConfig(format='%(message)s', level=logging.INFO)
logger = logging.getLogger()


hashtag_list = ['#100DaysOfCode']

keywords = ['data science', 'datascience', 'machine learning', \
            'machinelearning', 'deep learning', 'deeplearning', \
            'nlp', 'natural language processing', \
            'naturallanguageprocessing', 'computer vision', \
            'computervision', 'python', 'tensorflow', 'pytorch', \
            'womenintech', 'womenwhocode', 'bwiai', 'blacktechtwitter']


class LikesListener(StreamListener):
    ''' 
    Class that receives messages from a :class:`tweepy.Stream` instance 
    
    :param api: Wrapper for Twitter API
    :type api: class:`tweepy.api.API` 
    
    :param keywords: Keywords to filter live twitter stream
    :type keywords: list

    :param max_likes: Maximum number of likes in delta period, defaults to 900
    :type max_likes: int, optional

    :param log_interval: Number of liked tweets per log message, defaults to 50
    :type log_interval: int, optional

    :param delta: Fraction of 1 day, defaults to 1.0
    :type delta: float, optional
    '''

    def __init__(self, api, keywords=keywords, max_likes=900, log_interval=25, delta=1.0):
        '''
        Constructor for :class:`LikesListener` class
        '''

        self.api = api
        self.keywords = keywords
        self.max_likes = max_likes
        self.log_interval = log_interval
        self.delta = timedelta(days=delta)
        self.me = api.me()
        self.start_time = dt.now().replace(second=0, microsecond=0)
        self.num_likes = 0
        

    def on_status(self, tweet):
        '''
        Receives data from statuses from :class:`StreamListener` class

        :param tweet: Tweet data
        :type tweet: str
        '''
        if 'bot' not in tweet.user.screen_name.casefold():

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
                                f'at {dt.strftime(now, "%H:%M")}'
                            )

                    except Exception as e:
                        logger.error(
                            f'{e}\n'
                            f'Screen Name: {tweet.user.screen_name}\n'
                            f'Tweet ID: {tweet.id}'
                        )
                        
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
                            f'Code100Bot will resume at {resume_time_str} on {resume_date_str}'
                        )
                        sleep(sleep_time)
                        self.start_time = now
                        self.num_likes = 0
                

    def plural(self, num_tweets):
        '''
        Applies proper pluralization to the string 'tweet'

        :param num_tweets: Number of tweets that have been liked
        :type num_tweets: int

        :returns: Correct plural form of tweet
        :rtype: str
        '''
        
        if self.num_likes == 1:
            plural = 'tweet'
        else:
            plural = 'tweets'
        
        return plural


    def on_error(self, status_code):
        '''
        Disconnect the stream if connection rate limit has been exceeded

        :param status_code: Status code
        :type status_code: int
        '''

        if status_code == 420:
            logger.error('420 - Too many requests')
            return False

        if status_code == 429:
            logger.error('429 - Too many requests')
            return False

    
def twitter_auth():
    '''
    Authenticate credentials for Twitter API by building
    an OAuthHandler from environment variables
    
    :returns: Wrapper for Twitter API
    :rtype: class:`tweepy.api.API`
    '''

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
    logger.info('Code100Bot authentication successful')
    stream = Stream(api.auth, likes_listener, tweet_mode='extended')
    logger.info('Searching tweets...')
    stream.filter(track=hashtag_list, languages=['en'])


if __name__ == "__main__":
    
    api = twitter_auth()
    
    try:
        like_tweets(api, hashtag_list)
    
    except Exception as e:
        logger.error(f'{e}')
        