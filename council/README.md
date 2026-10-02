# Green Council

A council chamber in the browser. You put a proposal for the city, for example
"Ban cars from the city centre on weekends". Every delegate is an AI agent with a name, a role and
a character. They vote YES or NO, and the chair decides by the council charter.

```text
page (index.html) → backend (server.py) → CouncilChair ── knowledge base: council-charter.md
                                                       ── API tool: live air quality (OpenAPI)
                                                       ── A2A → one Delegate agent per person
```

| Building block | Where it is in this project                                              |
| -------------- | ------------------------------------------------------------------------ |
| Instructions   | Each delegate's role and character in `council.json`                     |
| Knowledge base | `council-charter.md`, uploaded and searched by the chair                 |
| Tool (API)     | `../openapi/air-quality.json`: live air quality from a public API        |
| Connection     | One A2A connection per delegate, created by `setup_council.py`           |
| A2A            | The chair calls every delegate                                           |
| Code           | `server.py` calls the chair and reads the steps of its answer            |

The page shows these blocks in the panel "Under the hood" and lights each one up as it is used.

## Run it

1. `copy council.example.json council.json` and put in your delegates (name, role, character).
2. `copy .env.example .env` and set `PROJECT_ENDPOINT` and `MODEL`.
3. `az login`
4. `python setup_council.py` — creates the chair, the delegates, the connections and the knowledge base.
5. `python server.py`
6. Open http://127.0.0.1:8000 and put a proposal. An answer takes up to a minute.

Run `setup_council.py` again after every change to `council.json` or `council-charter.md`.

## Build it yourself, step by step

[PROMPTS.md](PROMPTS.md) has one prompt per step for a coding agent. It builds the same project
from an empty folder.

## Notes

- `council.json` and `.env` stay on your machine; they are not committed.
- The air quality comes from the free Open-Meteo API. No key is needed.
