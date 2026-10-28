# Part 2 — One Conversation, One Session

This example links multiple agent turns to one conversation session in Arize Phoenix.

- **Trace:** one execution/turn.
- **Session:** the conversation grouping that connects the turn traces.
- **Conversation history:** messages passed to the model so later turns can use earlier context. A session ID does not provide memory by itself.

## 1. Start Phoenix

With Docker installed, run:

```bash
docker run --rm -p 6006:6006 -p 4317:4317 -p 4318:4318 arizephoenix/phoenix:latest
```

Open [http://localhost:6006](http://localhost:6006).

## 2. Set up Python

From the repository root:

```bash
cd part-02-session-tracing
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set `OPENAI_API_KEY`. Never commit a real API key.

## 3. Run

```bash
python agent_tracing.py
```

The script makes three model calls, keeps one in-memory conversation history, and uses the same `SESSION_ID` for all turns. Inspect the traces in Phoenix and group them by session.

## What to notice

1. Each model call creates trace data.
2. The shared session ID associates the turns with one conversation.
3. Later turns receive earlier messages as model context.
4. Session metadata is observability; conversation history is application state.

## Notes

This is a local learning demo, not a production scheduling agent. It has no calendar integration and does not book meetings. SDK APIs may change, so validate against your installed OpenInference/Phoenix versions. For production, persist history in your application, handle API errors, and avoid putting sensitive user data into span attributes.
