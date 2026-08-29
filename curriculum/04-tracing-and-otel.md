# Stage 4 — Tracing and OpenTelemetry

**You'll be able to:** instrument a multi-step agent with OpenTelemetry's
GenAI semantic conventions, read the resulting trace tree, and explain how
that vendor-neutral data maps into a real observability backend.

**Time:** 2–4 hours.

**Build:** [`code/04-tracing-otel`](../code/04-tracing-otel).

## Read, in this order

1. **[OpenTelemetry blog, "Inside the LLM Call: GenAI Observability with OpenTelemetry"](https://opentelemetry.io/blog/2026/genai-observability/)**
   (2026-05-14) - a walkthrough of the `gen_ai.*` attribute model, the same
   attributes `code/04`'s sample sets by hand.
2. **[`open-telemetry/semantic-conventions-genai`](https://github.com/open-telemetry/semantic-conventions-genai)**
   - don't just read about the spec, open the actual spec files
   (`gen-ai-spans.md`, `gen-ai-agent-spans.md`) in the repo. Confirm for
   yourself that every span and attribute is marked `Status: Development` -
   this matters for how much you should hard-code these exact names into
   production code today.
3. Pick **one** tracing backend from the comparison table in
   [`resources/curated-resources.md`](../resources/curated-resources.md#tracing-and-observability-vendor-tools)
   and read its self-hosting docs - Langfuse's Docker Compose guide is the
   fastest path if you want to see a real UI later. This is optional for
   completing this stage; `code/04`'s sample runs entirely without one.

## Do

```bash
cd code/04-tracing-otel
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 agent.py
```

Read the printed trace tree against
[`code/04-tracing-otel/README.md`](../code/04-tracing-otel/README.md)'s
walkthrough - in particular, notice that the parent/child span nesting
comes entirely from where `start_as_current_span()` calls are physically
nested in the code, with no manual parent-ID bookkeeping. Then run:

```bash
python3 agent.py --fail
```

and see the tool-call failure marked `[ERROR]`, propagating to the parent
span - even though the agent's final answer to the user was a graceful
apology with nothing visibly wrong in the text alone. This is the concrete
case for why tracing exists alongside evals, not instead of them (see
[Stage 0](00-setup-and-mental-model.md)): the failure is invisible in the
output text, and only visible in the trace.

## Checkpoint

You should be able to answer, without looking anything up:

- What does it mean that the OTel GenAI semantic conventions are
  `Status: Development`, and what should that change about how you build
  against them today?
- In `code/04/agent.py`, why does `execute_tool`'s failure case not need a
  manual `span.set_status()` or `span.record_exception()` call to show up
  correctly in the trace?
- Pick two of the four tracing backends compared in
  `resources/curated-resources.md`. What's one real difference between them
  beyond "which logo do I like" - self-host cost, OTel compliance, or
  something else?

Next: [Stage 5 — Debugging non-determinism](05-debugging-nondeterminism.md).
