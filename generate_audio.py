"""Generate an initial audio dataset from the Egyptian and Kuwaiti Arabic test cases.

This script converts the first few rows of each dialect's test-case CSV into
speech using OpenAI's text-to-speech API (gpt-4o-mini-tts, "marin" voice), so
we have a small audio dataset to validate the voice-agent evaluation pipeline
before generating audio for the full 50-case dataset per dialect.

Usage:
    python generate_audio.py

Requires an OPENAI_API_KEY in a .env file in the repo root (see README.md).
"""

import csv
import os

from dotenv import load_dotenv
from openai import OpenAI

# --- Configuration -----------------------------------------------------

# TTS model and voice to use for every generated file.
TTS_MODEL = "gpt-4o-mini-tts"
TTS_VOICE = "marin"

# Only generate audio for the first N rows of each CSV for this initial
# experiment (see _docs/specs.md, Phase 2 - Initial Audio).
NUM_INITIAL_CASES = 5

# Each dialect's source CSV and the human-readable dialect name used in the
# instructions we send to the TTS model.
DIALECTS = [
    {
        "csv_path": "egyptian_arabic_test_cases.csv",
        "audio_dir": os.path.join("audio", "egyptian"),
        "dialect_name": "Egyptian Arabic",
    },
    {
        "csv_path": "kuwaiti_arabic_test_cases.csv",
        "audio_dir": os.path.join("audio", "kuwaiti"),
        "dialect_name": "Kuwaiti Arabic",
    },
]


def build_instructions(dialect_name: str) -> str:
    """Build TTS instructions telling the model how to speak this dialect."""
    return (
        f"Speak naturally in {dialect_name}, as a native speaker would in a "
        "real phone conversation. Preserve the exact wording given - do not "
        "translate, paraphrase, or switch to Modern Standard Arabic. Use a "
        "natural, warm, conversational customer-service tone, as if talking "
        "to a customer on the phone."
    )


def read_first_n_cases(csv_path: str, n: int) -> list[dict]:
    """Read the first n rows of a test-case CSV."""
    # encoding="utf-8-sig" strips the UTF-8 BOM these CSVs start with, so the
    # "id" column header isn't misread as "﻿id".
    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            rows.append(row)
            if len(rows) >= n:
                break
    return rows


def generate_case_audio(client: OpenAI, case: dict, instructions: str, output_path: str) -> None:
    """Generate one MP3 file for a single test case using the TTS API."""
    with client.audio.speech.with_streaming_response.create(
        model=TTS_MODEL,
        voice=TTS_VOICE,
        input=case["text"],
        instructions=instructions,
    ) as response:
        response.stream_to_file(output_path)


def main() -> None:
    load_dotenv()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit(
            "OPENAI_API_KEY is not set. Create a .env file in the repo root "
            "with:\n\n    OPENAI_API_KEY=your-key-here\n"
        )

    client = OpenAI(api_key=api_key)

    for dialect in DIALECTS:
        os.makedirs(dialect["audio_dir"], exist_ok=True)
        instructions = build_instructions(dialect["dialect_name"])

        print(f"\n=== {dialect['dialect_name']} ===")
        cases = read_first_n_cases(dialect["csv_path"], NUM_INITIAL_CASES)

        for case in cases:
            case_id = case["id"]
            output_path = os.path.join(dialect["audio_dir"], f"{case_id}.mp3")

            print(f"Generating {case_id} -> {output_path} ...")
            try:
                generate_case_audio(client, case, instructions, output_path)
                print(f"  done: {output_path}")
            except Exception as exc:  # noqa: BLE001 - continue past per-case API errors
                print(f"  FAILED {case_id}: {exc}")
                continue

    print("\nAudio generation complete.")


if __name__ == "__main__":
    main()
