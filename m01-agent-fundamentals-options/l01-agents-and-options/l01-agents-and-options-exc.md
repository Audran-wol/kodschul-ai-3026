# Lab 1.1: Exercise: Pick the Right Azure Option

**Changes the TravelDesk baseline?** No. Short exercise; TravelDesk is only chosen, not built.

## Starting point

- Four short scenarios plus Aurora Logistics' own TravelDesk case
- Goal: decide per case which Azure option fits, or whether it is an agent problem at all

| #   | Scenario                                                                                          |
| --- | ------------------------------------------------------------------------------------------------- |
| S1  | Internal FAQ bot for non-technical HR staff; the HR team wants to maintain the answers themselves |
| S2  | Nightly job that transforms a CSV export and loads it into a reporting table                      |
| S3  | Claims assistant for an insurer; a developer team maintains it and wants portal and SDK access    |
| S4  | Assistant for the sales team that must appear inside Microsoft Teams; developers are available    |
| S5  | TravelDesk: internal travel and expense assistant for Aurora Logistics (see below)                |

**TravelDesk case (S5):**

- Answers travel-policy questions from the Aurora policy document
- Later checks concrete expense claims and may need more than one agent
- Built and maintained by the Aurora developer team, on Azure with Microsoft Entra
- Users start in a web app; Teams may follow

## Tasks

1. Fill the decision grid for S1 to S4 (template below).
2. Name an Azure option for each scenario and justify it in one line, naming the decision axis
   that decided it.
3. Mark every scenario that is not an agent problem and state the reason.
4. Apply the same axes to S5 and add it as the fifth row.
5. Confirm in one sentence why Foundry Agent Service is the right choice for today.

## Decision grid template

| #   | Agent problem? (yes/no, reason) | Azure option | One-line justification (name the axis) |
| --- | ------------------------------- | ------------ | -------------------------------------- |
| S1  |                                 |              |                                        |
| S2  |                                 |              |                                        |
| S3  |                                 |              |                                        |
| S4  |                                 |              |                                        |
| S5  |                                 |              |                                        |

## Checkpoint

- All five rows are filled
- At least one row is marked "not an agent problem" with a reason
- Every justification names at least one decision axis

## Completion criteria

- A completed grid with five rows exists
- The one-sentence confirmation for Foundry Agent Service is written down

## Extension

- Add a sixth row for a use case from the own work and apply the five axes

## Fallback

- If a product name in the grid is unclear, use the option table in `l01-agents-and-options-thx.md`
