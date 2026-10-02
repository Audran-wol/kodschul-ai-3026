# Green Council — the live build, in one file

Read this file from top to bottom. It has everything: what to say, who in the room gives what,
and every prompt to paste into your coding agent (Claude Code, Codex, GitHub Copilot in Agent
mode, or ChatGPT with a terminal).

- `SAY:` words for the trainer.
- `ASK:` a question to a participant. Their answer becomes part of the project.
- `DO:` what the trainer does.
- `PROMPT:` copy the box and paste it into the coding agent.
- `EXPECT:` what you should see before you go on.

If a step fails and you have no time, the finished files are next to this one:
`setup_council.py` (steps 1 to 4) and `server.py`, `index.html` (steps 5 and 6).

---

## Who gives what

Every participant owns one piece of the system. Write the names in before you start.

| Piece                                  | Seminar topic        | Given by    |
| -------------------------------------- | -------------------- | ----------- |
| Their own delegate: role and character | Instructions         | everyone    |
| The chair's style                      | Instructions         | [VOLUNTEER-INSTRUCTIONS] |
| The rules of the council (the charter) | Knowledge base       | [VOLUNTEER-KNOWLEDGE]    |
| The city and the live data             | Tool (API)           | [VOLUNTEER-API]          |
| Three proposals to test with           | Testing              | [VOLUNTEER-TEST]         |
| Two wishes for the look of the page    | Code / UI            | [VOLUNTEER-DESIGN]       |
| Runs the prompts                       | Everything           | the trainer |

---

## Part 0 — Show the goal (3 minutes)

DO: Open the finished Green Council page. Put one proposal, for example
"Ban cars from the city centre on weekends". Let it run.

SAY: This is what we build now, together, from an empty folder. A council chamber. Every seat is
an AI agent with one of your names. You give it a proposal for the city. Every delegate votes yes
or no. The chair decides.

SAY: Look at the panel on the right. It shows the four building blocks from today. The knowledge
base: the rules of the council. A tool: live air quality from a public API. A2A: the chair asks
every delegate. And the decision.

SAY: I will not write this code by hand. You give me the content, I give prompts to a coding
agent, and it builds the system in my Azure project.

---

## Part 1 — Collect the pieces from the room (8 minutes)

SAY: Each of you owns one piece. Please write your answer in the chat.

ASK (everyone): Your delegate needs a role and a character. Write one line like this:
`Role: City engineer. Character: I only care whether it can be built and paid for.`
You can be yourself, or the opposite of yourself.

ASK ([VOLUNTEER-KNOWLEDGE]): You write the rules of our council. Give me three rules. For example:
when is a proposal adopted, what happens when the vote is a tie, and when may the chair say no
against the majority?

ASK ([VOLUNTEER-INSTRUCTIONS]): You decide how the chair behaves. Strict? Friendly? Short answers?
Give me one or two sentences.

ASK ([VOLUNTEER-API]): Our council needs live data. Which city are we? The chair will look up the
real air quality of that city, right now.

ASK ([VOLUNTEER-TEST]): Give me three proposals to test with. One that should pass, one that should
fail, and one where you are not sure.

ASK ([VOLUNTEER-DESIGN]): Two wishes for the page. Colours, mood, what must be big.

DO: Copy the chat answers into a text file so you can paste them into the prompts.

---

## Part 2 — The empty folder and the settings (3 minutes)

DO: Create an empty folder and open a terminal in it.

```text
mkdir council-live
cd council-live
```

DO: Create a file named `.env` with these two lines, with your own values.

```text
PROJECT_ENDPOINT=https://<your-resource>.services.ai.azure.com/api/projects/<your-project>
MODEL=<your-model-deployment>
```

SAY: This is the only configuration. Two lines. The project endpoint says where my Foundry
project is. The model says which model the agents use. There is no key and no password in it.

DO: Show the login.

```text
az account show --query "{user:user.name, tenant:tenantId}" -o table
```

