#!/usr/bin/env python3
"""Analyze ELF generated JSONL files for quick quality signals.

Usage:
  python scripts/analyze_generations.py \
      outputs/elf_t-tinystories-smoke \
      outputs/elf_t-tinystories-medium5 \
      outputs/elf_t-tinystories-stage3-20e

Accepts JSONL files, directories, and glob patterns. For directories, the script
automatically finds files named all_generated_*.jsonl.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Iterable, List


TOKEN_RE = re.compile(r"[A-Za-z0-9']+")


def collect_jsonl_paths(inputs: Iterable[str]) -> List[Path]:
    paths: List[Path] = []
    for raw in inputs:
        p = Path(raw)
        if p.exists():
            if p.is_file() and p.suffix == ".jsonl":
                paths.append(p)
            elif p.is_dir():
                paths.extend(sorted(p.rglob("all_generated_*.jsonl")))
        else:
            # treat non-existing args as glob patterns
            paths.extend(sorted(Path(".").glob(raw)))
    # de-duplicate while preserving order
    seen = set()
    unique = []
    for p in paths:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            unique.append(rp)
    return unique


def load_generated_texts(path: Path) -> List[str]:
    out: List[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        text = obj.get("generated") or obj.get("output") or obj.get("text")
        if isinstance(text, str):
            out.append(text)
    return out


def tokenize(text: str) -> List[str]:
    return [m.group(0).lower() for m in TOKEN_RE.finditer(text)]


def safe_div(a: float, b: float) -> float:
    return a / b if b else 0.0


def summarize_texts(texts: List[str]) -> dict:
    if not texts:
        return {
            "n": 0,
            "avg_chars": 0.0,
            "avg_words": 0.0,
            "distinct1": 0.0,
            "distinct2": 0.0,
            "adj_repeat": 0.0,
            "prefix_diversity": 0.0,
            "top_tokens": [],
        }

    all_tokens: List[str] = []
    all_bigrams: List[tuple[str, str]] = []
    adj_repeat_count = 0
    adj_pair_count = 0
    prefixes = set()

    for t in texts:
        toks = tokenize(t)
        all_tokens.extend(toks)
        if toks:
            prefixes.add(tuple(toks[:5]))
        if len(toks) > 1:
            pairs = list(zip(toks, toks[1:]))
            all_bigrams.extend(pairs)
            adj_pair_count += len(pairs)
            adj_repeat_count += sum(1 for a, b in pairs if a == b)

    counts = Counter(all_tokens)
    top_tokens = counts.most_common(10)

    return {
        "n": len(texts),
        "avg_chars": sum(len(t) for t in texts) / len(texts),
        "avg_words": sum(len(tokenize(t)) for t in texts) / len(texts),
        "distinct1": safe_div(len(set(all_tokens)), len(all_tokens)),
        "distinct2": safe_div(len(set(all_bigrams)), len(all_bigrams)),
        "adj_repeat": safe_div(adj_repeat_count, adj_pair_count),
        "prefix_diversity": safe_div(len(prefixes), len(texts)),
        "top_tokens": top_tokens,
    }


def print_report(path: Path, summary: dict) -> None:
    print(f"\n=== {path} ===")
    print(f"samples: {summary['n']}")
    print(f"avg_chars: {summary['avg_chars']:.2f}")
    print(f"avg_words: {summary['avg_words']:.2f}")
    print(f"distinct1 (higher better): {summary['distinct1']:.4f}")
    print(f"distinct2 (higher better): {summary['distinct2']:.4f}")
    print(f"adjacent_repeat_ratio (lower better): {summary['adj_repeat']:.4f}")
    print(f"prefix_diversity (higher better): {summary['prefix_diversity']:.4f}")
    print("top_tokens:", ", ".join(f"{tok}:{cnt}" for tok, cnt in summary["top_tokens"]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "inputs",
        nargs="+",
        help="JSONL files, directories, or glob patterns containing all_generated_*.jsonl",
    )
    args = parser.parse_args()

    paths = collect_jsonl_paths(args.inputs)
    if not paths:
        raise SystemExit("No matching JSONL files found.")

    for p in paths:
        texts = load_generated_texts(p)
        summary = summarize_texts(texts)
        print_report(p, summary)


if __name__ == "__main__":
    main()
