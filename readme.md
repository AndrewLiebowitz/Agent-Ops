Vertex AI Agent with Custom Tool (Cloud Run + ADK)
This repository is a complete template for building, deploying, and connecting a custom tool (a REST API) to a Gemini agent using the Vertex AI Agent Development Kit (ADK).
The process is broken into three main parts:
Build the Tool: A Python web service (the MTG API) deployed to Cloud Run.
Build the Agent: A Python script using the ADK to deploy an agent to the Vertex AI Agent Engine, telling it how to use the tool via an OpenAPI spec.
Test the Agent: A Python script to query the deployed agent and get a response.
1. The Tool (Cloud Run API)
This is the external REST API that your agent will call. We'll deploy the Python code from the cloud-run-tool/ directory.
CLI Commands:
Install dependencies (first time only):
pip install google-cloud-run-deploy (if not already installed)
Deploy the Cloud Run service:
Navigate to the cloud-run-tool/ directory.
Run the gcloud deploy command. This will build and deploy your service.
gcloud run deploy agent-mtg-tool --source . --region "us-central1" --allow-unauthenticated
When this command finishes, it will give you a Service URL. Copy this URL.
Test the Tool (cURL):
Replace [YOUR_CLOUD_RUN_URL] with the URL from the previous step.
curl -X POST "[YOUR_CLOUD_RUN_URL]" -H "Content-Type: application/json" -d '{"card_name": "Black Lotus"}'
You should see the raw JSON data for the card.
2. The Agent (Vertex AI ADK)
Now we deploy the agent, which acts as the "brain" that knows how to use the tool.
Setup (One Time):
Install ADK Libraries:
pip install google-cloud-aiplatform[adk,agent_engines] --upgrade --force-reinstall
Configuration:
Edit vertex-ai-agent/mtg_spec.yaml:
Open this file and replace the placeholder url with your live Cloud Run URL from Part 1.
Edit vertex-ai-agent/deploy_agent.py:
Update the GCS_STAGING_BUCKET variable to point to a bucket in your project (e.g., gs://[YOUR-PROJECT-ID]-adk-staging).
Deployment:
Run the Deployment Script:
From the root of the repository, execute the deploy script:
python3 vertex-ai-agent/deploy_agent.py
This will take 5-15 minutes. It's successful when it prints the Agent Engine Name (which is a long number).
3. Test the Deployed Agent
Finally, we test the agent (the "brain") to see if it can correctly call the tool.
Configuration:
Edit vertex-ai-agent/test_agent.py:
Open this file and replace the AGENT_ID placeholder with the long number (the resource name) from the successful deployment output.
Run the Test:
Execute the Test Script:
python3 vertex-ai-agent/test_agent.py
If successful, you will see the agent's final, human-readable answer: Black Lotus is an Artifact...



Requirements for the Cloud Run tool
functions-framework==3.*
requests==2.*
