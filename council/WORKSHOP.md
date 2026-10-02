# Green Council — we build it together

This is the script for the live build. Read it from top to bottom.

How it works: we build one small piece, we test it, we understand it, then the next piece.
The room gives the content. The coding agent writes the code. Nobody types code by hand.

Three kinds of boxes:

- **Run** — a command for the terminal.
- **Paste into the file** — what the room gives us goes into a file in VS Code.
- **Tell the coding agent** — a prompt to copy into Claude Code, Codex, Copilot (Agent mode) or ChatGPT.

Who gives what (fill in the names before you start):

| Piece                         | Given by                 |
| ----------------------------- | ------------------------ |
| A delegate with a character   | everyone                 |
| The rules of the council      | [VOLUNTEER-KNOWLEDGE]    |
| How the chair behaves         | [VOLUNTEER-INSTRUCTIONS] |
| Our city                      | [VOLUNTEER-API]          |
| Proposals to test with        | [VOLUNTEER-TEST]         |
| Wishes for the look           | [VOLUNTEER-DESIGN]       |

---

## 1. What we build

Today we learned five things: instructions, knowledge, tools, connections, and agents that talk
to each other. Now we put all five into one system. And we make it a bit silly, because silly is
easier to remember.

We build a **Green Council**. A city council that decides about the environment. You type a
proposal, for example "Ban cars from the city centre on weekends".

Every seat in the council is an AI agent. And every agent has one of **your** names. So in ten
minutes there will be an AI version of you that votes in public. No pressure.

The delegates vote yes or no. Then the chair decides. The chair is the only one who has read the
rules, which makes it different from most meetings.

*(Show the finished page for one minute, so everybody sees where we are going.)*

Here is what the council needs. Remember this list, we tick it off one by one:

1. A connection to Azure
2. A folder where everything lives
3. Delegates — **instructions**
4. Rules — a **knowledge base**
5. Live data — a **tool** that calls an API
6. A chair who uses 4 and 5
7. A way for the chair to ask the delegates — **A2A**
8. A web page — **code**

---

## 2. Are we connected to Azure?

Before we build anything, let us check that my terminal knows who I am.

**Run**

```text
az account show --query "{user:user.name, tenant:tenantId, subscription:name}" -o table
```

There I am. That is the account everything will run as. Remember this: we will not type a single
password or key today. The coding agent works through this login. It can do what I am allowed to
do, and nothing more. If it ever asks me for a password, we fire it.

*(If the command says "Please run az login": run `az login`, pick the account, and run the check again.)*

---

## 3. The base folder

Every project starts with an empty folder and a bit of hope.

**Run**

```text
mkdir council-live
cd council-live
code .
```

Now I start the coding agent in this folder. And the first thing I tell it is not "write code".
The first thing is: here is what we are building, here is how the folder is organised, and here
are the rules. It is like a new colleague on the first day. If you explain nothing, you get
surprises.

**Tell the coding agent**

```text
We are building a small project called "Green Council" live in front of a class, step by step.
I will give you one small task at a time. After each task, stop and wait.

WHAT IT IS
A user types a proposal for a city. One AI agent per delegate votes YES or NO. A chair agent looks
up live air quality through an API tool, reads the council rules from a knowledge base, asks every
delegate over the A2A protocol, and decides. The agents live in my Microsoft Foundry project.
A small Python server connects a web page to the chair.

CREATE THIS STRUCTURE NOW (empty files are fine, I fill them with the class)
  .env                   my settings: PROJECT_ENDPOINT, MODEL, CITY (one NAME=value per line)
  .env.example           the same three names with placeholder values
  .gitignore             must contain .env and state.json
  README.md              five lines: what the project is and what each folder is for
  agents/delegates.txt   one delegate per line:  Name | Role | Character
  agents/chair.md        how the chair behaves (free text)
  knowledge/charter.md   the rules of the council = our knowledge base
  tools/                 OpenAPI definitions of API tools
  scripts/               one small Python script per step
  app/                   the web page and its server
  state.json             ids that the scripts create (vector store, connections). Starts as {}.

RULES FOR ALL LATER TASKS
- I am signed in with "az login". Use DefaultAzureCredential (azure-identity). Never ask for keys
  or passwords. Never print the values in .env.
- Python 3.11. Standard library plus azure-identity, azure-ai-projects and openai. Read .env by
  hand, do not add python-dotenv. Install a missing package with pip.
- Every script prints one short "OK ..." line per thing it creates. On an error it prints the
  HTTP status and the response body, and stops.
- Token scopes: https://ai.azure.com/.default for my project endpoint,
  https://management.azure.com/.default for management.azure.com.
- Tell me each command before you run it. Ask before you delete anything.

When the structure exists, show me the folder tree.
```

