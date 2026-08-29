# Security Policy

ai-evals is a set of educational docs and small, self-contained Python
sample programs. No sample runs a persistent service, and by default no
sample makes a network call at all - so the realistic attack surface is
narrow.

## What belongs in a report

Worth reporting privately:

- A sample that does something unsafe with untrusted input - none are
  designed to take untrusted input beyond their own fixture data or (in
  `--live` mode) a prompt you supply yourself, so this would itself be a
  bug.
- `code/common/llm_client.py` or any sample handling an API key
  (`ANTHROPIC_API_KEY`/`OPENAI_API_KEY`) in a way that could leak it - e.g.
  logging it, writing it to a fixture file, or sending it somewhere other
  than the intended provider's SDK.
- A script or dependency that fetches and executes something from the
  network without saying so.

Not a security issue, just a normal bug report (open a public issue
instead):

- A sample that produces the wrong output.
- A dead or incorrect link, or a stale claim, in the curated resources.
- `code/03-llm-judge`'s heuristic judges being wrong about a specific case
  - that's the entire teaching point of that stage, not a bug.

## Reporting a vulnerability

Use GitHub's private vulnerability reporting:

> https://github.com/Laaaaksh/ai-evals/security/advisories/new

That reaches the maintainer privately so any real issue can be fixed before
it's discussed in public.

## Credits

Reporters who wish to be credited may say so in the private report;
otherwise reports are handled without attribution.
