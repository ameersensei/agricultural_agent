import asyncio
import os
from google.adk.agents import Agent, SequentialAgent, ParallelAgent
from google.adk.tools import google_search
from google.adk.sessions import InMemorySessionService
from google.adk.runners import InMemoryRunner
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env file  
# Using raw string (r prefix) to handle backslashes correctly
load_dotenv(dotenv_path = r'p:\agricultural_agent\agricultural_agent\.env')

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

research_agent = Agent(
    model = 'gemini-2.5-flash-lite',
    name = 'ResearchAgent',
    description = 'ResearchAgent is a research assistant that finds research papers based on the given topic and provides a list of research papers with their titles, authors, and links to the papers.',
    instruction = '''
    you are a research assistant, ypur task is to find research papers based on the given topic and provide
    a list of research papers with their titles, authors, and links to the papers.
    1.find research paper based on topic given and only provide top 5 research papers.
    2.never to ask further questions after providing the list of research papers.
    3.always provide the list of research papers in the following format:
       1. title of research paper
       2. authors of research paper
       3. link to research paper
    4.use the given tools to find the research papers.
    ''',
    tools = [google_search],
    output_key = 'research_paper',
)

runner = InMemoryRunner(
    agent = research_agent,
)

response = asyncio.run(runner.run_debug(input('Enter your topic: ')))