Look at the tree. Every folder has one job. `agents` is who they are. `knowledge` is what they
know. `tools` is what they can do. `scripts` is how we build it. `app` is what people see.
If you forget everything else from today, keep this picture.

Now my settings. I open `.env` and put in three lines.

**Paste into the file** `.env`

```text
PROJECT_ENDPOINT=https://<your-resource>.services.ai.azure.com/api/projects/<your-project>
MODEL=<your-model-deployment>
CITY=<we fill this in soon>
```

This is all the configuration there is. The endpoint says where my Foundry project lives. The
model says which model the agents use. No key. No password. And this file stays on my machine:
look at `.gitignore`, it is listed there.

✔ Connection. ✔ Folder. Six to go.

---

## 4. The delegates — your instructions

A council without delegates is called a room. So we need people. That is you.

**Ask the room**

Everybody, please write one line in the chat, in this form:

```text
YourName | your role in the council | how you think, in one sentence
```

For example: `Mario | Business owner | I think about shops, jobs and costs, and I count twice.`

You can be yourself. You can be the opposite of yourself. You can be your boss. I will not ask.

*(Give them one minute. Roles that work well: climate scientist, business owner, city engineer,
finance delegate, citizens' voice, youth delegate, farmer, tourist.)*

**Paste into the file** `agents/delegates.txt` — one line per person, exactly as they wrote it.

These lines are **instructions**. This morning we wrote instructions for one agent. Now each of
you wrote them for your own.

**Tell the coding agent**

```text
Task: scripts/01_delegates.py. Create it and run it.

Read agents/delegates.txt (Name | Role | Character per line, skip empty lines) and CITY from .env.
For every delegate create a Microsoft Foundry prompt agent named "Delegate" + the name (letters
and digits only, first letter upper case):

  POST {PROJECT_ENDPOINT}/agents/{agent_name}/versions?api-version=v1
  Body: {"definition": {"kind": "prompt", "model": MODEL, "instructions": "..."}}

Instructions for each one:
  You are {name}, a delegate in the Green Council of {city}.
  Your role: {role}. {character}
  The chair sends you a proposal for the city. Judge it strictly from your role.
  Take a clear side; do not sit on the fence. Answer in exactly this format:
  VOTE: YES or NO
  Then one or two short sentences with your reason, in your own voice.

Then add a second script scripts/ask.py:
  python scripts/ask.py <AgentName> "<question>"
It calls the agent and prints item.type for every item in response.output, then the final text:
  from azure.ai.projects import AIProjectClient
  openai = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential()).get_openai_client()
  response = openai.responses.create(input=question,
      extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}})
```

**Test** — CITY is not set yet, so first ask [VOLUNTEER-API]: which city are we? Put it in `.env`,
then run the script again if needed. Now let us talk to one delegate directly.

```text
python scripts/ask.py Delegate<Name> "Proposal: every Monday is a day without meetings."
```

There. That is [name]'s agent, and it has an opinion. [Name], is that what you would say?

*(Open the Foundry portal → Agents. Show the new agents. Open one and show the instructions:
their own words from the chat.)*

They exist in my Azure project now. Real agents, with your names. If one of them says something
embarrassing later, remember who wrote its instructions.

✔ Delegates.

---

## 5. The rules — our knowledge base

Right now our delegates have opinions but the council has no rules. That is called social media.
We need a charter.

**Ask [VOLUNTEER-KNOWLEDGE]**

You are our law maker. Please give me three rules in the chat:

1. When is a proposal adopted?
2. What happens when the vote is a tie?
3. When may the chair say no, even against the majority?

**Paste into the file** `knowledge/charter.md` — first their three rules, then this fixed part:

```text
## Clean air rule
The chair looks up the live European Air Quality Index (EAQI) of our city before deciding.
0 to 20 is good, 20 to 40 is fair, 40 to 60 is moderate, above 60 is poor.
If the air is poor and the proposal would reduce pollution, a tie counts as ADOPTED.

## How the chair answers
First line:  DECISION: ADOPTED or REJECTED
Second line: COUNT: x YES, y NO
Third line:  AIR: the EAQI number and one word (good, fair, moderate or poor)
Then two sentences: why, and which delegates' reasons mattered most.
```

This file is **knowledge**. Not instructions. Instructions say how to behave. Knowledge says what
is true. The chair will search this document before every decision, the same way KodschulAssistant
searched our PDF this morning.

**Tell the coding agent**

```text
Task: scripts/02_knowledge.py. Create it and run it.

Upload knowledge/charter.md into a new vector store so an agent can search it:
  openai = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential()).get_openai_client()
  store = openai.vector_stores.create(name="council-charter")
  openai.vector_stores.files.upload_and_poll(vector_store_id=store.id, file=<the open file>)
Save the id in state.json under "vector_store_id" (keep the other keys in state.json).
```

It says OK. We cannot see anything yet, because nobody is reading the charter. Patience. The
chair comes in two steps.

✔ Knowledge base.

---

## 6. Live data — a tool that calls an API

Our council decides about the environment. So it should know one fact about the real world:
how good is the air in our city, right now? That is in no document. For this we need a **tool**.

[VOLUNTEER-API] chose our city. Let us see if the internet knows it.

**Tell the coding agent**

```text
Task: tools/air-quality.json. Create it, then test the API.

An OpenAPI 3.0.1 definition named "AirQuality" for the free Open-Meteo air quality API.
No authentication.
- Server: https://air-quality-api.open-meteo.com
- One operation: GET /v1/air-quality, operationId getAirQuality
- Query parameters, all required:
    latitude  (number)  "Latitude of the city, for example 48.78 for Stuttgart."
    longitude (number)  "Longitude of the city, for example 9.18 for Stuttgart."
    current   (string)  "Always send exactly this text: european_aqi,pm2_5,pm10"
- Response 200: an object "current" with time, european_aqi, pm2_5 and pm10.

Then call the API once yourself for the CITY in .env and tell me the air quality index and
whether that is good, fair, moderate or poor.
```

**Test** — the agent prints a real number.

That number is the air in our city at this minute. Not from the model's memory. From a sensor
network, through an API.

Look at the file. It does not contain the API. It **describes** the API: the address, the
parameters, what comes back. The agent reads these descriptions to know how to call it. If you
write a lazy description, you get a lazy tool.

✔ Tool.

---

## 7. The chair

Now the boss. The chair gets the knowledge base and the tool. Not the delegates yet. One thing at
a time, so that when something breaks we know who to blame.

**Ask [VOLUNTEER-INSTRUCTIONS]**

How should our chair behave? Strict? Friendly? Dramatic? Give me one or two sentences.

**Paste into the file** `agents/chair.md` — their sentences.

**Tell the coding agent**

```text
Task: scripts/03_chair.py. Create it and run it.

Create a Foundry prompt agent named "CouncilChair" (same POST call as the delegates) with two tools:
  {"type": "file_search", "vector_store_ids": [<vector_store_id from state.json>]}
  {"type": "openapi", "openapi": {"name": "AirQuality",
     "description": "Live air quality (European Air Quality Index) for a city.",
     "spec": <the content of tools/air-quality.json>, "auth": {"type": "anonymous"}}}

Instructions:
  You are the chair of the Green Council of {CITY}.
  {the content of agents/chair.md}
  When you get a proposal:
  1. Get the live air quality of {CITY} with the AirQuality tool.
  2. Ask every delegate for a vote, if you have delegates to ask.
  3. Look up the council charter in your knowledge file and decide by its rules.
  4. Answer in exactly the format that the charter defines.
```

**Test** — we ask the chair two things: one needs the tool, one needs the knowledge.

```text
python scripts/ask.py CouncilChair "How is the air in our city right now, and what does our charter say about a tie?"
```

Read the steps it printed. `openapi_call`: that is the tool. `file_search_call`: that is the
knowledge base. And the answer has the real number and [VOLUNTEER-KNOWLEDGE]'s rule about ties.

So now we have a chair that knows the rules and knows the air. But it sits alone in an empty
room, talking to itself. We have all been in that meeting.

✔ Chair.

---

## 8. A2A — the chair asks the delegates

The delegates exist. The chair exists. They cannot talk to each other. For that we need three
small things, and this is the part that cost me a whole night, so today you get it in one prompt.

1. Each delegate publishes a little card that says "I exist, and here is what I do".
2. A **connection** from the chair to each delegate.
3. An **A2A tool** on the chair for each connection.

**Tell the coding agent**

```text
Task: scripts/04_connect.py. Create it and run it.

For every delegate agent from agents/delegates.txt:

a) Enable incoming A2A:
   PATCH {PROJECT_ENDPOINT}/agents/{agent_name}?api-version=v1
   {"agent_card": {"description": "<name>, <role> in the Green Council. Votes yes or no on a proposal.",
                   "version": "1.0",
                   "skills": [{"id": "vote", "name": "Vote", "description": "Votes yes or no on a proposal."}]},
    "agent_endpoint": {"protocol_configuration": {"responses": {}, "a2a": {}}}}

b) Create a project connection named "council-" + the name in lower case (letters and digits only):
   PUT https://management.azure.com{PROJECT_RESOURCE_ID}/connections/{connection_name}?api-version=2025-04-01-preview
   {"properties": {"authType": "UserEntraToken", "category": "RemoteA2A",
                   "target": "{PROJECT_ENDPOINT}/agents/{agent_name}/endpoint/protocols/a2a",
                   "audience": "https://ai.azure.com", "Credentials": {}, "metadata": {}}}

   Find PROJECT_RESOURCE_ID yourself: the account name is the first part of the host name of
   PROJECT_ENDPOINT, the project name is its last path segment. List my subscriptions
   (GET https://management.azure.com/subscriptions?api-version=2022-12-01) and in each one search
   GET {subscription id}/resources?$filter=resourceType eq 'Microsoft.CognitiveServices/accounts' and name eq '<account>'&api-version=2021-04-01
   The project resource ID is "<account resource id>/projects/<project name>".

Save the connection resource ids in state.json under "connections".

Then change scripts/03_chair.py so the chair also gets one tool per connection:
  {"type": "a2a", "a2a_version": "1.0", "project_connection_id": <connection resource id>}
and so that step 2 of its instructions becomes:
  2. Ask EVERY delegate for a vote: {the delegate names}. Send each of them the full proposal.
     Never skip a delegate and never vote for a delegate yourself.
Run 03_chair.py again.
```

**Ask [VOLUNTEER-TEST]** — give us three proposals: one that should pass, one that should fail,
and one where you honestly do not know.

**Test** — the first real session of our council.

```text
python scripts/ask.py CouncilChair "<the first proposal>"
```

Count the steps. One `file_search_call`. One `openapi_call`. And one `a2a` step for each of you.
The chair asked every delegate, each delegate answered in character, and the chair decided by
the charter.

That is five different ideas from today in one answer. And nobody wrote a line of code by hand.

*(If a delegate is missing in the steps, send the proposal again. The chair sometimes forgets
someone, like every chair.)*

✔ A2A. The council works. It is just not pretty yet.

---

## 9. The backend

A terminal is fine for us. But a mayor will not open a terminal. We need a web page, and between
the page and the chair we need a small server. Why not call Foundry directly from the browser?
Because the login is on my machine, not in your browser. The server is the doorman.

**Tell the coding agent**

```text
Task: app/server.py. Create it, start it, and test it.

Python standard library (http.server) plus azure-ai-projects and azure-identity.
Listen on http://127.0.0.1:8000 only. Read .env from the project root.

- GET /             -> serve app/index.html (answer 404 with a short text while it does not exist)
- GET /api/council  -> {"city": CITY, "delegates": [{"name": ..., "role": ..., "character": ...}]}
                       from agents/delegates.txt
- POST /api/propose <- {"proposal": "..."}
                    -> {"votes": [{"name": "...", "vote": "YES" or "NO" or null, "reason": "..."}],
                        "air": {"eaqi": 23, "pm2_5": 5.5, "pm10": 7.5} or null,
                        "used_knowledge": true or false,
                        "decision": "ADOPTED" or "REJECTED" or null,
                        "explanation": "..."}
  Call the agent "CouncilChair" like scripts/ask.py does, and read response.output:
  - item.type == "file_search_call"    -> used_knowledge is true
  - item.type == "openapi_call_output" -> air: find the numeric values of european_aqi, pm2_5 and
    pm10 in the text of item.output (ignore the units block where the values are words)
  - type contains "a2a" and ends with "call_output" -> one vote. item.name is the connection name
    "council-<name>": map it back to the delegate's real name. item.output is the delegate's text:
    vote is YES or NO from the line "VOTE: ...", reason is the rest.
  - decision: ADOPTED or REJECTED from the line "DECISION: ..." in response.output_text
  - explanation: response.output_text without the lines that start with DECISION, COUNT or AIR
- A missing, empty or longer than 500 characters proposal: status 400 and {"error": "..."}.
- If the agent call fails: status 502 and {"error": "<short reason>"}. Never crash.

Test POST /api/propose with one proposal and show me the JSON. Leave the server running.
```

**Test** — the agent shows JSON with a vote for each of you, the air numbers, and a decision.

Not beautiful. But this JSON is everything a page needs. The hard part is done.

✔ Backend.

---

## 10. The page

Now we make it look like something you would show your boss.

**Ask [VOLUNTEER-DESIGN]** — two wishes. Colours? Mood? What must be big?

**Tell the coding agent**

```text
Task: app/index.html. One file, no libraries, no external fonts or images.
It talks only to GET /api/council and POST /api/propose on the same server.

Layout
- Header: "Green Council of <city>".
- A box to type a proposal, a button "Open the vote", and five example proposals as chips.
- The chamber: the delegates sit on a half circle, each as a coloured round avatar with the first
  letter of the name, the name and the role under it, and a small vote badge. The chair sits in
  the middle at the bottom. The decision appears large in the centre.
- A panel "Under the hood" with four steps that light up one after the other: KB (the charter was
  searched), API (the live air quality with the number and a small scale from good to poor),
  A2A (how many delegates answered), and the decision.
- "The debate": one card per delegate with name, role, vote and reason.

Behaviour
- While waiting, every avatar shows a spinning ring and the four steps blink.
- When the answer arrives, reveal it like a show: the knowledge step, then the air quality, then
  the delegates one by one (about 0.7 seconds apart: the avatar glows green for YES or red for NO
  and the speech card appears), then the decision pops in with "x YES · y NO" and the explanation.
- A delegate that is missing in the answer shows "not asked".
- Backend errors appear as a red line under the form.

Design wishes from the class: <PASTE THE WISHES HERE>
Make it look like a real product: dark background, soft glow, generous spacing.

Rules: put agent text on the page with textContent, never innerHTML. Respect
prefers-reduced-motion. It must also work on a narrow screen.
When done, tell me to reload http://127.0.0.1:8000.
```

**Test** — open http://127.0.0.1:8000 and put the second proposal.

*(While it thinks, about half a minute:)* The chair is asking each of you right now. Watch the
panel on the right. Knowledge. Tool. A2A. Those are our three building blocks, live.

There it is. [Name] voted no. [Name], would you have voted no?

*(If the generated page is broken, copy the finished `index.html` from this repo folder into
`app/` and reload. Nobody will know.)*

✔ Page. All eight. The council is open.

---

## 11. Now break it — on purpose

A system you cannot change is a museum. Let us change three things and watch what happens.

**Change a person.** Does your delegate think like you? If not, give me a better sentence.

*(Edit their line in `agents/delegates.txt`, then:)*

```text
python scripts/01_delegates.py
```

Same proposal again. Look: one sentence of instructions changed, and the vote changed.

**Change the law.** [VOLUNTEER-KNOWLEDGE], you are in power. Add a rule. Any rule.
"A tie always counts as adopted." "Proposals with the word free are always rejected."

*(Edit `knowledge/charter.md`, then:)*

```text
python scripts/02_knowledge.py
python scripts/03_chair.py
```

Same proposal again. We changed one line in a document. No code. And the decision is different.
That is what a knowledge base is for. And that is also why you should be careful who is allowed
to edit it.

**Change the world.** Put a city with worse air into `.env`, run `03_chair.py` again, and send
the third proposal: the one nobody was sure about.

---

## 12. Give everyone the link (optional)

Right now the council only runs on my machine. Let us open the doors.

**Run** (the first line only once)

```text
winget install Cloudflare.cloudflared
```

```text
cloudflared tunnel --url http://127.0.0.1:8000
```

It prints an address that ends in `trycloudflare.com`. I put it in the chat. Open it, and put
your own proposal. Be nice. It is your own name voting.

What happens now: your browser talks to my machine, my server calls my agents with my login, and
the answer travels back to you.

One honest word. This is a quick way to share a demo. It is not a real deployment. While this
runs, everybody with the link spends my Azure budget. So when we are done, I press Ctrl+C, and
the council goes home.

A real deployment would put `app/server.py` in a container on Azure, for example Azure Container
Apps, with its own identity instead of my login, and that identity would get permission to call
the chair. The code stays the same. Only the identity changes.

---

## 13. What you just built

Look at the folder one more time.

- `agents/` — your words. **Instructions.**
- `knowledge/` — the charter. **Knowledge.**
- `tools/` — the air quality. **A tool that calls an API.**
- `scripts/` — connections and **A2A**.
- `app/` — the page. **Code.**

That is the whole day in five folders. And the real lesson is not the council. The lesson is
that you can build a system like this in an hour, if you know these five pieces and you can
explain clearly what you want.

The council thanks you for your service. Session closed.

---

## If something goes wrong

| What you see | What to do |
| --- | --- |
| "Please run az login" | Run `az login`, then repeat the step. |
| A script prints HTTP 403 | The login has no permission on the project. Check the role "Foundry User" in the Azure Portal. |
| A script prints HTTP 404 | Check `PROJECT_ENDPOINT` in `.env`. |
| The chair answers without asking anyone | Run `scripts/03_chair.py` again, then send the proposal again. |
| One delegate is missing | Send the proposal again. |
| It takes longer than a minute | Normal with many delegates. Each one is a separate call. |
| The coding agent goes in circles | Stop it. Use the finished `setup_council.py`, `server.py` and `index.html` from this folder. |
