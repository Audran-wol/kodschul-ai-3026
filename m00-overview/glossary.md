# Glossary

| Term / abbreviation                  | Platform / area       | When used                                                                       | Primary users      | Occurrence             |
| ------------------------------------ | --------------------- | ------------------------------------------------------------------------------- | ------------------ | ---------------------- |
| A2A (Agent-to-Agent protocol)        | protocol              | agents owned by different teams discover and call each other                    | architects         | `m06/02`               |
| Agent                                | AI concept            | model with instructions and tools in a loop that decides the next step          | all                | Lab 1.1                |
| Agent card                           | A2A                   | describes the skills and endpoint of an agent                                   | developers         | `m06/02`               |
| Agent loop                           | AI concept            | request, decide, act, continue                                                  | developers         | Lab 1.1                |
| Agent playground                     | Microsoft Foundry     | chat with an agent, read traces and evaluations                                 | developers         | Labs 1.1, 2.1          |
| Agent version                        | Foundry Agent Service | stored state of an agent definition; every create call adds one                 | developers         | Lab 3.1                |
| Approval Agent                       | TravelDesk            | owns the expense tool and the approval decision                                 | developers         | Lab 5.1                |
| Assistants API                       | Microsoft Foundry     | older agent API with threads, messages, and runs; replaced by the Responses API | developers         | Lab 1.1                |
| Azure AI Studio / Azure AI Foundry   | Microsoft Foundry     | older product names of Microsoft Foundry; appear in older tutorials             | all                | Lab 1.1                |
| Boundary test                        | testing               | test case exactly at a rule threshold, such as EUR 180 versus 181               | developers         | Lab 6.1                |
| Checkpoint state                     | course project        | completed version of a lab result used to continue after falling behind         | all                | `project/checkpoints/` |
| Citation                             | grounding             | names the source passage of a fact so a reader can verify it                    | all                | Lab 2.2                |
| Content filter                       | Microsoft Foundry     | safety layer that screens model inputs and outputs                              | admins             | Lab 1.1                |
| Context window                       | LLM                   | how much text fits into one request                                             | developers         | primer                 |
| Conversation                         | Foundry Agent Service | ordered messages of one exchange; older term: thread                            | developers         | Labs 1.1, 2.1, 3.1     |
| Copilot Studio                       | Microsoft             | low-code agent building for business makers                                     | makers             | Lab 1.1                |
| Deep learning                        | AI concept            | many-layered neural networks                                                    | all                | primer                 |
| DefaultAzureCredential               | azure-identity        | signs the SDK in with the account from `az login`                               | developers         | Lab 3.1                |
| Direct model API                     | Azure                 | full control over every request; everything is built by hand                    | developers         | Lab 1.1                |
| Docstring                            | Python                | text of a function that tells the model when to call a tool                     | developers         | Lab 4.1                |
| Evaluation                           | Microsoft Foundry     | quality metrics on datasets and live chats                                      | developers         | Lab 6.1                |
| Few-shot examples                    | prompting             | one or two sample answers inside a prompt                                       | all                | primer                 |
| Few-shot prompting                   | prompting             | sample answers in the prompt that steer the output                              | all                | primer                 |
| File search                          | Foundry tool          | retrieves passages from attached documents for grounding                        | developers         | Labs 2.2, 3.1          |
| Foundry IQ                           | Microsoft Foundry     | shared, governed knowledge platform for several agents                          | architects         | `m02/01`               |
| Foundry Toolbox                      | Microsoft Foundry     | curated tools behind one managed MCP-compatible endpoint                        | developers         | Lab 4.2                |
| Function tool                        | Foundry tool          | own code that the model can call                                                | developers         | Lab 4.1                |
| Grounding                            | AI concept            | answering from retrieved documents instead of model memory                      | all                | Lab 2.2                |
| Guiding question                     | course method         | question that opens a lab before the explanation                                | all                | all labs               |
| Hallucination                        | LLM                   | fluent but invented content                                                     | all                | primer, Lab 2.1        |
| Handoff                              | orchestration         | one agent explicitly transfers a task to another based on content               | developers         | Lab 5.1                |
| Hosted agent                         | Microsoft Foundry     | own code and framework run as a container with managed endpoint                 | developers         | Lab 1.1                |
| Human approval                       | governance            | a person approves before anything is paid or changed                            | all                | Lab 6.1                |
| Inference                            | LLM                   | applying a trained model to a prompt                                            | all                | primer                 |
| Instructions                         | agent                 | prompt always sent first: role, rules, boundaries                               | all                | Labs 1.1, 2.1          |
| JSON Schema                          | function tools        | describes the parameters of a tool: types, required fields, fixed values        | developers         | Lab 4.1                |
| LLM (large language model)           | AI concept            | deep network trained on huge amounts of text                                    | all                | primer                 |
| Machine learning                     | AI concept            | learns patterns from data instead of hand-written rules                         | all                | primer                 |
| Magentic                             | orchestration         | open-ended pattern where a planner decides which agent acts next                | architects         | Lab 5.1                |
| MCP (Model Context Protocol)         | protocol              | tools discovered at runtime from a separately owned server                      | developers         | Lab 4.2                |
| Microsoft 365 Agents                 | Microsoft             | agents that live in Teams and Microsoft 365 Copilot                             | developers         | Lab 1.1                |
| Microsoft Agent Framework            | Microsoft             | code-first SDK for multi-agent orchestration                                    | developers         | `m05/01`               |
| Microsoft Entra                      | Azure                 | identity service used for access to Foundry                                     | admins             | Lab 1.1                |
| Microsoft Foundry                    | Azure                 | platform for models, agents, tools, tracing, and governance                     | developers         | Lab 1.1                |
| Model deployment                     | Microsoft Foundry     | the model instance an agent calls                                               | developers         | Lab 2.1                |
| Observability                        | operations            | traces, monitoring, and evaluation of agent behavior                            | developers         | Lab 6.1                |
| OpenAPI tool                         | Foundry tool          | describes an existing REST API for the agent to call                            | developers         | Lab 4.1                |
| Orchestration pattern                | multi-agent           | sequential, concurrent, group chat, handoff, Magentic                           | architects         | Lab 5.1                |
| Parameter                            | LLM                   | one learned number (weight) in a neural network                                 | all                | primer                 |
| Policy Agent                         | TravelDesk            | answers from the policy document and has no authority                           | developers         | Lab 5.1                |
| Power Fx                             | Microsoft             | expression language for logic in low-code workflows                             | makers             | `m05/02`               |
| Project                              | Microsoft Foundry     | Azure resource an agent and its model deployment belong to                      | developers         | Lab 2.1                |
| Prompt                               | prompting             | the request written each time                                                   | all                | primer                 |
| Prompt agent                         | Microsoft Foundry     | agent defined by instructions, model, and tools; Foundry runs it                | developers         | Lab 1.1                |
| RAG (retrieval-augmented generation) | AI concept            | look up passages first, then answer from them                                   | developers         | Lab 2.2                |
| RBAC (role-based access control)     | Azure                 | grants access to Azure resources by role                                        | admins             | Lab 1.1                |
| Response                             | Foundry Agent Service | one execution of the agent on a conversation; older term: run                   | developers         | Labs 1.1, 2.1          |
| Responses API                        | Microsoft Foundry     | API for agent calls; successor of the Assistants API                            | developers         | Labs 1.1, 3.1          |
| SKILL.md                             | GitHub Copilot        | file that describes a repeatable multi-step procedure                           | developers         | Lab 3.1                |
| Temperature                          | LLM setting           | low: predictable; high: more varied                                             | developers         | primer                 |
| Tier 1 / Tier 2 city                 | TravelDesk            | hotel limit class in the Aurora policy: EUR 180 versus EUR 120 per night        | all                | Labs 2.2, 4.2          |
| Token                                | LLM                   | unit of text the model reads and counts                                         | all                | primer                 |
| Tool                                 | agent                 | function, data source, or agent the model can call                              | all                | Labs 1.1, 4.1          |
| Tool call                            | agent                 | the model's request to run a tool with specific arguments                       | developers         | Lab 4.1                |
| Top-p                                | LLM setting           | limits the token choice to the most probable ones                               | developers         | primer                 |
| Trace                                | observability         | every model call and tool call of one request                                   | developers         | Labs 2.1, 4.1, 6.1     |
| TravelDesk                           | course project        | travel and expense assistant for the fictional Aurora Logistics                 | all                | all labs               |
| Trust boundary                       | security              | line between what an agent may advise and what it may decide                    | architects         | Lab 5.1                |
| Vector store                         | grounding             | searchable index of document passages used by file search                       | developers         | Lab 3.1                |
| Work IQ                              | Microsoft             | exposes workplace data to an agent                                              | architects         | `m06/01`               |
| Workflow                             | orchestration         | fixed path where AI fills individual steps                                      | makers, developers | Lab 1.1, `m05/02`      |
