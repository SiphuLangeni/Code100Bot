# Code100Bot

I recently started a coding challenge to commit at least 1 hour a day to coding for 100 days. Progress is shared across social media platforms using the hashtag #100DaysOfCode. I always appreciate it when people engage with my daily tweets as it motivates me to keep working diligently towards my goal. I created a Twitter bot that would automatically like tweets that used the hashtag. Eventually, I expanded the hashtag list to include #66DaysOfData and #BWIAI as I also follow these conversations.

## Getting started:
To follow along with this project, you will need to obtain Twitter developer credentials at https://developer.twitter.com. A total of 4 keys are required to authenticate the app:
* consumer key
* consumer secret
* access token
* access token secret

## Customizing the hashtags
Pass your selection of keywords and/or hashtage to the `keyword_list` in the code100bot.py file.

## Supporting files
Three additional files must be created to deploy to Heroku.
* requirements.txt: text file that lists Tweepy and all its dependencies with the .  
* runtime.txt file: instructs Heroku the Python version used
* Procfile: tells the bot what to do with the code

## Create a new Heroku app



