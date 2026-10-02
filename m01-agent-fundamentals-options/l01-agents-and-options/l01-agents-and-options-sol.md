# Lab 1.1: Solution: Pick the Right Azure Option

## Tasks

### 1. and 2. Decision grid with options and justification

| #   | Agent problem?                           | Azure option              | Justification (axis)                                                |
| --- | ---------------------------------------- | ------------------------- | ------------------------------------------------------------------- |
| S1  | Yes: repeated questions, fixed knowledge | Copilot Studio            | Who builds: business makers maintain it, low-code                   |
| S2  | No                                       | none: a scheduled script  | Fixed steps, no decisions; a script is cheaper and testable         |
| S3  | Yes: needs judgment and tools            | Foundry Agent Service     | Who builds and control: developers, managed service, portal and SDK |
| S4  | Yes                                      | Microsoft 365 Agents path | Where it runs: home is Teams, developers build it                   |
| S5  | Yes                                      | Foundry Agent Service     | Developers build, managed service, grounding and tools needed       |

### 3. Not an agent problem

- S2: the steps are fixed and nothing needs a decision; a script is predictable, cheap, and
  testable. An agent would add cost and unpredictability.

### 4. TravelDesk against the five axes

| Axis               | TravelDesk                                                           |
| ------------------ | -------------------------------------------------------------------- |
| Who builds         | Aurora developer team                                                |
| How much control   | medium: managed service with custom tools is enough                  |
| Where it runs      | web app now; publishing to Teams stays possible later                |
| Governance         | Microsoft Entra identity, RBAC, content filters in Foundry           |
| How far it carries | grounding, function tools, MCP, and agent handoff before a migration |

### 5. One-sentence confirmation

- Foundry Agent Service supports grounding, custom tools, MCP, and agent handoff without a
  premature migration to code-first orchestration.

## Valid alternatives

| Row | Alternative                      | When it is valid                                               |
| --- | -------------------------------- | -------------------------------------------------------------- |
| S1  | Foundry Agent Service            | if developers, not HR, end up maintaining the bot              |
| S4  | Foundry agent published to Teams | if the team prefers one platform and accepts publishing limits |
| S3  | Agent Framework                  | only if orchestration beyond handoff is required later         |

## Checkpoint

- Five rows are filled, S2 is marked as no agent, and every justification names an axis

## Extension

- A sixth row is valid when the justification names a decision axis and not only a product
  preference such as "it is the newest"
