# AI-3026 — Develop AI Agents on Azure: seminar files

The files used in the live demos and labs of the seminar. The example company is Kodschul, a training provider.

New here? Start with the short command guide: [OVERVIEW.md](OVERVIEW.md)

## Folders

| Folder       | File                                  | What it is                                                     | Slide section      |
| ------------ | ------------------------------------- | -------------------------------------------------------------- | ------------------ |
| `agent/`     | `kodschul-assistant.md`               | Instructions and test questions for `KodschulAssistant`        | 01 Agent           |
| `knowledge/` | `kodschul_agent_knowledge_source.pdf` | Knowledge file: facts the agent searches (upload to Foundry IQ) | 02 Knowledge       |
| `skills/`    | `support-reply/SKILL.md`              | Skill file: steps for one task (attach to a toolbox, preview)  | Knowledge vs skill |
| `openapi/`   | `course-availability.json`            | OpenAPI definition of the tool `CourseAvailability` for KodschulAssistant | 03 Tools |
| `openapi/`   | `exchange-rate.json`                  | OpenAPI definition of a public exchange-rate API (Frankfurter) | 03 Tools           |
| `openapi/`   | `todo-lookup.json`                    | OpenAPI definition of a second demo tool, `TodoLookup`         | 04 MCP             |
| `api/`       | `courses/<code>/availability.json`    | Sample data served as a small demo API                         | 03 Tools           |
| `code/`      | `run_agent.py`                        | Call an existing agent from Python and print every step        | 05 Code            |
| `code/`      | `approval_demo.py`                    | Human approval of an MCP tool call in your own code            | 05 Code            |
| `code/`      | `a2a_lab.py`                          | Build two agents that talk over A2A, then test them            | 06 Multi-Agent     |
| `project/`   | Pitch Jury                            | Final project: three AI jurors judge your idea in the browser  | 07 Project         |

## Setup (once per machine)

1. Install Python 3.11 or newer: `winget install Python.Python.3.12`
2. Install the Azure CLI: `winget install Microsoft.AzureCLI`
3. Sign in: `az login`
4. Install the packages: `pip install azure-ai-projects azure-identity openai`

macOS: `brew install python azure-cli`

### Sign in

- `az login` opens a sign-in window. Choose your lab account under "Work or school account".
- Wrong tenant, or "no subscription found": `az login --tenant <tenant-id>`
- Where the tenant ID is: Azure Portal → Microsoft Entra ID → Overview → Tenant ID
- When you are already signed in: `az account show --query tenantId -o tsv`

### Project endpoint

Each script has `PROJECT_ENDPOINT` at the top. Find your value in the Foundry portal:
your project → Overview → Project endpoint.

## Use a coding agent (Claude Code, Codex, GitHub Copilot)

After `az login`, a coding agent that runs in your terminal can work with your Foundry project
through the same login.

1. Sign in once: `az login`
2. Start the coding agent in this folder
3. Tell it what you want, for example:

```text
I am signed in with az login.
My Foundry project endpoint is <your endpoint>.
Run code/a2a_lab.py and explain each step to me.
```

Why this is better than giving the agent a key:

- No API keys in the chat or in the code
- The agent works as you: it can do what you are allowed to do, and nothing more
- Changes in Azure are logged under your name
- `az logout` ends its access

The agent changes real resources. Read each command before you approve it.

## Give KodschulAssistant a tool

The tool `CourseAvailability` tells the agent how many seats are left in a course.

1. Foundry → Build → Agents → `KodschulAssistant`
2. Tools → Add → Custom → OpenAPI
3. Name: `CourseAvailability`
4. Authentication: Anonymous (a public demo API)
5. Paste the content of `openapi/course-availability.json`
6. Save and ask: `How many seats are left for AI-3026?`

Expected answer: there are 4 seats left for AI-3026 on 10 October.

The demo API has three courses: `AI-3026` (4 seats), `AI-900` (fully booked) and `AZ-104` (9 seats).
An unknown course code returns 404.

## Knowledge file or skill?

