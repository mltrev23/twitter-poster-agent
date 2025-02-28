"""An agent posting tweet"""

import os
import operator
from typing import TypedDict, Any, Annotated  # Standard library import
from langgraph.graph import StateGraph, END, START  # Third-party import

from common.agent.agent_utils.load_yaml_config import load_yaml_config


class TwitterAgentState(TypedDict):
    """Represents the state of the Twitter agent."""

    prompt: Annotated[list[str], operator.add]
    context: str
    image: bytes
    tweet: str
    result: str


class TwitterAgent:
    """A class to manage the workflow of generating and posting tweets."""

    current_file_path = os.path.dirname(__file__)
    config_path = os.path.join(current_file_path, "twitter_agent.yaml")
    config = load_yaml_config(config_path)

    def __init__(self, model, tools, system_prompt=""):
        """Initializes the TwitterAgent with model, tools, and system prompt.

        Args:
            model: The model used for generating content.
            tools: A list of tools available for the agent.
            system_prompt: An optional prompt for the system.
        """
        self.tools = {t.name: t for t in tools}
        print(self.tools)
        self.model = model.bind_tools(tools)
        self.system_prompt = system_prompt

        self.graph = self.build_workflow()

    def build_workflow(self):
        """Builds the workflow for the Twitter agent.

        Returns:
            The compiled state graph for the agent's workflow.
        """
        graph = StateGraph(TwitterAgentState)

        graph.add_node("search_google", self.search_google)
        graph.add_node("write_tweet", self.write_tweet)
        graph.add_node("enhance_prompt", self.enhance_prompt)
        graph.add_node("art_generate", self.art_generate)
        graph.add_node("post_tweet", self.post_tweet)
        graph.add_node("blank_node", lambda x: {})

        graph.add_edge(START, "search_google")
        graph.add_edge("search_google", "write_tweet")
        # graph.add_edge(START, "enhance_prompt")
        # graph.add_edge("write_tweet", "enhance_prompt")
        graph.add_edge("write_tweet", "art_generate")
        graph.add_edge("write_tweet", "blank_node")
        graph.add_edge("blank_node", "post_tweet")
        graph.add_edge("art_generate", "post_tweet")
        graph.add_edge("post_tweet", END)

        self.graph = graph.compile()
        return self.graph

    def search_google(self, state: TwitterAgentState):
        """Retrieves context from Google based on the prompt.

        Args:
            state: The current state of the Twitter agent.

        Returns:
            Updated state with retrieved context.
        """
        prompt = state["prompt"][-1]
        context = self.tools["search_google"].invoke({"prompt": prompt})
        return {"context": context}

    def write_tweet(self, state: TwitterAgentState):
        """Writes a tweet based on the prompt and context.

        Args:
            state: The current state of the Twitter agent.

        Returns:
            Updated state with the generated tweet.
        """
        prompt, context = state["prompt"][0], state["context"]
        tweet = self.tools["tweet_writer"].invoke({"prompt": prompt, "context": context})
        return {"tweet": tweet}

    def enhance_prompt(self, state: TwitterAgentState):
        """Enhances the prompt prompt for better image generation using the model.

        Args:
            state: The current state of the Twitter agent.

        Returns:
            Updated state with the enhanced prompt.
        """
        prompt = state["tweet"]
        enhance_prompt = self.config["agent"]["prompt_enhancer"].format(prompt=prompt)
        new_prompt = self.model.invoke(enhance_prompt).content
        return {"prompt": [new_prompt]}

    def art_generate(self, state: TwitterAgentState):
        """Generates art based on the prompt.

        Args:
            state: The current state of the Twitter agent.

        Returns:
            Updated state with the generated image.
        """
        prompt = state["tweet"]
        image = self.tools["art_generator"].invoke({"prompt": prompt})
        return {"image": image}

    def post_tweet(self, state: TwitterAgentState):
        """Posts the tweet along with an image.

        Args:
            state: The current state of the Twitter agent.

        Returns:
            The original state after posting the tweet.
        """
        tweet, image = state["tweet"], state["image"]
        result = self.tools["tweet_poster"].invoke({"tweet": tweet, "image": image})
        return {"result": str(result)}
