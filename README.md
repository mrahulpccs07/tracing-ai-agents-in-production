# Tracing AI Agents in Production

A practical companion repository for the LinkedIn article series **Tracing AI Agents in Production**, exploring how to observe, debug, and reason about AI-agent executions using OpenTelemetry, OpenInference, and Arize Phoenix.

## Articles and examples

- **Part 1 — Why Agent Logs Are Not Enough**: explains why logs alone often fail to show why an agent reached a particular result.
- **Part 2 — One Conversation, One Session**: [run the session-tracing demo](part-02-session-tracing/README.md).

## Part 2 demo

The example models a short scheduling conversation across three turns. It demonstrates the distinction between:

- **Trace:** an individual execution/turn.
- **Session:** a grouping that connects traces from one conversation.
- **Conversation history:** application state passed into later model calls; session metadata does not create memory.

Start with the [Part 2 setup guide](part-02-session-tracing/README.md). This is a learning demo, not a production-ready agent, and it does not book calendar events.

## Project status

Examples are educational and may need adjustment as Phoenix, OpenInference, and OpenTelemetry SDKs evolve. Check each part's README for setup and limitations.
