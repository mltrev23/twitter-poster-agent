from typing import Optional, Type
from pydantic import BaseModel, Field

class TweetGenerationInput(BaseModel):
    prompt: str = Field(description="topic for a tweet")
    context: str = Field(description="relevant context of prompt")


class GoogleSearchInput(BaseModel):
    prompt: str = Field(description="topic for google search")


class ArtGenerationInput(BaseModel):
    prompt: str = Field(description="topic for an image")


class PostTweetInput(BaseModel):
    tweet: str = Field(description="text of tweet")
    image: Optional[bytes] = Field(default=None, description="image of tweet, can be None")
