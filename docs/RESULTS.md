# Laptop Experiment Results

## Scope

This experiment tested whether the ELF implementation can run end-to-end on a laptop-scale CPU setup. It was not intended to reproduce paper-scale quality.

The verified path was:

```text
TinyStories slice -> T5 tokenization -> ELF-T training -> checkpoint -> eval sampling -> interactive CLI sampling
```

## Main Finding

The implementation works as a research sandbox. The tiny model trains, loss decreases, checkpoints save/load, evaluation runs, and generated samples become recognizably TinyStories-shaped.

It should not be described as a high-quality language model or as a paper-scale reproduction.

## Best Confirmed Run

- Model: `ELF-T`
- Dataset: TinyStories, 2,000 train examples / 64 eval examples
- Sequence length: 64
- Batch size: 8
- Epochs: 20
- Steps: 5,000
- Sampling: 16-step SDE, CFG 1, self-conditioning CFG 3
- Final checkpoint: `outputs/elf_t-tinystories-stage3-20e/checkpoint_5000`

Final logged training values:

- `loss=0.9338`
- `l2=0.7588`
- `ce=1.6337`
- `steps/sec=5.38`

Final generation completed successfully and wrote local JSONL samples.

## Qualitative Readout

The trained checkpoint produces TinyStories-like text with common motifs such as:

- "Once upon a time"
- Lily, Jack, Tim
- parks, trees, flowers, friends, mom/dad
- short adventure-like story fragments

The generations are still rough. They show syntax errors, repeated words, and template collapse. That is expected for the intentionally tiny model, tiny dataset slice, short context length, and CPU run.

Representative sample:

```text
Once upon a time, there was a little boy named Jack. Tim was very happy and He liked to explore. Everyone made it he was very sad. One day, while the tree in the garden and ran to the park. He ran to it. He s help his to find it.
```

## Analyzer Signals

The generation analyzer was added to avoid relying only on subjective reading.

Use:

```bash
python scripts/analyze_generations.py outputs/elf_t-tinystories-stage3-20e
```

Useful fields:

- `distinct1` and `distinct2`: crude diversity signals.
- `adjacent_repeat_ratio`: lower is better for repetition.
- `prefix_diversity`: lower values indicate repeated openings/templates.
- `top_tokens`: quick view of collapse into common motifs.

Observed trend:

- The 5-epoch medium run still had heavy adjacent repetition.
- The 20-epoch run reduced adjacent repetition substantially.
- The model still has repeated story templates, especially "Once upon a time".

## Research Interpretation

This is enough for implementation-level research questions:

- instrumenting the training loop,
- testing changes to the flow path,
- probing the decode branch,
- trying alternative discrete modalities,
- adding conditional inputs,
- measuring sampler/debug behavior.

This is not enough for quality claims:

- not a chatbot,
- not prompt-following,
- not paper-scale ELF,
- not suitable for language-model benchmark claims.
