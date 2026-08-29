# Curated resources

Every entry here was actually fetched and checked at the time of writing
(August 2026) - GitHub stats came from the GitHub API (exact star counts and
push timestamps, not scraped estimates) and every URL was opened directly.
Dates are the resource's own stated publish/update date where one exists.
Where something has aged, that's said plainly, along with what to read
instead or alongside it. Curriculum stages link the specific entries
relevant to them; this page is the full, browsable list with the reasoning
behind each recommendation.

If a link here breaks, or you find something better, please open an issue
using the "Resource suggestion" template - see
[`CONTRIBUTING.md`](../CONTRIBUTING.md).

## Error analysis

| Resource | What it covers | Current as of | Verdict |
|---|---|---|---|
| [Hamel Husain, "A Field Guide to Rapidly Improving AI Products"](https://hamel.dev/blog/posts/field-guide/) | Calls error analysis "the single most valuable activity in AI development"; custom data viewers over dashboards; "criteria drift" | 2025-03-24 | **Current, start here.** The best single overview of the whole error-analysis-first workflow this stage is built around. |
| [Hamel Husain, "Evals: Doing Error Analysis Before Writing Tests"](https://hamel.dev/notes/llm/officehours/erroranalysis.html) | The concrete open-coding workflow: spreadsheet-based categorization of real failures before building any metric | 2024-12-21 | **Current, most tactical.** This is the practice `code/01-error-analysis` is a small, runnable version of. |
| [Hamel Husain & Shreya Shankar, "LLM Evals: Everything You Need to Know"](https://hamel.dev/blog/posts/evals-faq/) | FAQ-style: open coding → axial coding → theoretical saturation | Published 2025-05-28, last modified 2026-07-18 | Current and actively maintained - the saturation concept `analyze_taxonomy.py` implements comes from here. |
| [Shreya Shankar et al., "Who Validates the Validators?" (EvalGen)](https://arxiv.org/abs/2404.12272) | Formalizes gold-set alignment as an iterative process; coins "criteria drift" | Submitted 2024-04-18, ACM UIST '24 | Current, foundational academic grounding for why error analysis has to come before automated evals, not after. |
| [applied-llms.org, "What We Learned from a Year of Building with LLMs"](https://applied-llms.org) | Eugene Yan, Bryan Bischof, Charles Frye, Hamel Husain, Jason Liu, Shreya Shankar - the "Intern Test," daily log-review practice | 2024-06-08 | **Aged but still widely cited and worth reading** - a snapshot of shared practitioner consensus, not superseded by anything more current found in this research. |
| [Hamel Husain's `hamel.dev/notes/llm/evals/` hub](https://hamel.dev/notes/llm/evals/) | An index page linking ~13 of his own posts, organized by workflow stage | Confirmed live, spans posts from 2024-03 through 2026-08 | Current, but it's a **hub, not a self-contained article** - treat it as a map to the specific posts cited individually in this table, not as one thing to read start to end. |

## Building a first eval suite

| Resource | What it covers | Current as of | Verdict |
|---|---|---|---|
| [promptfoo](https://github.com/promptfoo/promptfoo) ([docs](https://promptfoo.dev/docs/configuration/expected-outputs/)) | Binary assertions (`equals`, `contains`, `regex`), structured-output checks (`is-json`, tool-call validation), plus model-graded metrics | 24,664★, pushed 2026-08-29 | **Current, the strongest general match for this stage.** One caveat: OpenAI announced acquiring promptfoo on 2026-03-09 (folded into "OpenAI Frontier," staying open source under its current license) - worth knowing if you're weighing it as a vendor-neutral tool. |
| [DeepEval](https://github.com/confident-ai/deepeval) | Pytest-style LLM testing - RAG/agent/multi-turn metrics, structured-output validation | 17,953★, pushed 2026-08-29 | Current and actively maintained; a good second option alongside promptfoo, closer in spirit to `code/06`'s pytest-based regression suite. |
| [Anthropic, "Define success criteria and build evaluations"](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) | SMART criteria framework; four grading methods (exact match, cosine similarity, ROUGE-L, LLM grading) with runnable code | Live docs, checked 2026-08-30 | Current. |
| [Anthropic Cookbook, "Building evals"](https://github.com/anthropics/claude-cookbooks) | A worked example of code-based, human, and model-based grading | Repo pushed 2026-08-28 | Current. |
| [Hamel Husain, "Your AI Product Needs Evals"](https://hamel.dev/blog/posts/evals/) | The original three-level framework: unit tests, human/model eval, A/B testing | 2024-03-29 | **Aged but still the canonical starting reference** - nothing found in this research supersedes it as the first thing to read on why evals matter at all. |
| [OpenAI Evals](https://github.com/openai/evals) | Framework + registry for LLM evals | 19,308★, pushed 2026-04-14 | **Aged-but-still-usable.** OpenAI's own README now steers users toward a hosted Dashboard product; the OSS repo gets infrequent commits relative to promptfoo/DeepEval. Fine for the registry/format ideas, don't expect active development. |

## LLM-as-judge methodology and calibration

| Resource | What it covers | Current as of | Verdict |
|---|---|---|---|
| [Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"](https://arxiv.org/abs/2306.05685) | Foundational: catalogs judge biases, shows GPT-4-class judges can match human-human agreement on MT-Bench | Submitted 2023-06-09 | **Current/foundational** - the canonical citation for the entire practice, still the right starting point despite its age. |
| [Eugene Yan, "Evaluating the Effectiveness of LLM-Evaluators"](https://eugeneyan.com/writing/llm-evaluators/) | Argues for Cohen's kappa over raw agreement; discusses criteria drift | 2024-08-18 | Current - directly informs why `code/03-llm-judge` reports kappa, not just accuracy. |
| [Hamel Husain, "Using LLM-as-a-Judge For Evaluation: A Complete Guide"](https://hamel.dev/blog/posts/llm-judge/) | "Critique Shadowing," a 7-step calibration process; recommends precision/recall over raw agreement on imbalanced data | 2024-10-29 | Current, the best single how-to guide found. |
| [Pratik Bhavsar (Galileo), "How to Calibrate Your LLM Judge With Human Annotations"](https://galileo.ai/blog/calibrate-llm-judge-human-annotations) | Continuous calibration framework - stratified sampling, kappa, Krippendorff's alpha | 2026-08-28 | **Current, the freshest resource found in this research** (two days before this repo was written). Vendor-authored; methodology is sound regardless. |
| [Rao & Callison-Burch, "Agreement Metrics for LLM-as-Judge Evaluation"](https://arxiv.org/abs/2606.00093) | Shows reported judge-human agreement varies 0.551-0.899 purely from protocol choice; proposes a reporting checklist | Submitted 2026-05-25, revised 2026-07-31 | Current and the most rigorous recent treatment of "which metric should I even report" - read this before trusting any single-number agreement claim, including this repo's own. |
| [Shreya Shankar et al., EvalGen](https://arxiv.org/abs/2404.12272) | See also under "Error analysis" above - the gold-set alignment methodology `code/03` follows | 2024-04-18 | Current. |
| [`CSHaitao/Awesome-LLMs-as-Judges`](https://github.com/CSHaitao/Awesome-LLMs-as-Judges) | Paper-list companion to a survey (arXiv:2412.05579) | 609★, pushed 2025-07-29 | **Aged-but-useful as a bibliography** - a paper list, not a practitioner guide; don't expect sequencing. |

## OpenTelemetry GenAI semantic conventions

| Resource | What it covers | Current as of | Verdict |
|---|---|---|---|
| [`open-telemetry/semantic-conventions-genai`](https://github.com/open-telemetry/semantic-conventions-genai) | The `gen_ai.*` span/attribute spec `code/04-tracing-otel` is built on - inference, embeddings, retrieval, agent, and tool-call spans | 307★, pushed 2026-08-27/29 | **Current - the vendor-neutral backbone this curriculum teaches - but every span and attribute is explicitly marked `Status: Development`, not Stable, as of this version.** The repo moved here from the old `open-telemetry/semantic-conventions/docs/gen-ai/` location (now deprecated) in June 2026 - many older blog posts still link the dead path; use this URL instead. |
| [`open-telemetry/opentelemetry-python-contrib`](https://github.com/open-telemetry/opentelemetry-python-contrib), `instrumentation-genai/` | Auto-instrumentation for real LLM calls (e.g. `opentelemetry-instrumentation-openai-v2`) - contrast this with `code/04`'s manual span code | 1,091★, pushed 2026-08-28, latest release 2026-08-10 | Current. Message content is redacted by default (`OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` opts in) - a real, easy-to-miss gotcha. |
| [OpenTelemetry blog, "Inside the LLM Call: GenAI Observability with OpenTelemetry"](https://opentelemetry.io/blog/2026/genai-observability/) | A walkthrough exporting GenAI-semconv telemetry to a real dashboard | 2026-05-14 | Current, solid intro-level companion to `code/04`. |
| [Traceloop/OpenLLMetry](https://github.com/traceloop/openllmetry) | OTel-based auto-instrumentation across 14 LLM providers, 7 vector DBs, 8 frameworks; Traceloop states it leads the OTel GenAI semconv working group | 7,407★, pushed 2026-08-10 | Current, the most star-validated instrumentation SDK in this space. |
| [OpenInference (Arize)](https://github.com/Arize-ai/openinference) | Arize's own pre-OTel-standard tracing schema, now converging with the official spec | 1,186★, pushed 2026-08-29 | Current - a good real example of a vendor schema predating and now reconciling with a later standard; see the Phoenix entry below for exactly where the two diverge today. |

## Tracing and observability vendor tools

All four self-host/pricing/OTel-mapping claims below were checked directly
against each vendor's own docs at the dates shown; two license
classifications (Phoenix, Langfuse) were reported by GitHub's API as "Other"
and not independently confirmed against the LICENSE file text itself - check
the license page directly before making a legal decision based on this
table.

| Tool | GitHub / license | Self-host | Agentic tracing | OTel GenAI mapping | Verdict |
|---|---|---|---|---|---|
| [Langfuse](https://github.com/langfuse/langfuse) | 33,910★, pushed 2026-08-29, open-core (MIT core + gated enterprise add-ons) | **Easiest of the four to run yourself** - documented Docker Compose path for a VM/local instance; Postgres + ClickHouse + Redis for production | Nested spans/observations, a dedicated `tool` span type, native LangGraph/CrewAI integrations | Ingests via `/api/public/otel`, states it "aims to be compliant" - but as of a live GitHub issue (#12657), doesn't yet handle the newer semconv v1.37+ events-based format, only the older attribute-based one | **Current, strongest default recommendation** - most stars, cleanest self-host story, real (if partial) OTel support. |
| [Arize Phoenix](https://github.com/Arize-ai/phoenix) | 11,243★, pushed 2026-08-29 | **Genuinely one-line**: `docker run -p 6006:6006 -p 4317:4317 arizephoenix/phoenix:latest` - free, unlimited, no tier gate | Nested retrieval/embedding/LLM/tool spans, a dedicated multi-turn **Sessions** feature; multi-agent orchestration coverage is thinner | **Important nuance**: Phoenix OSS is built on OpenInference, not the official OTel GenAI semconv directly - native `gen_ai.*` support exists only in the paid Arize AX product, which normalizes it into OpenInference | Current, **best self-host UX of the four** - but be precise that "Phoenix" and "OTel GenAI semconv-native" aren't the same claim. |
| [Braintrust](https://braintrust.dev) | Core platform closed-source SaaS; only SDKs are OSS (e.g. `braintrust-sdk-javascript`, Apache-2.0) | "Hybrid deployment" (you run the data plane via Terraform, Braintrust hosts the control plane) - **Enterprise tier only** | Proprietary span taxonomy (eval/task/llm/function/tool/score/classifier) | A separate integration page states OTel GenAI semconv support via `@braintrust/otel` - disconnected from the main tracing-docs page, itself a documentation-fragmentation flag | Current, with real lock-in caveats: closed source, self-hosting gated to Enterprise. |
| [LangSmith](https://smith.langchain.com) | Core platform closed-source SaaS; only the client SDK is OSS (`langsmith-sdk`, MIT) | Enterprise-only, sales-issued license key, Kubernetes recommended - heaviest operational overhead of the four; **no free or mid-tier self-host option** | `@traceable`/LangChain auto-instrumentation, thread/session continuity, waterfall view | Docs (`docs.langchain.com/langsmith/trace-with-opentelemetry`) document separate mapping tables for OTel GenAI, OpenLLMetry, and OpenInference attributes side by side - broader standards support than its reputation suggests, though exact default precedence is worth re-checking directly before depending on it | Current, but **the most vendor-locked of the four** - useful as a deliberate lock-in contrast case. |

Two awesome-lists worth knowing about, not as primary references:
[`ContextJet-ai/awesome-llm-observability`](https://github.com/ContextJet-ai/awesome-llm-observability)
(31★, pushed 2026-08-24, CC0, includes a genuinely structured OTel GenAI
section and a platform comparison table - worth citing despite its low star
count) and
[`rizzdev/awesome-llm-observability`](https://github.com/rizzdev/awesome-llm-observability)
(1★, pushed 2026-07-23, no LICENSE file - real editorial quality but
near-zero community validation and unclear reuse rights).

## Debugging non-determinism

| Resource | What it covers | Current as of | Verdict |
|---|---|---|---|
| [Thinking Machines Lab (Horace He), "Defeating Nondeterminism in LLM Inference"](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/) | The actual root cause of temperature-0 non-determinism: lack of batch invariance in GPU kernels, not floating-point non-associativity - demonstrated with a real experiment (1,000 identical prompts → 80 unique completions without batch-invariant kernels, 0 with them) | 2025-09-10 | **Current and the best technical source found** - read this before assuming "temperature 0" means deterministic. |
| [Anthropic, Messages API reference - `temperature`](https://platform.claude.com/docs/en/api/messages) | States plainly that results aren't fully deterministic even at `temperature=0.0`; notes models after Claude Opus 4.6 don't support setting temperature at all | Live docs, checked 2026-08-30 | Current, must-cite primary source. |
| [OpenAI, Advanced usage guide - `seed`](https://developers.openai.com/api/docs/guides/advanced-usage) | The `seed` + `system_fingerprint` mechanism is documented as best-effort, not a hard guarantee - "determinism may be impacted due to necessary changes OpenAI makes to model configurations" | Live docs, checked 2026-08-30 | Current. (`platform.openai.com/docs/api-reference/chat/create` blocks automated fetching - use the link above instead.) |
| [Dylan Castillo, "Controlling randomness in LLMs: Temperature and Seed"](https://dylancastillo.co/posts/seed-temperature-llms.html) | Practical cross-provider guidance; notes seed support is limited to OpenAI, Vertex AI Gemini, and self-hosted OSS models - not Anthropic | 2025-06-25 | Aged but accurate and useful as a cross-vendor cheat sheet. |

No single practitioner source was found that cleanly separates prompt
sensitivity, tool-format variance, retrieval variance, and judge noise into
one diagnostic framework the way `code/05-debug-nondeterminism` does -
that framework is original synthesis for this repo, built on the individual
sources above for each cause. If you find a better single source, please
open an issue.

## Regression suites and the "data flywheel"

| Resource | What it covers | Current as of | Verdict |
|---|---|---|---|
| [Braintrust, "How to turn LLM production failures into regression tests"](https://www.braintrust.dev/articles/turn-llm-production-failures-into-regression-tests) | A concrete 5-step workflow: capture failed traces → diagnose → promote into a dataset → write a scorer → gate releases in CI and on live traffic | 2026-05-29 | **Current, the closest practitioner match** to what `code/06-regression-suite-ci` demonstrates. Vendor-authored (Braintrust sells an eval platform); the methodology is sound regardless. |
| [`Jwuthri/Tracely-ai`](https://github.com/Jwuthri/Tracely-ai) | "Trace-native CI/CD for AI agents" - auto-detects and clusters production failures, freezes them into hermetic regression cases, replays them in CI for free | 1,203★, pushed 2026-08-29, created 2026-06-03 | Current and real, but **very young** (~3 months old at time of writing) - flag as early-stage/pre-1.0 to readers, not an established tool on the level of promptfoo. |
| [Hamel Husain, "A Field Guide to Rapidly Improving AI Products"](https://hamel.dev/blog/posts/field-guide/) | See also under "Error analysis" - discusses turning critiques into a synthetic-data "flywheel," a related but distinct idea from CI-blocking regression gating specifically | 2025-03-24 | Aged-but-foundational for the general flywheel concept; don't cite it as the source for the CI-gating mechanic specifically - use the Braintrust post above for that. |

## General LLM/agent eval frameworks

| Resource | What it covers | Current as of | Verdict |
|---|---|---|---|
| [DeepEval](https://github.com/confident-ai/deepeval) | "Pytest for LLM apps" - RAG, agentic (task completion, tool correctness), and multi-turn metrics | 17,953★, pushed 2026-08-29 | Current, actively maintained. |
| [ragas](https://github.com/vibrantlabsai/ragas) | RAG-specific evaluation (faithfulness, contextual precision) | 15,542★, pushed 2026-02-24 | **Aged-but-still-best-available for RAG eval specifically** - note the repo moved from `explodinggradients/ragas` to `vibrantlabsai/ragas` (old URLs redirect), and its commit cadence has slowed noticeably relative to DeepEval/promptfoo - possibly a stewardship transition worth watching. |
| [promptfoo](https://github.com/promptfoo/promptfoo) | See "Building a first eval suite" above | 24,664★, pushed 2026-08-29 | Current - and now OpenAI-owned since March 2026 (see note above), worth disclosing if you're framing tool choice as vendor-neutral. |

## Courses and books

| Resource | What it covers | Current as of | Verdict |
|---|---|---|---|
| [Hamel Husain & Shreya Shankar, "AI Evals for Engineers & PMs"](https://maven.com/parlance-labs/evals) (Maven) | The most-established structured course in this space - error analysis, synthetic data, LLM-as-judge, production monitoring, data flywheels | $4,200; cohorts confirmed for 2026-09-05 and 2026-10-10; claims 4,500+ trained, 4.7/5 over 897 reviews | **Current, the paid benchmark this free repo is deliberately positioned alongside**, not a replacement for. Its existence and evident scale is itself part of the demand evidence for this repository. |
| Shreya Shankar & Hamel Husain, *Evals for AI Engineers: Systematically Measuring and Improving AI Applications* (O'Reilly) | A book-length treatment of the same course material | Publication date 2026-10-31, [O'Reilly listing confirmed live](https://www.oreilly.com/library/view/evals-for-ai/9798341660717/) | Confirmed real but **not yet published** at the time of writing - worth watching for, not yet readable. |
| [`ai-evals-course/evals-skills`](https://github.com/ai-evals-course/evals-skills) | Hamel/Shreya's own extension: reusable "skills" that guide AI coding agents to help build product-specific evals | 487★, pushed 2026-08-16 | Current - a genuinely different artifact from the course itself (agent-facing skills, not a curriculum), worth knowing about if you're building evals *with* an AI coding assistant. |

## Existing GitHub attempts at this space (and why none of them close the gap)

Checked directly via the GitHub API on 2026-08-30, to confirm the gap this
repository fills is still open:

| Repo | Stars | Last push | Why it doesn't close the gap |
|---|---|---|---|
| [`calmrocks/ai-engineer-notebooks`](https://github.com/calmrocks/ai-engineer-notebooks) | 499 | 2026-08-28 | Evals is one topic notebook among RAG, tool calling, fine-tuning, and agents - not a dedicated, sequenced spine. |
| [`NVIDIA/SkillEvaluator`](https://github.com/NVIDIA/SkillEvaluator) | 351 | 2026-08-28 | A real framework, but narrowly scoped to evaluating agent *skills* (quality gates, semantic overlap) - a tool, not a learning path. |
| [`awslabs/agent-evaluation`](https://github.com/awslabs/agent-evaluation) | 371 | 2025-12-15 | A usable framework, but no push in 8+ months as of writing - effectively stale. |
| [`CSHaitao/Awesome-LLMs-as-Judges`](https://github.com/CSHaitao/Awesome-LLMs-as-Judges), [`llm-as-a-judge/Awesome-LLM-as-a-judge`](https://github.com/llm-as-a-judge/Awesome-LLM-as-a-judge) | 609 / 574 | 2025-07-29 / 2026-05-21 | Paper-list companions to academic surveys - bibliographies, not practitioner sequencing. |

## Ecosystem direction - where this sits now

A few data points worth knowing if you're deciding how much to invest here,
all checked directly at the time of writing:

- **[Langfuse](https://github.com/langfuse/langfuse) grew to 33,910★** as of
  2026-08-30 with commits landing essentially daily - observability tooling
  for LLM/agent systems is one of the fastest-moving parts of the current AI
  engineering ecosystem, which cuts both ways: fast improvement, but also
  fast API/attribute-schema churn (see the OTel GenAI semconv note above -
  still `Development` status, not Stable).
- **Evaluation practice lags observability practice.** Per a cited
  LangChain "State of Agent Engineering" survey (1,300+ professionals,
  reported via search rather than independently re-derived from the primary
  dataset): 89% of teams running agents in production have *some*
  observability, but only 52.4% run offline evals, 37.3% online evals, and
  29.5% report no evaluation at all. Read that gap as the actual market
  problem this repository is aimed at closing, not as a settled statistic -
  treat the exact percentages as approximate.
- **The role title "AI Evals Engineer" is now real**, not aspirational -
  e.g. a Scale AI "Evals Engineer, Applied AI" posting (San
  Francisco/NY/Seattle, $216,000-$270,000) was live as recently as this
  research; that specific posting has since closed, which is itself
  evidence it existed and was compensated at that level, not that the role
  category has gone away.
- **Vendor consolidation is happening in real time.** OpenAI acquired
  promptfoo (announced 2026-03-09); Ragas quietly changed GitHub orgs and
  slowed its commit cadence. If you're picking a tool to depend on for
  years, weight self-hostability and OTel GenAI compliance over current
  popularity - popularity in this space has proven to change ownership
  faster than the underlying standard has stabilized.

## Suggested reading order

This is denser than the curriculum's per-stage lists - use those first;
come back here for the full picture or a next step beyond what a stage asks
for.

1. Hamel Husain's "Your AI Product Needs Evals," then "A Field Guide to
   Rapidly Improving AI Products," for the overall philosophy this
   curriculum is built on.
2. Zheng et al.'s MT-Bench paper, then Eugene Yan's and Hamel Husain's
   judge-calibration posts, before attempting `code/03-llm-judge`'s
   `--live` mode against a real model.
3. The OTel GenAI semconv repo itself (skim the actual spec files, not just
   a blog post about them) alongside Langfuse's or Phoenix's self-host docs,
   before extending `code/04-tracing-otel` to a real backend.
4. Rao & Callison-Burch's agreement-metrics paper, as a corrective to
   over-trusting any single reported kappa number - including this repo's
   own in `code/03`.
5. The Maven course (paid) or the forthcoming O'Reilly book, once you want
   more depth or live cohort feedback than a self-paced repository can give.
