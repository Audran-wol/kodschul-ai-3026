"""A2A lab: build two agents that talk to each other, in one script.

    FrontDeskAgent  --A2A-->  ProjectSpecialist

Run it in the VS Code terminal:   python a2a_lab.py
Change only the two values below.
"""
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

from azure.identity import DefaultAzureCredential

# ---- CHANGE THESE TWO VALUES -------------------------------------------------
PROJECT_ENDPOINT = "https://<your-resource>.services.ai.azure.com/api/projects/<your-project>"
MODEL = "<your-model-deployment>"  # name of a model deployment in your project
# ------------------------------------------------------------------------------

# False = the specialist is called with YOUR login. Works immediately.
# True  = the front desk agent uses its OWN identity. This is the production way,
#         but it needs a role assignment (you must be Owner) and Azure needs ~5 minutes.
USE_AGENT_IDENTITY = False

# Only fill this in if step 3 cannot find your project automatically.
# Azure Portal -> your Foundry project -> Properties -> Resource ID
PROJECT_RESOURCE_ID = ""

SPECIALIST = "ProjectSpecialist"
FRONT_DESK = "FrontDeskAgent"
# One connection name per mode: Azure does not switch the auth type of an existing connection.
CONNECTION = "project-specialist-a2a-agent" if USE_AGENT_IDENTITY else "project-specialist-a2a-user"
QUESTION = "What is the deployment status of Project Alpha?"

ARM = "https://management.azure.com"
AGENT_CONSUMER_ROLE = "eed3b665-ab3a-47b6-8f48-c9382fb1dad6"  # Foundry Agent Consumer

sys.stdout.reconfigure(encoding="utf-8")
if "<" in PROJECT_ENDPOINT + MODEL:
    sys.exit("Please set PROJECT_ENDPOINT and MODEL at the top of this file first.")
credential = DefaultAzureCredential()


