# AutoDAN
(💥 News: We have released **[AutoDAN-Turbo](https://autodans.github.io/AutoDAN-Turbo/)**, a **life-long agent** for jailbreak redteaming! It's the newest and SotA attack we have developed! Check it out! [Project](https://autodans.github.io/AutoDAN-Turbo/), [Code](https://github.com/SaFoLab-WISC/AutoDAN-Turbo), [Paper](https://arxiv.org/abs/2410.05295), [AK's recommendation](https://x.com/_akhaliq/status/1844258704633340284) )

The official implementation of our ICLR2024 paper "[AutoDAN: Generating Stealthy Jailbreak Prompts on Aligned Large Language Models](https://arxiv.org/abs/2310.04451)", by *[Xiaogeng Liu](https://sheltonliu-n.github.io), [Nan Xu](https://sites.google.com/site/xunannancy/), [Muhao Chen](https://muhaochen.github.io), and [Chaowei Xiao](https://xiaocw11.github.io).* 

![ICLR 2024](https://img.shields.io/badge/ICLR-2024-blue.svg?style=plastic)
![Jailbreak Attacks](https://img.shields.io/badge/Jailbreak-Attacks-yellow.svg?style=plastic)
![Adversarial Attacks](https://img.shields.io/badge/Adversarial-Attacks-orange.svg?style=plastic)
![Large Language Models](https://img.shields.io/badge/LargeLanguage-Models-green.svg?style=plastic)

## Abstract
The aligned Large Language Models (LLMs) are powerful language understanding and decision-making tools that are created through extensive alignment with human feedback. However, these large models remain susceptible to jailbreak attacks, where adversaries manipulate prompts to elicit malicious outputs that should not be given by aligned LLMs. Investigating jailbreak prompts can lead us to delve into the limitations of LLMs and further guide us to secure them. Unfortunately, existing jailbreak techniques suffer from either (1) scalability issues, where attacks heavily rely on manual crafting of prompts, or (2) stealthiness problems, as attacks depend on token-based algorithms to generate prompts that are often semantically meaningless, making them susceptible to detection through basic perplexity testing. In light of these challenges, we intend to answer this question: Can we develop an approach that can automatically generate stealthy jailbreak prompts? In this paper, we introduce AutoDAN, a novel jailbreak attack against aligned LLMs. AutoDAN can automatically generate stealthy jailbreak prompts by the carefully designed hierarchical genetic algorithm. Extensive evaluations demonstrate that AutoDAN not only automates the process while preserving semantic meaningfulness, but also demonstrates superior attack strength in cross-model transferability, and cross-sample universality compared with the baseline. Moreover, we also compare AutoDAN with perplexity-based defense methods and show that AutoDAN can bypass them effectively.

<img src="AutoDAN.png" width="700"/>

## Latest Update
| Date       | Event    |
|------------|----------|
| **2024/10/09** | 💥 We have released **[AutoDAN-Turbo](https://autodans.github.io/AutoDAN-Turbo/)**, a **life-long agent** for jailbreak redteaming! It's the newest and SotA attack we have developed! Check it out! [Project](https://autodans.github.io/AutoDAN-Turbo/), [Code](https://github.com/SaFoLab-WISC/AutoDAN-Turbo), [Paper](https://arxiv.org/abs/2410.05295) |
| **2024/08/16** | 🎉 Our new [paper](https://www.usenix.org/conference/usenixsecurity24/presentation/yu-zhiyuan) on jailbreak attacks wins the **USENIX Security Distinguished Paper Award**! Don’t miss it! |
| **2024/02/07** | 🔥 AutoDAN is evaluated by the [Harmbench](https://www.harmbench.org) benchmark as one of the strongest attacks. Check it out! |
| **2024/02/07** | 🔥 AutoDAN is evaluated by the [Easyjailbreak](http://easyjailbreak.org) benchmark as one of the strongest attacks. Check it out! |
| **2024/02/03** | We have released the full implementation of AutoDAN. Thanks to all the collaborators.  |
| **2024/01/16** | AutoDAN is accepted by ICLR 2024!  |
| **2023/10/11** | We have released a quick implementation of AutoDAN.  |
| **2023/10/03** | We have released our paper.  |

## Quick Start
- **Get code**
```shell 
git clone https://github.com/SheltonLiu-N/AutoDAN.git
```

- **Build environment**
```shell
cd AutoDAN
conda create -n AutoDAN python=3.9
conda activate AutoDAN
pip install -r requirements.txt
```

Use **`numpy>=1.25,<2`** with cluster **torch 2.1** wheels; otherwise pip can pull **NumPy 2.x** and you will see conflicts with `torch` and `gradio` (`numpy<2.0` required).

If you load **Meta Llama 3** checkpoints, use **`transformers>=4.40,<5`** (as in `requirements.txt`). Older versions instantiate the wrong attention layout (full multi-head K/V instead of grouped-query), which triggers a weight shape mismatch such as `[1024, 4096]` vs `[4096, 4096]` when loading shards. **Transformers 5.8+** expects **PyTorch ≥ 2.4**; clusters such as Narval often provide **torch 2.1.x** (`+computecanada`), which makes recent `transformers` disable PyTorch and can break imports (for example `GenerationMixin` from `transformers.generation`). Stay on **transformers 4.x** unless you load a newer PyTorch module. Also use **`fschat>=0.2.36`**: older `fschat==0.2.20` declares `transformers<4.29`, which conflicts with that requirement (pip will warn or force a downgrade). This repo registers a **`llama-3`** chat template when the installed FastChat build does not include it.

- **Download LLMs**
*(You can modify this file to download other models from huggingface)*
```shell
cd models
python download_models.py
cd ..
```

- **AutoDAN**
```shell
python autodan_ga_eval.py # AutoDAN-GA
```
```shell
python autodan_hga_eval.py # AutoDAN-HGA
```

- **With GPT mutation**
```shell
python autodan_hga_eval.py --API_key <your openai API key>
```


- **Get responses**
```shell
python get_responses.py
```

- **Check keyword ASR**
```shell
python check_asr.py
```

## Acknowledge
Some of our codes are built upon [llm-attack](https://github.com/llm-attacks/llm-attacks).

## BibTeX 
```bibtex
@inproceedings{
      liu2024autodan,
      title={AutoDAN: Generating Stealthy Jailbreak Prompts on Aligned Large Language Models},
      author={Xiaogeng Liu and Nan Xu and Muhao Chen and Chaowei Xiao},
      booktitle={The Twelfth International Conference on Learning Representations},
      year={2024},
      url={https://openreview.net/forum?id=7Jwpw4qKkb}
}
```
