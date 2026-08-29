"""A minimal OpenTelemetry SpanExporter that renders finished spans as an
indented waterfall tree instead of raw JSON - what a real tracing UI
(Langfuse, Phoenix, Braintrust, LangSmith) draws as nested boxes, this
prints as nested text. Teaching-only: a real backend does far more
(searching across traces, diffing, cost rollups) - see
resources/curated-resources.md.
"""
from __future__ import annotations

from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult

KEY_ATTRS = [
    "gen_ai.operation.name",
    "gen_ai.system",
    "gen_ai.agent.name",
    "gen_ai.tool.name",
    "gen_ai.tool.call.arguments",
    "gen_ai.tool.call.result",
    "gen_ai.usage.input_tokens",
    "gen_ai.usage.output_tokens",
]


class TreeExporter(SpanExporter):
    def __init__(self) -> None:
        self.spans: list[ReadableSpan] = []

    def export(self, spans) -> SpanExportResult:
        self.spans.extend(spans)
        return SpanExportResult.SUCCESS

    def shutdown(self) -> None:
        pass

    def render_tree(self) -> str:
        by_parent: dict[int | None, list[ReadableSpan]] = {}
        for span in self.spans:
            parent_id = span.parent.span_id if span.parent else None
            by_parent.setdefault(parent_id, []).append(span)
        for children in by_parent.values():
            children.sort(key=lambda s: s.start_time)

        roots = by_parent.get(None, [])
        lines = ["--- trace ---"]

        def walk(span: ReadableSpan, depth: int) -> None:
            duration_ms = (span.end_time - span.start_time) / 1_000_000
            status = span.status.status_code.name
            marker = "" if status == "UNSET" else f" [{status}]"
            lines.append(f"{'  ' * depth}{span.name} ({duration_ms:.1f}ms){marker}")
            for key in KEY_ATTRS:
                if key in span.attributes:
                    lines.append(f"{'  ' * depth}  {key} = {span.attributes[key]!r}")
            for event in span.events:
                lines.append(f"{'  ' * depth}  event: {event.name}")
            for child in by_parent.get(span.context.span_id, []):
                walk(child, depth + 1)

        for root in roots:
            walk(root, 0)
        return "\n".join(lines)
