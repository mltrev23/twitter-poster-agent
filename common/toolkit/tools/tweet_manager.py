"""Module for tweet manager tool implementation"""

import os
import io
import re
import logging
import base64
from typing import Union
import requests
import tweepy
from PIL import Image
from common.toolkit.tools.utils.hyperbolic_api import (
    make_hyperbolic_llama_inference,
    make_hyperbolic_sdxl_inference,
)


class TwitterManager:
    def __init__(self):
        """Initialize the bot with OAuth 2.0 authentication."""
        self.api_key = os.getenv("TWITTER_API_KEY")
        self.api_secret_key = os.getenv("TWITTER_API_SECRET_KEY")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

        # Authenticate using OAuth 1.0
        self.tweepy_auth = tweepy.OAuth1UserHandler(
            self.api_key,
            self.api_secret_key,
            self.access_token,
            self.access_token_secret,
        )
        self.tweepy_api = tweepy.API(self.tweepy_auth)

        # Authenticate using OAuth 2.0
        self.client = tweepy.Client(
            bearer_token=self.bearer_token,
            consumer_key=self.api_key,
            consumer_secret=self.api_secret_key,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
        )

    @staticmethod
    def generate_image(prompt: str) -> Union[None, bytes]:
        """Generates an image based on the given prompt using SDXL."""
        try:
            response_body = make_hyperbolic_sdxl_inference(prompt)

            if "images" in response_body and isinstance(response_body["images"], list):
                base64_image = response_body["images"][0]["image"]
                image_data = base64.b64decode(base64_image)
                logging.info("Successfully generated an image with prompt: %s", prompt)
                return image_data

            logging.info("Failed to generate an image with prompt: %s", prompt)
            return None
        except requests.exceptions.RequestException as e:
            logging.error("Network error generating image: %s", e)
            return None
        except OSError as e:
            logging.error("Error handling image data: %s", e)
            return None

    @staticmethod
    def write_tweet(topic: str, context: str) -> str:
        system_prompt = (
            "Create a tweet that captures the excitement of the topic while keeping it engaging."
            "Include relevant hashtags. Do not add any other description than tweet content."
        )
        complete_prompt = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context: {context}"},
            {"role": "user", "content": f'The topic is "{topic}"'},
        ]

        try:
            response_body = make_hyperbolic_llama_inference(complete_prompt)
            tweet = response_body["choices"][0]["message"]["content"].strip()
            return tweet
        except requests.exceptions.RequestException as e:
            logging.error("Network error generating tweet: %s", e)
            return f"Couldn't generate a tweet on {topic}."
        except TypeError as e:
            logging.error("TypeError error generating tweet: %s", e)
            return f"Couldn't generate a tweet on {topic}."

    def post_tweet(self, content: str, image_data: Union[bytes, None] = None) -> dict:
        """Post a tweet with text and optional images."""
        try:
            media_ids = []

            if image_data:
                img_buffer = io.BytesIO(image_data)
                img_buffer.name = "image.png"  # Fake filename for Tweepy.

                media = self.tweepy_api.media_upload(filename=img_buffer.name, file=img_buffer)
                media_ids.append(media.media_id_string)

            response = self.client.create_tweet(
                text=content, media_ids=media_ids if media_ids else None
            )
            tweet_id = response.data["id"]

            return {
                "success": True,
                "tweet_id": tweet_id,
                "message": "Tweet posted successfully!",
                "media_ids": media_ids,
            }

        except tweepy.TweepyException as e:  # Catch specific Tweepy errors
            logging.error("Tweepy error posting tweet: %s", e)
            return {"success": False, "error": str(e)}
        except requests.exceptions.RequestException as e:
            logging.error("Network error posting tweet: %s", e)
            return {"success": False, "error": str(e)}
