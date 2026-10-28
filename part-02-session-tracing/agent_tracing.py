"""Demonstrate conversation-level sessions and per-turn traces in Phoenix.

Start Phoenix locally, set OPENAI_API_KEY in .env, and run this script.
Each turn reuses the same session ID and conversation history.
"""
import os

from dotenv import load_dotenv
from openai import OpenAI
from openinference.instrumentation import using_session
from openinference.instrumentation.openai import OpenAIInstrumentor
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

load_dotenv()

PHOENIX_ENDPOINT = os.getenv("PHOENIX_COLLECTOR_ENDPOINT", "http://localhost:6006")
SESSION_ID = os.getenv("SESSION_ID", "scheduling-demo-001")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

provider = trace_sdk.TracerProvider()
provider.add_span_processor(
    SimpleSpanProcessor(
        OTLPSpanExporter(endpoint=f"{PHOENIX_ENDPOINT.rstrip('/')}/v1/traces")
    )
)
trace.set_tracer_provider(provider)
OpenAIInstrumentor().instrument(tracer_provider=provider)

tracer = trace.get_tracer("session-tracing-demo")
client = OpenAI()
messages = [
    {
        "role": "system",
        "content": (
            "You are a scheduling assistant. Help the user refine a meeting request. "
            "No calendar integration is configured, so never claim that a meeting "
            "has actually been booked. Keep responses concise."
        ),
    }
]


def agent_turn(user_message: str) -> str:
    """Run one turn, linked to the conversation session and prior messages."""
    messages.append({"role": "user", "content": user_message})

    with using_session(session_id=SESSION_ID):
        with tracer.start_as_current_span("agent.turn") as span:
            span.set_attribute("demo.user_message", user_message)
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
            )
            answer = response.choices[0].message.content or ""
            messages.append({"role": "assistant", "content": answer})
            span.set_attribute("demo.turn_number", (len(messages) - 1) // 2)
            return answer


if __name__ == "__main__":
    turns = [
        "Help me plan a 30-minute meeting with the design team tomorrow.",
        "Actually, make it 3 PM.",
        "Summarize the final meeting request, but don't say it is booked.",
    ]

    try:
        for turn_number, user_message in enumerate(turns, start=1):
            print(f"\nTurn {turn_number} — user: {user_message}")
            print(f"Turn {turn_number} — agent: {agent_turn(user_message)}")
    finally:
        provider.force_flush()
        OpenAIInstrumentor().uninstrument()
