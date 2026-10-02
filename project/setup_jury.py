"""Pitch Jury: create the four agents in your Foundry project.

    JuryLead  --A2A-->  JurorCustomer
              --A2A-->  JurorEngineer
              --A2A-->  JurorInvestor

The lead also gets rubric.md as a knowledge file, so every idea is scored by the same rules.

Run it once:   python setup_jury.py
Needs .env (PROJECT_ENDPOINT, MODEL) in this folder, and "az login".
"""
import json
import os
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

# Only fill this in if step 2 cannot find your project automatically.
# Azure Portal -> your Foundry project -> Properties -> Resource ID
PROJECT_RESOURCE_ID = ""

LEAD = "JuryLead"
JURORS = {
    "customer": (
        "You are the CUSTOMER on a pitch jury. You are a busy person with a limited budget. "
        "Judge the idea only as a possible buyer: would you pay for it, how much, and what would stop you? "
        "Be honest and a little impatient. Answer in at most 3 short sentences."
    ),
    "engineer": (
        "You are the ENGINEER on a pitch jury. You have built many products. "
        "Judge the idea only on how to build it: how hard is it, how long does a small team need, "
        "and what breaks first? Be practical and direct. Answer in at most 3 short sentences."
    ),
    "investor": (
        "You are the INVESTOR on a pitch jury. You care about money and risk. "
        "Judge the idea only as a business: who pays, how big can it get, and what is the biggest risk? "
        "Be sceptical but fair. Answer in at most 3 short sentences."
    ),
}

ARM = "https://management.azure.com"
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


# 1. Knowledge: upload the scoring rubric so the lead can search it.
openai = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential).get_openai_client()
store = openai.vector_stores.create(name="pitch-jury-rubric")
with (HERE / "rubric.md").open("rb") as handle:
    openai.vector_stores.files.upload_and_poll(vector_store_id=store.id, file=handle)
print("OK   1. upload the scoring rubric as knowledge")

# 2. The three jurors: each one is an agent with its own role, reachable over A2A.
project_id = find_project_resource_id()
a2a_tools = []
for role, instructions in JURORS.items():
    agent = f"Juror{role.title()}"
    must(f"2. create {agent}", *call(
        "POST", f"{PROJECT_ENDPOINT}/agents/{agent}/versions?api-version=v1",
        {"definition": {"kind": "prompt", "model": MODEL, "instructions": instructions}},
    ))
    must(f"   enable incoming A2A on {agent}", *call(
        "PATCH", f"{PROJECT_ENDPOINT}/agents/{agent}?api-version=v1",
        {
            "agent_card": {
                "description": f"The {role} on a pitch jury. Gives a short opinion on a product idea.",
                "version": "1.0",
                "skills": [{"id": f"judge-as-{role}", "name": f"Judge as {role}",
                            "description": f"Judges a product idea from the {role}'s point of view."}],
            },
            "agent_endpoint": {"protocol_configuration": {"responses": {}, "a2a": {}}},
        },
    ))
    connection_id = f"{project_id}/connections/jury-{role}"
    must(f"   create the A2A connection jury-{role}", *call(
        "PUT", f"{ARM}{connection_id}?api-version=2025-04-01-preview",
        {"properties": {
            "authType": "UserEntraToken",   # the juror is called with your own login
            "category": "RemoteA2A",
            "target": f"{PROJECT_ENDPOINT}/agents/{agent}/endpoint/protocols/a2a",
            "audience": "https://ai.azure.com",
            "Credentials": {},
            "metadata": {},
        }},
        scope=f"{ARM}/.default",
    ))
    a2a_tools.append({"type": "a2a", "a2a_version": "1.0", "project_connection_id": connection_id})

# 3. The jury lead: has the rubric as knowledge and the three jurors as A2A tools.
must(f"3. create {LEAD} with knowledge and three A2A tools", *call(
    "POST", f"{PROJECT_ENDPOINT}/agents/{LEAD}/versions?api-version=v1",
    {"definition": {
        "kind": "prompt",
        "model": MODEL,
        "instructions": (
            "You are the lead of a pitch jury. A user sends you a product or project idea.\n"
            "1. Ask ALL THREE jurors for their opinion: the customer, the engineer and the investor. "
            "Send each of them the full idea. Never skip a juror.\n"
            "2. Look up the scoring rubric in your knowledge file and score the idea by its rules.\n"
            "3. Answer in exactly this format:\n"
            "Two sentences that sum up the jury's view.\n"
            "ADVICE: one piece of advice.\n"
            "SCORE: N/10"
        ),
        "tools": [{"type": "file_search", "vector_store_ids": [store.id]}] + a2a_tools,
    }},
))

print(f"\nThe jury is ready. Agents in your project: {LEAD}, "
      + ", ".join(f"Juror{role.title()}" for role in JURORS))
