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
        image = TwitterManager.generate_image(prompt)
    
    def write_tweet(prompt: str, context: str):
        text = TwitterManager.write_tweet(prompt, context)
    
    def search_google(topic: str):
        conetext = GoogleSearchManager.get_google_search_data(topic)

    def post_tweet(text: str, image: Image.Image):
        TwitterManager.post_tweet(text, image)