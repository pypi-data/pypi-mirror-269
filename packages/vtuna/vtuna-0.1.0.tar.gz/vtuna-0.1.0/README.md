
# vtuna

Tuning adapters for visual generation models, a library highly inspired by [torchtune](https://github.com/pytorch/torchtune). 

&nbsp;

## Introduction

`vtuna` is a PyTorch library for easily authoring, fine-tuning and experimenting with visual generation model, especially the text-to-image diffusion model.

[diffusers](https://github.com/huggingface/diffusers) is the go-to library for state-of-the-art pretrained diffusion models. However, if your goal is to develop diffusion adapters that do not yet exist, you will need `vtuna`. The main goal of `vtuna` is to support researchers in freely exploring new adapter technologies for visual generative models.

vtuna provides:

- Easy-to-use and hackable training recipes for popular fine-tuning, adapting techniques (LoRA, IP-Adapter, ControlNet, ELLA...).
- YAML configs for easily configuring training, evaluation or inference recipes.

vtuna focuses on integrating with popular tools and libraries from the ecosystem. These are just a few examples, with more under development:

- [Hugging Face Diffusers](https://github.com/huggingface/diffusers) for diffusion models, pipelines.
- [Hugging Face Hub](https://huggingface.co/docs/hub/en/index) for [accessing model weights](vtuna/_cli/download.py)
- [Hugging Face Datasets](https://huggingface.co/docs/datasets/en/index) for [access](vtuna/datasets/_instruct.py) to training and evaluation datasets
- [Deepspeed](https://www.deepspeed.ai/) for distributed training

&nbsp;

---

## Get Started

`vtuna` is currently under development.

## Design Principles

vtuna embodies PyTorch’s design philosophy [[details](https://pytorch.org/docs/stable/community/design.html)], especially "usability over everything else".

### Simplicity and Extensibility

vtuna is designed to be easy to understand, use and extend.

- Composition over implementation inheritance - layers of inheritance for code re-use makes the code hard to read and extend
- Code duplication is preferred over unnecessary abstractions
- Modular building blocks over monolithic components


## Acknowledgements

This repository is highly inspired by [torchtune](https://github.com/pytorch/torchtune).

## License

vtuna is released under the [Apache License 2.0](./LICENSE).
