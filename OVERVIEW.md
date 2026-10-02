# Quick overview: from sign-in to a running agent

A short guide to the commands used in the seminar. Details are in [README.md](README.md).

## 1. Sign in

```text
az login
```

A sign-in window opens. Choose your lab account under "Work or school account".

Check who is signed in:

```text
az account show --query "{user:user.name, tenant:tenantId, subscription:name}" -o table
```

Only the account name:

```text
az account show --query user.name -o tsv
```

If the answer is "Please run 'az login' to setup account", the login has expired. Run `az login` again.

## 2. Wrong tenant, or "no subscription found"

Sign in to a specific tenant:

```text
az login --tenant <tenant-id>
```

The primary domain works too:

```text
az login --tenant <your-domain>.onmicrosoft.com
```

Where to find both values: Azure Portal → search "Microsoft Entra ID" → Overview → **Tenant ID** and **Primary domain**.

## 3. Install the packages (once)

```text
pip install "azure-ai-projects>=2.1.0" azure-identity openai
```

Keep the quotes. Without them the terminal reads `>` as "write to a file".

## 4. Where your settings go

After `az login` there is no other connection step: no key, no password. Each script only needs to know your project.

| What you run                      | Where the settings go                              |
| --------------------------------- | -------------------------------------------------- |
| `project/` (Pitch Jury)           | `.env` file: `PROJECT_ENDPOINT` and `MODEL`        |
| `code/a2a_lab.py`                 | top of the file: `PROJECT_ENDPOINT` and `MODEL`    |
| `code/run_agent.py`               | top of the file: `PROJECT_ENDPOINT`                |
| `code/approval_demo.py`           | top of the file: `PROJECT_ENDPOINT`                |

- `PROJECT_ENDPOINT`: Foundry portal → your project → Overview → Project endpoint
- `MODEL`: the name of a model deployment in your project (Foundry portal → Models)

Create the `.env` file for the final project:

```text
copy .env.example .env
```

macOS: `cp .env.example .env`

## 5. Run the code from "Continue in code"

The Foundry portal shows ready-made Python code for every agent.

1. Open your agent in the portal and select **Continue in code**.
2. Copy the Python code with the copy icon.
3. In VS Code, create a file, for example `call_agent.py`, and paste the code.
4. Change the question in the code to your own question.
5. Run it:

```text
python call_agent.py
```

The endpoint and the agent name are already filled in by the portal. The line
`DefaultAzureCredential()` uses your `az login`.

The portal code prints only the final answer. To see every step the agent took, for example an
A2A call, use `code/run_agent.py`.

## 6. The order of the day

| Step | What                                   | Command or place                               |
| ---- | -------------------------------------- | ---------------------------------------------- |
| 1    | Create the agent                       | Foundry → Build → Agents → Create agent        |
| 2    | Add knowledge                          | Foundry IQ → upload `knowledge/*.pdf`          |
| 3    | Add a tool                             | Tools → Add → Custom → OpenAPI → `openapi/*.json` |
| 4    | Call the agent from code               | `python code/run_agent.py`                     |
| 5    | Two agents over A2A                    | `python code/a2a_lab.py`                       |
| 6    | Final project: Pitch Jury              | `project/`: `setup_jury.py`, then `server.py`  |
