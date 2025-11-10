# This script queries your DEPLOYED agent (the "brain")
# to see if it can successfully call your tool.

import os
import vertexai
from vertexai import agent_engines # Import the module directly

# --- Configuration ---
PROJECT_ID = os.getenv("CLOUDSDK_CORE_PROJECT") 
REGION = "us-central1"

# --- !!! REPLACE THIS with your agent's numeric ID from the deploy_agent.py output !!! ---
AGENT_ID = "[YOUR_AGENT_RESOURCE_ID_NUMBER]" 

# 1. Initialize the Vertex AI SDK
vertexai.init(project=PROJECT_ID, location=REGION)

# 2. Get a reference to your agent
print("Retrieving deployed agent...")
remote_agent = agent_engines.get(
    f"projects/{PROJECT_ID}/locations/{REGION}/reasoningEngines/{AGENT_ID}"
)

print("✅ Agent retrieved successfully. Sending a test query...")

# 3. Send a query to the agent
response = remote_agent.query(
    input="What is the mana cost of Black Lotus?"
)

print("\n--- Agent Response ---")
# The final, human-readable answer is in the 'output' attribute
print(response.output)
