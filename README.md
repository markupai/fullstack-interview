# Markup AI Fullstack Interview

A take-home project for full-stack candidates, and the scaffold to build it
on: a Chrome extension, a FastAPI server, and a Temporal worker. The first
half of this file is the brief. The second half is how the repo works.

## The project

Thanks for taking the time to do this. Please don't spend more than 2 hours
on it. It is fine to not finish everything; we would rather see a smaller
piece that works and that you can explain than a larger one that doesn't. In
the interview you will demo it and we will build on it together.

### What to build

Wire up this flow end to end:

1. The user highlights some text on a webpage.
2. The user clicks a button in the extension's side panel.
3. The extension sends the highlighted text to the API. The API starts a
   Temporal workflow to handle it.
4. The workflow calls the model endpoint described below and gets back a
   rewrite of the text and a color.
5. The result makes its way back to the extension, which changes the page as
   described in the next section.

Test against
[Say Goodbye to Robot Prose With Content Integrity Agents](https://markup.ai/blog/content-integrity-guardian-agents/).
We will use the same page in the interview.

How the result gets from the workflow back to the extension is up to you.
The existing `hello` module shows one way to read a workflow's result from
the API.

That flow is the core, and it has to work as described. Beyond that, take
the project wherever you want. Just keep the core intact.

### What happens to the text

Your workflow takes the highlighted text and produces two things from it,
using the model endpoint below:

- A rewrite of the text. What kind of rewrite is up to you. Something fun is
  encouraged: Shakespeare, pirate, haiku, or whatever you like.
- A color for it: `red`, `green`, `blue` or `yellow`. How the color is
  chosen is also up to you. It could reflect tone, length, the model's mood,
  or anything else you can explain.

When the result arrives, the extension replaces the highlighted text on the
page with the rewrite, in the same place, and shows the rewritten text in
the returned color. Nothing else on the page changes.

Only the selected text is sent and only the selected text is replaced.

### The model endpoint

We host a thin proxy in front of a language model. It authenticates with an
API key.

```
POST https://api.markup.ai/interview/prompts
Authorization: Bearer <MODEL_API_KEY>
Content-Type: application/json

{ "prompt": "your prompt, including the highlighted text" }
```

```
200 OK
{ "content": "<the model's reply, as a string>" }
```

The endpoint can be slow and it can fail. Treat it like any third-party API.

### Getting started

The second half of this file covers setup and how to run each piece. The
repo already has a working end-to-end `hello` example that goes
extension-less from API to workflow to activity and back.

### Using AI tools

Use whatever tools you normally would, including coding agents. We expect
you will. Be ready to walk through the code as your own: what it does, what
you chose to do differently from what an agent suggested, and why.

### What we look at

- Does the flow work end to end?
- Does new code follow the structure that is already here?
- What happens when things go wrong: the endpoint is down, the selection is
  empty, the page changed while the workflow was running?
- Tests where they earn their keep. We do not need coverage for its own sake.
- Decisions you can explain, including what you chose to add or leave out.

### The interview

Don't push this anywhere. Have it ready to run with `docker compose up` and
`pnpm dev` when the interview starts. We will begin with you demoing it, then
we will make changes to it together.

## The repo

```
extension/           WXT + React 19 + Tailwind v4 (pnpm)
backend/             FastAPI API + Temporal worker, one Python package (uv)
docker-compose.yml   Temporal dev server, api, worker
```

### Prerequisites

- [uv](https://docs.astral.sh/uv/)
- Node 22 or newer with corepack enabled (`corepack enable`), which provides pnpm
- Docker
- Chrome

### Setup

```sh
cd backend && uv sync
cd extension && pnpm install
```

### Run

Everything in Docker:

```sh
docker compose up --build
```

- API: http://localhost:8000 (docs at `/docs`)
- Temporal UI: http://localhost:8233

For a faster loop, run only Temporal in Docker and the Python processes on
the host:

```sh
docker compose up temporal                      # terminal 1
cd backend && uv run python -m app.main api     # terminal 2
cd backend && uv run python -m app.main worker  # terminal 3
```

The extension always runs on the host. It opens a Chrome profile with the
extension loaded and hot reloads on change:

```sh
cd extension && pnpm dev
```

### Try it

```sh
curl -X POST localhost:8000/hello -H 'content-type: application/json' -d '{"name":"Ada"}'
# {"workflow_id":"hello-..."}
curl localhost:8000/hello/<workflow_id>
# {"workflow_id":"hello-...","status":"COMPLETED","greeting":"Hello, Ada!"}
```

### Checks

```sh
cd backend
uv run ruff format --check . && uv run ruff check . && uv run pyright
uv run pytest

cd extension
pnpm lint && pnpm typecheck
pnpm test:run
```

### Layout

#### backend/app

| Path | Purpose |
|---|---|
| `main.py` | Process entrypoint. `python -m app.main api` or `... worker`. |
| `config.py` | `Settings` from environment variables via pydantic-settings. |
| `api/main.py` | The FastAPI app and its lifespan. |
| `api/routers.py` | Registers every router on the app. |
| `api/modules/<name>/` | One directory per API domain: `main.py` holds the router, `schemas.py` the request and response models. |
| `api/dependencies/` | FastAPI dependencies, including the cached Temporal client. |
| `workflows/` | Temporal workflow definitions. |
| `activities/` | Temporal activity definitions. |
| `workers/main.py` | Builds the worker and registers workflows and activities. |
| `tests/` | pytest. API tests go through httpx's ASGI transport; workflow tests use Temporal's time-skipping test server. |

#### extension

Two entrypoints. `entrypoints/sidepanel/` is the React UI, opened by clicking
the toolbar icon. `entrypoints/background.ts` only wires up that click. Add
other entrypoints (content scripts, popup, options) as files in `entrypoints/`
and WXT picks them up by filename.
