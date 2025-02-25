from agentipy import SolanaAgentKit
from typing import Optional
from ..tools.TweetManager import TwitterManager
from ..tools.GoogleSearch import GoogleSearchManager
from PIL import Image

class BotifyAgentKit(SolanaAgentKit):

    def __init__(self,
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
        generate_wallet: bool = False):
        
        
        super().init(
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
            generate_wallet
        )
    
    def generate_twitter_image(prompt: str):
        return TwitterManager.generate_image(prompt)
    
    def write_tweet(prompt: str, context: str):
        return TwitterManager.write_tweet(prompt, context)
    
    def search_google(self, topic: str):
        google_search_manager = GoogleSearchManager()
        context = google_search_manager.get_google_search_data(topic)
        # Return or use the search context as needed
        return context

    def post_tweet(self, text: str, image: bytes):
        tweet_manager = TwitterManager()
        tweet_manager.post_tweet(text, image)
