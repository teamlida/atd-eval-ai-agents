import os

import requests
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

# Which model? "gemini" by default. For the local backup, set AGENT_MODEL=local in .env,
# or change "gemini" to "local" on the last line. Local needs: ollama pull gemma4:e2b
MODELS = {
    "gemini": "gemini-3.5-flash-lite",
    "local": LiteLlm(model="ollama_chat/gemma4:e2b", think=False),
}
MODEL = MODELS[os.getenv("AGENT_MODEL", "gemini")]


MOCK_API_BASE_URL = "https://fake-json-api.mock.beeceptor.com/users"


def get_user_data(user_id: str) -> dict:
    try:
        response = requests.get(f"{MOCK_API_BASE_URL}/{user_id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

root_agent = Agent(
    model=MODEL,
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge. Use the get_user_data tool to retrieve user data. Put user ID to the input of the tool.',
    tools=[get_user_data]
)