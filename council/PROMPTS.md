# Green Council: build it live, one prompt at a time

Show the finished page first: "this is what we want to build". Then give these prompts to your
coding agent (Claude Code, Codex or GitHub Copilot in Agent mode), one after the other.

If a step does not work, the finished scripts are in this folder: `setup_council.py` and `server.py`.

## Before you start

Make an empty working folder and copy in only the parts that are given:

```text
mkdir council-live
copy council\index.html           council-live\
copy council\council-charter.md   council-live\
copy council\council.example.json council-live\council.json
copy council\.env.example         council-live\.env
copy openapi\air-quality.json     council-live\
cd council-live
```

Then:

1. Open `council.json` and put in the names, roles and characters of your delegates.
2. Open `.env` and set `PROJECT_ENDPOINT` and `MODEL`.
3. Sign in: `az login`
4. Start your coding agent in the `council-live` folder.

What we build, in the order of the prompts:

| Prompt | Builds                       | Seminar topic         |
| ------ | ---------------------------- | --------------------- |
| 0      | Checks the login             | Identity              |
| 1      | Six delegate agents          | Agent + instructions  |
| 2      | A2A endpoint and connections | A2A + connections     |
| 3      | The knowledge base           | Knowledge             |
| 4      | The chair agent              | Tools (API) + A2A     |
| 5      | The backend for the page     | Code                  |
| 6      | A change, made by the room   | Everything together   |

---

## Prompt 0 — check the login

```text
I am signed in to Azure in this terminal with "az login". Never ask me for keys or passwords.
Run "az account show" and tell me which account and tenant I am signed in to.
Then read .env, council.json, council-charter.md and air-quality.json in this folder and
tell me in three sentences what you think we are going to build.
```

## Prompt 1 — the delegate agents

```text
Create a Python script "step1_delegates.py" and run it.

It reads PROJECT_ENDPOINT and MODEL from .env (one NAME=value per line) and the delegates and the
city from council.json. Use only the standard library plus azure-identity.

For every delegate, create a Microsoft Foundry prompt agent named "Delegate" + the delegate's name
(letters and digits only, first letter upper case), with this REST call:

  POST {PROJECT_ENDPOINT}/agents/{agent_name}/versions?api-version=v1
  Authorization: Bearer <token from DefaultAzureCredential, scope https://ai.azure.com/.default>
  Body: {"definition": {"kind": "prompt", "model": MODEL, "instructions": "..."}}

The instructions for each delegate:
  You are {name}, a delegate in the Green Council of {city}.
  Your role: {role}. {character}
  The chair sends you a proposal for the city. Judge it strictly from your role.
  Take a clear side; do not sit on the fence. Answer in exactly this format:
  VOTE: YES or NO
  Then one or two short sentences with your reason, in your own voice.

Print one "OK" line per agent. On an error, print the HTTP status and the response body and stop.
```

## Prompt 2 — A2A: open the delegates and connect them

```text
Create "step2_a2a.py" and run it. Same .env, council.json and authentication as step 1.

For every delegate agent do two things.

1. Enable incoming A2A on the agent:
   PATCH {PROJECT_ENDPOINT}/agents/{agent_name}?api-version=v1
   Body: {
     "agent_card": {"description": "<name>, <role> in the Green Council. Votes yes or no on a proposal.",
                    "version": "1.0",
                    "skills": [{"id": "vote", "name": "Vote", "description": "Votes yes or no on a proposal."}]},
     "agent_endpoint": {"protocol_configuration": {"responses": {}, "a2a": {}}}
   }

2. Create a project connection named "council-" + the delegate's name in lower case
   (letters and digits only). This call goes to Azure Resource Manager, so use a token with the
   scope https://management.azure.com/.default:
   PUT https://management.azure.com{PROJECT_RESOURCE_ID}/connections/{connection_name}?api-version=2025-04-01-preview
   Body: {"properties": {
     "authType": "UserEntraToken",
     "category": "RemoteA2A",
     "target": "{PROJECT_ENDPOINT}/agents/{agent_name}/endpoint/protocols/a2a",
     "audience": "https://ai.azure.com",
     "Credentials": {}, "metadata": {}}}

Find PROJECT_RESOURCE_ID yourself: the account name is the first part of the host name in
PROJECT_ENDPOINT and the project name is its last path segment. List my subscriptions
(GET https://management.azure.com/subscriptions?api-version=2022-12-01), then in each one search
GET {subscription id}/resources?$filter=resourceType eq 'Microsoft.CognitiveServices/accounts' and name eq '<account>'&api-version=2021-04-01
The project resource ID is "<account resource id>/projects/<project name>".

Save the list of connection resource IDs to "connections.json". Print one "OK" line per step.
```