def call(method, url, body=None, scope="https://ai.azure.com/.default"):
    """Send one REST request as the signed-in user. Returns (status, json)."""
    token = credential.get_token(scope).token
    request = urllib.request.Request(
        url,
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return response.status, json.loads(response.read() or b"{}")
    except urllib.error.HTTPError as error:
        text = error.read().decode(errors="replace")
        try:
            return error.code, json.loads(text)
        except ValueError:
            return error.code, {"error": text}


def must(step, status, result):
    if status >= 300:
        sys.exit(f"\nFAILED at: {step}\nHTTP {status}\n{json.dumps(result, indent=2)[:1500]}")
    print(f"OK   {step}")
    return result


def find_project_resource_id():
    """Find the Azure resource ID of the project from its endpoint."""
    if PROJECT_RESOURCE_ID:
        return PROJECT_RESOURCE_ID
    account = urllib.parse.urlparse(PROJECT_ENDPOINT).hostname.split(".")[0]
    project = PROJECT_ENDPOINT.rstrip("/").split("/")[-1]
    arm_scope = f"{ARM}/.default"
    _, subscriptions = call("GET", f"{ARM}/subscriptions?api-version=2022-12-01", scope=arm_scope)
    for subscription in subscriptions.get("value", []):
        query = urllib.parse.quote(
            f"resourceType eq 'Microsoft.CognitiveServices/accounts' and name eq '{account}'"
        )
        _, found = call(
            "GET",
            f"{ARM}{subscription['id']}/resources?$filter={query}&api-version=2021-04-01",
            scope=arm_scope,
        )
        if found.get("value"):
            return f"{found['value'][0]['id']}/projects/{project}"
    sys.exit("Could not find the project. Fill in PROJECT_RESOURCE_ID at the top of this file.")


# 1. The specialist: it is the only agent that knows the project facts.
must("1. create the specialist agent", *call(
    "POST", f"{PROJECT_ENDPOINT}/agents/{SPECIALIST}/versions?api-version=v1",
    {"definition": {
        "kind": "prompt",
        "model": MODEL,
        "instructions": (
            "You are the project status specialist. Answer only from these facts.\n"
            "Project Alpha: deployed to staging on Monday. Production release is planned for Friday. "
            "2 open bugs, both low priority.\n"
            "Project Beta: on hold, waiting for customer approval.\n"
            "If you do not have a fact, say that you do not have this information."
        ),
    }},
))

# 2. Open the specialist for A2A: publish an agent card and enable the A2A protocol.
must("2. enable incoming A2A on the specialist", *call(
    "PATCH", f"{PROJECT_ENDPOINT}/agents/{SPECIALIST}?api-version=v1",
    {
        "agent_card": {
            "description": "Answers questions about project status and deployments.",
            "version": "1.0",
            "skills": [{
                "id": "project-status",
                "name": "Project status",
                "description": "Deployment status, releases and open bugs of projects.",
            }],
        },
        "agent_endpoint": {"protocol_configuration": {"responses": {}, "a2a": {}}},
    },
))

# 3. The connection: where the specialist lives and which identity is used to call it.
project_id = find_project_resource_id()
connection_id = f"{project_id}/connections/{CONNECTION}"
must("3. create the A2A connection", *call(
    "PUT", f"{ARM}{connection_id}?api-version=2025-04-01-preview",
    {"properties": {
        "authType": "AgenticIdentityToken" if USE_AGENT_IDENTITY else "UserEntraToken",
        "category": "RemoteA2A",
        "target": f"{PROJECT_ENDPOINT}/agents/{SPECIALIST}/endpoint/protocols/a2a",
        "audience": "https://ai.azure.com",
        "Credentials": {},
        "metadata": {},
    }},
    scope=f"{ARM}/.default",
))

# 4. The front desk agent: it has no project facts, only the A2A tool.
must("4. create the front desk agent with the A2A tool", *call(
    "POST", f"{PROJECT_ENDPOINT}/agents/{FRONT_DESK}/versions?api-version=v1",
    {"definition": {
        "kind": "prompt",
        "model": MODEL,
        "instructions": (
            "You are the front desk assistant. You do not know any project facts yourself. "
            "For questions about project status, deployments or releases, ask the project specialist."
        ),
        "tools": [{"type": "a2a", "a2a_version": "1.0", "project_connection_id": connection_id}],
    }},
))

# 5. Permission: the front desk agent's own identity may call agents in this project.
if USE_AGENT_IDENTITY:
    front_desk = must("5a. read the front desk agent's identity", *call(
        "GET", f"{PROJECT_ENDPOINT}/agents/{FRONT_DESK}?api-version=v1"))
    principal_id = front_desk["instance_identity"]["principal_id"]
    assignment = uuid.uuid5(uuid.NAMESPACE_URL, project_id + principal_id)
    status, result = call(
        "PUT",
        f"{ARM}{project_id}/providers/Microsoft.Authorization/roleAssignments/{assignment}?api-version=2022-04-01",
        {"properties": {
            "roleDefinitionId": f"/{'/'.join(project_id.split('/')[1:3])}"
                                f"/providers/Microsoft.Authorization/roleDefinitions/{AGENT_CONSUMER_ROLE}",
            "principalId": principal_id,
            "principalType": "ServicePrincipal",
        }},
        scope=f"{ARM}/.default",
    )
    if status == 409:  # the role is already assigned
        status = 200
    must("5b. give the identity the 'Foundry Agent Consumer' role", status, result)

# 6. Test. With agent identity, the new role needs a few minutes, so we retry.
print(f"\nQUESTION to {FRONT_DESK}: {QUESTION}")
for attempt in range(20):
    status, response = call(
        "POST", f"{PROJECT_ENDPOINT}/openai/v1/responses",
        {"input": QUESTION, "agent_reference": {"name": FRONT_DESK, "type": "agent_reference"}},
    )
    if status < 300:
        break
    if not USE_AGENT_IDENTITY:
        sys.exit(f"\nFAILED\nHTTP {status}\n{json.dumps(response, indent=2)[:1500]}")
    print(f"     not ready yet (HTTP {status}), waiting for the role assignment... {attempt + 1}/20")
    time.sleep(30)
else:
    sys.exit(f"\nStill failing:\n{json.dumps(response, indent=2)[:1500]}")

for item in response["output"]:
    if item["type"].startswith("a2a"):
        print(f"STEP: {item['type']}: {str(item.get('arguments') or item.get('output'))[:300]}")
    elif item["type"] == "message":
        print(f"\nANSWER: {item['content'][0]['text']}")
