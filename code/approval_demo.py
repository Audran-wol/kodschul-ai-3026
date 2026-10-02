"""Human approval in your own application.

In the portal, Foundry shows the Approve button. In your own code, you build that step yourself:
the agent asks for permission to call a tool, you show the request, a person answers.

Usage:
    python approval_demo.py "your question" AgentName
    python approval_demo.py "your question" AgentName 2     -> a specific agent version

The agent needs an MCP tool that requires approval (the default for MCP tools).
Login first with:  az login
"""
import sys

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

sys.stdout.reconfigure(encoding="utf-8")  # Windows console: show quotes correctly

PROJECT_ENDPOINT = "https://<your-resource>.services.ai.azure.com/api/projects/<your-project>"
if "<" in PROJECT_ENDPOINT or len(sys.argv) < 3:
    sys.exit('Set PROJECT_ENDPOINT at the top of this file, then run:\n'
             '  python approval_demo.py "your question" AgentName')

question, agent_name = sys.argv[1], sys.argv[2]
agent = {"name": agent_name, "type": "agent_reference"}
if len(sys.argv) > 3:
    agent["version"] = sys.argv[3]

project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())
openai = project.get_openai_client()

print(f"\nQUESTION to {agent_name}: {question}\n")
response = openai.responses.create(input=question, extra_body={"agent_reference": agent})

# The agent stops and waits whenever it wants to call a tool that needs approval.
while True:
    requests = [item for item in response.output if item.type == "mcp_approval_request"]
    if not requests:
        break
    answers = []
    for request in requests:
        print(f"The agent wants to call: {request.name}")
        print(f"With these arguments:    {request.arguments}")
        approved = input("Approve? [y/n] ").strip().lower() == "y"
        answers.append({
            "type": "mcp_approval_response",
            "approval_request_id": request.id,
            "approve": approved,
        })
    # Send the decision and let the agent continue where it stopped.
    response = openai.responses.create(
        previous_response_id=response.id,
        input=answers,
        extra_body={"agent_reference": agent},
    )

print(f"\nANSWER: {response.output_text}\n")