## Prompt 3 — the knowledge base

```text
Create "step3_knowledge.py" and run it.

Upload council-charter.md as a knowledge base that an agent can search:
  from azure.ai.projects import AIProjectClient
  from azure.identity import DefaultAzureCredential
  openai = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential()).get_openai_client()
  store = openai.vector_stores.create(name="council-charter")
  openai.vector_stores.files.upload_and_poll(vector_store_id=store.id, file=<the open file>)

Save the vector store id to "knowledge.json" and print it.
Install azure-ai-projects and openai with pip if they are missing.
```

## Prompt 4 — the chair: knowledge + an API tool + A2A

```text
Create "step4_chair.py" and run it.

Create a Foundry prompt agent named "CouncilChair" with the same REST call as in step 1.
It gets three kinds of tools:

1. The knowledge base from knowledge.json:
   {"type": "file_search", "vector_store_ids": [<vector store id>]}

2. An API tool from air-quality.json (an OpenAPI definition, no authentication):
   {"type": "openapi", "openapi": {"name": "AirQuality",
     "description": "Live air quality (European Air Quality Index) for a city.",
     "spec": <the content of air-quality.json>, "auth": {"type": "anonymous"}}}

3. One A2A tool per connection in connections.json:
   {"type": "a2a", "a2a_version": "1.0", "project_connection_id": <connection resource id>}

The instructions of the chair:
  You are the chair of the Green Council of {city}. A user sends a proposal for the city.
  1. Get the live air quality of {city} with the AirQuality tool.
  2. Ask EVERY delegate for a vote: {the delegate names}. Send each of them the full proposal.
     Never skip a delegate and never vote for a delegate yourself.
  3. Look up the council charter in your knowledge file and decide by its rules.
  4. Answer in exactly this format:
  DECISION: ADOPTED or REJECTED
  COUNT: x YES, y NO
  AIR: the EAQI number and one word (good, fair, moderate or poor)
  Then two sentences that explain the decision and name the delegates whose reasons mattered most.

Then test it once and print every step of the answer:
  response = openai.responses.create(
      input="Ban cars from the city centre on weekends",
      extra_body={"agent_reference": {"name": "CouncilChair", "type": "agent_reference"}})
  For each item in response.output print item.type, and at the end print response.output_text.
```

## Prompt 5 — the backend for the page

```text
index.html is a finished page. Do not change it. Read the comment at the top of its script: it
describes the two endpoints the page needs.

Build "server.py" with the Python standard library (http.server) plus azure-ai-projects and
azure-identity. It listens on http://127.0.0.1:8000 only.

- GET /             -> serve index.html
- GET /api/council  -> the content of council.json
- POST /api/propose <- {"proposal": "..."}
  Call the agent "CouncilChair" as in step 4 and build the answer from response.output:
  - item.type == "file_search_call"            -> "used_knowledge": true
  - item.type == "openapi_call_output"         -> "air": read the numbers european_aqi, pm2_5 and
                                                   pm10 out of the text in item.output
  - type contains "a2a" and ends with "call_output" -> one vote. item.name is the connection name
    ("council-<name>"): map it back to the delegate's name from council.json. item.output is the
    delegate's text: "vote" is YES or NO from the line "VOTE: ...", "reason" is the rest.
  - "decision" is ADOPTED or REJECTED from the line "DECISION: ..." in response.output_text.
  - "explanation" is response.output_text without the lines that start with DECISION, COUNT or AIR.
- Reject a missing, empty or longer than 500 characters proposal with status 400 and {"error": "..."}.
- If the agent call fails, return status 502 and {"error": "<short reason>"}. Never crash.

Run it, send one test proposal to /api/propose, show me the JSON, and tell me the URL to open.
```

## Prompt 6 — let the room change it

Ask each participant for one sentence about how their delegate should think. Then:

```text
In council.json, change the character of the delegate "<name>" to: "<their sentence>".
Run step1_delegates.py again so the agent gets the new instructions, then send the proposal
"Make public transport free for everyone" to /api/propose and show me how <name> voted and why.
```

More changes that are fun to watch:

- Change a rule in `council-charter.md`, for example "A tie always counts as ADOPTED", run
  step 3 and step 4 again, and send the same proposal.
- Change the city in `council.json` to a city with worse air, run step 1 and step 4 again.
- Add a seventh delegate: a mayor, a farmer, a tourist.
