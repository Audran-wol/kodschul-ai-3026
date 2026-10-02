"""Green Council: create the chair agent and one delegate agent per person in council.json.

    CouncilChair  --A2A-->  Delegate<Name>   (one per delegate)

The chair also gets:
  - council-charter.md as a knowledge file: the rules for the final decision
  - an API tool: live air quality for the city (../openapi/air-quality.json)

Run it after every change to council.json:   python setup_council.py
Needs .env (PROJECT_ENDPOINT, MODEL) and council.json in this folder, and "az login".
"""
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

HERE = Path(__file__).parent
sys.stdout.reconfigure(encoding="utf-8")

# Read .env: one NAME=value per line.
if (HERE / ".env").exists():
    for line in (HERE / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            name, value = line.split("=", 1)
            os.environ.setdefault(name.strip(), value.strip())

PROJECT_ENDPOINT = os.environ.get("PROJECT_ENDPOINT", "")
MODEL = os.environ.get("MODEL", "")
if not PROJECT_ENDPOINT or not MODEL or "<" in PROJECT_ENDPOINT + MODEL:
    sys.exit("Copy .env.example to .env and set PROJECT_ENDPOINT and MODEL.")
if not (HERE / "council.json").exists():
    sys.exit("Copy council.example.json to council.json and put in your delegates.")

# Only fill this in if the script cannot find your project automatically.
# Azure Portal -> your Foundry project -> Properties -> Resource ID
PROJECT_RESOURCE_ID = ""

CHAIR = "CouncilChair"
COUNCIL = json.loads((HERE / "council.json").read_text(encoding="utf-8"))
CITY = COUNCIL["city"]
DELEGATES = COUNCIL["delegates"]
AIR_QUALITY_SPEC = json.loads((HERE.parent / "openapi" / "air-quality.json").read_text(encoding="utf-8"))
ARM = "https://management.azure.com"
credential = DefaultAzureCredential()


def key(name):
    """A delegate's name as a safe identifier: 'Ana-Maria' -> 'anamaria'."""
    return re.sub(r"[^a-z0-9]", "", name.lower())


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


# 1. Knowledge: the council charter, so the chair decides by the same rules every time.
openai = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential).get_openai_client()
store = openai.vector_stores.create(name="council-charter")
with (HERE / "council-charter.md").open("rb") as handle:
    openai.vector_stores.files.upload_and_poll(vector_store_id=store.id, file=handle)
print("OK   1. upload the council charter as knowledge")

# 2. One agent per delegate, each with its own role and character, reachable over A2A.
project_id = find_project_resource_id()
a2a_tools = []
for delegate in DELEGATES:
    name, role, character = delegate["name"], delegate["role"], delegate["character"]
    agent = f"Delegate{key(name).title()}"
    must(f"2. create {agent} ({role})", *call(
        "POST", f"{PROJECT_ENDPOINT}/agents/{agent}/versions?api-version=v1",
        {"definition": {"kind": "prompt", "model": MODEL, "instructions": (
            f"You are {name}, a delegate in the Green Council of {CITY}.\n"
            f"Your role: {role}. {character}\n"
            "The chair sends you a proposal for the city. Judge it strictly from your role. "
            "Take a clear side; do not sit on the fence. Answer in exactly this format:\n"
            "VOTE: YES or NO\n"
            "Then one or two short sentences with your reason, in your own voice."
        )}},
    ))
    must(f"   enable incoming A2A on {agent}", *call(
        "PATCH", f"{PROJECT_ENDPOINT}/agents/{agent}?api-version=v1",
        {
            "agent_card": {
                "description": f"{name}, {role} in the Green Council. Votes yes or no on a proposal.",
                "version": "1.0",
                "skills": [{"id": "vote", "name": "Vote", "description": "Votes yes or no on a proposal."}],
            },
            "agent_endpoint": {"protocol_configuration": {"responses": {}, "a2a": {}}},
        },
    ))
    connection_id = f"{project_id}/connections/council-{key(name)}"
    must(f"   create the A2A connection council-{key(name)}", *call(
        "PUT", f"{ARM}{connection_id}?api-version=2025-04-01-preview",
        {"properties": {
            "authType": "UserEntraToken",   # the delegate is called with your own login
            "category": "RemoteA2A",
            "target": f"{PROJECT_ENDPOINT}/agents/{agent}/endpoint/protocols/a2a",
            "audience": "https://ai.azure.com",
            "Credentials": {},
            "metadata": {},
        }},
        scope=f"{ARM}/.default",
    ))
    a2a_tools.append({"type": "a2a", "a2a_version": "1.0", "project_connection_id": connection_id})

# 3. The chair: knowledge (charter) + an API tool (live air quality) + every delegate over A2A.
names = ", ".join(delegate["name"] for delegate in DELEGATES)
must(f"3. create {CHAIR} with knowledge, an API tool and {len(DELEGATES)} A2A tools", *call(
    "POST", f"{PROJECT_ENDPOINT}/agents/{CHAIR}/versions?api-version=v1",
    {"definition": {
        "kind": "prompt",
        "model": MODEL,
        "instructions": (
            f"You are the chair of the Green Council of {CITY}. A user sends a proposal for the city.\n"
            f"1. Get the live air quality of {CITY} with the AirQuality tool.\n"
            f"2. Ask EVERY delegate for a vote: {names}. Send each of them the full proposal. "
            "Never skip a delegate and never vote for a delegate yourself.\n"
            "3. Look up the council charter in your knowledge file and decide by its rules.\n"
            "4. Answer in exactly this format:\n"
            "DECISION: ADOPTED or REJECTED\n"
            "COUNT: x YES, y NO\n"
            "AIR: the EAQI number and one word (good, fair, moderate or poor)\n"
            "Then two sentences that explain the decision and name the delegates whose reasons mattered most."
        ),
        "tools": [
            {"type": "file_search", "vector_store_ids": [store.id]},
            {"type": "openapi", "openapi": {
                "name": "AirQuality",
                "description": "Live air quality (European Air Quality Index) for a city.",
                "spec": AIR_QUALITY_SPEC,
                "auth": {"type": "anonymous"},
            }},
        ] + a2a_tools,
    }},
))

print(f"\nThe council is ready: {CHAIR} and {len(DELEGATES)} delegates ({names}).")
