# Background: AI Primer

- Terms needed for the rest of the day
- Models do not keep learning during use; instructions and context decide answer quality

## AI, machine learning, deep learning, LLM

| Term                    | Meaning                                                                           |
| ----------------------- | --------------------------------------------------------------------------------- |
| Artificial intelligence | machines doing tasks that normally need human intelligence                        |
| Machine learning        | learns patterns from data instead of hand-written rules                           |
| Deep learning           | many-layered neural networks, a branch of machine learning                        |
| LLM                     | deep network trained on huge amounts of text; basis of Copilot and Foundry models |

## How AI learns

| Term          | Meaning                                                                        |
| ------------- | ------------------------------------------------------------------------------ |
| Training      | model reads huge data once and adjusts internal numbers; weeks, very expensive |
| Inference     | finished model is applied to a prompt on every use; nothing new is learned     |
| Learning task | a language model learns one thing: predict the most likely next token          |
| Feedback      | human feedback afterwards teaches it to be helpful and safe                    |

- Training data → training → model (parameters)
- A model is not a database of texts; it is a file of numbers that encode learned patterns
- Learning styles, all before deployment: supervised (labeled examples), unsupervised
  (structure in unlabeled data), reinforcement (reward and penalty)

## Parameters

- One parameter is one learned number (weight): how strongly one connection in the network counts
- Training sets billions of them; "70B" means 70 billion parameters
- Knowledge is spread across all of them; no single parameter holds a single fact
- Frozen after training: a prompt cannot change them, it only selects which ones are used

## Tokens

```text
Aurora Logistics reimburses taxi rides up to EUR 60.
Tokens (illustrative): Aurora | Logistics | reimburse | s | taxi | rides | up | to | EUR | 60 | .
```

- Each token becomes a vector: a list of numbers that encodes meaning
- Limits and cost are counted in tokens, not words

## Settings and limits

| Setting        | Effect                                                              |
| -------------- | ------------------------------------------------------------------- |
| Temperature    | low: predictable and repeatable; high: more varied and creative     |
| Top-p          | limits the choice to the most probable tokens that add up to p      |
| Max tokens     | caps the length of the answer                                       |
| Context window | how much text (instructions, history, answer) fits into one request |

- Low temperature: right for policy answers and tool calls
- High temperature: right for brainstorming, wrong for rules
- None of these settings changes what the model learned

## How a model answers

```text
Prompt → tokens → vectors → most likely next token → repeat → answer text
```

- Statistics, not understanding: nothing in this loop checks facts
- That is where hallucinations come from

## Why a good prompt matters

- A prompt activates the learned patterns that fit the task; it teaches nothing new
- Missing context activates the wrong patterns: fluent, generic, or invented answers
- Agent instructions are a prompt sent with every request

| Weak                    | Strong                                                                         |
| ----------------------- | ------------------------------------------------------------------------------ |
| "Can I expense a taxi?" | role, situation, format, citation requirement, and a fallback when not covered |

## Top prompting techniques

| Technique             | Meaning                                                                     |
| --------------------- | --------------------------------------------------------------------------- |
| Role                  | say who the model is and who it talks to                                    |
| Context               | give the facts it cannot know: situation, data, audience                    |
| Task and format       | state the one task and the answer shape: bullets, table, length             |
| Examples              | one or two sample answers (few-shot); examples steer better than adjectives |
| Constraints, fallback | name limits and what to do when unsure: "say not covered, never guess"      |

```text
ROLE        You are the travel-policy assistant of Aurora Logistics.
CONTEXT     The employee is on a two-day business trip.
TASK        Decide whether the airport taxi ride is reimbursable.
FORMAT      Answer in three bullet points and cite the policy section.
EXAMPLE     Q: Business class on a 2-hour domestic flight?
            A: No. Economy only under 3 hours. [Policy section 1]
CONSTRAINT  If the policy does not cover it, say "not covered". Never guess.
```

## From model to agent

| Term         | Meaning                                                                   |
| ------------ | ------------------------------------------------------------------------- |
| Model        | predicts the next token; alone: no memory, no tools, no goal              |
| Prompt       | the request written each time                                             |
| Instructions | a prompt always sent first: role, rules, boundaries                       |
| Tools        | functions, data sources, or other agents the model can call               |
| Agent        | model with instructions and tools in a loop: decide, act, observe, repeat |

> **Rule of thumb:** Better context, better instructions, better agent.

Applied in Lab 1.1 (the agent loop) and Lab 2.1 (writing and testing instructions).
