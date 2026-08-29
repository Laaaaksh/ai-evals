# 04 — Tracing an agentic system with OpenTelemetry GenAI conventions

A toy multi-step support agent ([`agent.py`](agent.py)), instrumented with
real OpenTelemetry spans using the `gen_ai.*` attribute names from the
[OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai)
- the vendor-neutral attribute schema that Langfuse, Arize Phoenix (via
Arize AX), Braintrust, and LangSmith all ingest in some form. **As of the
spec version checked for this repo (2026-08-27/29), every `gen_ai.*` span
and attribute is marked `Status: Development`** - not yet Stable. That's
stated here, not hidden, because it changes how you should read this
sample: the attribute *names* below are current, but expect some of them to
be renamed or restructured before the spec stabilizes. See
[`resources/curated-resources.md`](../../resources/curated-resources.md)
for the exact spec URL, version, and date, and note that the *old* spec
location (`open-telemetry/semantic-conventions/docs/gen-ai/`) is deprecated
- many older blog posts still link there.

Companion to [`curriculum/04-tracing-and-otel.md`](../../curriculum/04-tracing-and-otel.md).

## Run it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 agent.py
```

The agent itself is entirely simulated (no real LLM calls, no real tools,
no network) - the point of this sample is the *trace shape*, not the agent.
`agent.py` prints a readable indented tree (via
[`tree_exporter.py`](tree_exporter.py), a ~50-line custom `SpanExporter`
that renders finished spans as a waterfall instead of raw JSON):

```
--- trace ---
invoke_agent support-agent (43.6ms)
  gen_ai.operation.name = 'invoke_agent'
  gen_ai.agent.name = 'support-agent'
  chat claude-sonnet-5 (15.0ms)
    gen_ai.operation.name = 'chat'
    gen_ai.system = 'anthropic'
    gen_ai.usage.input_tokens = 7
    gen_ai.usage.output_tokens = 7
  execute_tool get_order_status (14.3ms)
    gen_ai.operation.name = 'execute_tool'
    gen_ai.tool.name = 'get_order_status'
    gen_ai.tool.call.arguments = 'order_id=A1029'
    gen_ai.tool.call.result = "{'status': 'shipped', 'eta': '2026-08-14'}"
  chat claude-sonnet-5 (14.2ms)
    ...
```

That nesting - one `invoke_agent` root span, with `chat` and `execute_tool`
spans as children in call order - is exactly what a real tracing backend
draws as a waterfall UI. You're looking at the same data structure a
$50M-funded observability vendor's product renders, just as indented text.

Then run the failure case:

```bash
python3 agent.py --fail
```

The `execute_tool` span comes back marked `[ERROR]` with an `exception`
event attached, and that error status propagates to the parent
`invoke_agent` span too - even though the agent itself recovered gracefully
and gave the user a reasonable answer. **This is the single most useful
thing tracing gives you that error analysis (Stage 1) can't**: a transcript
alone shows a clean apology message with no visible problem; the trace
shows a tool call that failed underneath a response that looked fine.

## What to look for

- `execute_tool` errors: [`agent.py`](agent.py)'s `execute_tool` function
  just raises - it does **not** manually call `span.set_status()` or
  `span.record_exception()`. `start_as_current_span`'s defaults
  (`record_exception=True`, `set_status_on_exception=True`) do both for you
  automatically when an exception propagates out of the `with` block.
  Calling both yourself as well double-records the exception event - a real
  and easy mistake worth avoiding on purpose here.
- `gen_ai.usage.input_tokens` / `output_tokens` on every `chat` span: this
  is the attribute path a real backend sums to build a cost dashboard.
  Notice it's per-span, not per-trace - a trace's total cost is a rollup
  over every `chat` span nested inside it.
- The parent/child relationship is carried by OpenTelemetry's own context
  propagation (`start_as_current_span` inside another `start_as_current_span`
  block), not by anything this sample's code manages manually - that's
  what makes tracing composable across real, larger codebases: any function
  that opens a span while another span is active gets nested automatically,
  no explicit parent ID passing required.

## Sending this to a real backend

This sample's default exporter (`tree_exporter.py`) only prints to your
terminal. To see the same trace in a real UI, swap it for an OTLP exporter
pointed at a self-hosted backend - Langfuse's self-host (Docker Compose) is
the easiest of the four covered in
[`curriculum/04-tracing-and-otel.md`](../../curriculum/04-tracing-and-otel.md)
to stand up for this. **This repo does not include or verify a working
docker-compose setup** - follow Langfuse's own self-hosting docs (cited in
`resources/curated-resources.md`) and point `OTEL_EXPORTER_OTLP_ENDPOINT`
at your instance's `/api/public/otel` path instead of using
`tree_exporter.py`. As of the version checked for this repo, Langfuse maps
the *older* attribute-based `gen_ai.*` format (not the newer events-based
format some spec versions use) - if your traces don't show up as expected,
that mismatch is the first thing to check.

## Try this

- Add a second tool call (e.g. `execute_tool("issue_refund", ...)`) inside
  `run_agent` and confirm it appears as a sibling of `get_order_status` in
  the tree, not nested inside it - only spans opened while another span's
  `with` block is still open become children.
- Add a `gen_ai.response.finish_reasons` attribute to `fake_llm_call` (a
  real attribute in the spec) and see it appear in the tree output - you
  don't need to modify `tree_exporter.py`, it prints whatever's in
  `KEY_ATTRS`; add the new key there too.
- Compare this sample's manual `tracer.start_as_current_span()` calls with
  what an auto-instrumentation package like `opentelemetry-instrumentation-openai-v2`
  (cited in `resources/curated-resources.md`) generates automatically for a
  *real* OpenAI call - same attribute names, zero manual span code.