SAY: I am signed in with az login. The coding agent will work through this login. It can do what
my account is allowed to do, and nothing more.

DO: Start the coding agent in the `council-live` folder.

---

## Part 3 — The build, prompt by prompt

### Prompt 1 — the project brief

SAY: The first prompt does not build anything. It explains the project to the agent: what we
build, how the folder is organised, and the rules. A good first prompt saves ten corrections later.

PROMPT:

```text
You are helping me build a small project called "Green Council" live in front of a class.
Read this brief, then wait for my next prompts. Do not build anything yet.

WHAT WE BUILD
A web page that shows a council chamber. A user types a proposal for a city. One AI agent per
delegate votes YES or NO over the A2A protocol. A chair agent asks all delegates, looks up live
air quality through an API tool, reads the council rules from a knowledge base, and decides.
The agents live in my Microsoft Foundry project. A small Python server connects the page to them.

THE FOLDER (everything goes in this folder, no sub-folders)
  .env                 EXISTS. I created it. PROJECT_ENDPOINT and MODEL, one NAME=value per line.
                       Read it, never print its values, never change it.
  council.json         the city and the delegates (name, role, character)        - prompt 2
  council-charter.md   the rules of the council = our knowledge base              - prompt 3
  air-quality.json     OpenAPI definition of the live-data tool                   - prompt 4
  setup_council.py     creates all agents and connections in Foundry              - prompt 5
  server.py            the backend for the page                                   - prompt 6
  index.html           the page                                                   - prompt 7

RULES
- I am signed in with "az login". Authenticate with DefaultAzureCredential (azure-identity).
  Never ask for keys or passwords and never put secrets in a file.
- Python 3.11. Use the standard library plus azure-identity, azure-ai-projects and openai.
  Install a missing package with pip.
- Read .env by hand: one NAME=value per line. Do not add python-dotenv.
- Every script prints one short "OK ..." line per step. On an error it prints the HTTP status
  and the response body and stops.
- Ask before you delete anything. Tell me each command before you run it.

FIRST TASK
Run "az account show" and tell me which account and tenant I am signed in to. Then list the
files in this folder and confirm that .env has both values (do not print them).
```

EXPECT: The agent names your account and says `.env` has both values.

SAY: Look, it checked who I am with az account show. No key was given.

### Prompt 2 — the delegates (instructions)

SAY: Now your delegates. These lines are their instructions. This is the first building block.

PROMPT (paste the chat lines of the participants where it says so):

```text
Create council.json with this shape:
{ "city": "<city>", "delegates": [ { "name": "...", "role": "...", "character": "..." } ] }

The city is: <CITY FROM THE PARTICIPANT>

The delegates, one per line (name: role and character):
<PASTE THE PARTICIPANTS' LINES HERE>

Keep each person's own words for the character. Fix only spelling. Show me the file.
```

EXPECT: `council.json` with one entry per person.

### Prompt 3 — the knowledge base

SAY: The second building block is knowledge. [VOLUNTEER-KNOWLEDGE] gave us the rules. They go
into a document. Later the chair searches this document before every decision.

PROMPT:

```text
Create council-charter.md: the charter of our Green Council. It is the knowledge base the chair
searches before every decision. Write it as short, numbered rules in plain English.

These rules come from the class and must be in it, in their meaning:
<PASTE THE THREE RULES HERE>

Also include these fixed parts:
- Every delegate votes YES or NO and gives a reason.
- Clean air rule: the chair looks up the live European Air Quality Index (EAQI) of the city.
  0 to 20 is good, 20 to 40 is fair, 40 to 60 is moderate, above 60 is poor. If the air is poor
  and the proposal would reduce pollution, a tie counts as ADOPTED.
- If a proposal is illegal or harmful, it is REJECTED without a vote.
- The answer of the chair: first line "DECISION: ADOPTED or REJECTED", second line
  "COUNT: x YES, y NO", third line "AIR: the EAQI number and one word", then two sentences that
  explain the decision and name the delegates whose reasons mattered most.

If two rules contradict each other, tell me instead of choosing silently. Show me the file.
```

