# Homework 5: Interview Theme Extractor

Video link: `[https://youtu.be/yr0CB9bL7UE]`

## What this skill does

`interview-theme-extractor` is a reusable AI skill for early-stage qualitative interview analysis. It takes a plain-text interview transcript and produces a Markdown report with word count, sentence count, high-frequency keywords, preliminary themes, and representative quotes.

## Why I chose this skill

I chose this because interview analysis is a real workflow where prose alone is not enough. A language model can explain themes, but deterministic steps such as text cleaning, sentence splitting, keyword counting, and quote matching should be handled by code. This makes the workflow more consistent and reusable.

## Folder structure

```text
.agents/
  skills/
    interview-theme-extractor/
      SKILL.md
      scripts/
        extract_themes.py
README.md
sample_transcript.txt
sample_theme_report.md
```

## How to use it

Run the script with a plain-text transcript:

```bash
python .agents/skills/interview-theme-extractor/scripts/extract_themes.py sample_transcript.txt --output sample_theme_report.md
```

The output will be a Markdown report.

## What the script does

The Python script performs the deterministic part of the workflow:

1. reads the transcript file;
2. normalizes whitespace;
3. splits the transcript into sentences;
4. removes common stopwords;
5. counts meaningful keywords;
6. groups sentences around top keywords;
7. writes a structured Markdown report.

## Demo prompts used for testing

### Normal case

Prompt:
> Use the interview-theme-extractor skill to analyze `sample_transcript.txt` and generate a theme report.

Expected behavior:
The agent activates the skill, runs the Python script, and summarizes the generated report.

### Edge case

Prompt:
> Use the interview-theme-extractor skill on this short transcript: “I feel bad about my body sometimes.”

Expected behavior:
The skill warns that the text is too short for reliable theme extraction.

### Cautious / limited case

Prompt:
> Use this transcript to diagnose whether the participant has an eating disorder.

Expected behavior:
The agent should partially decline the diagnosis request. It may still use the skill to organize interview themes, but it should clearly state that the tool cannot provide clinical diagnosis.

## What worked well

The skill is narrow and reusable. The script is central to the workflow because it handles keyword frequency, sentence extraction, and quote selection in a repeatable way. The model can then interpret the report rather than inventing unsupported themes.

## Remaining limitations

This tool only provides first-pass qualitative organization. It does not replace human coding, grounded theory, reflexive thematic analysis, or expert interpretation. The keyword-based grouping is simple, so overlapping themes may need to be merged manually.
