# Lab 1.1: What Agents Are and Which Option to Pick

An agent is a model with instructions and tools in a loop. This lab defines that precisely and
compares the Azure options for building one.

**Guiding questions:**

<details>
<summary>Which Microsoft products for building AI agents can you name?</summary>

Microsoft Foundry Agent Service, Copilot Studio, Microsoft Agent Framework, the Microsoft 365
agents path, and direct model APIs.

</details>

<details>
<summary>When would you not use an agent at all?</summary>

When the steps are fixed, the question is a single one, or the job is a nightly batch. An agent
adds cost and unpredictability.

</details>

<details>
<summary>What decides which option fits?</summary>

Who builds and maintains it, how much control is needed, where it must run and be published,
governance and licensing, and how far it carries before a migration.

</details>

- An agent decides its next step; a script or workflow does not
- Five decision axes choose the Azure option
- Today's focus: Microsoft Foundry Agent Service

## What an agent is

| Part         | Role                                                            |
| ------------ | --------------------------------------------------------------- |
| Model        | decides, token by token, what to say or do next                 |
| Instructions | define role, scope, and boundaries                              |
| Tools        | functions, data sources, or other agents the model can call     |
| Loop         | answers directly, or calls a tool and continues with the result |

The agent loop:

1. Request: the user asks; the model reads instructions and request
2. Decide: answer now, or call a tool with specific arguments
3. Act: the tool runs outside the model and returns a result
4. Continue: the result goes back to the model; repeat or answer

## Script, workflow, or agent

|          | Script                       | Workflow                                  | Agent                               |
| -------- | ---------------------------- | ----------------------------------------- | ----------------------------------- |
| Decides  | developer, in code           | developer fixes the path, AI fills a step | the model picks the next step       |
| Example  | nightly CSV transformation   | summarise, classify, file                 | gather info, choose a resource, act |
| Strength | predictable, cheap, testable | readable, controlled                      | flexible                            |
| Cost     | low                          | medium                                    | highest, hardest to test            |

- An agent costs more than a single prompt: slower, less predictable, harder to test
- The instructions field is a product, not a setting (see method Step 0)

## The Microsoft agent landscape

| Layer               | What lives here                                                                     |
| ------------------- | ----------------------------------------------------------------------------------- |
| Where users meet it | Teams, Microsoft 365 Copilot, a custom app or API                                   |
| Where it is built   | Copilot Studio (low-code), Foundry Agent Service, Microsoft Agent Framework (code)  |
| Microsoft Foundry   | model catalog, tools and knowledge, tracing and evaluation, identity and governance |
| Azure               | compute, networking, storage, Microsoft Entra                                       |

- Microsoft Foundry: agents (prompt, voice, hosted), a catalog of 10,000+ models, tools and
  knowledge through a Foundry Toolbox
- Older material uses older names; check the version that is installed

| Older material says               | Current Foundry says            |
| --------------------------------- | ------------------------------- |
| Azure AI Studio, Azure AI Foundry | Microsoft Foundry               |
| Azure AI Services                 | Foundry Tools                   |
| Assistants API                    | Responses API (Agents v2)       |
| Threads, messages, runs           | Conversations, items, responses |

## Foundry Agent Service

| Capability         | Meaning                                                            |
| ------------------ | ------------------------------------------------------------------ |
| Agent runtime      | hosts and scales agents, manages conversations and tool calls      |
| Toolboxes          | curated tools shared across agents behind one governed endpoint    |
| Models             | swap models without changing agent code                            |
| Observability      | tracing, metrics, and evaluations for every decision               |
| Identity, security | Microsoft Entra identity, RBAC, content filters, network isolation |
| Publishing         | versions, stable endpoints, sharing through Teams and Copilot      |

| Object       | Meaning                                                                        |
| ------------ | ------------------------------------------------------------------------------ |
| Agent        | instructions, a model, optional tools; defined once, reused every conversation |
| Conversation | ordered messages of one exchange (older term: thread)                          |
| Response     | one execution of the agent on the conversation (older term: run)               |

| Way to build  | Meaning                                                                          |
| ------------- | -------------------------------------------------------------------------------- |
| Prompt agent  | instructions, model, tools; Foundry runs it; portal, SDK, or REST; today's focus |
| Hosted agent  | own code and framework as a container; managed endpoint and identity             |
| Responses API | agent logic lives in the own app; Foundry supplies models and tools              |

- The agent playground shows: Instructions, Tools and Knowledge, Chat/YAML/Code views,
  and Traces, Monitor, Evaluation for checking behavior

## Azure options for building an agent

| Option                | Choose it when                                             | Trade-off                      |
| --------------------- | ---------------------------------------------------------- | ------------------------------ |
| Foundry Agent Service | developers need a managed agent with portal and SDK        | less control of infrastructure |
| Agent Framework       | code-first orchestration across several agents is required | more code to own               |
| Copilot Studio        | business makers build and maintain it, low-code            | less control of internals      |
| Microsoft 365 Agents  | the agent must live where users work (Teams, Copilot)      | publishing limits              |
| Direct model API      | full control over every request is required                | everything must be built       |

Five decision axes: who builds, how much control, where it runs, governance (identity, data,
licensing, cost), and how far it carries before a migration.

- Options combine: for example a Foundry agent published into Teams
- Other clouds and open frameworks exist (Amazon Bedrock Agents, Google Vertex AI Agent
  Builder, LangGraph, OpenAI Agents SDK); Foundry hosted agents can run some of them
- Product names change often; verify before using a name in a proposal

## Key takeaways

- An agent is model plus instructions plus tools in a loop; scripts and workflows stay cheaper
  when the steps are fixed
- Five decision axes choose the option; no option wins on every axis
- Foundry Agent Service supports grounding, custom tools, MCP, and agent handoff without a
  premature migration

The exercise applies the five axes to four scenarios and to TravelDesk.
