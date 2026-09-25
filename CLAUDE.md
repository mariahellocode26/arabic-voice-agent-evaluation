# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project evaluates whether OpenAI voice models can reliably understand and respond to **Egyptian Arabic** and **Kuwaiti Arabic** in realistic customer-service voice-agent scenarios (booking, cancellation, availability, dates/times, numbers, Arabic/English code-switching). It measures both technical accuracy (transcription, intent, entities, latency) and conversation quality (naturalness, dialect authenticity, response quality) to decide whether investing in a full phone-based AI receptionist is justified.

The full specification lives in [_docs/specs.md](_docs/specs.md) — read it before implementing any evaluation pipeline, metric, or notebook, since it defines the exact schema, metrics, and phased plan this project follows.

**Current state:** the repository only contains the spec and the two dialect test-case datasets. None of the code (`src/`, notebooks, `generate_audio.py`) described in the target structure exists yet — this is Phase 1 (Dataset) of the plan in `_docs/specs.md` §20.

## Repository Structure (target, per spec)

The spec defines this target layout; build toward it rather than inventing a different structure:

```
notebooks/
├── egyptian_arabic_eval.ipynb
└── kuwaiti_arabic_eval.ipynb
data/
├── egyptian/{audio/, test_cases.csv}
└── kuwaiti/{audio/, test_cases.csv}
src/
├── audio.py
├── openai_client.py
├── evaluation.py
└── metrics.py
results/
├── egyptian_results.csv
└── kuwaiti_results.csv
generate_audio.py
```

Keep the two dialects' notebooks and results independent/parallel (never merged) so dialect-specific analysis and comparison stay easy — this mirrors the current top-level split between `egyptian_arabic_test_cases.csv` and `kuwaiti_arabic_test_cases.csv`.

## Test Case Dataset

`egyptian_arabic_test_cases.csv` and `kuwaiti_arabic_test_cases.csv` share one schema:

```
id, dialect, category, difficulty, context_type, text, expected_intent, expected_entities
```

- IDs are prefixed `EG###` / `KW###`.
- `expected_entities` uses `key=value` pairs separated by `;` (e.g. `date=tomorrow;time_period=afternoon`), and is left blank when no entity is expected.
- Categories: greeting, general, services, availability, booking, cancellation, rescheduling, date_time, numbers, code_switching — see the category table in `_docs/specs.md` §6 for the intent behind each.
- Valid `expected_intent` values are the fixed set listed in `_docs/specs.md` §9.2 (e.g. `greeting`, `check_availability`, `create_booking`, `cancel_booking`, `reschedule_booking`, `provide_information`, `pricing_question`, `confirmation`). Keep new test cases consistent with this vocabulary rather than inventing new intents ad hoc.

## Engineering Principles (from spec)

- Keep the implementation simple, reproducible, modular, measurable, and easy to extend; only move shared code into `src/` when duplication actually becomes meaningful.
- Do not introduce Kubernetes, microservices, Kafka, complex agent frameworks, dedicated vector databases, or production infrastructure — this is an evaluation project, not the production voice receptionist.
- Explicit non-goals for this project: Twilio/SIP integration, a booking backend, a production database, auth, multi-user support, production deployment. These belong to the separate future "voice receptionist" project described in `_docs/specs.md` §22, which should stay independent from this evaluation codebase.

## Commands

No build/lint/test tooling exists yet (no `pyproject.toml`, notebooks, or `src/` package). When adding them, follow the spec's target structure above rather than a different layout, and update this section with the actual commands once they exist.
