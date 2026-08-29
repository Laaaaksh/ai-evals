# Stage 7 — Where this sits now

**You'll be able to:** choose a tracing/eval vendor for a real, specific
constraint - not "which one is most popular" - and know which parts of
this whole stack are still moving under you.

**Time:** 1–2 hours.

**Build:** no code this time. Pick one of the three scenarios below and
write a one-page decision: which tool, why, and what you'd re-check in six
months. That last part matters as much as the choice itself in a market
this described below.

## Read first

The **"Ecosystem direction - where this sits now"** and **"Tracing/
observability vendor tools"** sections of
[`resources/curated-resources.md`](../resources/curated-resources.md) -
you'll need the specifics from both to do the exercise below.

## Why this stage exists

This is a fast-moving corner of the industry, and pretending otherwise
would make this curriculum stale within months. Some concrete, checked
facts as of August 2026, so you can calibrate how fast:

- The OpenTelemetry GenAI semantic conventions - the vendor-neutral
  attribute schema [Stage 4](04-tracing-and-otel.md) is built on - are
  still `Status: Development`, not Stable.
- OpenAI acquired promptfoo in March 2026. Ragas quietly changed GitHub
  organizations and its commit cadence slowed. Ownership in this space is
  changing faster than the standards underneath it have stabilized.
- Langfuse grew past 33,900 GitHub stars with commits landing essentially
  daily - real, fast-moving investment, which also means real, fast-moving
  API surface to keep re-checking against.
- Per a cited industry survey, most teams running agents in production have
  *some* observability, but well under half run actual online evals. If
  you're building this stack for a real team, you're likely ahead of where
  most of the industry actually is, not behind.

None of this means "wait for it to stabilize before learning it." It means:
build the mental model (this whole curriculum), but hold the *specific*
vendor and attribute-name choices loosely, and re-check them against
current docs before shipping - the same discipline
[`resources/curated-resources.md`](../resources/curated-resources.md)
applies to every citation in this repository.

## Do

Pick one scenario and write a one-page decision (tool, why, and what you'd
re-verify in six months) using the comparison table in
`resources/curated-resources.md` as your primary input:

1. **A two-person startup**, pre-revenue, wants agent tracing today with
   zero infrastructure budget and no ops team to run anything.
2. **A regulated mid-size company** needs self-hosted tracing (data can't
   leave their VPC) and has a small platform team who can run Docker
   Compose but not a Kubernetes cluster.
3. **A team already committed to OpenTelemetry** company-wide for
   non-AI services, and wants their agent traces to live in the same
   pipeline rather than a separate vendor-specific one.

For each, the "right" answer isn't the same tool - that's the point. Defend
your choice against the *specific* constraint given, not against "which
tool is best" in the abstract.

## Checkpoint

You should be able to answer, without looking anything up:

- Name one tool from the comparison table that's a poor fit for scenario 2
  above, and the specific fact (not a vibe) that makes it a poor fit.
- What's one thing that was true about this ecosystem in this repository's
  citations that you should actively expect to have changed by the time
  you're reading this - and how would you check whether it has?

## You've finished the curriculum

You now have hands-on, verified experience with the full loop this
repository set out to teach: read failures by hand, build checks for them,
build and calibrate a judge for the ones that need judgment, trace the
system that's producing them, diagnose the ones that don't reproduce
cleanly, and freeze what you've fixed so it stays fixed. That loop, run
continuously, is what "AI evals and observability engineering" actually
is - not a single tool, and not a single skill.

What this repository doesn't cover, and where to go instead: multi-agent
system evaluation specifically (evaluating coordination between multiple
agents, not just one agent's tool use), red-teaming and adversarial
robustness testing (promptfoo, cited throughout this curriculum, has real
depth here), and RAG-specific evaluation metrics beyond the grounding-style
judge task in Stage 3 (ragas, also cited above, is the deeper resource for
that). See [`README.md`](../README.md#what-this-repository-does-not-cover)
for the full list.
