"""Module for agent kit"""
from typing import Optional
from agentipy import SolanaAgentKit
from PIL import Image
from common.toolkit.tools.tweet_manager import TwitterManager
from common.toolkit.tools.google_search import GoogleSearchManager


class BotifyAgentKit(SolanaAgentKit):

    def __init__(
        self,
        private_key: Optional[str] = None,
        rpc_url: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        helius_api_key: Optional[str] = None,
        helius_rpc_url: Optional[str] = None,
        backpack_api_key: Optional[str] = None,
        backpack_api_secret: Optional[str] = None,
        quicknode_rpc_url: Optional[str] = None,
        jito_block_engine_url: Optional[str] = None,
        jito_uuid: Optional[str] = None,
        stork_api_key: Optional[str] = None,
        generate_wallet: bool = False,
    ):
        # Call the parent class's __init__ method
        super().__init__(
            private_key,
            rpc_url,
            openai_api_key,
            helius_api_key,
            helius_rpc_url,
            backpack_api_key,
            backpack_api_secret,
            quicknode_rpc_url,
            jito_block_engine_url,
            jito_uuid,
            stork_api_key,
            generate_wallet,
        )

    def generate_twitter_image(self, prompt: str):
        image = TwitterManager.generate_image(prompt)
        # Return or use the image as needed
        return image

    def write_tweet(self, prompt: str, context: str):
        text = TwitterManager.write_tweet(prompt, context)
        # Return or use the tweet text as needed
        return text

    def search_google(self, topic: str):
        context = GoogleSearchManager.get_google_search_data(topic)
        # Return or use the search context as needed
        return context

    def post_tweet(self, text: str, image: Image.Image):
        TwitterManager.post_tweet(text, image)
