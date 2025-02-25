"""An agent posting tweet"""

from typing import TypedDict, Any  # Standard library import
import yaml
from langgraph.graph import StateGraph, END, START  # Third-party import


def load_yaml_config(file_path: str) -> Any:
    """Loads a YAML configuration file.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        Any: The content of the YAML file as a Python object.
    """
    with open(file_path, "r", encoding="utf-8") as file:  # Specified encoding
        config = yaml.safe_load(file)
    return config


class TwitterAgentState(TypedDict):
    """Represents the state of the Twitter agent."""

    topic: str
    context: str
    image: str
    tweet: str


class TwitterAgent:
    """A class to manage the workflow of generating and posting tweets."""

    config = load_yaml_config("twitter_agent.yaml")

    def __init__(self, model, tools, system_prompt=""):
        """Initializes the TwitterAgent with model, tools, and system prompt.

        Args:
            model: The model used for generating content.
            tools: A list of tools available for the agent.
            system_prompt: An optional prompt for the system.
        """
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)
        self.system_prompt = system_prompt

        self.graph = self.build_workflow()

    def build_workflow(self):
        """Builds the workflow for the Twitter agent.

        Returns:
            The compiled state graph for the agent's workflow.
        """
        graph = StateGraph(TwitterAgentState)

        graph.add_node("retrieve_google", self.retrieve_google)
        graph.add_node("write_tweet", self.write_tweet)
        graph.add_node("enhance_prompt", self.enhance_prompt)
        graph.add_node("art_generate", self.art_generate)
        graph.add_node("post_tweet", self.post_tweet)

        graph.add_edge(START, "retrieve_google")
        graph.add_edge("retrieve_google", "write_tweet")
        graph.add_edge(START, "enhance_prompt")
        graph.add_edge("enhance_prompt", "art_generate")
        graph.add_edge("write_tweet", "post_tweet")
        graph.add_edge("art_generate", "post_tweet")
        graph.add_edge("post_tweet", END)

        self.graph = graph.compile()
        return self.graph

    def retrieve_google(self, state: TwitterAgentState):
        """Retrieves context from Google based on the topic.

        Args:
            state: The current state of the Twitter agent.

        Returns:
            Updated state with retrieved context.
        """
        topic = state["topic"]
        context = self.tools["retrieve_google"].invoke(topic)
        return {"topic": topic, "context": context}

    def write_tweet(self, state: TwitterAgentState):
        """Writes a tweet based on the topic and context.

        Args:
            state: The current state of the Twitter agent.

        Returns:
            Updated state with the generated tweet.
        """
        topic, context = state["topic"], state["context"]
        tweet = self.tools["tweet_writer"].invoke(topic, context)
        return {"topic": topic, "context": context, "tweet": tweet}

    def enhance_prompt(self, state: TwitterAgentState):
        """Enhances the topic prompt for better image generation using the model.

        Args:
            state: The current state of the Twitter agent.

        Returns:
            Updated state with the enhanced topic.
        """
        topic = state["topic"]
        enhance_prompt = self.config["agent"]["prompt_enhancer"].format(topic=topic)
        new_topic = self.model.invoke(enhance_prompt)
        return {"topic": new_topic}

    def art_generate(self, state: TwitterAgentState):
        """Generates art based on the topic.

        Args:
            state: The current state of the Twitter agent.

        Returns:
            Updated state with the generated image.
        """
        topic = state["topic"]
        image = self.tools["art_generate"].invoke(topic)
        return {"topic": topic, "image": image}

    def post_tweet(self, state: TwitterAgentState):
        """Posts the tweet along with an image.

        Args:
            state: The current state of the Twitter agent.

        Returns:
            The original state after posting the tweet.
        """
        tweet, image = state["tweet"], state["image"]
        self.tools["tweet_poster"].invoke(tweet, image)
        return state
