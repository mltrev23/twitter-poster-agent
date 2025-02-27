"""Module for custom langchain tools"""

from typing import Optional, Type

# Third-party imports
from pydantic import BaseModel, Field
from PIL import Image
from langchain.tools import BaseTool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

# Local application imports
from common.toolkit.agent_kit.agent_kit import BotifyAgentKit
from common.toolkit.langchain_tools.langchain_schema_config import (
    TweetGenerationInput,
    GoogleSearchInput,
    ArtGenerationInput,
    PostTweetInput,
)


class TweetGenerationTool(BaseTool):
    name: str = "tweet_writer"
    description: str = "useful tool to create tweet"
    args_schema: Type[BaseModel] = TweetGenerationInput

    def _run(self, *args, **kwargs):
        """
        Twitter generation tool call function

        Required Arguments:
            - prompt: str    # prompt or topic for tweet generation
            - context: str   # relevant context of topic
        """

        prompt = kwargs.get("prompt")
        context = kwargs.get("context")

        if prompt is None:
            return "This is my test tweet!"

        botify_agent_kit = BotifyAgentKit()
        return botify_agent_kit.write_tweet(prompt, context)

    async def _arun(self, *args, **kwargs) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("TweetGenerationTool does not support async")


class GoogleSearchTool(BaseTool):
    name: str = "search_google"
    description: str = "useful tool to search google with topic and get context"
    args_schema: Type[BaseModel] = GoogleSearchInput

    def _run(self, *args, **kwargs) -> str:
        """
        Google search tool call function

        Required Arguments:
            - prompt: str    # prompt to search google
        """
        prompt = kwargs.get("prompt")

        botify_agent_kit = BotifyAgentKit()
        return botify_agent_kit.search_google(prompt)

    async def _arun(self, *args, **kwargs) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("GoogleSearchTool does not support async")


class ArtGenerationTool(BaseTool):
    name: str = "art_generator"
    description: str = "useful tool to create an image"
    args_schema: Type[BaseModel] = ArtGenerationInput

    def _run(self, *args, **kwargs) -> str:
        """
        Image generation tool call function

        Required Arguments:
            - prompt: str    # prompt or topic for image generation
        """
        prompt = kwargs.get("prompt")

        botify_agent_kit = BotifyAgentKit()
        return botify_agent_kit.generate_twitter_image(prompt)

    async def _arun(self, *args, **kwargs) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("ArtGenerationTool does not support async")


class PostTweetTool(BaseTool):
    name: str = "tweet_poster"
    description: str = "useful tool to post a tweet with an image"
    args_schema: Type[BaseModel] = PostTweetInput

    def _run(self, *args, **kwargs) -> str:
        """
        Post tweet on twitter

        Required Arguments:
            - tweet: str    # tweet data of tweet
            - image: str   # image on tweet
        """
        tweet = kwargs.get("tweet")
        image = kwargs.get("image")

        botify_agent_kit = BotifyAgentKit()
        return botify_agent_kit.post_tweet(tweet, image)

    async def _arun(self, *args, **kwargs) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("PostTweetTool does not support async")
