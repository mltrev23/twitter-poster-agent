from typing import TypedDict, Annotated, List, Any
import operator
import openai

from langgraph.graph import StateGraph, END
from langchain_core.messages import AnyMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

from common.toolkit.langchain_tools.langchain_tools import (
    TweetGenerationTool,
    ArtGenerationTool,
    GoogleSearchTool,
    PostTweetTool,
)

from .agent_resources.twitter_agent.twitter_agent import TwitterAgent


class AgentState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]


class AgentBuilder:
    def __init__(self):
        """
        Initializes the agent instance.
        """
        self.tools = []

    @staticmethod
    def create_text_gen_prompt() -> str:
        return (
            "You are an intelligent React agent designed to assist users by answering "
            "their queries related to business documents from audio-transcribed meeting notes. "
            "When a user inputs a query, your task is to:\n\n"
            "1. Understand the intent and context of the user's query.\n"
            "2. Use the integrated information retrieval tool to retrieve the most "
            "relevant information snippets from the document vector store that align with "
            "the user's query.\n"
            "3. Formulate a comprehensive and concise response based on the retrieved "
            "information, ensuring that your answer is coherent and directly addresses "
            "the query using the most pertinent details available.\n"
            "4. If the user asks a question that is unrelated or beyond the scope of the "
            "documents, respond using your own general knowledge without accessing the "
            "retriever tool. Ensure that your response is still relevant and valuable to the "
            "user and inform them that the information is not contained in the business "
            "document.\n\n"
            "Be accurate, engaging, and maintain a professional yet friendly tone. Always "
            "strive to provide clarity and actionable insights."
        )

    @staticmethod
    def create_tweet_gen_prompt(topic: str) -> str:
        return (
            f"1. Search Google for context about \"{topic}\".\n"
            f"2. Generate a tweet based on the context.\n"
            f"3. Generate an image related to \"{topic}\".\n"
            f"4. Post the tweet and image to Twitter."
        )

    def create_retriever_agent(
        self, retriever: Any, model_provider: str = "open-ai", model_name: str = "gpt-3.5-turbo"
    ) -> 'Agent':
        model = self.create_chat_model(provider=model_provider, name=model_name)
        retriever_tool = self.create_retriever_tool(retriever)
        self.tools.append(retriever_tool)
        prompt = self.create_text_gen_prompt()
        return Agent(model, self.tools, system=prompt)

    def create_twitter_agent(
        self, topic: str, model_provider: str = "open-ai", model_name: str = "gpt-3.5-turbo"
    ) -> 'Agent':
        # Define model
        model = self.create_chat_model(provider=model_provider, name=model_name)

        # Build a prompt
        prompt = self.create_tweet_gen_prompt(topic)

        # Load tools
        google_retriever = self.create_google_retriever_tool()
        art_generator = self.create_art_generation_tool()
        tweet_generator = self.create_tweet_generation_tool()
        tweet_poster = self.create_tweet_post_tool()

        self.tools.extend([google_retriever, tweet_generator, art_generator, tweet_poster])

        return Agent(model, self.tools, system=prompt)

    @staticmethod
    def create_art_generation_tool() -> ArtGenerationTool:
        return ArtGenerationTool()

    @staticmethod
    def create_google_retriever_tool() -> GoogleSearchTool:
        return GoogleSearchTool()

    @staticmethod
    def create_tweet_generation_tool() -> TweetGenerationTool:
        return TweetGenerationTool()

    @staticmethod
    def create_tweet_post_tool() -> PostTweetTool:
        return PostTweetTool()

    @staticmethod
    def create_blink_agent() -> None:
        print("Not implemented")

    @staticmethod
    def create_deepseek_agent() -> None:
        print("Not implemented")

    @staticmethod
    def create_chat_model(provider: str, name: str) -> ChatOpenAI:
        if provider == "open-ai":
            return ChatOpenAI(model=name)
        raise ValueError(f"Unsupported model provider: {provider}")

    @staticmethod
    def create_retriever_tool(retriever: Any) -> 'RetrieverTool':
        return RetrieverTool(retriever=retriever)


class Agent:
    def __init__(self, model: ChatOpenAI, tools: List[Any], system: str = ""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm", self.exists_action, {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def exists_action(self, state: AgentState) -> bool:
        result = state["messages"][-1]
        return len(result.tool_calls) > 0

    def call_openai(self, state: AgentState) -> dict:
        messages = state["messages"]
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {"messages": [message]}

    def take_action(self, state: AgentState) -> dict:
        tool_calls = state["messages"][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            if t["name"] not in self.tools:  # check for bad tool name from LLM
                print("\n ....bad tool name....")
                result = "bad tool name, retry"  # instruct LLM to retry if bad
            else:
                result = self.tools[t["name"]].invoke(t["args"])
            results.append(
                ToolMessage(tool_call_id=t["id"], name=t["name"], content=str(result))
            )
        print("Back to the model!")
        return {"messages": results}
