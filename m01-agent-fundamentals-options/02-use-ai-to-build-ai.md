# Background: Use AI to Build AI (The Six-Step Method)

- One method, taught in order; each step is shown once and applied in a later lab
- Question answered: where do good agent instructions and the right tool list come from?
- Most agents fail because instructions were written vaguely and tools were guessed

## The six steps

| Step | Name                       | Question                                                   | Applied in              |
| ---- | -------------------------- | ---------------------------------------------------------- | ----------------------- |
| 0    | Know what you are steering | How does AI learn, and why do instructions decide quality? | Lab 2.1 (instructions)  |
| 1    | Understand the problem     | Is this even an agent problem?                             | Lab 1.1 (decision grid) |
| 2    | Design the solution        | Which tools, and does it need two agents?                  | Lab 4.1, Lab 5.1        |
| 3    | Generate the instructions  | Where do good instructions come from?                      | Lab 2.1                 |
| 4    | Scaffold the build         | How to stop re-explaining the project to the AI?           | Lab 4.1 (skill)         |
| 5    | Test and iterate           | How to know it works before a real user does?              | Lab 6.1 (test sheet)    |

## Step 0: know what you are steering

- Supervised, unsupervised, and reinforcement learning all happen before deployment
- An agent does not learn on the job
- The model predicts the most likely next text; context decides quality
- The instructions field is a product, not a setting

## Steps 1 to 3: the three-assistant chain

| Assistant                 | Input                         | Output                                                            | Prompt file                                           |
| ------------------------- | ----------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------- |
| 1 Problem-Solver          | free-form problem description | use-case canvas, scoring, top-1 recommendation                    | `../project/assistants/01-problem-solver.md`          |
| 2 Solution Architect      | problem plus chosen idea      | tools, agent split, human-approval points, handover package       | `../project/assistants/02-solution-architect.md`      |
| 3 System-Prompt Generator | problem plus handover package | finished instructions, improved against two adversarial questions | `../project/assistants/03-system-prompt-generator.md` |

- Each assistant receives the previous output as input
- The human decides at every step: which problem, which concept, which tool
- Result for TravelDesk: `../project/traveldesk-instructions.md`

## Step 4: scaffold the build

| File                      | Holds                                    | Example in this course                              |
| ------------------------- | ---------------------------------------- | --------------------------------------------------- |
| `copilot-instructions.md` | project-wide conventions, always applied | `../project/skills/copilot-instructions.example.md` |
| `SKILL.md`                | a repeatable multi-step procedure        | `../project/skills/add-agent-tool/SKILL.md`         |
| custom agent              | a specialised reviewer or builder role   | not built today                                     |

## Step 5: test and iterate

- Same adversarial move as in Step 3, applied to the finished system
- Test correct use, a boundary, and a deliberate misuse
- Any outcome that approves money routes to a human

> **Rule of thumb:** Generating and testing instructions deliberately beats hand-writing them and hoping.

Applied in Lab 2.1, Lab 4.1, and Lab 6.1.