EXPECT: `council-charter.md` with the class rules in it.

SAY: Notice the last line of the prompt. If two rules contradict each other, the agent must tell
us. We do not want it to decide that alone.

### Prompt 4 — the tool (an API)

SAY: The third building block is a tool. The chair needs live data that is in no document:
the air quality right now. For that we describe a public API in an OpenAPI file.

PROMPT:

```text
Create air-quality.json: an OpenAPI 3.0.1 definition named "AirQuality" for the free Open-Meteo
air quality API. No authentication.

- Server: https://air-quality-api.open-meteo.com
- One operation: GET /v1/air-quality, operationId getAirQuality
- Query parameters, all required:
    latitude  (number)  description: "Latitude of the city, for example 48.78 for Stuttgart."
    longitude (number)  description: "Longitude of the city, for example 9.18 for Stuttgart."
    current   (string)  description: "Always send exactly this text: european_aqi,pm2_5,pm10"
- Response 200: an object "current" with time, european_aqi, pm2_5 and pm10.

Then test the API itself with one request for the city in council.json and show me the numbers.
```

EXPECT: The file, and real numbers for your city.

SAY: The agent called the API to check it. This number is the air quality in our city right now.
The descriptions in this file are written for the agent. It reads them to know how to call the tool.

### Prompt 5 — the agents, the connections and A2A

SAY: Now the big step. We create the agents in Foundry: one per delegate, and the chair. And we
connect them over A2A. This is the part that took me hours the first time. Today it is one prompt,
because the prompt contains what I learned.

PROMPT:

```text
Create setup_council.py and run it. It reads .env and council.json and does four things in my
Microsoft Foundry project. Use DefaultAzureCredential. Tokens: scope https://ai.azure.com/.default
for the project endpoint, scope https://management.azure.com/.default for management.azure.com.

1. KNOWLEDGE. Upload council-charter.md into a vector store:
     from azure.ai.projects import AIProjectClient
     openai = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential).get_openai_client()
     store = openai.vector_stores.create(name="council-charter")
     openai.vector_stores.files.upload_and_poll(vector_store_id=store.id, file=<open file>)

2. DELEGATES. For every delegate create a prompt agent named "Delegate" + the name (letters and
   digits only, first letter upper case):
     POST {PROJECT_ENDPOINT}/agents/{agent}/versions?api-version=v1
     {"definition": {"kind": "prompt", "model": MODEL, "instructions": "..."}}
   Instructions:
     You are {name}, a delegate in the Green Council of {city}.
     Your role: {role}. {character}
     The chair sends you a proposal for the city. Judge it strictly from your role.
     Take a clear side; do not sit on the fence. Answer in exactly this format:
     VOTE: YES or NO
     Then one or two short sentences with your reason, in your own voice.

3. A2A. For every delegate agent:
   a) enable incoming A2A:
        PATCH {PROJECT_ENDPOINT}/agents/{agent}?api-version=v1
        {"agent_card": {"description": "<name>, <role> in the Green Council. Votes yes or no on a proposal.",
                        "version": "1.0",
                        "skills": [{"id": "vote", "name": "Vote", "description": "Votes yes or no on a proposal."}]},
         "agent_endpoint": {"protocol_configuration": {"responses": {}, "a2a": {}}}}
   b) create a connection named "council-" + the name in lower case (letters and digits only):
        PUT https://management.azure.com{PROJECT_RESOURCE_ID}/connections/{connection}?api-version=2025-04-01-preview
        {"properties": {"authType": "UserEntraToken", "category": "RemoteA2A",
                        "target": "{PROJECT_ENDPOINT}/agents/{agent}/endpoint/protocols/a2a",
                        "audience": "https://ai.azure.com", "Credentials": {}, "metadata": {}}}
   Find PROJECT_RESOURCE_ID yourself: the account name is the first part of the host name of
   PROJECT_ENDPOINT, the project name is its last path segment. List my subscriptions
   (GET https://management.azure.com/subscriptions?api-version=2022-12-01) and in each one search
   GET {subscription id}/resources?$filter=resourceType eq 'Microsoft.CognitiveServices/accounts' and name eq '<account>'&api-version=2021-04-01
   The project resource ID is "<account resource id>/projects/<project name>".

4. THE CHAIR. Create a prompt agent named "CouncilChair" (same POST as in 2) with these tools:
     {"type": "file_search", "vector_store_ids": [store.id]}
     {"type": "openapi", "openapi": {"name": "AirQuality",
        "description": "Live air quality (European Air Quality Index) for a city.",
        "spec": <content of air-quality.json>, "auth": {"type": "anonymous"}}}
     one per delegate: {"type": "a2a", "a2a_version": "1.0", "project_connection_id": <connection resource id>}
   Instructions of the chair:
     You are the chair of the Green Council of {city}. A user sends a proposal for the city.
     <THE CHAIR'S STYLE FROM THE PARTICIPANT>
     1. Get the live air quality of {city} with the AirQuality tool.
     2. Ask EVERY delegate for a vote: {the delegate names}. Send each of them the full proposal.
        Never skip a delegate and never vote for a delegate yourself.
     3. Look up the council charter in your knowledge file and decide by its rules.
     4. Answer in exactly the format that the charter defines.

Then test once and print every step:
  response = openai.responses.create(input="<FIRST TEST PROPOSAL>",
      extra_body={"agent_reference": {"name": "CouncilChair", "type": "agent_reference"}})
  Print item.type for each item in response.output, then response.output_text.
```

