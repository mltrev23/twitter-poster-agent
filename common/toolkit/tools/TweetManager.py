import os
import io
import re
import tweepy
import base64
import logging
from PIL import Image
from typing import Union
from .utils.hyperbolic_api import make_hyperbolic_llama_inference, make_hyperbolic_sdxl_inference

class TwitterManager:
    def __init__(self):
        """Initialize the bot with OAuth 2.0 authentication."""
        self.API_KEY = os.getenv("TWITTER_API_KEY")
        self.API_SECRET_KEY = os.getenv("TWITTER_API_SECRET_KEY")
        self.ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
        self.ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        self.BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

        # Authenticate using OAuth 1.0
        self.tweepy_auth = tweepy.OAuth1UserHandler(
            f"{self.API_KEY}",
            f"{self.API_SECRET_KEY}",
            f"{self.ACCESS_TOKEN}",
            f"{self.ACCESS_TOKEN_SECRET}"
        )
        self.tweepy_api = tweepy.API(self.tweepy_auth)
        
        # Authenticate using OAuth 2.0
        self.client = tweepy.Client(
            bearer_token=self.BEARER_TOKEN,
            consumer_key=self.API_KEY,
            consumer_secret=self.API_SECRET_KEY,
            access_token=self.ACCESS_TOKEN,
            access_token_secret=self.ACCESS_TOKEN_SECRET
        )

    @staticmethod
    def generate_image(prompt, enhance = False):
        """Uses SDXL to generate an image based on the enhanced prompt."""
        
        # if enhance:
        #     prompt = TwitterManager.enhance_prompt(prompt)

        try:
            response_body = make_hyperbolic_sdxl_inference(prompt)

            # 🔹 Extract base64 image data
            if "images" in response_body and isinstance(response_body["images"], list):
                base64_image = response_body["images"][0]["image"]  # Extract the first image's base64 data
                
                # Decode the base64 string
                image_data = base64.b64decode(base64_image)
                logging.info(f"Successfully generated an image with prompt: {prompt}")

                return image_data  # Return image data

            logging.info(f"Failed to generate an image with prompt: {prompt}")
            return None

        except Exception as e:
            print(f"Error generating image: {e}")
            return None

    @staticmethod
    def write_tweet(topic: str, context: str):
        system_prompt = f"""
        Create a tweet that captures the excitement of given topic while keeping it engaging. Include relevant hashtags. Do not include any other text.
        """
        complete_prompt = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': f'Context: {context}'},
            {'role': 'user', 'content': f'The topic is "{topic}"'}
        ]

        try:        
            response_body = make_hyperbolic_llama_inference(complete_prompt)
            tweet = response_body['choices'][0]['message']['content'].strip()
            logging.info(f'Successfully generated tweet: {tweet}')
            return tweet
        except Exception as e:
            logging.error(f"Error generating tweet: {e}")
            return f"Couldn't generate a tweet on {topic}."

    def post_tweet(self, content: str, image_data: str):
        """Post a tweet with text and optional images using the agent's credentials."""
        try:
            media_ids = []
            
            # Upload images if provided
            if image_data:
                image = Image.open(io.BytesIO(image_data))
                
                buffer = io.BytesIO()
                image.save(buffer, format='JPEG')  # You can change the format as needed
                buffer.seek(0)  # Move to the beginning of the BytesIO buffer

                upload_response = self.tweepy_api.simple_upload(buffer)
                media_id = re.search(r"media_id=(\d+),", str(upload_response))
                if media_id:
                    media_ids.append(media_id.group(1))
                else:
                    logging.warning("No media_id found in the upload response.")
            
            # Post tweet with text and media
            response = self.client.create_tweet(text=content, media_ids=media_ids if media_ids else None)
            tweet_id = response.data['id']
            
            return {
                "success": True,
                "tweet_id": tweet_id,
                "message": "Tweet posted successfully!",
                "media_ids": media_ids
            }
        except Exception as e:
            error_msg = f"Error posting tweet: {str(e)}"
            logging.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }