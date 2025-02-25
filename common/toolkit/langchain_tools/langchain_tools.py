""" Module for custom langchain tools """
from typing import Optional, Type

# Third-party imports
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from PIL import Image
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

# Local application imports
from common.toolkit.agent_kit.agent_kit import BotifyAgentKit


class TweetGenerationInput(BaseModel):
    prompt: str = Field(description="topic for a tweet")
    context: str = Field(description="relevant context of prompt")


class GoogleSearchInput(BaseModel):
    topic: str = Field(description="topic for google search")


class ArtGenerationInput(BaseModel):
    prompt: str = Field(description="topic for an image")


class PostTweetInput(BaseModel):
    text: str = Field(description="text of tweet")
    image: Image.Image = Field(description="image of tweet")


class TweetGenerationTool(BaseTool):
    name = "tweet_writer"
    description = "useful tool to create tweet"
    args_schema: Type[BaseModel] = TweetGenerationInput

    def _run(self, *args, **kwargs):
        """
        Twitter generation tool call function 

        Required Arguments:
            - prompt: str    # prompt or topic for tweet generation
            - context: str   # relevant context of topic
        """

        prompt = kwargs.get('prompt')
        context = kwargs.get('context')

        if prompt is None:
            return 'This is my test tweet!'
        
        botify_agent_kit = BotifyAgentKit()
        return botify_agent_kit.write_tweet(prompt, context)

    async def _arun(self, *args, **kwargs) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("TweetGenerationTool does not support async")


class GoogleSearchTool(BaseTool):
    name = "search_google"
    description = "useful tool to search google with topic and get context"
    args_schema: Type[BaseModel] = GoogleSearchInput

    def _run(self, *args, **kwargs) -> str:
        """Use the tool."""
        topic = kwargs.get('topic')

        botify_agent_kit = BotifyAgentKit()
        return botify_agent_kit.search_google(topic)

    async def _arun(self, *args, **kwargs) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("GoogleSearchTool does not support async")


class ArtGenerationTool(BaseTool):
    name = "art_generator"
    description = "useful tool to create an image"
    args_schema: Type[BaseModel] = ArtGenerationInput

    def _run(self, *args, **kwargs) -> str:
        """Use the tool."""
        prompt = kwargs.get('prompt')

        botify_agent_kit = BotifyAgentKit()
        return botify_agent_kit.generate_twitter_image(prompt)

    async def _arun(self, *args, **kwargs) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("ArtGenerationTool does not support async")


class PostTweetTool(BaseTool):
    name = "tweet_poster"
    description = "useful tool to post a tweet with an image"
    args_schema: Type[BaseModel] = PostTweetInput

    def _run(self, *args, **kwargs) -> str:
        """Use the tool."""
        text = kwargs.get('text')
        image = kwargs.get('image')

        botify_agent_kit = BotifyAgentKit()
        return botify_agent_kit.post_tweet(text, image)

    async def _arun(self, *args, **kwargs) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("PostTweetTool does not support async")
