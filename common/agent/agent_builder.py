from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
import openai
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

from toolkit.langchain_tools.langchain_tools import TweetGenerationTool, ArtGenerationTool, GoogleSearchTool, PostTweetTool

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class AgentBuilder:

    tools = []

    def __init__(self):
        """
        Initializes the agent instance.
        """
        pass

    def create_text_gen_prompt(self):
        return """
                You are an intelligent React agent designed to assist users by answering their queries related to business documents from audio-transcribed meeting notes. When a user inputs a query, your task is to:

                Understand the intent and context of the user's query.
                Use information retrieval tool integrated to retrieve the top most relevant information snippets from the document vector store that align with the user's query.
                Formulate a comprehensive and concise response based on the retrieved information, ensuring that your answer is coherent and directly addresses the query using the most pertinent details available.
                If the user asks a question that is unrelated or beyond the scope of the documents, respond using your own general knowledge, without accessing the retriever tool. Ensure that your response is still relevant and valuable to the user and let them know that the information is not contained in the business doc.
                Be accurate, engaging, and maintain a professional yet friendly tone. Always strive to provide clarity and actionable insights.

                """

    def create_tweet_gen_prompt(self, topic: str):
        return f"""
            1. Search Google for context about "{topic}".
            2. Generate a tweet based on the context.
            3. Generate an image related to "{topic}".
            4. Post the tweet and image to Twitter.
            """

    def create_retriever_agent(self,retriever, model_provider= 'open-ai',model_name = 'gpt-3.5-turbo'):
        model = self.create_chat_model(provider = model_provider, name = model_name)
        retriever_tool = self.create_retriever_tool(retriever)
        self.tools.append(retriever_tool)
        prompt = self.create_text_gen_prompt()
        return Agent(model, self.tools, system=prompt)

    def create__agent(self,retriever, model_provider= 'open-ai',model_name = 'gpt-3.5-turbo'):
        model = self.create_chat_model(provider = model_provider, name = model_name)
        retriever_tool = self.create_retriever_tool(retriever)
        self.tools.append(retriever_tool)
        prompt = self.create_text_gen_prompt()
        return Agent(model, self.tools, system=prompt)
    
    def create_twitter_agent(self, model_provider='open-ai', model_name='gpt-3.5-turbo'):
        # Define model
        model = self.create_chat_model(provider=model_provider, name=model_name)

        # Built a prompt
        prompt = self.create_tweet_gen_prompt()
        
        # Load tools
        google_retriever = self.create_google_retriever_tool()
        art_generator = self.create_art_generation_tool()
        tweet_generator = self.create_tweet_generation_tool()
        tweet_poseter = self.create_tweet_post_tool()

        self.tools.append(google_retriever, tweet_generator, art_generator, tweet_poseter)
        
        return Agent(model, self.tools, system=prompt)

    def create_art_generation_tool(self, model_provider='open-ai-image'):
        return ArtGenerationTool()

    def create_google_retriever_tool(self):
        return GoogleSearchTool()

    def create_tweet_generation_tool(self):
        return TweetGenerationTool()

    def create_tweet_post_tool(self):
        return PostTweetTool()

    def create_blink_agent():
        print("Not implemented")

    def create_deepseek_agent():
        print("Not implemented")

    def create_chat_model(self, provider, name):
        match provider:
            case 'open-ai':
                return ChatOpenAI(model=name)

    def create_retriever_tool(self,retriever):
        return RetrieverTool(retriever = retriever)


class Agent:

    def __init__(self, model, tools, system=""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def call_openai(self, state: AgentState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}

    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            if not t['name'] in self.tools:      # check for bad tool name from LLM
                print("\n ....bad tool name....")
                result = "bad tool name, retry"  # instruct LLM to retry if bad
            else:
                result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        print("Back to the model!")
        return {'messages': results}