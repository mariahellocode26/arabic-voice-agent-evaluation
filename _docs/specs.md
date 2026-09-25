# Arabic Voice Agent Evaluation

## 1. Project Overview

This project evaluates whether OpenAI voice models are suitable for building customer-service voice agents that need to understand and respond naturally in Arabic dialects.

The initial evaluation focuses on:

* Egyptian Arabic
* Kuwaiti Arabic

The project uses realistic customer-service scenarios such as booking, cancellation, availability questions, dates, times, numbers, and Arabic/English code-switching.

The goal is to identify the strengths, limitations, and failure cases of the voice model before investing in a full phone-based AI receptionist.

---

## 2. Research Question

> Can an OpenAI voice model reliably understand and respond to Egyptian and Kuwaiti Arabic in realistic customer-service voice-agent scenarios?

The evaluation should measure both **technical accuracy** and **conversation quality**.

---

## 3. Goals

### Primary Goals

* Evaluate Arabic speech recognition quality.
* Evaluate intent understanding.
* Evaluate entity extraction.
* Evaluate response quality.
* Evaluate dialect handling.
* Evaluate Arabic/English code-switching.
* Measure response latency.
* Identify common failure patterns.
* Compare Egyptian Arabic and Kuwaiti Arabic results.
* Determine whether further development of a voice receptionist is justified.

### Secondary Goals

* Establish a reusable evaluation framework.
* Make it easy to add additional Arabic dialects.
* Make it easy to evaluate different OpenAI voice models.
* Produce measurable results that can be included in a portfolio or technical interview.

---

## 4. Non-Goals

This project does **not** initially build a complete voice receptionist.

The following are intentionally outside the initial scope:

* Twilio phone integration
* SIP infrastructure
* Appointment/booking backend
* Production database
* Authentication
* Multi-user support
* Production deployment
* Complex agent frameworks
* Kubernetes
* Production monitoring infrastructure
* Full web application

These may be added later if the evaluation shows that the voice model is suitable.

---

# 5. Evaluation Languages

## Egyptian Arabic

Dataset prefix:

`EG`

Examples:

* EG001
* EG002
* EG003

Directory:

```text
data/egyptian/
```

## Kuwaiti Arabic

Dataset prefix:

`KW`

Examples:

* KW001
* KW002
* KW003

Directory:

```text
data/kuwaiti/
```

---

# 6. Test Dataset

Each dialect initially contains 50 test cases.

Each test case contains:

```text
id
dialect
category
difficulty
context_type
text
expected_intent
expected_entities
```

### Test Categories

| Category          | Purpose                                          |
| ----------------- | ------------------------------------------------ |
| Greetings         | Basic conversational interaction                 |
| General questions | Understanding general customer questions         |
| Services          | Understanding questions about available services |
| Availability      | Understanding availability requests              |
| Booking           | Understanding booking requests                   |
| Cancellation      | Understanding cancellation requests              |
| Rescheduling      | Understanding changes to existing bookings       |
| Dates & times     | Understanding Arabic date/time expressions       |
| Numbers           | Understanding phone numbers, quantities, etc.    |
| Code switching    | Handling Arabic mixed with English               |

---

# 7. Audio Dataset

The evaluation should eventually use real human recordings because synthetic TTS audio does not fully represent real-world callers.

## Initial Phase

Use AI-generated speech for rapid experimentation.

Generate the first 5 cases for each dialect:

```text
EG001–EG005
KW001–KW005
```

Output:

```text
audio/
├── egyptian/
│   ├── EG001.mp3
│   ├── EG002.mp3
│   ├── EG003.mp3
│   ├── EG004.mp3
│   └── EG005.mp3
└── kuwaiti/
    ├── KW001.mp3
    ├── KW002.mp3
    ├── KW003.mp3
    ├── KW004.mp3
    └── KW005.mp3
```

If the initial results are promising, expand to the complete dataset.

## Final Evaluation

Use representative human recordings where possible.

The human recordings should include variation in:

* Speaker
* Accent
* Speaking speed
* Background noise
* Pronunciation
* Code-switching
* Natural conversational phrasing

---

# 8. Evaluation Pipeline

The basic evaluation pipeline is:

```text
Test Case
    ↓
Audio Input
    ↓
OpenAI Voice Model
    ↓
Transcription
    ↓
Intent / Entity Evaluation
    ↓
Response Evaluation
    ↓
Latency Measurement
    ↓
Store Results
    ↓
Failure Analysis
```

---

# 9. Metrics

## 9.1 Speech Recognition

Measure transcription quality using:

