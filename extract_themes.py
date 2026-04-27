#!/usr/bin/env python3
"""
Interview Theme Extractor

A deterministic helper script for early-stage qualitative interview analysis.
It extracts frequent meaningful keywords, groups transcript sentences around
those keywords, and outputs a Markdown report with representative quotes.
"""

import argparse
import re
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

STOPWORDS = {
    "about", "above", "after", "again", "against", "also", "although", "always",
    "because", "before", "being", "below", "between", "could", "does", "doing",
    "during", "each", "from", "further", "have", "having", "here", "hers", "herself",
    "himself", "into", "itself", "just", "more", "most", "other", "over", "same",
    "should", "some", "such", "than", "that", "their", "theirs", "them", "themselves",
    "then", "there", "these", "they", "this", "those", "through", "under", "until",
    "very", "what", "when", "where", "which", "while", "with", "would", "your",
    "youre", "youve", "dont", "cant", "wont", "didnt", "isnt", "wasnt", "were",
    "been", "like", "feel", "felt", "think", "really", "maybe", "kind", "sort",
    "interviewer", "participant"
}


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    return path.read_text(encoding="utf-8")


def split_sentences(text: str) -> List[str]:
    text = re.sub(r"\s+", " ", text.strip())
    raw_sentences = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [s.strip() for s in raw_sentences if len(s.strip()) > 15]


def tokenize(text: str) -> List[str]:
    words = re.findall(r"\b[a-zA-Z][a-zA-Z'-]{3,}\b", text.lower())
    clean_words = []
    for word in words:
        word = word.strip("'-")
        if word and word not in STOPWORDS:
            clean_words.append(word)
    return clean_words


def extract_keywords(text: str, top_n: int) -> List[Tuple[str, int]]:
    return Counter(tokenize(text)).most_common(top_n)


def group_sentences_by_keyword(sentences: List[str], keywords: List[Tuple[str, int]], quotes_per_theme: int) -> Dict[str, List[str]]:
    groups: Dict[str, List[str]] = {}
    for keyword, _ in keywords:
        matching = []
        pattern = re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)
        for sentence in sentences:
            if pattern.search(sentence):
                matching.append(sentence)
        if matching:
            groups[keyword] = matching[:quotes_per_theme]
    return groups


def build_markdown_report(text: str, top_n: int, quotes_per_theme: int) -> str:
    sentences = split_sentences(text)
    keywords = extract_keywords(text, top_n)
    themes = group_sentences_by_keyword(sentences, keywords[: min(6, len(keywords))], quotes_per_theme)
    word_count = len(re.findall(r"\b\w+\b", text))

    lines = []
    lines.append("# Interview Theme Extraction Report")
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- Word count: {word_count}")
    lines.append(f"- Sentence count: {len(sentences)}")
    lines.append(f"- Candidate themes generated: {len(themes)}")
    lines.append("")

    if word_count < 80 or len(sentences) < 3:
        lines.append("## Caution")
        lines.append("The input is short, so the extracted themes may not be reliable. Add more interview text before using this for research interpretation.")
        lines.append("")

    lines.append("## Top Keywords")
    if keywords:
        for word, count in keywords:
            lines.append(f"- {word}: {count}")
    else:
        lines.append("No meaningful keywords were found.")
    lines.append("")

    lines.append("## Preliminary Themes and Representative Quotes")
    if themes:
        for index, (theme, quotes) in enumerate(themes.items(), start=1):
            lines.append(f"### Theme {index}: {theme}")
            lines.append(f"This theme appears in {len(quotes)} representative sentence(s) selected by keyword matching.")
            lines.append("")
            for quote in quotes:
                lines.append(f"> {quote}")
                lines.append("")
    else:
        lines.append("No preliminary themes could be generated from the input.")
        lines.append("")

    lines.append("## Suggested Next Steps")
    lines.append("- Review the candidate themes manually.")
    lines.append("- Merge overlapping themes where appropriate.")
    lines.append("- Compare these preliminary themes with the research question.")
    lines.append("- Use human coding before making final academic claims.")
    lines.append("")

    lines.append("## Limitation")
    lines.append("This report is a first-pass computational organization of the transcript. It does not replace grounded theory, reflexive thematic analysis, or human interpretation.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract preliminary qualitative themes from an interview transcript.")
    parser.add_argument("input", help="Path to a plain-text interview transcript")
    parser.add_argument("--output", "-o", default="theme_report.md", help="Path for the Markdown output report")
    parser.add_argument("--top-n", type=int, default=12, help="Number of keywords to include")
    parser.add_argument("--quotes-per-theme", type=int, default=3, help="Maximum representative quotes per theme")
    args = parser.parse_args()

    text = read_text(Path(args.input))
    report = build_markdown_report(text, args.top_n, args.quotes_per_theme)
    Path(args.output).write_text(report, encoding="utf-8")
    print(f"Report written to {args.output}")


if __name__ == "__main__":
    main()
