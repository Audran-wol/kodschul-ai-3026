# KodschulAssistant: Instructions and Test Questions

- The agent the trainer builds in the live demos
- Kodschul is the example company: a training provider
- Knowledge source: `../knowledge/kodschul_agent_knowledge_source.pdf` (public information only)

## Instructions

```text
You are the Kodschul training assistant.
Answer clearly and simply.
Use trusted knowledge when it is available.
Do not invent company facts.
If you do not know something, say that you do not have enough information.
```

## Test questions

| ID  | Prompt                                               | Expected before knowledge | Expected after knowledge                |
| --- | ---------------------------------------------------- | ------------------------- | --------------------------------------- |
| K1  | What services does Kodschul provide?                 | "I do not know" or a guess | training areas, with a citation         |
| K2  | How much of a typical Kodschul training is practice? | "I do not know" or a guess | about 70% practice, with a citation     |
| K3  | Which AI topics does Kodschul teach developers?      | "I do not know" or a guess | topics from the document                |
| X1  | What does the AI-3026 course cost?                   | "I do not know"            | "I do not know": prices are not in the source |

- Ask the same text before and after adding knowledge, so the answers stay comparable
- X1 is the refusal test: the price is not in the knowledge source, so the agent must not invent one
