import logging
from fastapi import FastAPI
from pydantic import BaseModel

from common.agent.agent_builder import AgentBuilder


class TweetPrompt(BaseModel):
    prompt: str


app = FastAPI()


@app.post("/post-tweet")
def post_tweet(prompt: TweetPrompt):
    agent_builder = AgentBuilder()
    twitter_agent = agent_builder.create_twitter_agent()

    data = {"prompt": [prompt.prompt]}

    result = twitter_agent.graph.invoke(data)
    logging.info("result: %s", result)

    return True


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=60001)
