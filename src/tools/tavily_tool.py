import os
from langchain_community.tools import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from config.environment import get_env_variable

# Get the Tavily API key
tavily_api_key = get_env_variable('TAVILY_API_KEY')
if tavily_api_key is None:
    raise ValueError("TAVILY_API_KEY is not set in environment variables or secrets")

# Set the Tavily API key in the environment
os.environ['TAVILY_API_KEY'] = tavily_api_key

# Description for the Tavily tool
tool_description = '''
Searches internet for information using the tavily api. Best for generic information gathering.
'''

# Initialize the Tavily search tool
search = TavilySearchAPIWrapper()
tavily_tool = TavilySearchResults(api_wrapper=search, description=tool_description) 