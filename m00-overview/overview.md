# Develop AI Agents on Azure: Course Overview

## Course goal

- Build, ground, code, tool-enable, and connect an AI agent in Microsoft Foundry, and test it
  before a real user does
- Completion result: a running TravelDesk agent for the fictional Aurora Logistics, split across
  two agents, with a completed test sheet and a personal transfer note
- Training ID AI-3026, 1 day, delivered in English

## Audience and prerequisites

- Role: AI engineers
- Familiarity with fundamental AI concepts and Azure services (AI-900 level)
- Ability to read and modify small Python scripts
- Per participant: Microsoft Foundry project with a deployed chat model, VS Code with the
  Microsoft Foundry extension, Python 3.11 or newer, network access to the Azure portal and
  the Foundry endpoint

## Agenda

| Time        | Block                                                             |
| ----------- | ----------------------------------------------------------------- |
| 09:00-09:20 | Kickoff: introductions, goals, scope, the method                  |
| 09:20-09:30 | Environment preflight                                             |
| 09:30-10:30 | Module 1: Fundamentals and options (Lab 1.1)                      |
| 10:30-10:45 | Break                                                             |
| 10:45-12:15 | Module 2: First agent and grounding (Labs 2.1, 2.2)               |
| 12:15-13:15 | Lunch                                                             |
| 13:15-14:45 | Module 3: Agents in code (Lab 3.1), Module 4: Lab 4.1             |
| 14:45-15:00 | Break                                                             |
| 15:00-16:15 | Module 4: MCP (Lab 4.2), Module 5: Multi-agent (Lab 5.1)          |
| 16:15-16:30 | Break                                                             |
| 16:30-17:00 | Module 6: Test and guard (Lab 6.1), next steps (Lab 6.2), closing |

## Modules and labs

| Module                           | Labs                                                            | Checkpoint: TravelDesk can                                |
| -------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------- |
| `m01-agent-fundamentals-options` | 1.1 Agents and options                                          | not built yet; Foundry Agent Service chosen with a reason |
| `m02-first-agent-grounding`      | 2.1 First Foundry agent, 2.2 Grounding and citations            | answer policy questions with traceable citations          |
| `m03-agent-sdk-vscode`           | 3.1 Agent in VS Code and the Python SDK                         | run from code with the same grounded answer               |
| `m04-function-tools-mcp`         | 4.1 Custom function tools, 4.2 MCP tools                        | validate a claim and reach an MCP tool                    |
| `m05-multi-agent-orchestration`  | 5.1 Connected agents and orchestration                          | separate policy advice from approval decisions            |
| `m06-evaluation-integration`     | 6.1 Test, guard, human approval, 6.2 Integration and next steps | survive a misuse test; transfer plan written              |

- Six modules instead of the Kodschul default of three: a compacted one-day course
- Each lab consists of theory (`-thx`), exercise (`-exc`), and solution (`-sol`)
- Background files at the module root cover topics that are explained, not practised

## Continuous project: TravelDesk

- Internal travel and expense assistant for the fictional company Aurora Logistics
- Needs every course topic: documents (grounding), rules (function tool), external data (MCP),
  a trust boundary (policy advice versus approval), and money (human approval, misuse testing)
- Assets: `project/README.md`

## The method: use AI to build AI

| Step | Name                       | Applied in    |
| ---- | -------------------------- | ------------- |
| 0    | Know what you are steering | Lab 2.1       |
| 1    | Understand the problem     | Lab 1.1       |
| 2    | Design the solution        | Labs 4.1, 5.1 |
| 3    | Generate the instructions  | Lab 2.1       |
| 4    | Scaffold the build         | Lab 4.1       |
| 5    | Test and iterate           | Lab 6.1       |

- Each step is demonstrated once, immediately before the matching hands-on step
- Full method with prompts: `m01-agent-fundamentals-options/02-use-ai-to-build-ai.md`

## Coverage of the Microsoft learning path

| Microsoft module                                  | Treatment                                   | Where              |
| ------------------------------------------------- | ------------------------------------------- | ------------------ |
| Develop AI agents with Foundry and VS Code        | hands-on                                    | Labs 1.1, 2.1, 3.1 |
| Integrate custom tools into your agent            | hands-on                                    | Lab 4.1            |
| Integrate MCP tools with Azure AI agents          | hands-on                                    | Lab 4.2            |
| Build knowledge-enhanced agents with Foundry IQ   | file grounding hands-on, background segment | Lab 2.2, `m02/01`  |
| Multi-agent solution, connected agents            | hands-on handoff                            | Lab 5.1            |
| Microsoft Agent Framework (build and orchestrate) | options comparison, background segment      | Lab 1.1, `m05/01`  |
| Agent-driven workflows                            | background segment                          | `m05/02`           |
| Integrate your agent with Microsoft 365           | options comparison, background segment      | Lab 1.1, `m06/01`  |
| Discover Azure AI agents with A2A                 | background segment                          | `m06/02`           |

## Working method

- Short theory, then immediate application
- Every lab opens with three guiding questions
- Every exercise has one baseline outcome; extensions are optional and never required later
- Pair work is allowed in every lab
- Each lab that changes TravelDesk has a checkpoint state, so the next lab can start from it

## Environment and safety

- All company, policy, and employee data is fictional; no real data is entered anywhere
- No secrets in code; endpoints and keys come from `.env` and sign-in
- Every outcome that approves money needs a person; agents only validate
- Product names, portal menus, and SDK signatures change often; labs state when a detail is
  version-sensitive

## Participant introduction

Name and current role. Professional background and what is done today. Route into the field.
Organization and time with it. City or region and the local weather (optional). Previous
experience with AI agents or Azure. Expectations for the day. A project or use case to apply
today's learning to. Personal prompts may be skipped.

## Level check

| Question                                             | Typical answer                                                                    |
| ---------------------------------------------------- | --------------------------------------------------------------------------------- |
| What is an AI agent, in your own words?              | a model with instructions and tools in a loop that decides the next step          |
| Which AI tools have you used for work, and for what? | no single right answer; calibrates how much of the primer is needed               |
| Where do AI agents usually go wrong?                 | vague instructions, invented facts, uncalled tools, no testing, no human approval |
