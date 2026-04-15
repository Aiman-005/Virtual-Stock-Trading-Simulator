import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from openai import AsyncClient


class ChatBot:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        set_tracing_disabled(True)

        # Read Gemini API credentials
        api_key = os.getenv("GEMINI_API_KEY")
        base_path = os.getenv("GEMINI_BASE_PATH")
        model_name = os.getenv("GEMINI_MODEL_NAME")

        if not all([api_key, base_path, model_name]):
            raise ValueError("Please set GEMINI_API_KEY, GEMINI_BASE_PATH, and GEMINI_MODEL_NAME in your .env file.")

        # Initialize OpenAI Gemini async client
        client = AsyncClient(api_key=api_key, base_url=base_path)
        model = OpenAIChatCompletionsModel(model=model_name, openai_client=client)

        # Define the agent
        self.agent = Agent(
            name="Stock Recommender",
            instructions=(
                "You are a stock recommender of Pakistan. "
                "Help users understand stock market investing, "
                "its pros, cons, and related terms." \
                "Answer to the user in just 2 lines"
            ),
            model=model,
        )

    async def start(self):
        print("💬 Chatbot started! Type 'exit' to quit.\n")
        while True:
            # Get user input asynchronously
            user_input = await asyncio.to_thread(input, "You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("👋 Goodbye!")
                break
            try:
                result = await Runner.run(self.agent, user_input)
                print("🤖 Bot:", result.final_output)
            except Exception as e:
                print("⚠️ Error:", e)
