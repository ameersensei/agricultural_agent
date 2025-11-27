import asyncio
import os
from google.adk.agents import Agent, SequentialAgent, ParallelAgent
from google.adk.tools import google_search, AgentTool
from google.adk.sessions import InMemorySessionService
from google.adk.runners import InMemoryRunner
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env file  
# Using raw string (r prefix) to handle backslashes correctly
load_dotenv(dotenv_path = r'P:\agricultural_agent\agricultural_agent\agricultural_agent\.env')

# Get API key
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file!")

retry_config = types.HttpRetryOptions(
    attempts = 5,
    exp_base = 7,
    initial_delay = 1,
    http_status_codes = [429, 500, 503, 504],
)

treatment_agent = Agent(
    model = 'gemini-2.5-flash-lite',
    name = 'TreatmentAgent',
    description = 'TreatmentAgent is a research agent that finds research papers on how to treat the disease mentioned by user for crops.',
    instruction = '''
    you are a treatment agent, you find treatment to the mentioned crop disease and provide a list of treatment with their titles, authors, and links to the papers.
    first search for treatment using tools and make a list of it and then provide the list of treatments.
    1.use only top 5 research papers to find treatment.
    2.respond only for crops diseases.
    3.instead of crop if user asks for other topic respond with "I don't know".
    4.use the given tools to find the treatment.
    ''',
    tools = [google_search],
    output_key = 'treatment',
)





runner = InMemoryRunner(
    agent = treatment_agent,
)

response = asyncio.run(runner.run_debug(input('Enter your topic: ')))


