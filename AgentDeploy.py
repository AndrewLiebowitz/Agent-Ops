# This script deploys the agent to the Vertex AI Agent Engine.
# It uses the ADK to define an agent that uses the OpenAPI spec (mtg_spec.yaml).

import os
import vertexai
from google.adk.agents import LlmAgent 
from google.adk.tools.openapi_tool import OpenAPIToolset 
from vertexai.agent_engines import create as agent_engine_create

# --- Configuration ---
AGENT_DISPLAY_NAME = "MTG_Tool_Only_Agent"
PROJECT_ID = os.getenv("CLOUDSDK_CORE_PROJECT") 
REGION = "us-central1"
OPENAPI_FILE_PATH = "mtg_spec.yaml" 

# !!! REPLACE THIS with your GCS bucket name !!!
GCS_STAGING_BUCKET = "gs://[YOUR_GCS_STAGING_BUCKET_NAME]"

# --- Initialize Vertex AI SDK ---
vertexai.init(
    project=PROJECT_ID,
    location=REGION,
    staging_bucket=GCS_STAGING_BUCKET
)

# --- Define the Agent ---
def create_minimal_agent():
    """Instantiates a simple ADK agent with only the MTG OpenAPI tool."""
    
    try:
        with open(OPENAPI_FILE_PATH, 'r') as f:
            openapi_spec_yaml = f.read()
    except FileNotFoundError:
        print(f"ERROR: {OPENAPI_FILE_PATH} not found. Ensure it is in the same directory.")
        raise

    toolset = OpenAPIToolset(
        spec_str=openapi_spec_yaml,
        spec_str_type="yaml"
    )
    
    return LlmAgent(
        name=AGENT_DISPLAY_NAME,
        model='gemini-2.5-flash',
        instruction=(
            "You are a helpful Magic: The Gathering card expert. "
            "Your sole function is to use the provided tool to look up card information "
            "when the user provides a specific card name."
        ),
        tools=[toolset] 
    )

# --- Deployment ---
def deploy_agent():
    print(f"Deploying Agent {AGENT_DISPLAY_NAME} to {REGION}...")
    
    agent_instance = create_minimal_agent()
    
    # This explicitly passes all required packages to the remote build environment.
    remote_agent = agent_engine_create(
        agent_instance,
        requirements=[
            "google-cloud-aiplatform",
            "google-adk",
            "pydantic",
            "cloudpickle",
            "pyyaml",
            "requests" # Also needed by the toolset to make the call
        ]
    )
    
    print(f"\n✅ Deployment command successfully sent!")
    print(f"Agent Engine Name: {remote_agent.name}")
    print("\nCheck the Vertex AI Agent Engine dashboard to monitor the build status.")

if __name__ == "__main__":
    deploy_agent()