### Word Error Rate (WER)

Compare:

```text
Expected text
      vs.
Model transcription
```

Arabic normalization should be applied before calculating WER.

Normalization may include:

* Removing punctuation
* Normalizing whitespace
* Handling Arabic diacritics
* Normalizing common orthographic variations

Both raw and normalized transcripts should be preserved.

---

## 9.2 Intent Accuracy

Determine whether the model understood the customer's intended action.

Example:

```text
Expected:
create_booking

Model:
create_booking

Result:
correct
```

Possible intents include:

```text
greeting
general_question
service_information
check_availability
create_booking
cancel_booking
reschedule_booking
date_time_question
number_information
```

Metric:

```text
Intent Accuracy =
Correct Intent Predictions / Total Test Cases
```

---

## 9.3 Entity Accuracy

Evaluate whether important entities were correctly understood.

Examples:

```text
service
date
time
phone number
customer name
quantity
```

Example:

```text
Expected:
service = consultation
date = Thursday
time = 6 PM

Model:
service = consultation
date = Thursday
time = 6 PM

Result:
correct
```

Entity evaluation should account for partial correctness where appropriate.

---

# 10. Response Quality

Evaluate whether the generated response is appropriate for a customer-service voice agent.

Consider:

* Correctness
* Relevance
* Groundedness
* Completeness
* Naturalness
* Appropriate conversational tone
* Arabic language consistency
* Dialect appropriateness

For the initial evaluation, human review can be used instead of building a complex automated evaluator.

Suggested rating:

```text
1 = Poor
2 = Weak
3 = Acceptable
4 = Good
5 = Excellent
```

---

# 11. Dialect Quality

Evaluate whether the model handles the intended dialect naturally.

### Egyptian Arabic

Evaluate:

* Egyptian vocabulary
* Common expressions
* Pronunciation
* Natural phrasing
* Egyptian/English code-switching

### Kuwaiti Arabic

Evaluate:

* Kuwaiti vocabulary
* Common expressions
* Pronunciation
* Natural phrasing
* Kuwaiti/English code-switching

Important:

Dialect quality should be evaluated separately from basic semantic correctness.

A response can understand the user's intent correctly while still sounding unnatural for the target dialect.

---

# 12. Code-Switching

Some customer conversations may naturally mix Arabic and English.

Examples:

```text
عايز أعمل booking لبكرة
```

or:

```text
ممكن cancel الحجز؟
```

Evaluate whether the model:

* Understands the English words in context.
* Preserves their intended meaning.
* Responds coherently.
* Avoids unnecessary translation.
* Maintains the target Arabic dialect.

---

# 13. Conversation Context

After the initial single-turn evaluation, add multi-turn scenarios.

Example:

```text
Customer:
عايز أحجز كشف بكرة.

Agent:
أكيد، تحب الساعة كام؟

Customer:
الساعة ستة.

Agent:
تمام، هحجزلك الساعة ستة.
```

Evaluate whether the model correctly maintains:

* Intent
* Previously provided information
* Dates
* Times
* Services
* Customer information

Initial target:

```text
5 multi-turn scenarios per dialect
```

---

# 14. Voice Quality

Human evaluation should consider:

* Naturalness
* Pronunciation
* Intelligibility
* Speaking speed
* Voice consistency
* Dialect authenticity
* Customer-service tone
* Appropriate pauses

Use a 1–5 rating scale.

---

# 15. Latency

Measure voice-agent responsiveness.

Important metric:

```text
Time to First Audio
```

Measure the time between the user's completed utterance and the beginning of the model's audio response.

Also record:

```text
Total response latency
```

Latency should eventually be evaluated under realistic conversational conditions.

---

# 16. Failure Analysis

The evaluation should not only produce aggregate metrics.

Every failed test should be analyzed.

Potential failure categories:

```text
speech_recognition
dialect
slang
code_switching
date
time
numbers
entity_extraction
intent
context
response_quality
latency
pronunciation
```

Example:

```text
EG023
Category: booking

Failure:
Model correctly understood the booking intent but interpreted
"بعد المغرب" incorrectly.

Failure category:
time_expression
```

The goal is to understand **why** the system fails, not only how often it fails.

---

# 17. Results

Store evaluation results in CSV format.

Example:

```text
id
dialect
category
speaker
transcription
transcription_correct
intent_correct
entities_correct
dialect_quality
response_quality
latency_ms
failure_category
notes
```

Results should be saved separately:

```text
results/
├── egyptian_results.csv
└── kuwaiti_results.csv
```

---

# 18. Repository Structure

