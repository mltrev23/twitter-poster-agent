from agentipy import SolanaAgentKit
from typing import Optional

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
        generate_wallet: bool = False
        )