# Credits And Provenance

This repository is a derivative laptop-scale exploration of the official ELF implementation.

## Original Research

All core ELF research credit belongs to the authors of:

> Hu, Keya and Qiu, Linlu and Lu, Yiyang and Zhao, Hanhong and Li, Tianhong and Kim, Yoon and Andreas, Jacob and He, Kaiming. "ELF: Embedded Language Flows." arXiv preprint arXiv:2605.10938, 2026.

Paper: https://arxiv.org/abs/2605.10938

The upstream implementation was cloned from:

https://github.com/lillian039/ELF

The license file is retained from the upstream repository.

## External Assets And Data

- TinyStories dataset: `roneneldan/TinyStories`, used only as a small laptop-scale training/evaluation source.
- T5 tokenizer and encoder components: `t5-small` and the ELF authors' referenced Hugging Face encoder checkpoint path.
- Hugging Face datasets and transformers libraries are used for local data preparation.

## Local Exploration Additions

The laptop exploration added:

- CPU dependency file.
- TinyStories preparation script.
- Tiny `ELF-T` / `ELF-XS` model variants for laptop experiments.
- Laptop training and sampling configs.
- Generation analysis script.
- Interactive terminal sampler.
- Experiment results and timeline docs.
