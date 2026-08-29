#!/usr/bin/env python3
"""A toy multi-step support agent, instrumented with OpenTelemetry using the
OTel GenAI semantic conventions attribute names (gen_ai.* - see
https://github.com/open-telemetry/semantic-conventions-genai, "Development"
maturity as of the spec version checked for this repo - see
resources/curated-resources.md for the exact version and date).

The agent itself is entirely simulated - no real LLM calls, no real tools -
so this sample needs nothing but the two `opentelemetry-*` packages, no API
key, no network call except the (local) console exporter. The point isn't
the agent, it's the trace shape: one invoke_agent span as the root, with
chat and execute_tool spans nested inside it, each carrying the specific
gen_ai.* attributes a real observability backend (Langfuse, Phoenix,
Braintrust, LangSmith - see curriculum/04-tracing-and-otel.md) would key its
UI off of.

Run:
    python3 agent.py            # a request that succeeds
    python3 agent.py --fail     # a request where a tool call fails
"""
from __future__ import annotations

import argparse
import random
import time

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.trace import Status, StatusCode

from tree_exporter import TreeExporter

resource = Resource.create({"service.name": "toy-support-agent"})
provider = TracerProvider(resource=resource)
tree_exporter = TreeExporter()
provider.add_span_processor(SimpleSpanProcessor(tree_exporter))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("ai-evals.stage04")

FAKE_ORDER_DB = {"A1029": {"status": "shipped", "eta": "2026-08-14"}}


def fake_llm_call(operation_name: str, prompt: str, model: str = "claude-sonnet-5") -> str:
    """Stands in for a real LLM call. Span attributes follow gen_ai.* -
    see the spec for the full attribute list; this sample uses the core
    request/response ones every backend displays.
    """
    with tracer.start_as_current_span(f"{operation_name} {model}") as span:
        span.set_attribute("gen_ai.operation.name", operation_name)
        span.set_attribute("gen_ai.system", "anthropic")
        span.set_attribute("gen_ai.request.model", model)
        span.set_attribute("gen_ai.input.messages", prompt[:200])
        time.sleep(0.01)  # simulated latency
        if "order status" in prompt.lower():
            response = "I'll check the order status for you."
        else:
            response = "Here's a summary of what I found."
        span.set_attribute("gen_ai.output.messages", response)
        span.set_attribute("gen_ai.usage.input_tokens", len(prompt.split()))
        span.set_attribute("gen_ai.usage.output_tokens", len(response.split()))
        return response


def execute_tool(tool_name: str, order_id: str, should_fail: bool = False) -> dict:
    """A tool call span, per gen_ai.agent-spans.md's execute_tool naming."""
    with tracer.start_as_current_span(f"execute_tool {tool_name}") as span:
        span.set_attribute("gen_ai.operation.name", "execute_tool")
        span.set_attribute("gen_ai.tool.name", tool_name)
        span.set_attribute("gen_ai.tool.call.arguments", f"order_id={order_id}")
        time.sleep(0.01)
        if should_fail:
            # Raising inside `start_as_current_span` is enough - by default
            # it records the exception as a span event and sets the span's
            # status to ERROR for you. No manual set_status/record_exception
            # call needed (doing both would double up the exception event).
            raise RuntimeError(f"order_status_service timeout for {order_id}")
        result = FAKE_ORDER_DB.get(order_id, {"status": "unknown"})
        span.set_attribute("gen_ai.tool.call.result", str(result))
        return result


def run_agent(user_message: str, order_id: str, fail: bool = False) -> str:
    """The root span: invoke_agent, per gen_ai-agent-spans.md. Every span
    opened inside this `with` block is automatically its child - that
    parent/child nesting IS the trace, and it's what every tracing backend
    in curriculum/04-tracing-and-otel.md renders as a waterfall.
    """
    with tracer.start_as_current_span("invoke_agent support-agent") as span:
        span.set_attribute("gen_ai.operation.name", "invoke_agent")
        span.set_attribute("gen_ai.agent.name", "support-agent")
        span.set_attribute("gen_ai.agent.description", "Answers order-status questions")

        fake_llm_call("chat", f"Plan how to answer: {user_message}")

        try:
            result = execute_tool("get_order_status", order_id, should_fail=fail)
        except RuntimeError:
            span.set_status(Status(StatusCode.ERROR, "tool call failed"))
            answer = "Sorry, I couldn't look up that order right now - please try again shortly."
            fake_llm_call("chat", f"Apologize for tool failure on {order_id}")
            return answer

        answer = fake_llm_call("chat", f"Order {order_id} status: {result['status']}")
        return answer


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fail", action="store_true", help="simulate a tool-call failure")
    parser.add_argument("--order-id", default="A1029")
    args = parser.parse_args()

    random.seed(0)
    answer = run_agent("Where's my order?", args.order_id, fail=args.fail)

    provider.force_flush()
    print(tree_exporter.render_tree())
    print("--- final answer ---")
    print(answer)


if __name__ == "__main__":
    main()
