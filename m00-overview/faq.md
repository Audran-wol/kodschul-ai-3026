# FAQ

## Course scope

**Is every Microsoft module of the learning path practised?**

- No. Five topics are hands-on; Foundry IQ at scale, Agent Framework, workflows, publishing,
  and A2A are explained in short background files
- The coverage table is in `overview.md`

**Why does the course use Python only?**

- One SDK track fits into one day
- C# is not taught in the labs

**Do the labs need GitHub Copilot?**

- No. Copilot is used only in trainer demos; the generated skill is handed out

## Concepts

**Does the model learn from my chats?**

- No. Training is finished; during use the model only applies what it learned

**What is the difference between a prompt and instructions?**

- A prompt is written each time; instructions are a prompt that is always sent first

**When is an agent the wrong choice?**

- When the steps are fixed, the question is single, or the job is a nightly batch
- A script or workflow is cheaper, faster, and easier to test

**Why does the agent invent a policy number?**

- The model never saw the document; better wording cannot add facts
- Attach the document and check citations

**Does a citation prove an answer is right?**

- Only if it traces to a real passage that contains the stated fact

## Tools and orchestration

**How does the model know when to call a tool?**

- From the tool's name, parameters, and docstring

**Why not put all tools into one agent?**

- Too many tools make the model pick the wrong one, and one prompt cannot both advise freely
  and decide strictly

**What is the difference between a local function and an MCP tool?**

- A local function ships with the agent; an MCP tool lives on a separately owned server and can
  change without an agent release

**Are connected agents available in Foundry?**

- The available agent-to-agent options depend on the service generation; the course implements
  the handoff in code so it works either way

## Safety

**Can the agent approve expense claims?**

- It validates against rules; a person approves and pays

**What if someone claims to be the CEO?**

- Rules do not depend on seniority; the test sheet in Lab 6.1 covers exactly this case

## After the course

**What is the smallest version for a first pilot?**

- One grounded agent, one or two tested tools, and a clear human-approval boundary

**Which risks decide whether a pilot may start?**

- Quota and cost, governance and access, and who owns the source documents
