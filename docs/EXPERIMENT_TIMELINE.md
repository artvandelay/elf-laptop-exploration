# Experiment Timeline

## 1. Paper Capture And Local Source Copy

The first phase archived the ELF paper materials locally:

- downloaded the arXiv source bundle for `2605.10938v1`,
- compiled the LaTeX source to a local PDF,
- mirrored the arXiv HTML page with supporting assets for offline reading,
- kept the official paper source separate from the code repository.

This established the paper as the conceptual reference for later code exploration.

## 2. Concept Walkthrough

The next phase converted the paper's idea into compact training and inference pseudocode:

- tokens are mapped into continuous embeddings,
- denoising happens mostly in embedding space,
- the model predicts clean embeddings and converts that to velocity,
- final discretization happens at the decode step,
- the same shared ELF network supports denoising and decoding modes.

The scope was then narrowed from general modality questions to training mechanics and actual function calls in the repository.

## 3. Upstream Repository Clone

The official implementation was cloned from:

```text
https://github.com/lillian039/ELF
```

The clone was placed at:

```text
/Users/jigar/projects/0n-going/ELF-Paper/ELF
```

## 4. Laptop Training Path

The exploration then focused on whether ELF could run on a normal laptop:

- created a CPU-oriented dependency file,
- created a Python environment with `uv` under `~/pyenv/elf-laptop`,
- added a TinyStories preparation script,
- added a tiny `ELF-T` model factory,
- added a laptop training config and 16-step sampling config,
- disabled online GPT-2-large perplexity evaluation for the small run.

The target changed from reproducing paper-scale metrics to validating an end-to-end working implementation.

## 5. Pilot Experiments

Short runs were used to find a safe laptop configuration:

- smoke run: 1 epoch, batch size 8,
- speed test: 1 epoch, batch size 16,
- medium run: 5 epochs,
- longer stage-3 run: 20 epochs.

The evidence favored batch size 8 because it gave a stronger quality signal than the larger batch despite the small scale.

## 6. Stage-3 Working Checkpoint

The main confirmed run was:

```text
model: ELF-T
dataset: TinyStories slice
train examples: 2,000
eval examples: 64
max_length: 64
batch size: 8
epochs: 20
steps: 5,000
```

The run finished cleanly and wrote:

- `checkpoint_5000`,
- generation samples,
- a full local training log.

Final logged values:

```text
step=5000
loss=0.9338
l2=0.7588
ce=1.6337
steps/sec=5.38
```

## 7. Post-Run Analysis

`scripts/analyze_generations.py` was added to compare generated JSONL files with simple quality signals:

- average length,
- distinct token ratios,
- adjacent repetition ratio,
- prefix diversity,
- most common tokens.

This made it easier to distinguish a working but weak model from a stuck or non-learning run.

## 8. Interactive Model CLI

`src/interact.py` was added to make the trained checkpoint inspectable from a terminal.

The CLI:

- loads a checkpoint once,
- generates samples interactively,
- prints runtime/debug stats,
- logs session events to JSONL,
- supports commands such as `/gen`, `/samples`, `/sample`, `/steps`, `/seed`, `/cfg`, `/sccfg`, `/debug`, and `/quit`.

The current trained checkpoint is unconditional. User text after `/gen` is logged but does not condition the generated sample.

## 9. Current Conclusion

The project has a working laptop-scale ELF implementation path:

```text
data -> tokenizer -> encoder -> ELF training -> checkpoint -> sampling -> interactive inspection
```

The checkpoint is not a strong language model. It is a working implementation suitable for research instrumentation, ablations, and experiments around the ELF training/sampling mechanics.
