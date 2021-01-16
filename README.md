# Code100Bot

I recently started a coding challenge to commit at least 1 hour a day to coding for 100 days. Progress is shared across social media platforms using the hashtag #100DaysOfCode. I always appreciate it when people engage with my daily tweets as it motivates me to keep working diligently towards my goal. I created a Twitter bot that would automatically like tweets that used the hashtag. To avoid hitting the rate limit of 1,000 likes per day, additional keywords were added to filter the stream further. As a fail-safe, the script will sleep for the remainder of the 24 hour period when 900 tweets are liked.

## Getting started:
To follow along with this project, you will need to obtain Twitter developer credentials at https://developer.twitter.com. A total of 4 keys are required to authenticate the app:
* consumer key
* consumer secret
* access token
* access token secret

## Customizing the hashtags
In the code100bot.py file:
* Pass a list of search terms and/or hashtage to the `hashtags_list`
* Pass a list of additional keywords to filter the stream to the `keywords`

## Supporting files
Three additional files must be created to deploy to Heroku.
* requirements.txt: dependencies needed to run the app  
* runtime.txt file: Python version
* Procfile: declares process types that describe how app will run

## Create a new Heroku app



