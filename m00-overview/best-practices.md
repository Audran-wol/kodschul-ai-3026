# Best Practices

## Instructions and testing

| Practice                                                                | Reason                                                                 |
| ----------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Generate instructions from a defined problem and design, then test them | vague hand-written instructions are the most common reason agents fail |
| Include role, scope, rules, output format, and fallback                 | each section closes a different failure mode                           |
| Define a fallback for "not covered"                                     | otherwise the agent guesses and sounds sure                            |
| Use the same fixed test questions before and after every change         | changes become comparable                                              |
| Record answer text verbatim                                             | "worked" or "failed" hides invented details                            |

## Grounding

| Practice                                                                   | Reason                                               |
| -------------------------------------------------------------------------- | ---------------------------------------------------- |
| Ground company-specific facts in a document                                | instructions cannot supply facts the model never saw |
| Check every citation against the source                                    | a model can cite a section that does not exist       |
| Name an owner for each source document                                     | answers are only as current as the document          |
| Move to a shared knowledge platform only when several agents share sources | per-agent files are simpler for one agent            |

## Tools

| Practice                                                        | Reason                                                |
| --------------------------------------------------------------- | ----------------------------------------------------- |
| Write the docstring as the tool contract: when to call it       | the model never sees the function body                |
| Constrain parameters with types and fixed values                | fewer wrong arguments                                 |
| Test the tool function on its own first                         | a tool returning nonsense looks like an agent failure |
| Prove calls with the trace                                      | the answer text alone does not show a call            |
| Keep agent-specific logic local, share capabilities through MCP | ownership and versioning stay clear                   |
| Review MCP servers as their own trust boundary                  | a shared server changes every agent that uses it      |

## Agents and architecture

| Practice                                                                    | Reason                                                       |
| --------------------------------------------------------------------------- | ------------------------------------------------------------ |
| Start with one agent; split only for trust boundary, tools, or instructions | each extra agent costs latency, tokens, and debugging effort |
| Give each agent only the tools it owns                                      | limits what a manipulated agent can do                       |
| Pick the Azure option with the five decision axes                           | prevents choosing by product name                            |
| Check product names and SDK signatures against the installed version        | this area changes often                                      |

## Safety and operations

| Practice                                            | Reason                                  |
| --------------------------------------------------- | --------------------------------------- |
| Route every outcome that approves money to a person | automated checks are not authority      |
| Test correct use, a boundary, and a misuse          | a demo shows one path once              |
| Fail safely when model output cannot be parsed      | model output at a boundary is untrusted |
| Keep secrets in environment variables and sign-in   | no credentials in code or files         |
| Use only fictional or anonymised data in exercises  | privacy by default                      |
