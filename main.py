import tweepy
import openai

# Authenticate to Twitter API
auth = tweepy.OAuthHandler("consumer_key", "consumer_secret")
auth.set_access_token("access_token", "access_token_secret")

# Connect to Twitter API
api = tweepy.API(auth)

# Authenticate to OpenAI GPT API
openai.api_key = "YOUR_API_KEY"

# Listen for new mentions
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, tweet):
        # Ignore retweets and replies to other users
        if (not tweet.retweeted) and ('RT @' not in tweet.text) and (tweet.in_reply_to_screen_name is None):
            # Extract tweet metadata
            user = tweet.user.screen_name
            tweet_id = tweet.id_str
            text = tweet.text

            # Generate response using GPT API
            response = openai.Completion.create(
                engine="davinci",
                prompt=text,
                max_tokens=50,
                n=1,
                stop=None,
                temperature=0.5,
            )
            response_text = response.choices[0].text

            # Send reply
            reply_text = f"@{user} {response_text}"
            api.update_status(
                status=reply_text,
                in_reply_to_status_id=tweet_id,
            )

stream_listener = MyStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=[f"@{bot_twitter_handle}"])
