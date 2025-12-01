from google.adk.agents import Agent, SequentialAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search, ToolContext
import dotenv
import asyncio
import os


dotenv.load_dotenv(r'P:\agricultural_agent\agricultural_agent\agricultural_agent\.env')

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file!")


crop_disease_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='CropDiseaseAgent',
    description='A helpful assistant for user questions.',
    instruction='''describe the crop disease based on the image url given by the user. use the given tools to find the image and provide with disease and crop name 
    no assumptions are allowed and only provide name of disease and crop name these two are compulsory no other information.
    ''',
    tools = [google_search],
    output_key = 'crop_disease',
)

treatment_agent = Agent(
    model = 'gemini-2.5-flash-lite',
    name = 'TreatmentAgent',
    description = 'TreatmentAgent is a research agent that finds research papers on how to treat the disease mentioned by crop_disease_agent agent for crops.',
    instruction = '''
    you are a treatment agent, you find treatment to the mentioned crop disease provided by crop_disease_agent as {crop_disease} and provide a list of treatment with their titles, authors, and links to the papers.
    first search for treatment using tools and make a list of it and then provide the list of treatments.
    1.use only top 5 research papers to find treatment.
    2.respond only for crops diseases.
    3.instead of crop if user asks for other topic respond with "I don't know".
    4.use the given tools to find the treatment.
    ''',
    tools = [google_search],
    output_key = 'treatment',
)

root_agent = SequentialAgent(
    name = 'RootAgent',
    sub_agents = [crop_disease_agent, treatment_agent],
)


runner = InMemoryRunner(root_agent)



# response = asyncio.run(runner.run_debug(r'https://cdn.britannica.com/83/115383-050-166AB7C8/Plant-crown-gall.jpg?w=300'))

if __name__ == '__main__':
    # Example: Run the root agent
    response = asyncio.run(runner.run_debug(r'https://cdn.britannica.com/83/115383-050-166AB7C8/Plant-crown-gall.jpg?w=300'))
    
    # Example: Run the treatment agent
    # treatment_runner = InMemoryRunner(treatment_agent)
    # treatment_response = asyncio.run(treatment_runner.run_debug("How to treat wheat rust?"))