EXPECT: One `OK` line per agent and connection. Then the test: a list of steps with
`file_search_call`, `openapi_call`, several `a2a` steps, and a text that starts with `DECISION:`.

DO: Open the Foundry portal → Agents. Show the new agents. Open one delegate and show its
instructions: the participant's own words.

SAY: Here they are in my project. This is [a participant]'s delegate, and these are the words
they wrote in the chat. And look at the test output. First the knowledge search. Then the API
call. Then one A2A call per delegate. That is the whole day in one answer.

### Prompt 6 — the backend

SAY: The agents work. Now we need code between a web page and the chair. The page cannot talk to
Foundry directly, because the login is on my machine, not in the browser.

PROMPT:

```text
Create server.py with the Python standard library (http.server) plus azure-ai-projects and
azure-identity. It listens on http://127.0.0.1:8000 only.

- GET /             -> serve index.html from this folder
- GET /api/council  -> the content of council.json
- POST /api/propose <- {"proposal": "..."}
                    -> {"votes": [{"name": "...", "vote": "YES" or "NO" or null, "reason": "..."}],
                        "air": {"eaqi": 23, "pm2_5": 5.5, "pm10": 7.5} or null,
                        "used_knowledge": true or false,
                        "decision": "ADOPTED" or "REJECTED" or null,
                        "explanation": "..."}
  Call the agent "CouncilChair" as in the test of setup_council.py and read response.output:
  - item.type == "file_search_call"   -> used_knowledge is true
  - item.type == "openapi_call_output" -> air: find the numbers european_aqi, pm2_5 and pm10 in
    the text of item.output (skip the units block, take the numeric values)
  - type contains "a2a" and ends with "call_output" -> one vote. item.name is the connection name
    "council-<name>": map it back to the delegate's name from council.json. item.output is the
    delegate's text: vote is YES or NO from the line "VOTE: ...", reason is the rest.
  - decision: ADOPTED or REJECTED from the line "DECISION: ..." in response.output_text
  - explanation: response.output_text without the lines that start with DECISION, COUNT or AIR
- Reject a missing, empty or longer than 500 characters proposal with status 400 and {"error": "..."}.
- If the agent call fails, answer with status 502 and {"error": "<short reason>"}. Never crash.

Start it and test POST /api/propose with one proposal. Show me the JSON. Leave the server running.
```

EXPECT: JSON with one vote per delegate, the air numbers, and a decision.

