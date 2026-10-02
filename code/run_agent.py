"""Call a Foundry agent from Python.

Usage:
    python run_agent.py                      -> asks FrontDeskAgent the A2A demo question
    python run_agent.py "your question"      -> asks FrontDeskAgent your question
    python run_agent.py "question" AgentName -> asks another agent

Login first with:  az login
"""
import sys

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

sys.stdout.reconfigure(encoding="utf-8")  # Windows console: show quotes correctly

PROJECT_ENDPOINT = "https://<your-resource>.services.ai.azure.com/api/projects/<your-project>"
if "<" in PROJECT_ENDPOINT:
    sys.exit("Please set PROJECT_ENDPOINT at the top of this file first.")

question = sys.argv[1] if len(sys.argv) > 1 else "What is the deployment status of Project Alpha?"
agent_name = sys.argv[2] if len(sys.argv) > 2 else "FrontDeskAgent"

# 1. Who am I?  -> the identity from "az login"
project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())
openai = project.get_openai_client()

# 2. Ask the agent
print(f"\nQUESTION to {agent_name}: {question}\n")
response = openai.responses.create(
    input=question,
    extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
)

# 3. Show every step the agent took, so we can see the delegation
for item in response.output:
    if item.type == "reasoning":
        continue
    name = getattr(item, "name", "")
    detail = getattr(item, "arguments", None) or getattr(item, "output", None) or ""
    print(f"STEP: {item.type} {name} {str(detail)[:200]}".rstrip())

print(f"\nANSWER: {response.output_text}\n")
