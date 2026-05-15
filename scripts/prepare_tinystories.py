#!/usr/bin/env python
"""Tokenize a tiny slice of TinyStories with the T5 tokenizer and save it
locally as a HuggingFace Arrow dataset for ELF training/eval.

Two splits are produced:
  - train: the first N_TRAIN examples
  - eval:  the next N_EVAL examples

Each example has only `input_ids` (unconditional generation).
"""

import argparse
import os

from datasets import load_dataset
from transformers import T5Tokenizer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_train", type=int, default=2000)
    parser.add_argument("--n_eval", type=int, default=64)
    parser.add_argument("--max_length", type=int, default=64)
    parser.add_argument(
        "--out_dir",
        type=str,
        default=os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "tinystories_t5"),
    )
    parser.add_argument("--tokenizer_name", type=str, default="t5-small")
    args = parser.parse_args()

    print(f"Loading TinyStories streaming and tokenizer {args.tokenizer_name}...")
    tok = T5Tokenizer.from_pretrained(args.tokenizer_name)

    raw = load_dataset("roneneldan/TinyStories", split="train", streaming=True)

    def take(stream, n):
        out = []
        for i, ex in enumerate(stream):
            if i >= n:
                break
            out.append(ex)
        return out

    print(f"Pulling first {args.n_train + args.n_eval} stories...")
    pulled = take(raw, args.n_train + args.n_eval)
    train_raw = pulled[: args.n_train]
    eval_raw = pulled[args.n_train : args.n_train + args.n_eval]

    def tokenize_split(examples):
        ids_list = []
        for ex in examples:
            ids = tok(ex["text"], add_special_tokens=False, truncation=True, max_length=args.max_length)["input_ids"]
            ids_list.append({"input_ids": ids})
        return ids_list

    print("Tokenizing...")
    train_tok = tokenize_split(train_raw)
    eval_tok = tokenize_split(eval_raw)

    from datasets import Dataset

    train_ds = Dataset.from_list(train_tok)
    eval_ds = Dataset.from_list(eval_tok)

    train_out = os.path.join(args.out_dir, "train")
    eval_out = os.path.join(args.out_dir, "eval")
    os.makedirs(args.out_dir, exist_ok=True)
    train_ds.save_to_disk(train_out)
    eval_ds.save_to_disk(eval_out)

    print(f"Saved train ({len(train_ds)} ex) to {train_out}")
    print(f"Saved eval  ({len(eval_ds)} ex) to {eval_out}")
    print("Example train tokens:", train_tok[0]["input_ids"][:20], "...")


if __name__ == "__main__":
    main()