### Prompt 7 — the page

SAY: Last piece: the page. [VOLUNTEER-DESIGN] gave us two wishes for the design.

PROMPT:

```text
Create index.html: one file, no libraries, no external fonts or images. It is the page for the
Green Council and talks only to GET /api/council and POST /api/propose on the same server.

Layout
- A header with the title "Green Council of <city>".
- A box to type a proposal, a button "Open the vote", and five example proposals as chips.
- The chamber: the delegates sit on a half circle, each as a coloured round avatar with the
  first letter of the name, the name and the role under it, and a small vote badge. The chair sits
  in the middle at the bottom. The decision appears large in the centre.
- A panel "Under the hood" with four steps that light up one after the other: KB (knowledge base:
  the charter was searched), API (the live air quality, with the number and a small scale from
  good to poor), A2A (how many delegates answered), and the decision.
- "The debate": one card per delegate with the name, role, vote and reason.

Behaviour
- While waiting: every avatar shows a spinning ring and the four steps blink.
- When the answer arrives, reveal it as a show: knowledge step, then the air quality, then the
  delegates one by one (about 0.7 seconds apart: the avatar glows green for YES or red for NO and
  the speech card appears), then the decision pops in with the count "x YES · y NO" and the
  explanation.
- A delegate that is missing in the answer shows "not asked".
- Errors from the backend are shown as a red line under the form.

Design wishes from the class: <PASTE THE TWO WISHES HERE>
Make it look like a real product: dark background, soft glow, generous spacing.

Rules: put agent text on the page with textContent, never innerHTML. Respect
prefers-reduced-motion. It must also work on a narrow screen.
When done, tell me to reload http://127.0.0.1:8000.
```

EXPECT: The chamber in the browser with your names.

IF NEEDED: If the generated page is broken, copy the finished `index.html` from this repo folder
into `council-live` and reload.

---

## Part 4 — Play (10 minutes)

DO: Open http://127.0.0.1:8000. Put the first test proposal.

SAY: The chair is now asking every delegate. That takes about half a minute. Watch the panel on
the right.

SAY: [name], your delegate voted no. Would you have voted no?

ASK (everyone): Does your delegate think like you? If not, give me a better sentence.

PROMPT (change one delegate):

```text
In council.json change the character of "<name>" to: "<their new sentence>".
Run setup_council.py again, then send the same proposal to /api/propose and tell me how
<name> voted before and now.
```

PROMPT (change the knowledge base):

```text
Add this rule to council-charter.md: "<a new rule from the class>".
Run setup_council.py again so the chair gets the new knowledge, send the same proposal again,
and tell me whether the decision changed and why.
```

SAY: We changed one sentence in a document, and the decision changed. No code was touched.
That is what a knowledge base is for.

---

## Part 5 — Share it with the room (optional, 5 minutes)

SAY: Right now the page only runs on my machine. Let us give it a public address so you can use
it from your own browser.

DO: Install the tunnel tool once, then start it in a second terminal.

```text
winget install Cloudflare.cloudflared
```

```text
cloudflared tunnel --url http://127.0.0.1:8000
```

DO: Copy the `https://....trycloudflare.com` address from the output into the meeting chat.

SAY: Open this link and put your own proposal. Your request goes to my machine, my server calls
my agents with my login, and the answer comes back to you.

SAY: This is a quick way to share a demo. It is not a production deployment. While the tunnel
runs, anyone with the link uses my agents and my Azure budget. So I stop it when we are done.

DO: Stop the tunnel with Ctrl+C at the end.

SAY: For a real deployment you would put server.py in a container on Azure, for example Azure
Container Apps, give that app its own managed identity, and give that identity permission to call
the chair agent. The code stays the same, because DefaultAzureCredential then uses the app's
identity instead of my login.

---

## Closing words

SAY: Look at what each of you built. Your delegate is your instructions. The charter is the
knowledge base. The air quality is a tool. The votes travel over A2A. The page is code. Nothing
here is new: it is everything from today, put together in one system.