Target structure:

```text
arabic-voice-agent-evaluation/
│
├── notebooks/
│   ├── egyptian_arabic_eval.ipynb
│   └── kuwaiti_arabic_eval.ipynb
│
├── data/
│   ├── egyptian/
│   │   ├── audio/
│   │   └── test_cases.csv
│   │
│   └── kuwaiti/
│       ├── audio/
│       └── test_cases.csv
│
├── src/
│   ├── audio.py
│   ├── openai_client.py
│   ├── evaluation.py
│   └── metrics.py
│
├── results/
│   ├── egyptian_results.csv
│   └── kuwaiti_results.csv
│
├── generate_audio.py
├── README.md
├── spec.md
├── pyproject.toml
├── .env
└── .gitignore
```

The implementation should remain simple. Shared functionality should move into `src/` only when duplication becomes meaningful.

---

# 19. Notebook Design

There should be two independent notebooks.

## Egyptian Arabic

```text
notebooks/egyptian_arabic_eval.ipynb
```

The notebook should:

1. Load the Egyptian test cases.
2. Load the corresponding audio.
3. Send audio to the OpenAI voice model.
4. Capture the model output.
5. Evaluate transcription.
6. Evaluate intent.
7. Evaluate entities.
8. Evaluate response quality.
9. Measure latency.
10. Display failures.
11. Save results.
12. Summarize metrics.

## Kuwaiti Arabic

```text
notebooks/kuwaiti_arabic_eval.ipynb
```

Follow the same structure using the Kuwaiti dataset.

Keeping the notebooks separate makes dialect-specific analysis easier.

---

# 20. Development Phases

## Phase 1 — Dataset

* Create 50 Egyptian Arabic test cases.
* Create 50 Kuwaiti Arabic test cases.
* Review expected intents and entities.

## Phase 2 — Initial Audio

Generate:

```text
5 Egyptian
5 Kuwaiti
```

Use these to validate the evaluation pipeline.

## Phase 3 — Egyptian Evaluation

Build:

```text
egyptian_arabic_eval.ipynb
```

Run the initial 5 cases.

## Phase 4 — Kuwaiti Evaluation

Build:

```text
kuwaiti_arabic_eval.ipynb
```

Run the initial 5 cases.

## Phase 5 — Full Dataset

If the initial results justify continuing:

```text
50 Egyptian
50 Kuwaiti
```

Run the complete evaluation.

## Phase 6 — Human Audio

Replace or supplement synthetic audio with human recordings.

## Phase 7 — Multi-Turn Evaluation

Add multi-turn customer-service conversations.

## Phase 8 — Analysis

Produce:

* Metric summaries
* Failure analysis
* Dialect comparison
* Example successes
* Example failures
* Recommendations for further testing

---

# 21. Success Criteria

The project should not define success as simply "the model works."

Instead, the evaluation should provide enough evidence to answer:

1. How accurately does the model understand each dialect?
2. How accurately does it identify customer intent?
3. How accurately does it extract important entities?
4. How natural are its responses?
5. How well does it maintain the target dialect?
6. How does it handle code-switching?
7. How responsive is it?
8. What types of requests cause failures?
9. Are there meaningful differences between Egyptian and Kuwaiti Arabic?
10. Is the evidence strong enough to justify building a real voice receptionist prototype?

---

# 22. Future Extension — Voice Receptionist

If the evaluation results support continuing, the next project can build a real customer-service voice agent.

Potential architecture:

```text
Customer
   ↓
Phone / Telephony
   ↓
Real-time Voice Model
   ↓
Tool Calling
   ↓
FastAPI Backend
   ↓
├── PostgreSQL
├── Booking System
├── Customer Data
└── Company Knowledge / RAG
   ↓
Tool Result
   ↓
Voice Model
   ↓
Customer
```

Potential tools:

```text
check_availability
create_booking
cancel_booking
reschedule_booking
get_customer
search_company_information
```

The voice model should decide **when a tool is needed**, while the backend should validate and execute the actual operation.

This evaluation project should remain independent from the receptionist implementation so that the voice-model decision is based on measured evidence rather than assumptions.

---

# 23. Engineering Principles

Keep the project:

* Simple
* Reproducible
* Modular
* Measurable
* Easy to extend
* Easy to understand

Avoid premature complexity.

Do not introduce:

* Kubernetes
* Microservices
* Kafka
* Complex agent frameworks
* Dedicated vector databases
* Production infrastructure

unless a later requirement actually justifies them.

The primary objective is to produce **credible evaluation evidence**, not infrastructure complexity.