| File           | Contains                            | The agent uses it to answer | Example                         |
| -------------- | ----------------------------------- | --------------------------- | ------------------------------- |
| Knowledge file | Facts: services, policies, manuals  | "What is true?"             | `knowledge/*.pdf`               |
| Skill          | Steps for one task (`SKILL.md`)     | "How do we do this?"        | `skills/support-reply/SKILL.md` |

Skills in Microsoft Foundry are in preview.

## A2A lab

1. Open `code/a2a_lab.py` and set `PROJECT_ENDPOINT` and `MODEL` at the top.
   `MODEL` is the name of a model deployment in your project.
2. Run it:

```text
cd code
python a2a_lab.py
```

### The test case

- `FrontDeskAgent` talks to the user. It has no project facts. It has one tool: A2A to the specialist.
- `ProjectSpecialist` is the only agent that knows the project facts, for example
  "Project Alpha: deployed to staging on Monday".
- The question: "What is the deployment status of Project Alpha?"
- A correct answer can only come from the specialist. That is the proof that A2A worked.

### Expected output

```text
OK   1. create the specialist agent
OK   2. enable incoming A2A on the specialist
OK   3. create the A2A connection
OK   4. create the front desk agent with the A2A tool

QUESTION to FrontDeskAgent: What is the deployment status of Project Alpha?
STEP: a2a_preview_call: ...
STEP: a2a_preview_call_output: Project Alpha was deployed to staging on Monday. ...

ANSWER: Project Alpha was deployed to staging on Monday. ...
```

| Step | What it creates                                                        |
| ---- | ---------------------------------------------------------------------- |
| 1    | The specialist agent with the project facts                            |
| 2    | The agent card and the A2A endpoint of the specialist                  |
| 3    | The connection: where the specialist lives and which identity calls it |
| 4    | The front desk agent with the A2A tool                                 |

### If something goes wrong

- A step fails: the script prints the step name and the error.
- No `a2a_preview_call` line: the front desk agent answered alone. Check its instructions.
- The model does not support A2A: try another model deployment in the `MODEL` line.

## Call an agent from Python

Set `PROJECT_ENDPOINT` at the top of `code/run_agent.py`, then:

```text
cd code
python run_agent.py
python run_agent.py "What is the status of Project Beta?"
python run_agent.py "Hello" ProjectSpecialist
```

## Human approval in your own code

`code/approval_demo.py` works with any agent that has an MCP tool requiring approval.

```text
python approval_demo.py "your question" AgentName
```

The script shows the tool and its arguments, asks `Approve? [y/n]`, and sends your decision back to the agent.

## Final project: Pitch Jury

You type an idea for a product. Three AI jurors judge it, and the jury lead gives a score out of 10.

```text
your idea (index.html)  →  backend (server.py)  →  JuryLead  →  A2A  →  JurorCustomer
                                                    (rubric.md)        →  JurorEngineer
                                                                       →  JurorInvestor
```

| File in `project/` | What it is                                                          |
| ------------------ | ------------------------------------------------------------------- |
| `index.html`       | The finished web page                                               |
| `rubric.md`        | Knowledge file: the rules the jury lead uses to score               |
| `setup_jury.py`    | Creates the four agents and connects them over A2A                  |
| `PROMPT.md`        | The prompt for your coding agent: it writes the backend `server.py` |
| `.env.example`     | Template for your settings                                          |

Steps:

1. Go to the `project/` folder.
2. Create your settings file: `copy .env.example .env` (macOS: `cp .env.example .env`).
   Open `.env` and set `PROJECT_ENDPOINT` and `MODEL`.
3. Create the agents: `python setup_jury.py`
4. Start your coding agent in this folder and give it the prompt from `PROMPT.md`.
5. Run the backend: `python server.py`
6. Open http://127.0.0.1:8000, type an idea and select **Ask the jury**. It takes about 30 seconds.

What it uses from the seminar:

| Topic        | Where                                                        |
| ------------ | ------------------------------------------------------------ |
| Instructions | Each juror has its own character                             |
| Knowledge    | `rubric.md` is uploaded and searched by the jury lead        |
| A2A          | The jury lead calls the three jurors                         |
| Code         | The backend calls the jury lead and reads the A2A steps      |

The `.env` file stays on your machine and is never committed (it is in `.gitignore`).
There is no password in it: the scripts use your `az login`.
