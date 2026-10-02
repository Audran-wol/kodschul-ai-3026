# Prompt for your coding agent

Run `python setup_jury.py` first, so the four agents exist.

Then copy everything in the box below and give it to Claude Code, Codex or GitHub Copilot.
Start the coding agent in this `project/` folder, after `az login`.

```text
I am signed in to Azure with "az login". Build the backend for the Pitch Jury page in this folder.

Context
- index.html is a finished page. Do not change it. It sends a product idea to the backend and
  shows three juror opinions, a verdict and a score.
- .env holds PROJECT_ENDPOINT, my Microsoft Foundry project endpoint.
- My Foundry project already has an agent named "JuryLead". It asks three other agents over A2A
  (customer, engineer, investor) and then answers with a verdict that ends in "SCORE: N/10".

Build one file: server.py
- Python 3.11, using only the standard library plus azure-ai-projects, azure-identity and openai.
- Read PROJECT_ENDPOINT from .env. Stop with a clear message if it is missing.
- Authenticate with DefaultAzureCredential. No keys or passwords in the code.
- Listen on http://127.0.0.1:8000 only.
- GET /           -> serve index.html
- POST /api/judge <- {"idea": "..."}
                  -> {"jurors": [{"name": "Customer", "opinion": "..."},
                                 {"name": "Engineer", "opinion": "..."},
                                 {"name": "Investor", "opinion": "..."}],
                      "verdict": "...", "score": 7}
  Call the agent like this:
    project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())
    openai = project.get_openai_client()
    response = openai.responses.create(
        input=idea,
        extra_body={"agent_reference": {"name": "JuryLead", "type": "agent_reference"}},
    )
  How to read the response:
  - Each juror answer is one item in response.output whose type contains "a2a" and ends with
    "call_output". item.name is the connection name ("jury-customer", "jury-engineer",
    "jury-investor"); item.output is the opinion text. The juror name for the page is the part
    after "jury-", capitalised.
  - "verdict" is response.output_text.
  - "score" is the number N from "SCORE: N/10" in the verdict, or null if it is not there.
- Reject a missing, empty or longer than 1000 characters idea with status 400 and {"error": "..."}.
- If the agent call fails, return status 502 and {"error": "<short reason>"}. Never crash.

When server.py is written
1. Run it.
2. Send one test idea to /api/judge and show me the JSON answer.
3. Tell me the URL to open in the browser.
```

## Then

1. Open http://127.0.0.1:8000 in the browser.
2. Type your own idea and select **Ask the jury**. It takes about 30 seconds.
3. Compare scores with your neighbours.

## Make it yours

- Change a juror's character in `setup_jury.py` (for example, a very strict investor), run the
  script again, and send the same idea.
- Change the rules in `rubric.md`, run `setup_jury.py` again, and see how the score changes.
- Add a fourth juror: a lawyer, a designer, or your own boss.
