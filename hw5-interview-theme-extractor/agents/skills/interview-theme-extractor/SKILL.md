---
name: interview-theme-extractor
description: Extracts preliminary themes, keywords, and representative quotes from qualitative interview transcripts. Use when the user asks to inspect, organize, or summarize interview data for early-stage qualitative analysis.
---

# Interview Theme Extractor

## When to use this skill
Use this skill when the user provides one or more interview transcripts and wants a structured first-pass theme report. This is especially useful for qualitative research, semi-structured interviews, reflection data, student interviews, or exploratory coding.

Good requests include:
- “Extract themes from this interview transcript.”
- “Find repeated concerns in these participant responses.”
- “Give me keywords and representative quotes from this transcript.”
- “Create a preliminary qualitative coding report.”

## When not to use this skill
Do not use this skill when:
- the input is not interview-style text;
- the text is extremely short and cannot support theme extraction;
- the user asks for final academic conclusions without human review;
- the user wants clinical diagnosis, legal judgment, or sensitive personal classification.

If the transcript contains sensitive personal information, remind the user to anonymize names and identifying details before sharing or publishing the output.

## Expected input
The user should provide:
- a plain-text interview transcript, or
- a `.txt` file containing interview text.

The transcript should ideally include multiple sentences or participant responses.

## What the script does
Run `scripts/extract_themes.py` on the transcript. The script performs deterministic text processing:
1. cleans and normalizes the transcript;
2. splits the text into sentences;
3. removes common stopwords;
4. counts keyword frequencies;
5. groups sentences around the highest-frequency meaningful keywords;
6. selects representative quotes;
7. produces a Markdown report.

The script is load-bearing because frequency counting, sentence extraction, keyword ranking, and quote matching need deterministic processing. The model should interpret and explain the result, but the script should produce the structured evidence.

## Recommended workflow
1. Ask the user for the transcript or file.
2. Save the transcript as a temporary `.txt` file if needed.
3. Run:

```bash
python .agents/skills/interview-theme-extractor/scripts/extract_themes.py input.txt --output theme_report.md
```

4. Read the generated report.
5. Present the report to the user with a short explanation.
6. Add a limitation note: this is preliminary qualitative analysis and does not replace human coding.

## Expected output
The output should include:
- word count and sentence count;
- top keywords;
- preliminary themes;
- representative quotes for each theme;
- limitations and suggested next steps.

## Important limitations
This skill does not replace formal grounded theory, thematic analysis, or human coding. It is a first-pass organization tool. The user should review all themes manually and adjust them based on research context.
