"""Green Council backend: one small web server between the page and the CouncilChair agent.

    python server.py      then open http://127.0.0.1:8000

Needs index.html, council.json and .env in the same folder, "az login",
and the agents from setup_council.py.
"""
import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

HERE = Path(__file__).parent
AGENT_NAME = "CouncilChair"

# Read .env: one NAME=value per line.
if (HERE / ".env").exists():
    for line in (HERE / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            name, value = line.split("=", 1)
            os.environ.setdefault(name.strip(), value.strip())

PROJECT_ENDPOINT = os.environ.get("PROJECT_ENDPOINT", "")
if not PROJECT_ENDPOINT or "<" in PROJECT_ENDPOINT:
    sys.exit("Copy .env.example to .env and set PROJECT_ENDPOINT.")

COUNCIL = json.loads((HERE / "council.json").read_text(encoding="utf-8"))
# The A2A step of each delegate is named after its connection: "council-<name in lower case>".
BY_KEY = {re.sub(r"[^a-z0-9]", "", d["name"].lower()): d["name"] for d in COUNCIL["delegates"]}

project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())
openai = project.get_openai_client()


def number(text, field):
    """Find a numeric value such as  "european_aqi": 23  in the raw tool output."""
    match = re.search(field + r"\W{1,6}(\d+(?:\.\d+)?)", text)
    return float(match.group(1)) if match else None


def propose(proposal):
    response = openai.responses.create(
        input=proposal,
        extra_body={"agent_reference": {"name": AGENT_NAME, "type": "agent_reference"}},
    )
    votes, air, used_knowledge = [], None, False
    for item in response.output:
        if item.type == "file_search_call":                      # the knowledge base was searched
            used_knowledge = True
        elif item.type == "openapi_call_output":                 # the API tool answered
            raw = str(item.output)
            air = {"eaqi": number(raw, "european_aqi"), "pm2_5": number(raw, "pm2_5"), "pm10": number(raw, "pm10")}
        elif "a2a" in item.type and item.type.endswith("call_output"):   # a delegate answered over A2A
            text = item.output.strip()
            vote = re.search(r"VOTE:\s*(YES|NO)", text, re.I)
            votes.append({
                "name": BY_KEY.get(item.name.split("-")[-1], item.name),
                "vote": vote.group(1).upper() if vote else None,
                "reason": re.sub(r"VOTE:\s*(YES|NO)\s*", "", text, flags=re.I).strip(),
            })
    verdict = response.output_text.strip()
    decision = re.search(r"DECISION:\s*(ADOPTED|REJECTED)", verdict, re.I)
    explanation = re.sub(r"^(DECISION|COUNT|AIR):.*$", "", verdict, flags=re.I | re.M).strip()
    return {
        "votes": votes,
        "air": air,
        "used_knowledge": used_knowledge,
        "decision": decision.group(1).upper() if decision else None,
        "explanation": explanation,
    }


class Handler(BaseHTTPRequestHandler):
    def reply(self, status, body, content_type="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/":
            self.reply(200, (HERE / "index.html").read_bytes(), "text/html; charset=utf-8")
        elif self.path == "/api/council":
            self.reply(200, COUNCIL)
        else:
            self.reply(404, {"error": "Not found"})

    def do_POST(self):
        if self.path != "/api/propose":
            return self.reply(404, {"error": "Not found"})
        try:
            length = int(self.headers.get("Content-Length", 0))
            proposal = json.loads(self.rfile.read(min(length, 10_000))).get("proposal")
        except (ValueError, AttributeError):
            return self.reply(400, {"error": "Send JSON with a 'proposal' field."})
        if not isinstance(proposal, str) or not proposal.strip() or len(proposal) > 500:
            return self.reply(400, {"error": "The proposal must be text, 1 to 500 characters."})
        try:
            self.reply(200, propose(proposal.strip()))
        except Exception as error:  # the agent call failed: tell the page, keep the server running
            self.reply(502, {"error": f"The council could not answer: {str(error)[:300]}"})


if __name__ == "__main__":
    print("Open http://127.0.0.1:8000   (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
